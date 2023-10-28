from addressbook import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as ex:
            if str(ex) == "Phone is in the wrong format.":
                return "Phone is in the wrong format."
            elif str(ex) == "Date is in the wrong format.":
                return "Date is in the wrong format."
            elif func.__name__ == "add_contact":
                return "Give me name and phone please."
            elif func.__name__ == "change_contact":
                return "Give me name, old phone and new phone please."
            elif func.__name__ == "add_birthday":
                return "Give me name and birthday please."
            elif func.__name__ == "show_phone" or func.__name__ == "show_birthday":
                return "Give me name please."

            return "Invalid command."
        except IndexError:
            return "You don't have any contacts yet."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    if name not in book.keys():
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    else:
        if book[name].find_phone(phone) == phone:
            return "This phone number already exist."
        else:
            book[name].add_phone(phone)

    return "Contact added."


@input_error
def change_contact(args, book): 
    name, old_phone, new_phone = args
    if name in book.keys():
        book[name].edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError


@input_error
def show_phone(args, book): 
    name, = args
    if name in book.keys():
        phones = [str(phone) for phone in book[name].phones]
        return "\n".join(phones)
    else:
        raise KeyError


@input_error
def show_all(book):  
    contact_book = list()
    if book == {}:
        raise IndexError
    for records in book.values():
        contact_book.append('|{:<}'.format(str(records)))
    return "\n".join(contact_book)


@input_error
def add_birthday(args, book):  
    name, birthday = args
    if name in book.keys():
        book[name].add_birthday(birthday)
        return "Birthday added to contact."
    else:
        raise KeyError


@input_error
def show_birthday(args, book): 
    name, = args
    if name in book.keys() and book[name].birthday == "":
        return "There is no birthday record for this contact."
    elif name in book.keys():
        return book[name].birthday
    else:
        raise KeyError


@input_error
def birthdays(book):
    if book == {}:
        raise IndexError
    else:
        return book.get_birthdays_per_week()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
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
            print("Invalid command.")


if __name__ == "__main__":
    main()
