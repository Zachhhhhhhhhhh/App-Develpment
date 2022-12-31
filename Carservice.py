import Service


class Carservice(Service.Service):
    count_id = 0

    def __init__(self, name, image, description, location, hotline, starting_hour, ending_hour, opening_days, availability):
        super().__init__(name, image, description, availability)
        Carservice.count_id += 1
        self.__carservice_id = Carservice.count_id
        self.__hotline = hotline
        self.__location = location
        self.__starting_hour = starting_hour
        self.__ending_hour = ending_hour
        self.__opening_days = opening_days

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_hotline(self):
        return self.__hotline

    def set_hotline(self, hotline):
        self.__hotline = hotline

    def get_carservice_id(self):
        return self.__carservice_id

    def set_carservice_id(self, carservice_id):
        self.__carservice_id = carservice_id

    def get_starting_hour(self):
        return self.__starting_hour

    def set_starting_hour(self, starting_hour):
        self.__starting_hour = starting_hour

    def get_ending_hour(self):
        return self.__ending_hour

    def set_ending_hour(self, ending_hour):
        self.__ending_hour = ending_hour

    def get_opening_days(self):
        return self.__opening_days

    def set_opening_days(self, opening_days):
        self.__opening_days = opening_days
