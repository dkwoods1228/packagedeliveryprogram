# Creation of a class for packages
class Packages:
    def __init__(self, ID, address, city, state, zip, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return (
            "ID: %s | %s, %s, %s, %s | Deadline: %s | Weight: %s | Status: %s | Delivery Time: "
            "%s") % (self.ID, self.address, self.city, self.state, self.zip,
                     self.deadline, self.weight, self.status, self.delivery_time)

    # Status_checker used to show the status of the package(s) when the user requests package status information
    # within the command-line interface.
    def status_checker(self, time_conversion):
        if self.delivery_time < time_conversion:
            self.status = "Delivered"
        elif self.departure_time > time_conversion:
            self.status = "En route"
        else:
            self.status = "At Hub"
