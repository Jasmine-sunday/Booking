from abc import ABC, abstractmethod
from datetime import datetime
from q2 import *
from q1 import *
class BookingException(Exception):
    pass

class Booking(ABC):
    _NEXT_ID = 1

    def __init__(self, scheduledTour, customers):
        if not scheduledTour.bookSeats(len(customers)):
            raise BookingException("Not enough seats available for booking!!")
        self._scheduledTour = scheduledTour
        self._customers = customers
        self._bookingId = Booking._NEXT_ID
        Booking._NEXT_ID += 1

    @property
    def bookingId(self):
        return self._bookingId

    @property
    def scheduledTour(self):
        return self._scheduledTour

    @property
    def customers(self):
        return self._customers

    @property
    def seats(self):
        return len(self._customers)

    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def addSeats(self, qty):
        pass

    def searchCustomer(self, passport_numbers):

        for customer in self._customers:
            if customer.passportNumber in passport_numbers:
                return True
        return False

    def getPenaltyAmount(self):
        days_difference = (self._scheduledTour.departureDateTime - datetime.now()).days
        penalty_rate = self._scheduledTour.getPenaltyRate(days_difference)
        base_cost = self.cost() 
        handling_charge = self._scheduledTour.getHandlingFee()
        penalty_amount = handling_charge + (penalty_rate * base_cost)
        return min(penalty_amount, base_cost)

    def __str__(self):
        customer_info = "\n".join([f"Passport: {customer.passportNumber}\tName: {customer.name}\tAge: {customer.getAge()}\tContact: {customer.contact}" for customer in self._customers])
        return (f"Booking Id: {self.bookingId}\tSeats: {self.seats}\tFinal Cost: ${self.cost():,.2f}\n"
                f"{self._scheduledTour}\n{customer_info}")

class IndividualBooking(Booking):
    _SINGLE = 0.5

    def __init__(self, scheduledTour, customer, single):
        if not customer:
            raise BookingException("Customer information is required!")
        if single is None:
            raise BookingException("Single room information is required!")
        if isinstance(customer, list):
            raise BookingException("Individual booking can only have one customer!")
        if customer.getAge() < 20:
            raise BookingException("Customer must be at least 20 years old!!")
        super().__init__(scheduledTour, [customer])
        self._single = single

    @property
    def single(self):
        return self._single

    def cost(self):
        base_cost = self._scheduledTour.cost
        if self._single:
            return base_cost * (1 + IndividualBooking._SINGLE)
        return base_cost

    def addSeats(self, customers):
        raise BookingException("Cannot add seats to an individual booking!!")


class GroupBooking(Booking):
    _DISCOUNT = {10: 0.1, 6: 0.05}

    def __init__(self, scheduledTour, customers):
        if len(customers) < 2:
            raise BookingException("Group size must be at least 2!!")
        all_under_20 = True
        for customer in customers:
            if customer.getAge() >= 20:
                all_under_20 = False
                break
        
        if all_under_20:
            raise BookingException("At least one customer must be 20 year old and above!!")
        super().__init__(scheduledTour, customers)

    def getDiscount(self):
        group_size = len(self._customers)
        if group_size < 6:
            return 0
        for size, discount in sorted(GroupBooking._DISCOUNT.items(), reverse=True):
            if group_size >= size:
                return discount
        return 0

    def cost(self):
        base_cost = self._scheduledTour.cost
        discount = self.getDiscount()
        if discount > 0:
            return base_cost * (1 - discount) * len(self._customers)
        return base_cost * len(self._customers)

    def addSeats(self, customers):
        for customer in customers:
            if customer in self._customers:
                raise BookingException("Customer is already in this booking!!")
        if not self._scheduledTour.bookSeats(len(customers)):
            raise BookingException("Scheduled tour may have reached full capacity.")
        self._customers.extend(customers)
        return True


def main():
    try:
        # Reusing 1c
        JP = Tour('JPHA08', 'Best of Hokkaido',8,7,2699.08)
        KO = Tour('KMBK08', 'Mukbang Korea', 8, 6,1699.36)
        VN = Tour('VNDA06', 'Discover Vietnam', 6,5,999.00)

        # Reusing 2c
        JP_ST1 = PeakScheduledTour('505', JP, datetime(2024, 5, 5, 10, 30), 'English', 30)
        JP_ST2 = ScheduledTour('408', JP, datetime(2024, 4, 8, 8, 45), 'English', 25)
        KO_ST1 = PeakScheduledTour('503', KO, datetime(2024, 5, 3, 8, 5), 'English', 32)
        KO_ST2 = ScheduledTour('403', KO, datetime(2024, 4, 3, 10, 5), 'Mandarin', 25)
        VN_ST1 = PeakScheduledTour('503', VN, datetime(2024, 5, 3, 11, 8), 'Mandarin', 28)

        #Add customers
        c1 = Customer('E4428006Z', 'Tan Yan Meng', datetime(1948, 7, 8), 96324545)
        c2 = Customer('K4096807E', 'Wong Yong Heng', datetime(2011, 1, 1), 98790098)
        c3 = Customer('E4501021Z', 'Lee Beng Beng', datetime(1945, 4, 1), 62845234)
        c4 = Customer('K5385050B', 'Liu Gu Feng', datetime(1953, 5, 5), 91776544)
        c5 = Customer('E5572364H', 'Sharon Mok', datetime(2007, 8, 9), 92927865)
        c6 = Customer('E6539436G', 'Raymond Low', datetime(1965, 8, 9), 98007655)
        c7 = Customer('E7004670I', 'Soh Yuan Tai', datetime(1970, 9, 3), 86542201)
        c8 = Customer('K9672820D', 'Gan Siao Buang', datetime(1996, 10, 29), 62543478)
        c9 = Customer('E5904462A', 'Cheng Wei Ren', datetime(2009, 12, 31), 97210234)
        c10 = Customer('E9511525Z', 'Jessica Ong', datetime(1995, 8, 8), 98772534)
        c11 = Customer('K0770957E', 'Alvin Chin', datetime(2007, 8, 1), 62594962)
        c12 = Customer('K9914489J', 'Charles Wong', datetime(1999, 8, 9), 96543322)
        c13 = Customer('E1234567G', 'Alice Oh', datetime(2000, 1, 20), 98989898)
        c14 = Customer('E2714897X', 'Henry Tan', datetime(1960, 12, 15), 97777777)
        c15 = Customer('E2323232Y', 'Joyce Seetoh', datetime(2008, 4, 5), 62349000)
        c16 = Customer('K5324732Y', 'Mary Tham', datetime(2010, 7, 8), 87112345)
        c17 = Customer('K1234771H', 'Marvin Heng', datetime(1965, 2, 13), 89699090)


        # Individual Booking for a customer more than 20 years old
        b1 = IndividualBooking(JP_ST1, c1, False)
        print(b1)
        b1.addSeats(c1)  # expecting BookingException

    except BookingException as e:
        print("Booking Error:", e)
    
    try:
        penalty_amount = b1.getPenaltyAmount()
        print("Penalty Amount:", f"${penalty_amount:,.2f}")
    except BookingException as e:
        print("Booking Error:", e)

    # Individual Booking for a customer less than 20 years old
    print('='*80)
    print('Individual Booking for a customer less than 20 years old:')
    try:                
        b2 = IndividualBooking(KO_ST2, c2, False)  # Expecting BookingException
    except BookingException as e:
        print("Booking Error:", e)

    # Group Booking for 2 customers less than 20 years old
    print('='*80)
    print('Group Booking for 2 customers less than 20 years old:')    
    try:
        b3 = GroupBooking(KO_ST2, [c2, c9])  # Expecting BookingException
    except BookingException as e:
        print("Booking Error:", e)

    # Group Booking for 5 customers with at least one more than 20 years old
    print('='*80)
    print('Group Booking for 5 customers with at least one more than 20 years old:') 
    try:
        b4 = GroupBooking(KO_ST2, [c1, c3, c4, c2, c9])
        print(b4)
        
        print('='*80)
        print('Adding 2 more customers to the booking:') 
        # Adding 2 more customers to the booking
        b4.addSeats([c10, c11])
        print(b4)
        
    except BookingException as e:
        print("Booking Error:", e)

if __name__ == "__main__":
    main()

