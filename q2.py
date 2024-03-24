from q1 import Tour
from datetime import datetime
class ScheduledTour:
    _HANDLING_FEE = 120
    
    @classmethod
    def getHandlingFee(cls) -> float:
        return cls._HANDLING_FEE
    
    def __init__(self, scheduledCode:str, tour: Tour, departureDateTime: datetime, lang: str, capacity:int) -> None:
        self._scheduleCode = scheduledCode
        self._tour = tour
        self._departureDateTime = departureDateTime
        self._lang = lang
        self._capacity = capacity
        self._seatsAvailable = capacity
        self._status = True
        
    
    @property
    def code(self) -> str:
        return f"{self._tour.code}-{self._scheduleCode}"
    
    @property
    def cost(self) -> float:
        return self._tour.cost
    
    @property
    def departureDateTime(self) -> datetime:
        return self._departureDateTime
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def seatsAvailable(self) -> int:
        return self._seatsAvailable
    
    @property
    def status(self) -> bool:
        return self._status
    
    @status.setter
    def status(self, newStatus: bool):
        self._status = newStatus
        
    def bookSeats(self, qty:int) -> bool:
        if self._status and 0 < qty <= self._seatsAvailable:
            self._seatsAvailable -= qty
            return True
        else:
            return False
    def cancelSeats(self, qty: int) -> bool:
        if self._status and 0 < qty <= (self._capacity - self._seatsAvailable):
            self._seatsAvailable += qty
            return True
        else:
            return False
    def getPenaltyRate(self, days: int) -> float:
        if days <= 7:
            return 1.0  
        elif days <= 14:
            return 0.5
        elif days <= 45:
            return 0.25
        elif days >= 46:
            return 0.1
        else:
            return 1.0
    def __str__(self) -> str:
        return f"Name: {self._tour.name} ({self._tour.daysNights})\tBase Cost: ${self.cost:,.2f}\nCode: {self.code}\tDeparture: {self.departureDateTime.strftime('%d')}-{self.departureDateTime.strftime('%b')}-{self.departureDateTime.year} {self.departureDateTime.strftime('%H')}:{self.departureDateTime.strftime('%M')}\tLanguage: {self._lang}\nCapacity: {self.capacity}\tAvailable: {self.seatsAvailable}\tOpen: {'Yes' if self.status == True else 'No'}"

class PeakScheduledTour(ScheduledTour):
    _HANDLING_FEE = 200
    _SURCHARGE = 0.15

    def __init__(self, scheduledCode: str, tour: Tour, departureDateTime: datetime, lang: str, capacity: int) -> None:
        super().__init__(scheduledCode, tour, departureDateTime, lang, capacity)

    @property
    def cost(self) -> float:
        cost = super().cost * (1 + type(self)._SURCHARGE)
        return cost

    def getPenaltyRate(self, days: int) -> float:
        base_penalty_rate = super().getPenaltyRate(days)
        additional_penalty = 0.1 
        return min(base_penalty_rate + additional_penalty, 1)  # Maximum penalty rate is 100%

if __name__ == "__main__":
    try:
        #Q2c
        # Creating Tour objects
        JP = Tour('JPHA08', 'Best of Hokkaido',8,7,2699.08)
        KO = Tour('KMBK08', 'Mukbang Korea', 8, 6,1699.36)
        VN = Tour('VNDA06', 'Discover Vietnam', 6,5,999.00)

        # Creating ScheduledTour objects
        JP_ST1 = PeakScheduledTour('505', JP, datetime(2024, 5, 5, 10, 30), 'English', 30)
        JP_ST2 = ScheduledTour('408', JP, datetime(2024, 4, 8, 8, 45), 'English', 25)
        KO_ST1 = PeakScheduledTour('503', KO, datetime(2024, 5, 3, 8, 5), 'English', 32)
        KO_ST2 = ScheduledTour('403', KO, datetime(2024, 4, 3, 10, 5), 'Mandarin', 25)
        VN_ST1 = PeakScheduledTour('503', VN, datetime(2024, 5, 3, 11, 8), 'Mandarin', 28)
        
        #print ScheduledTour
        print(JP_ST1)
        print(JP_ST2)
        print(KO_ST1)
        print(KO_ST2)
        print(VN_ST1)
        print(f'='*100)
        
        print(JP_ST1.bookSeats(26))  # Expect False
        print(JP_ST1.seatsAvailable)  # print Available seats

        # Attempt to cancel more seats than booked
        print(JP_ST1.cancelSeats(2))  # Expect False
        print(JP_ST1.seatsAvailable)  # print Available seats

        # Book seats
        print(JP_ST1.bookSeats(5))  # Expect True
        print(JP_ST1.seatsAvailable)

        # Cancel seats
        print(JP_ST1.cancelSeats(2))  # Expect True
        print(JP_ST1.seatsAvailable)

        # Test penalty rate calculation
        for days in range(1, 60):
            penalty_rate = JP_ST1.getPenaltyRate(days)
            print(f"For {days} days, penalty rate is: {penalty_rate}")

        # Change status to False
        JP_ST1.status = False
        print(JP_ST1.status)

    except Exception as e:
        print("An error occurred:", e)