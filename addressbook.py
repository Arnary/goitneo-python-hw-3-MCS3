from collections import UserDict
from collections import defaultdict
from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if any((not value.isdigit(), len(value) != 10)):
            raise ValueError("Phone is in the wrong format.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        birthday_validation = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$'
        if not re.match(birthday_validation, value):
            raise ValueError("Date is in the wrong format.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ""

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday if self.birthday != '' else 'no data'}"

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        for idx, abook_phone in enumerate(self.phones):
            if str(abook_phone) == phone:
                self.phones.pop(idx)
                break

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone):
        for abook_phone in self.phones:
            if str(abook_phone) == phone:
                return phone
        return "Phone not found"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        happy_days = defaultdict(list)
        current_day = datetime.today().date()
        for name, record in self.data.items():
            if str(record.birthday) == "":
                continue
            user_Bday = datetime.strptime(str(record.birthday), '%d.%m.%Y')
            user_Bday = datetime.date(user_Bday)
            birthday_this_year = user_Bday.replace(year=current_day.year)

            if birthday_this_year < current_day:
                birthday_this_year = birthday_this_year.replace(
                    year=current_day.year+1)
            delta_days = (birthday_this_year - current_day).days

            if delta_days < 7:
                day_of_the_week = birthday_this_year.strftime("%A")
                current_week_day = current_day.strftime("%A")
                if day_of_the_week == "Saturday" or day_of_the_week == "Sunday":
                    if (current_week_day == "Sunday" or current_week_day == "Monday") and birthday_this_year > current_day:
                        continue

                    happy_days["Monday"].append(name)
                    continue
                happy_days[day_of_the_week].append(name)

        return self.show_bd(happy_days)

    def show_bd(self, happy_days):
        if len(happy_days) == 0:
            return "There are no birthdays for the next 7 days."
        result = list()
        for day, names in happy_days.items():
            weekday_and_names = str()
            weekday_and_names += day + ": "
            for name in names:
                weekday_and_names += name + ", " if name != names[-1] else name
            result.append(weekday_and_names)
        return "\n".join(result)
