from datetime import datetime
class CustomerException(Exception):
    pass

class Customer:
    def __init__(self, passportNumber: str, name: str, dob: datetime, contact: int) -> None:
        if not passportNumber:
            raise CustomerException("Passport number is required.")
        self._passportNumber = passportNumber
        self._name = name
        self._dob = dob
        self._contact = contact
    @property
    def passportNumber(self) -> str:
        return self._passportNumber
    @property
    def name(self) -> str:
        return self._name
    @property
    def dob(self) -> datetime:
        return self._dob
    @property
    def contact(self) -> int:
        return self._contact
    
    @contact.setter
    def contact(self, newContact: int):
        self._contact = newContact
    
    def getAge(self) -> int:
        age = datetime.now().year - self.dob.year
        return int(age)
        
    def __str__(self) -> str:
        return f"Passport: {self._passportNumber}\tName: {self._name}\tAge: {self.getAge()}\tContact: {self._contact}"

#Q1b    
class Tour:
    def __init__(self, tourCode:str, tourName:str, days:int, nights:int, cost:float) -> None:
        self._code = tourCode
        self._name = tourName
        self._days = days
        self._nights = nights
        self._cost = cost
    @property
    def code(self) -> str:
        return self._code
    @property
    def name(self) -> str:
        return self._name
    @property
    def cost(self) -> float:
        return self._cost
    @cost.setter
    def cost(self, newCost:float):
        self._cost = newCost
    @property
    def daysNights(self) -> str:
        return f"{self._days}D/{self._nights}N"
    def __str__(self) -> str:
        return f"Tour Code: {self.code}\tName: {self.name} ({self.daysNights})\tBase Cost: ${self.cost:,.2f}"
    
if __name__ == "__main__":
    
    #Q1a
    print('#Q1a')
    c1 = Customer('K4096807E','Wong Yong Heng', datetime(1991, 6, 18),88120023)
    c2 = Customer('K5572364H','Sharon Mok', datetime(1956, 6, 18),96320098)
    c3 = Customer('MB004670I','Soh Yuan Tai', datetime(1971, 6, 18),98783343)
    print(c1)
    print(c2)
    print(c3)
    c3.contact = 12345678
    print(c3.contact)
    #Q1c
    print('#Q1c')
    t1 = Tour('JPHA08', 'Best of Hokkaido',8,7,2699.08)
    t2 = Tour('KMBK08', 'Mukbang Korea', 8, 6,1699.36)
    t3 = Tour('VNDA06', 'Discover Vietnam', 6,5,999.00)
    print(t1)
    print(t2)
    print(t3)
    t3.cost = 1314520.00
    print(f'${t3.cost:,.2f}')
