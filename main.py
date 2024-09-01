# Kayla Daigle
# Student ID: 010273708
# C950 WGUPS Routing Program Project

import csv
from datetime import datetime, time, timedelta
from deliveryTruck import Truck
from package import Package
from hashTable import HashTable


# function to create package objects and load into hash map
my_hash = HashTable()


def loadPackageData(filename):
    with open(filename,'r',encoding='utf-8-sig') as pCSV:
        packagesCSV = csv.reader(pCSV, delimiter=',')
        for package in packagesCSV:
            if not any(package):  # Skip empty lines
                continue

            id = package[0]
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            specialNotes = package[7]
            departureTime = None
            timeOfDelivery = None
            packageStatus = "At Hub"

            # create package object
            package = Package(id, address, city, state, zipcode, deadline, weight, specialNotes, departureTime, timeOfDelivery, packageStatus)
            # print(package)
            my_hash.insert(id, package)
    return my_hash

# load package objects into hash table

package_data = loadPackageData('data/packages.csv')

# print hash table function

def printHashTable():
    for i in range(len(package_data.table)):
        bucket_list = package_data.table[i]
        for keyValue in bucket_list:
            key, package = keyValue
            print(f"Key:{key} and Package Details:{vars(package)}")


"""
manually load boxes onto trucks
packages delayed and not arriving until 9:05am - 6,25,28,32
can only be on truck 2 - 36,38,18,3
14 must be delivered with 15,19
16 must be delivered with 13,19
20 must be delivered with 13,15
"""
truck_one = Truck("Truck One",
                  [1,2,13,14,15,19,20,21,27,29,30,33,34,35,37],
                  "4001 South 700 East",
                  0.0,
                  18,
                  datetime(2024, 8, 23,8,0))

truck_two = Truck("Truck Two",
                  [4,6,11,12,17,18,17,18,23,24,31,32,36,40,3,38],
                  "4001 South 700 East",
                  0.0,
                  18,
                  datetime(2024,8,23,9,5))

truck_three = Truck("Truck Three",
                    [5,7,8,9,10,16,26,28,39,25,22],
                    "4001 South 700 East",
                    0.0,
                    18,
                    datetime(2024,8,23,9,50)) # placeholder - truck 3 needs to wait until truck 1 returns

# csv files - address-list and distances opened and made available
with open('data/addresses_list.csv','r',encoding='utf-8-sig') as aCSV:
    addressChart = csv.reader(aCSV)
    key = []
    addresses = []
    for row in addressChart:
        if row:
            key.append(row[0])
            addresses.append(row[1].strip())


with open('data/distances.csv', 'r', encoding='utf-8-sig') as dCSV:
    distanceChart = csv.reader(dCSV)
    distanceChart = list(distanceChart)


# connects package ID to package address -returns address
def connect_id_to_address(package_id):
    string_id = str(package_id)
    for i in range(len(package_data.table)):
        bucket_list = package_data.table[i]
        for key_value in bucket_list:
            key, package = key_value
            if key == string_id:
                return package.address
    return None


# connect package address to key - returns key
def address_to_key(package):
    package_address = connect_id_to_address(package)
    location_key = None
    for address in addresses:
        if address == package_address:
            location_key = addresses.index(address) + 1
    return location_key

# calculate distance from package locations
def location_distances(row, column):
    total_distance = distanceChart[row][column]
    return float(total_distance)


# choosing the package closest to the location that the truck is currently at (greedy method)
def nearest_location(start, package_list):
    smallest_distance = float('inf')
    next_location = None
    start_key = address_to_key(start)
    for package in package_list:
        id_to_key = address_to_key(package)
        if id_to_key is not None:
            distance = location_distances(start_key, id_to_key)
            if distance < smallest_distance:
                smallest_distance = distance
                next_location = package
    return next_location


# ordering the route that the trucks will go in based on closest distance to current location
def deliveryRoute(truck):
    route = []
    start_point = 0
    packages_left = truck.packages[:]
    while packages_left:
        next_location = nearest_location(start_point,packages_left)
        route.append(next_location)
        packages_left.remove(next_location)
        start_point = next_location
    return route

# runs the trucks through delivery while keeping track of mileage, time, and status
def truck_run(truck):
    truck_list = deliveryRoute(truck)
    wgu_key = 1
    mileage = 0
    start = 1
    start_time = truck.departTime
    current_time = datetime.now().time()
    for package in truck_list:
        string_id = str(package)
        package_info = package_data.search(string_id)

        if package_info.id == '9':
            if current_time > datetime(2024,8,23,10,20):  # Time after 10:20 AM
                package_info.address = "410 S State St"
                package_info.zipcode = "84111"

        package_info.packageStatus = f"In route"

        address = connect_id_to_address(package)
        package_key = address_to_key(package)

        distance = location_distances(start,package_key)
        timepast = distance/(truck.speed)
        minutes = timepast * 60
        time_delta = timedelta(minutes=minutes)
        current_time = start_time + time_delta

        package_info.departureTime = start_time.strftime("%I:%M %p")
        package_info.timeOfDelivery = current_time.strftime("%I:%M %p")
        package_info.packageStatus = f"Delivered"


        print(f"{truck.name} delivered package {package} to {address} at {current_time.strftime('%I:%M %p')}")
        start_time = current_time
        mileage += distance
        start = package_key


    return_distance = location_distances(start,wgu_key)
    mileage += return_distance
    extra_time = return_distance / truck.speed
    extra_time_minutes = extra_time * 60
    time_delta = timedelta(minutes=extra_time_minutes)
    current_time += time_delta


    if truck == truck_one:
        print(f"Truck One returned to headquarters at {current_time.strftime('%I:%M %p')}")
        mileage = round(mileage,2)
        print(f"Truck One traveled {mileage} miles.")
        return mileage
    elif (truck == truck_two):
        print(f"Truck Two returned to headquarters at {current_time.strftime('%I:%M %p')}")
        mileage = round(mileage,2)
        print(f"Truck Two traveled {mileage} miles.")
        return mileage
    else:
        print(f"Truck Three returned to headquarters at {current_time.strftime('%I:%M %p')}")
        mileage = round(mileage,2)
        print(f"Truck Three traveled {mileage} miles.")
        print("\nAll trucks have made their deliveries for the day and have returned to headquarters.")

        return mileage


# find the truck the package is on
truck_options = [truck_one, truck_two, truck_three]

def find_truck(package,trucks):
    for truck in trucks:
        if package in truck.packages:
            return truck.name


# prints the status for all packages at any given time
def print_status(input_time):
    for i in range(len(package_data.table)):
        bucket_list = package_data.table[i]
        for keyValue in bucket_list:
            key, package = keyValue

            if key != '0':
                time_datetime = datetime.strptime(input_time, "%I:%M %p").time()
                formatted_time = time_datetime.strftime("%H:%M")

                # package 9 is not updated until 10:20am
            if key == '9':

                if (time_datetime > datetime.strptime('10:20 am',"%I:%M %p").time()):  # Time after 10:20 AM
                        package.address = "410 S State St"
                        package.zipcode = "84111"
                elif (time_datetime < datetime.strptime('10:20 am',"%I:%M %p").time()):
                        package.address = "300 State St"
                        package.zipcode = "84103"


            if package.departureTime == None:
                package.packageStatus = 'at hub'
                int_package = int(package.id)
                truck_number = find_truck(int_package,truck_options)
                print(f"Package:{key} on {truck_number}     Address: {package.address}            Deadline: {package.deadline}      Package Status:{package.packageStatus}")
            elif formatted_time <= package.departureTime:
                package.packageStatus = 'at hub'
                int_package = int(package.id)
                truck_number = find_truck(int_package,truck_options)
                print(f"Package:{key} on {truck_number}     Address: {package.address}            Deadline: {package.deadline}      Package Status:{package.packageStatus}")
            elif formatted_time <= package.timeOfDelivery:
                package.packageStatus = 'en route'
                int_package = int(package.id)
                truck_number = find_truck(int_package,truck_options)
                print(f"Package:{key} on {truck_number}      Address: {package.address}            Deadline: {package.deadline}      Package Status:{package.packageStatus}")
            else:
                package.packageStatus = 'delivered'
                int_package = int(package.id)
                truck_number = find_truck(int_package,truck_options)
                print(f"Package:{key} on {truck_number}      Address: {package.address}            Deadline: {package.deadline}      Package Status:{package.packageStatus} at {package.timeOfDelivery}")

# prints the status for one of the packages at any given time
def print_status_package(time,package):
    time_datetime = datetime.strptime(time, "%I:%M %p").time()
    formatted_time = time_datetime.strftime("%H:%M")
    package_info = package_data.search(package)
    int_package = int(package)
    truck_number = find_truck(int_package,truck_options)

    # package 9 is not updated until 10:20am
    if package == '9':

        if (time_datetime > datetime.strptime('10:20 am',"%I:%M %p").time()):  # Time after 10:20 AM
            package_info.address = "410 S State St"
            package_info.zipcode = "84111"
        elif (time_datetime < datetime.strptime('10:20 am',"%I:%M %p").time()):
            package_info.address = "300 State St"
            package_info.zipcode = "84103"

    if package_info.departureTime == None:
        package_info.packageStatus = 'at hub'
        print(f"Package:{package} on {truck_number}      Address: {package_info.address}       Deadline: {package_info.deadline}     Package Status:{package_info.packageStatus}")
    elif formatted_time <= package_info.departureTime:
        package_info.packageStatus = 'at hub'
        print(f"Package:{package} on {truck_number}      Address: {package_info.address}       Deadline: {package_info.deadline}     Package Status:{package_info.packageStatus}")
    elif formatted_time <= package_info.timeOfDelivery:
        package_info.packageStatus = 'en route'
        print(f"Package:{package} on {truck_number}      Address: {package_info.address}       Deadline: {package_info.deadline}     Package Status:{package_info.packageStatus}")
    else:
        package_info.packageStatus = 'delivered'
        print(f"Package:{package} on {truck_number}      Address: {package_info.address}       Deadline: {package_info.deadline}     Package Status:{package_info.packageStatus} at {package_info.timeOfDelivery}")

# gives user options to look up packages and delivery status
def multiple_choice():
    options = {
        "A":"Check Status of ALL Packages at a Certain Time",
        "B":"Check Status of ONE Package at a Certain Time.",
        "C":"Exit Program"
    }

    print("Please select how you would like to proceed:")
    for letter, value in options.items():
        print(f"{letter}: {value}")

    user_input = input("Enter the letter of your choice: ").strip().upper()
    return user_input


# plays out what the user picked during multiple choice
def handle_choice(choice):

    if choice == 'A':
        a_input = input("What time would you like to view? (Please input HH:MM am/pm)")
        print_status(a_input)
        user_choice = multiple_choice()
        handle_choice(user_choice)


    elif choice == 'B':
        package_input = input("What package would you like to view?")
        time_input =  input("What time would you like to view this package? (Please input HH:MM am/pm)")
        print_status_package(time_input,package_input)
        user_choice = multiple_choice()
        handle_choice(user_choice)

    elif choice == 'C':
        print("You have choose to exit the program.")


# runs the delivery program
def deliveryPrompt():
    print("Welcome to the WGUPS Routing Program!")
    print("Running routing program.....\n")
    mileage1 = truck_run(truck_one)
    mileage2 = truck_run(truck_two)
    mileage3 = truck_run(truck_three)
    total_mileage = mileage1 + mileage2 + mileage3
    total_mileage = round(total_mileage,2)
    print(f"\nIn total the trucks traveled {total_mileage} miles today.\n")

    user_choice = multiple_choice()
    handle_choice(user_choice)



deliveryPrompt()

