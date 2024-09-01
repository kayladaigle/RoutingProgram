from datetime import timedelta
class Truck:
    def __init__(self, name, packages, location, mileage, speed, departTime):
        self.name = name
        self.packages = packages
        self.location = location
        self.mileage = mileage
        self.speed = speed
        self.departTime = departTime

    def __str__(self):
        return (f"Truck Speed: {self.speed}, Truck name:{self.name}, Mileage:{self.mileage},"
                f"Current Location: {self.location}, Packages: {self.packages} ,"
                f" Time of Departure: {self.departTime}")




