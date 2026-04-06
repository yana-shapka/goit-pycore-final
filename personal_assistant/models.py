import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name is required.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value: str):
        if not self._validate(value):
            raise ValueError(
                f"Invalid phone number '{value}'. Must be exactly 10 digits."
            )
        super().__init__(value)

    def _validate(self, value: str) -> bool:
        return value.isdigit() and len(value) == 10


class Email(Field):
    def __init__(self, value: str):
        if not self._validate(value):
            raise ValueError(
                f"Invalid email format '{value}'. Example: name@example.com"
            )
        super().__init__(value)

    def _validate(self, value: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return bool(re.match(pattern, value))


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError(
                f"Invalid date format '{value}'. Please use DD.MM.YYYY (e.g. 25.12.1990)."
            )

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str):
        if self.find_phone(phone):
            raise ValueError(f"Phone {phone} already exists for this contact.")
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj is None:
            raise ValueError(f"Phone {phone} not found for this contact.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError(f"Phone {old_phone} not found for this contact.")
        self.phones[self.phones.index(phone_obj)] = Phone(new_phone)

    def add_email(self, email: str):
        self.email = Email(email)

    def remove_email(self):
        self.email = None

    def add_address(self, address: str):
        self.address = Address(address)

    def remove_address(self):
        self.address = None

    def add_birthday(self, date_str: str):
        self.birthday = Birthday(date_str)

    def remove_birthday(self):
        self.birthday = None

    def __str__(self) -> str:
        phones = "; ".join(p.value for p in self.phones) or "none"
        email = str(self.email) if self.email else "none"
        address = str(self.address) if self.address else "none"
        birthday = str(self.birthday) if self.birthday else "none"
        return (
            f"Name:     {self.name.value}\n"
            f"  Phones:  {phones}\n"
            f"  Email:   {email}\n"
            f"  Address: {address}\n"
            f"  Birthday:{birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def get(self, name: str) -> Record:
        record = self.data.get(name)
        if record is None:
            raise KeyError(f"Contact '{name}' not found.")
        return record

    def delete(self, name: str):
        if name not in self.data:
            raise KeyError(f"Contact '{name}' not found.")
        del self.data[name]

    def search(self, query: str) -> List[Record]:
        query = query.lower()
        results = []
        for record in self.data.values():
            if (
                query in record.name.value.lower()
                or any(query in p.value for p in record.phones)
                or (record.email and query in record.email.value.lower())
                or (record.address and query in record.address.value.lower())
            ):
                results.append(record)
        return results

    def get_upcoming_birthdays(self, days: int = 7) -> List[dict]:
        upcoming = []
        today = datetime.today().date()

        for record in self.data.values():
            if not record.birthday:
                continue

            try:
                bday = record.birthday.value.replace(year=today.year)
            except ValueError:
                bday = record.birthday.value.replace(year=today.year, month=3, day=1)

            if bday < today:
                try:
                    bday = bday.replace(year=today.year + 1)
                except ValueError:
                    bday = bday.replace(year=today.year + 1, month=3, day=1)

            if 0 <= (bday - today).days <= days:
                if bday.weekday() >= 5:
                    bday += timedelta(days=7 - bday.weekday())
                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": bday.strftime("%d.%m.%Y"),
                })

        return upcoming