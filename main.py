# Name - Darren Woods
# Student ID - 011059884
import csv
import datetime
import trucks
from builtins import ValueError

from hash import Hashtable
from packages import Packages

# Opens and reads address data from csv distance table file
with open("CSV/address_table.csv") as csvfile1:
    address_table = csv.reader(csvfile1)
    address_table = list(address_table)

# Opens and reads distance data from csv distance table file
with open("CSV/distance_table.csv") as csvfile2:
    distance_table = csv.reader(csvfile2)
    distance_table = list(distance_table)

# Opens and reads package data from csv package file
with open("CSV/package_table.csv") as csvfile3:
    package_table = csv.reader(csvfile3)
    package_table = list(package_table)


# Creation of package objects based on the fields within the csv package file
# Newly created package objects are loaded into hashtable_for_packages
def load_packages(file, hashtable_for_packages):
    with open(file) as packages:
        packageData = csv.reader(packages)
        for package in packageData:
            packageID = int(package[0])
            packageAddress = package[1]
            packageCity = package[2]
            packageState = package[3]
            packageZip = package[4]
            packageDeadline = package[5]
            packageWeight = package[6]
            packageStatus = "At Hub"

            # Represents the package objects
            pack = Packages(packageID, packageAddress, packageCity, packageState, packageZip, packageDeadline,
                            packageWeight, packageStatus)

            # The package data is inserted into the package hash table here
            hashtable_for_packages.insert_item(packageID, pack)


# Used to obtain the exact number of the address from the csv address table file
def get_address(address):
    for row in address_table:
        if address in row[2]:
            return int(row[0])


# Used to obtain the distance difference between two addresses
# Obtain distances between addresses from the csv distance table file
def distances_between_addresses(first_address, second_address):
    distances = distance_table[first_address][second_address]
    if distances == '':
        distances = distance_table[second_address][first_address]

    return float(distances)


# Creation of Truck One objects
# Truck One = Departs at 8:00 AM (Earliest it can leave)
# Packages 13, 14, 15, 16, 19, 20 must all be on the same truck based on certain packages needing to be on same truck
# Package 15 must arrive to location by 9:00 AM, therefore placed on earliest truck
truckOnePackages = trucks.Trucks(16, 0.0, 18, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
                                 "4001 South 700 East", datetime.timedelta(hours=8))

# Creation of Truck Two objects
# Truck Two = Departs at 9:05 AM (Departs once delayed packages arrive)
# Packages 3, 18, 36, & 38 must be on Truck Two
truckTwoPackages = trucks.Trucks(16, 0.0, 18, [3, 6, 18, 25, 27, 28, 32, 33, 35, 36, 38, 39],
                                 "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Creation of Truck Three objects
# Truck Three = departs at 10:20 AM
# Package 9 originally delayed due to incorrect address. Address corrected at 10:20 AM (must be on this truck)
truckThreePackages = trucks.Trucks(16, 0.0, 18, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26],
                                   "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# Creation of hash table
hashtable_for_packages = Hashtable()

# Packages are loaded into the hash table
load_packages("CSV/package_table.csv", hashtable_for_packages)


# Nearest neighbor algorithm used to arrange packages on given truck to deliver to the next nearest address
# The distance a given truck drives is also determined
def nearest_neighbor_delivery(trucks):
    # Packages that are undelivered is placed into an array
    packagesUndelivered = []
    for packageID in trucks.packages_on_truck:
        package = hashtable_for_packages.lookup_item(packageID)
        packagesUndelivered.append(package)
    # Package list is cleared, as packages on the truck are placed back in order to deliver to the next nearest address
    trucks.packages_on_truck.clear()
    # The items within packagesUndelivered list is used until there are no items (packages) left
    while len(packagesUndelivered) > 0:
        upcomingPackage = None
        upcomingAddress = 2000
        for package in packagesUndelivered:
            if distances_between_addresses(get_address(trucks.address),
                                           get_address(package.address)) <= upcomingAddress:
                upcomingAddress = distances_between_addresses(get_address(trucks.address), get_address(package.address))
                upcomingPackage = package
        # The next nearest package is added to the packages_on_truck list
        trucks.packages_on_truck.append(upcomingPackage.ID)
        # Since that package was moved to the packages_on_trucks list, it's removed from the undelivered list
        packagesUndelivered.remove(upcomingPackage)
        # Miles driven to the upcoming package address is recorded
        trucks.miles += upcomingAddress
        # The given truck's current address is updated to package's address it went to
        trucks.address = upcomingPackage.address
        # Time driven to the nearest package address is updated
        trucks.time += datetime.timedelta(hours=upcomingAddress / 18)
        upcomingPackage.delivery_time = trucks.time
        upcomingPackage.departure_time = trucks.departure


# Apply algorithm to trucks
nearest_neighbor_delivery(truckOnePackages)
nearest_neighbor_delivery(truckTwoPackages)
# Truck three is directed to leave only AFTER truck one and two are done delivering packages,
# as there are only 2 drivers for 3 trucks
truckThreePackages.depart_time = min(truckOnePackages.time, truckTwoPackages.time)
nearest_neighbor_delivery(truckThreePackages)


# Creation of Main class for user interface
class Main:
    # Showcases the total mileage driven by all 3 trucks
    print("Total Mileage:", truckOnePackages.miles + truckTwoPackages.miles + truckThreePackages.miles)
    # Asks user to either check package status or truck info
    text = input("Would you like to check package status or view truck information? (Type 'status' for "
                 "package status or 'truck' for truck information): ")
    # If "status" is inputted, user must enter a time to view status of package(s) at the chosen time
    # If neither "status" nor "truck" are inputted, the program closes
    if text == "status":
        try:
            status_input = input("Please enter a time to view package status (format: HH:MM | military time): ")
            (h, m) = status_input.split(":")
            time_conversion = datetime.timedelta(hours=int(h), minutes=int(m))
            # Asks user to view either one package or all packages
            status_input2 = input("Would you like to view the status of one package or all packages? "
                                  "(Type 'one' to view one package, type 'all' to view all packages): ")
            # If "one" is inputted, user asked for specific package ID number to view the status of the package
            if status_input2 == "one":
                try:
                    one_input = input("Please enter a package ID number (1-40): ")
                    package = hashtable_for_packages.lookup_item(int(one_input))
                    package.status_checker(time_conversion)
                    print(str(package))
                    # Allows user to check the status of another package at time they inputted
                    status_input3 = input("Would you like to view the status of another package? (Type 'yes' or 'no'): ")
                    if status_input3 == "yes":
                        try:
                            yes_input = input("Please enter a package ID number (1-40): ")
                            package = hashtable_for_packages.lookup_item(int(yes_input))
                            package.status_checker(time_conversion)
                            print(str(package))
                        except ValueError:
                            print("Invalid entry. Program will now close. Please try again.")
                            exit()
                    # If "no" is inputted, the program quits
                    elif status_input3 == "no":
                        print("Program will now close. Thank you.")
                        exit()
                except ValueError:
                    print("Invalid entry. Program will now close. Please try again.")
                    exit()
            # If "all" is inputted, the package status of all 40 packages are shown at the time the user inputted
            elif status_input2 == "all":
                try:
                    for packageID in range(1, 41):
                        package = hashtable_for_packages.lookup_item(packageID)
                        package.status_checker(time_conversion)
                        print(str(package))
                except ValueError:
                    print("Invalid entry. Program will now close. Please try again.")
                    exit()
            # If neither "one" nor "all" are inputted, the program closes
            else:
                exit()
        except ValueError:
            print("Invalid entry. Program will now close. Please try again.")
            exit()
    # If user inputs "truck", the 3 trucks and their departure time, list of packages, and mileage are showcased
    elif text == "truck":
        print("Truck 1:")
        print("Time of departure from hub: 8:00AM")
        print("Mileage:", truckOnePackages.miles)
        print("Packages on truck:", truckOnePackages.packages_on_truck)
        print("----------------------------------------------------------------------------")
        print("Truck 2:")
        print("Time of departure from hub: 9:05AM")
        print("Mileage:", truckTwoPackages.miles)
        print("Packages on Truck:", truckTwoPackages.packages_on_truck)
        print("----------------------------------------------------------------------------")
        print("Truck 3:")
        print("Time of departure from hub: 10:20AM")
        print("Mileage:", truckThreePackages.miles)
        print("Packages on Truck:", truckThreePackages.packages_on_truck)
        # Package 9 address changed to accurate address
        print("Note: Package #9 - Address successfully changed to correct address in time for 10:20AM departure.")
        print("----------------------------------------------------------------------------")
    else:
        print("Invalid entry. Program will now close. Please try again.")
        exit()
