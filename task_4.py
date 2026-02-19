from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return f"Error: Contact '{e.args[0]}' not found."
        except IndexError:
            return "Invalid arguments."
    return inner


def parse_input(user_input):
    """
    Parses the user input into a command and arguments.
    """
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    """
    Adds a new contact or updates an existing one.
    Usage: add [name] [phone]
    """
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Updates the phone number for an existing contact.
    Usage: change [name] [new_phone]
    """
    name, phone = args
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """
    Shows the phone number for a specific contact.
    Usage: phone [name]
    """
    name = args[0]
    return f"Phone number for '{name}': {contacts[name]}"


def show_all(contacts):
    """
    Displays all saved contacts.
    Usage: all
    """
    header = f"{'Name':<15} | {'Phone':<15}"
    separator = "-" * len(header)

    lines = [header, separator]

    for name, phone in sorted(contacts.items()):
        lines.append(f"{name:<15} | {phone:<15}")

    return "\n".join(lines)


def main():
    """
    Main loop for the assistant bot.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
        except KeyboardInterrupt:
            print("\nGood bye!")
            break
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
