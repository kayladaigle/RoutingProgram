import datetime


class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, specialNotes, departureTime, timeOfDelivery, packageStatus):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.specialNotes = specialNotes
        self.departureTime = departureTime
        self.timeOfDelivery = timeOfDelivery
        self.packageStatus = packageStatus

    def __str__(self):
        return f"ID: {self.id}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zipcode}, Deadline: {self.deadline}, Weight: {self.weight}, Special Notes: {self.specialNotes},Time of Departure:{self.departureTime}, Time of Delivery:{self.timeOfDelivery}, Package Status: {self.packageStatus}"




