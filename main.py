from q1 import *
from q2 import *
from q3 import *
from q4 import *
import csv
from datetime import datetime
class InvalidFileError(Exception):
    pass
def loadData(customersFile, toursFile, scheduledToursFile):
    customers = []
    tours = []
    sts = []

    # Load customers from appendix-a.csv
    with open(customersFile, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dob = datetime.strptime(row['DOB (YYYYMMDD)'], '%Y%m%d')
            customer = Customer(row['Passport Number'],row['Name'], dob, row['Contact'])
            customers.append(customer)

    # Load tours from table1.csv
    with open(toursFile, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tour = Tour(row['Tour Code'], row['Tour Name'],int(row['No. of Days']),int(row['No. of Nights']),float(row['Cost ($)']))
            tours.append(tour)

    # Load scheduled tours from table2-2.csv
    with open(scheduledToursFile, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            departure_date = row['Departure']
            time = row['DateTime']
            departure_datetime = datetime.strptime(f"{departure_date} {time}", '%d-%b-%Y %H:%M')
            peak = row['Peak']
            tour_code = row['Tour Code']
            language = row['Language']
            capacity = int(row['Capacity'])
            for tour in tours:
                if tour.code == tour_code:
                    if peak == 'Yes':
                        st = PeakScheduledTour(row['Schedule Code'], tour, departure_datetime, language, capacity)
                    else:
                        st = ScheduledTour(row['Schedule Code'], tour, departure_datetime, language, capacity)
                    break
            sts.append(st)

    return customers, tours, sts
def main():
    try:
        #create TourAgency object
        tourAgency = TourAgency()

        # Load data from CSV files
        customers, tours, sts = loadData('appendix-a.csv', 'table1.csv', 'table2-2.csv' )

        # Add loaded data to the TourAgency object
        for customer in customers:
            tourAgency.addCustomer(customer) 
        for tour in tours:
            tourAgency.addTour(tour)
        for st in sts:
            tourAgency.addScheduledTour(st)

    except InvalidFileError as e:
        print(f"Error loading data: {e}")

    #Main Menu:
    while True:
        print("\n<<<< Main Menu >>>>")
        print("1. Tour management")
        print("2. Booking management")
        print("0. Quit")
        choice = input("Enter choice: ")

        if choice == '1':
            tourManagement(tourAgency)
        elif choice == '2':
            bookingManagement(tourAgency)
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
    
#Tour Management
def tourManagement(tourAgency):
    while True:
        print("\n<< Tour Menu >>")
        print("1. Schedule Tour")
        print("2. Open/Close Scheduled Tour")
        print("3. Remove Scheduled Tour")
        print("4. List Scheduled Tours")
        print("0. Back to main menu")
        choice = input("Enter choice: ")

        if choice == "1":
            scheduleTour(tourAgency)
        elif choice == "2":
            openCloseScheduledTour(tourAgency)
        elif choice == "3":
            removeScheduledTour(tourAgency)
        elif choice == "4":
            print(tourAgency.listScheduledTours())
        elif choice == "5":
            pass
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a valid option.")
#Tour Menu Option 1:
def scheduleTour(tourAgency):
    print("List of available tours:")
    print("========================")
    print(tourAgency.listTours())
    try:
        tourCode = input("Enter Tour Code: ")
        scheduleCode = input("Enter Schedule Code: ")
        departureDatetimeStr = input("Enter Departure Datetime in (YYYY-MM-DD HH:MM): ")
        lang = input("Language used to conduct the tour: ")
        capacity = int(input("Enter Capacity: "))
        peakNormal = input("(P)eak or (N)ormal: ").upper()

        # Convert departure date and time to datetime object
        departureDatetime = datetime.strptime(departureDatetimeStr, '%Y-%m-%d %H:%M')

        # Create a new ScheduledTour object
        if peakNormal == 'P':
            st = PeakScheduledTour(scheduleCode, tourAgency.searchTour(tourCode), departureDatetime, lang, capacity)
        elif peakNormal == 'N':
            st = ScheduledTour(scheduleCode, tourAgency.searchTour(tourCode), departureDatetime, lang, capacity)
        else:
            print("Enter P for Peak Scheduled Tour and N for Normal Scheduled Tour!!")
        # Add the scheduled tour to the TourAgency
        tourAgency.addScheduledTour(st)
        print("Setup complete...")
        print(st)
    except ValueError:
        print("Invalid input. Please enter valid information.")

#Tour Menu Option 2:
def openCloseScheduledTour(tourAgency):
    while True:
        print("\n<< Open/Close Scheduled Tour >>")
        scheduledTourCode = input("Enter Scheduled Tour Code to update: ")
        scheduledTour = tourAgency.searchScheduledTour(scheduledTourCode)

        if scheduledTour is not None:
            print(scheduledTour)

            if scheduledTour.status:
                openStatus = input("Close? (Y/N): ").upper()
            else:
                openStatus = input("Open? (Y/N): ").upper()

            if openStatus == 'Y':
                scheduledTour.status = not scheduledTour.status  # Toggle the status
                print("Status updated!!")
            else:
                print("No changes made.")

            print(scheduledTour)
        else:
            print(f"Scheduled tour with code {scheduledTourCode} not found.")

        option = input("\nDo you want to update another scheduled tour? (Y/N): ").upper()
        if option != 'Y':
            break

#Tour Menu Option 3:
def removeScheduledTour(tourAgency):
    while True:
        print("\n<< Remove Scheduled Tour >>")
        scheduledTourCode = input("Enter Scheduled Tour Code to remove: ")
        scheduledTour = tourAgency.searchScheduledTour(scheduledTourCode)

        if scheduledTour is not None:
            print(scheduledTour)            
            removeConfirm = input("Remove? (Y/N): ").upper()
            if removeConfirm == 'Y':
                tourAgency.removeScheduledTour(scheduledTour.code)
                print("Removal done...")
            else:
                print("Removal canceled.")

        else:
            print(f"Scheduled tour with code {scheduledTourCode} not found.")

        option = input("\nDo you want to remove another scheduled tour? (Y/N): ").upper()
        if option != 'Y':
            break

#Booking Management
def bookingManagement(tourAgency):
    while True:
        print("\n<<<< Booking Management >>>>")
        print("1. Create Booking")
        print("2. Cancel Bookings")
        print("3. Add Seats to Bookings")
        print("4. List Bookings")
        print("0. Back to main menu")
        choice = input("Enter choice: ")

        if choice == '1':
            createBooking(tourAgency)
        elif choice == '2':
            cancelBooking(tourAgency)
        elif choice == '3':
            addSeatsToBooking(tourAgency)
        elif choice == '4':
            listBookings(tourAgency)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

#Booking Menu Option 1: Create Booking
def createBooking(tourAgency):
    while True:
        passportNumber = input("Enter passport number: ")
        passportNumber = passportNumber.upper()
        customer = tourAgency.searchCustomer(passportNumber)        
        if customer is None:
            print("Customer not found. Please register with the Tour Agency first.")
        passportNumbers = []
        passportNumbers.append(passportNumber)
        print("\nList of open scheduled tours:")
        print("=============================")
        print(tourAgency.listOpenScheduledTours())

        scheduleTourCode = input("Enter Schedule Tour Code: ")
        scheduledTour = tourAgency.searchScheduledTour(scheduleTourCode)
        
        if scheduledTour is None:
            print("Scheduled tour not found.")
            continue

        bookingType = input("(I)ndividual or (G)roup Booking? ").upper()
        
        if bookingType not in ['I', 'G']:
            print("Invalid booking type.")
            continue
        singleRoom = False
        if bookingType == 'I':
            if input("Single Room (Y/N): ").upper() == 'Y':
                singleRoom = True
            booking = tourAgency.addBooking(scheduledTour, [customer], 'I', singleRoom)
        else:  # Assuming it's always 'G' if not 'I'
            while True:
                passport = input("Enter passport number <enter to stop>: ").strip().upper()
                if passport:
                    passportNumbers.append(passport)
                else:
                    break
            customers = [tourAgency.searchCustomer(passport) for passport in passportNumbers]            
            booking = tourAgency.addBooking(scheduledTour, customers, 'G', singleRoom)
        print("Booking is added...\n")
        print(booking)

        option = input("\nDo you want to create another booking? (Y/N): ").upper()
        if option != 'Y':
            break

#Booking Menu Option 2: Cancel Booking
def cancelBooking(tourAgency):
    while True:
        print("\n<< Cancel Booking >>")
        bookingId = input("Enter booking Id: ")

        try:
            bookingId = int(bookingId)
        except ValueError:
            print("Invalid input. Booking Id must be an integer.")
            continue

        booking = tourAgency.searchBooking(bookingId)

        if booking is None:
            print("Booking with this ID does not exist.")
            continue

        print(booking)

        for customer in booking.customers:
            print(customer)

        penalty_amount = booking.getPenaltyAmount()
        print(f"Penalty for cancellation: ${penalty_amount:.2f}")

        confirmation = input("Proceed to cancel (Y/N): ").upper()

        if confirmation == 'Y':
            try:
                tourAgency.cancelBooking(bookingId)
                print("Cancellation done... Please pay $%.2f." % penalty_amount)
            except BookingException as e:
                print(e)
        else:
            print("Cancellation aborted.")

        option = input("\nDo you want to cancel another booking? (Y/N): ").upper()
        if option != 'Y':
            break

#Booking Menu Option 3: Add Seats to Booking
def addSeatsToBooking(tourAgency):
    while True:
        print("\n<< Add Seats to Booking >>")
        bookingId = input("Enter booking Id: ")

        try:
            bookingId = int(bookingId)
        except ValueError:
            print("Invalid input. Booking Id must be an integer.")
            continue

        booking = tourAgency.searchBooking(bookingId)

        if booking is None:
            print("Booking with this ID does not exist.")
            continue

        if isinstance(booking, IndividualBooking):
            print("Individual booking cannot add travelers.")
            continue

        print("Enter passport number <enter to stop> : ")
        passportNumbers = []
        while True:
            passport = input().strip().upper()
            if passport:
                passportNumbers.append(passport)
            else:
                break

        customers = [tourAgency.searchCustomer(passport) for passport in passportNumbers]

        try:
            additional_cost = tourAgency.addSeats(bookingId, customers)
            print(f"Seats added, please pay ${additional_cost:.2f}")
        except BookingException as e:
            print(e)

        option = input("\nDo you want to add seats to another booking? (Y/N): ").upper()
        if option != 'Y':
            break


#Booking Menu Option 4: List Bookings
def listBookings(tourAgency):
    print("\n<< List Bookings >>")
    print(tourAgency.listBookings())

if __name__ == "__main__":
    main()