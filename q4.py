from q1 import *
from q2 import *
from q3 import *
class TourAgency:
    def __init__(self):
        #instance variables
        self._tours = []
        self._customers = []
        self._scheduledTours = []
        self._bookings = []
    
    #search methods
    def searchCustomer(self, passportNumber: str) -> Customer:
        for customer in self._customers:
            if passportNumber == customer.passportNumber:
                return customer
        return None
    
    def searchTour(self, code: str) -> Tour:
        for tour in self._tours:
            if code == tour.code:
                return tour
        return None
    
    def searchScheduledTour(self, code: str) -> ScheduledTour:
        for scheduledtour in self._scheduledTours:
            if code == scheduledtour.code:
                return scheduledtour
        return None

    def searchBooking(self, bookingId: int) -> Booking:
        for booking in self._bookings:
            if bookingId == booking.bookingId:
                return booking
        return None
    
    #list methods
    def listTours(self) -> str:
        return "\n".join([str(tour) for tour in self._tours])
    
    def listBookings(self) -> str:
        return "\n".join([str(booking) for booking in self._bookings])

    def listScheduledTours(self) -> str:
        sorted_tours = sorted(self._scheduledTours, key=lambda x: x.departureDateTime)
        return "\n".join([str(scheduledtour) for scheduledtour in sorted_tours])
    
    def listOpenScheduledTours(self) -> str:
        return "\n".join([str(scheduledtour) for scheduledtour in self._scheduledTours if scheduledtour.status])
    
    #generic add methods
    def addCustomer(self, customer: Customer):
        if self.searchCustomer(customer.passportNumber) is not None:
            raise BookingException("Customer already exists!!")
        self._customers.append(customer)
    
    def addTour(self, tour: Tour):
        if self.searchTour(tour.code) is not None:
            raise BookingException("Tour already exists!!")
        self._tours.append(tour)
    
    def addScheduledTour(self, st: ScheduledTour):
        if self.searchScheduledTour(st.code) is not None:
            raise BookingException("Scheduled tour already exists!!")
        self._scheduledTours.append(st)
    
    #remove scheduled tour
    def removeScheduledTour(self, code: str):
        st = self.searchScheduledTour(code)
    
        if st is None:
            raise BookingException("Scheduled tour does not exist. Please try another code !!")    
        for booking in self._bookings:
            if booking.st.code == code:
                raise BookingException("Cannot remove scheduled tour with bookings!!")
    
        self._scheduledTours.remove(st)

    #add Booking method
    def addBooking(self, st: ScheduledTour, customers: list, type: str, single: bool) -> Booking:
        if not st.status:
            raise BookingException("Scheduled tour is not open for booking.")
        # for customer in customers:
        #     for booking in self._bookings:
        #         if booking.scheduledTour.code == st.code and booking.searchCustomer([customer.passportNumber]):
        #             raise BookingException("Customer is already booked for this scheduled tour.")
        if type == 'I':
            booking = IndividualBooking(st, customers[0], single)
        elif type == 'G':
            booking = GroupBooking(st, customers)
        else:
            raise BookingException("Invalid booking type. Use 'I' for individual booking and 'G' for group booking.")
        self._bookings.append(booking)
        return booking
    
    #cancelBooking method
    def cancelBooking(self, bookingId: int):
        booking = self.searchBooking(bookingId)
        if booking is None:
            raise BookingException("Booking with this ID does not exist.")
        self._bookings.remove(booking)
        st = booking.scheduledTour
        st.cancelSeats(1)
    
    def addSeats(self, bookingId: int, customers: list) -> float:
        booking = self.searchBooking(bookingId)
        if booking is None:
            raise BookingException("Booking with this ID does not exist.")
        st = booking.scheduledTour
        if not st.status:
            raise BookingException("Scheduled tour is not open for booking.")
        booking.addSeats(customers)
        cost = st.cost
        pax = len(customers)
        return cost * pax 
if __name__ == "__main__":
    tA = TourAgency()
    t1 = Tour('VNDA06', 'Discover Vietnam', 6,5,999.00)
    tA.addScheduledTour(ScheduledTour(808, t1, datetime(2024, 5, 5, 10, 30), 'English', 30))
    print(tA.listScheduledTours())
    print(tA.searchScheduledTour('VNDA06-808'))