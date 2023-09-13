# Creation of a class for trucks
class Trucks:
    def __init__(self, max_capacity, miles, truck_speed, packages_on_truck, address, depart_time):
        self.max_capacity = max_capacity
        self.miles = miles
        self.truck_speed = truck_speed
        self.packages_on_truck = packages_on_truck
        self.address = address
        self.departure = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.max_capacity, self.miles, self.truck_speed, self.packages_on_truck,
                                           self.address, self.departure)
