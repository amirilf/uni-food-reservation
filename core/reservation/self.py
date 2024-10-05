import requests
from bs4 import BeautifulSoup, Tag
from core.utility.variables import SELF_URL
        
def process_food_row(tr: Tag) -> dict[str, str]:
    """
    Get `tr` element of the food row. Fetch details and return them as a dictionary.

    Result:
        - day
        - place
        - food
        - price
        - status
    """
    
    tds = tr.find_all("td", recursive=False)
    
    day = tds[1].get_text(strip=True)
    place = tds[2].find("option", selected=True).get_text(strip=True)
    food = tds[3].find("option", selected=True).get_text(strip=True)
    price = tds[6].find("span").get_text(strip=True)
    
    try:
        status = tds[7].find("img").attrs.get("title").split("-")[0]
    except:
        status = "قابل رزرو"
    
    return dict({"day":day, "place":place, "food":food, "price":price, "status":status})

def process_food_rows(soup: BeautifulSoup, process_each_row: bool = False) -> dict[str, list[Tag]] | dict[str, dict[int, dict[str, str]]]:
    """
    Get the source page of the self(رستوران سلف) food program page in cullinan.<br>Find all food rows including breakfast, lunch and dinner. 
    separate them into 3 groups and return them in a dictionary with those keys.

    Each value is a list of `tr` items representing a table row as a food.

    If `process_each_row` is True, process each row with `process_food_row` and return a nested dictionary for each meal.

    Result:
        - breakfast
        - dinner
        - lunch
        
    Result if process_each_row is True:
        - breackfast
            - 1
                - day
                - ...
            - ...
        - ...
    """

    breakfast = soup.find(id="tabs-1").find("table").find_all("tr")[1:]
    dinner = soup.find(id="tabs-2").find("table").find_all("tr")[1:]
    lunch = soup.find(id="tabs-3").find("table").find_all("tr")[1:]
    
    if not process_each_row:
        return {"breakfast": breakfast, "dinner": dinner, "lunch": lunch}
    
    res = {
        "breakfast": {i: process_food_row(breakfast[i]) for i in range(len(breakfast))},
        "dinner": {i: process_food_row(dinner[i]) for i in range(len(dinner))},
        "lunch": {i: process_food_row(lunch[i]) for i in range(len(lunch))}
    }
    
    return res    

def get_food_program(session: requests.Session, next_week = False):
    """Fetch and parse current and next week food program."""
    
    # get current week
    response = session.get(SELF_URL)
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    current_week_program = process_food_rows(soup, True)
        
    if not next_week:
        return current_week_program
    
    # get next week        
    form_data = {
        "ctl00$ScriptManager": "ctl00$UpdatePanel1|ctl00$cphMain$imgbtnNextWeek",
        "__VIEWSTATE": soup.find('input', {'name': '__VIEWSTATE'})['value'],
        "__EVENTTARGET": "ctl00$cphMain$imgbtnNextWeek",
    }
    
    response = session.post(SELF_URL, data=form_data)
    soup = BeautifulSoup(response.content.decode("utf-8"), 'html.parser')
    next_week_program = process_food_rows(soup, True)
    
    return [current_week_program, next_week_program]
