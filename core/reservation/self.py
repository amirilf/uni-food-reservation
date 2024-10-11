import requests
from enum import Enum
from bs4 import BeautifulSoup, Tag
from utility.config import SELF_URL


class SELF_PLACE(Enum):
    SOLEYMAN_KHATER = 2
    SHAHID_FAHMIDEH = 3
    SHAHID_BAHONAR = 4
    SHAHID_RAJAEI = 6
    SHAHID_MOFATEH = 7
    NIKAN_MANDEGAR = 8

class MEAL_TIME(Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"

def get_self_page_response(session: requests.Session, next_week: bool = False) -> requests.Response:
    """Fetch & return current or next week page source"""
    
    response = session.get(SELF_URL)
    
    if not next_week:
        return response
    
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    
    form_data = {
        "ctl00$ScriptManager": "ctl00$UpdatePanel1|ctl00$cphMain$imgbtnNextWeek",
        "__VIEWSTATE": soup.find('input', {'name': '__VIEWSTATE'})['value'],
        "__EVENTTARGET": "ctl00$cphMain$imgbtnNextWeek",
    }
    
    response = session.post(SELF_URL, data=form_data)

    return response
        
def process_food_row(tr: Tag) -> dict[str, str | int]:
    """
    Get `tr` element of the food row. Fetch details and return them as a dictionary.

    Result:
        - day
        - place
            - detail: for each place item there is a list [name, value]
            - all: all of places (actually is used for dormitory students)
            - selected: the selected place
        - food
            - detail: for each food item there is a list [name, value]
            - all: all of the food options
            - selected: selected food option
        - price
        - status
            - options:
                - قابل رزور
                - رزرو شده
                - رزرو شده، خورده نشده، غیرفعال
                - خورده شده
                - غیرفعال
    """

    tds = tr.find_all("td", recursive=False)
    
    day = tds[1].get_text(strip=True)
    
    # places
    place_options = tds[2].find_all("option")
    place = {
        "all": [],
        "selected": None
    }
    for option in place_options:
        name = option.get_text(strip=True)
        value = option.get('value')
        place["all"].append([name, value])
        
        if option.has_attr('selected'):
            place["selected"] = [name, value]

    # foods 
    food_options = tds[3].find_all("option")
    food = {
        "all": [],
        "selected": None
    }
    for option in food_options:
        name = option.get_text(strip=True)
        value = option.get('value')
        food["all"].append([name, value])

        if option.has_attr('selected'):
            food["selected"] = [name, value]
    
    price = int(tds[6].find("span").get_text(strip=True))
    
    try:
        status = tds[7].find("img").attrs.get("title").split("-")[0]
    except:
        status = "قابل رزرو"
    
    return dict({"day":day, "place":place, "food":food, "price":price, "status":status})

def process_food_rows(soup: BeautifulSoup, process_each_row: bool = True, get_credit: bool = True) -> dict[str, dict[int, dict[str, str]] | int]:
    """
    Get the source page of the self(رستوران سلف) food program page in cullinan.<br>Find all food rows including breakfast, lunch and dinner. 
    separate them into 3 groups and return them in a dictionary with those keys.

    Each value is a list of `tr` items representing a table row as a food.

    If `process_each_row` is True, process each row with `process_food_row` and return a nested dictionary for each meal.

    Result:
        - breakfast
        - lunch
        - dinner
        
    Result if process_each_row is True:
        - breackfast
            - 1
                - day
                - ...
            - ...
        - ...
    """

    breakfast = soup.find(id="tabs-1").find("table").find_all("tr")[1:]
    lunch = soup.find(id="tabs-2").find("table").find_all("tr")[1:]
    dinner = soup.find(id="tabs-3").find("table").find_all("tr")[1:]
    
    if not process_each_row:
        return {"breakfast": breakfast, "lunch": lunch, "dinner": dinner}
    
    res = {
        "breakfast": {i: process_food_row(breakfast[i]) for i in range(len(breakfast))},
        "lunch": {i: process_food_row(lunch[i]) for i in range(len(lunch))},
        "dinner": {i: process_food_row(dinner[i]) for i in range(len(dinner))}
    }
    
    if get_credit:
        credit_str = soup.find(id="cphMain_lblCreditValue").get_text().split(" ")[2]
        credit_str = credit_str.replace(",", "")
        res["credit"] = int(credit_str)

    return res

def generate_reserve_form_data(meal_time: MEAL_TIME, viewstate: str, self_place: SELF_PLACE, foods: list[bool | int]) -> dict[str, str]:
    """
    - meal_time must be one of (Breakfast | Lunch | Dinner)
    - self place is actually one place for each student & no one's gonna get the food from different self places like idiots
    """
    
    meal_time = meal_time.value
    
    form_data = {
        "__VIEWSTATE" : viewstate,       
        "ctl00$ScriptManager": f"ctl00$UpdatePanel1|ctl00$cphMain$btnSave{meal_time}",
        f"ctl00$cphMain$btnSave{meal_time}": "ذخیره",
    }
        
    # add reservations
    for i in range(6):
        form_data[f"ctl00$cphMain$grdReservation{meal_time}$ctl0{i + 2}$drpFood"] = foods[i][1]
        if foods[i][0]:
            form_data[f"ctl00$cphMain$grdReservation{meal_time}$ctl0{i + 2}$chkReserve"] = "on"

    # for lunch there is only one choice and no need to specify!
    if meal_time != "Lunch":
        for i in range(6):
            form_data[f"ctl00$cphMain$grdReservation{meal_time}$ctl0{i + 2}$drpSelf"] = self_place.value

    return form_data

def get_food_program(session: requests.Session, next_week = False) -> dict[str, dict[str, list[Tag]] | dict[str, dict[int, dict[str, str]]]]:
    """Fetch and parse current and next week food program."""
        
    # get current week
    response = session.get(SELF_URL)
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    current_week_program = process_food_rows(soup)
    
    if not next_week:
        return {"current": current_week_program}
    
    # get next week        
    form_data = {
        "ctl00$ScriptManager": "ctl00$UpdatePanel1|ctl00$cphMain$imgbtnNextWeek",
        "__VIEWSTATE": soup.find('input', {'name': '__VIEWSTATE'})['value'],
        "__EVENTTARGET": "ctl00$cphMain$imgbtnNextWeek",
    }
    
    response = session.post(SELF_URL, data=form_data)
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    next_week_program = process_food_rows(soup)
    
    return {"current": current_week_program, "next": next_week_program}

def reserve(session: requests.Session, meal_time: MEAL_TIME, self_place: SELF_PLACE, foods: list[bool | int], next_week: bool = False):
    """
    Main reservation method. Get the meal_time (Breakfast)
    """
    
    response = get_self_page_response(session,next_week)
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    form_data = generate_reserve_form_data(meal_time, viewstate, self_place, foods)
    response = session.post(SELF_URL, data=form_data)
    print("reserved")


# Testing
session = requests.Session()
session.cookies.set("ASP.NET_SessionId","mhigg1fbbfnqeuu5rur3cpea")
print(reserve(session, MEAL_TIME.BREAKFAST, SELF_PLACE.SHAHID_RAJAEI, [[0,-1], [1,35916], [1,35919], [1,35922], [1,35925], [1,35928], [0,-1]],True))
    