from database_mysql_local.point import Point


# TOOO Person -> PersonLocal
class Person:
    "person details class"
    # TODO: is there a way to give a default values for Point?
    # Point(None, None) is not working
    def __init__(self, number: int = None, last_coordinate: Point = Point(0, 0),
                 birthday_date: str = None, day: int = None,
                 month: int = None, year: int = None, first_name: str = None,
                 last_name: str = None, location_id: int = None,
                 nickname: str = None, gender_id: int = None,
                 father_name: str = None, main_email_address: str = None, 
                 is_test_data: bool = False) -> None:
        self.number = number
        self.gender_id = gender_id
        self.last_coordinate = last_coordinate
        self.location_id = location_id
        self.birthday_date = birthday_date
        self.day = day
        self.month = month
        self.year = year
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.father_name = father_name
        self.main_email_address = main_email_address
        self.is_test_data = is_test_data
