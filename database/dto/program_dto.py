from utility.time import get_tehran_time

class FoodItem:
    def __init__(self, name: str, price: dict, place: dict, status: str):
        self.name = name
        self.price = price
        self.place = place
        self.status = status

    def __repr__(self):
        return f"FoodItem(name={self.name}, price={self.price}, place={self.place}, status={self.status})"

class MealTime:
    def __init__(self, meal: FoodItem = None):
        self.meal = meal

    def __repr__(self):
        return f"MealTime(meal={self.meal})"

class DayProgram:
    def __init__(self, breakfast: MealTime, lunch: MealTime, dinner: MealTime):
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner

    def __repr__(self):
        return f"DayProgram(breakfast={self.breakfast}, lunch={self.lunch}, dinner={self.dinner})"

class WeekProgram:
    def __init__(self, days: list[DayProgram]):
        self.days = days
        self.creation_time = get_tehran_time()

    def __repr__(self):
        return f"WeekProgram(days={self.days}, creation_time={self.get_creation_time})"

    def get_creation_time(self):
        return self.creation_time.strftime('%Y-%m-%d %H:%M:%S')