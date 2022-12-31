class Service:
    count_id = 0

    def __init__(self, name, image, description, availability):
        Service.count_id += 1
        self.__service_id = Service.count_id
        self.__image = image
        self.__name = name
        self.__description = description
        self.__availability = availability

    def get_service_id(self):
        return self.__service_id

    def set_service_id(self, service_id):
        self.__service_id = service_id

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_availability(self):
        return self.__availability

    def set_availability(self, availability):
        self.__availability = availability
