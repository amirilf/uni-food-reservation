import enum


class UserStage(enum.Enum):
    NEW = 1
    TERMS = 2
    LOGIN = 3
    PAID = 4
    
class SELF_PLACE(enum.Enum):
    SOLEYMAN_KHATER = 2
    SHAHID_FAHMIDEH = 3
    SHAHID_BAHONAR = 4
    SHAHID_RAJAEI = 6
    SHAHID_MOFATEH = 7
    NIKAN_MANDEGAR = 8

class MEAL_TIME(enum.Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
