from collections import UserDict, defaultdict
from datetime import datetime, timedelta

weekday_names = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError("The phone number must have 10 digits")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                return
        raise ValueError("Phone number not found")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        raise ValueError("Phone number not found")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        birthday_dict = defaultdict(list)
        today = datetime.today().date()
        current_weekday = today.weekday()

        for record in self.data.values():
            name = record.name.value
            print(type(record.birthday))
            birthday = datetime.strptime(
                record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days
            birthday_weekday = birthday_this_year.weekday()
            if birthday_weekday in [5, 6]:
                delta_days += 7 - birthday_weekday

            if delta_days < 7:
                greeting_weekday = (current_weekday + delta_days) % 7
                birthday_dict[weekday_names[greeting_weekday]].append(name)

        print(birthday_dict)
        result = ''
        for day, names in birthday_dict.items():
            result += f"{day}: {', '.join(names)}\n"
        return result


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone(10 digits) please."
        except IndexError:
            return "Give me name please."

    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    if name not in book.data:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        return "Contact with the same name already exists."


@input_error
def change_contact(args, book):
    name, new_phone = args
    if name in book.data:
        record = book.find(name)
        record.edit_phone(record.phones[0].value, new_phone)
        return "Contact updated."
    else:
        return "Contact not found."


@input_error
def show_phone(args, book):
    name = args[0]
    if name in book.data:
        record = book.find(name)
        return record.phones[0].value
    else:
        return "Contact not found."


@input_error
def show_all(book):
    contacts = []
    for record in book.data.values():
        contacts.append(f"{record.name.value}: {record.phones[0].value}")
    return "\n".join(contacts)


def add_birthday(args, book):
    if len(args) != 2:
        return "Invalid number of arguments. Provide name and birthday."

    name, birthday = args
    try:
        datetime.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        return "Incorrect date format. Should be 'DD.MM.YYYY'."

    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday}."
    elif record and not record.birthday:
        return f"{name} has no birthday set."
    else:
        return f"Contact {name} not found."


def birthdays(book):
    upcoming_birthdays = book.get_birthdays_per_week()
    if upcoming_birthdays:
        return upcoming_birthdays
    else:
        return "No upcoming birthdays in the next week."


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            else:
                raise
        except:
            print("Invalid command.")


if __name__ == "__main__":
    main()
