from personal_assistant.storage import (
    load_contacts,
    load_notes,
    save_contacts,
    save_notes,
)
from personal_assistant.handlers import (
    add_contact,
    add_phone,
    delete_contact,
    change_phone,
    show_phone,
    show_all,
    search_contacts,
    add_email,
    change_email,
    add_address,
    change_address,
    add_birthday,
    show_birthday,
    birthdays,
    add_note,
    show_all_notes,
    find_note,
    edit_note,
    delete_note,
    show_help,
)


def parse_input(user_input: str):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args


def main():
    book = load_contacts()
    notebook = load_notes()
    print("Welcome to Personal Assistant!")
    print("Type 'help' to see all commands.")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if not command:
                continue

            if command in ["close", "exit"]:
                break

            elif command == "help":
                print(show_help())

            # --- CONTACTS ---
            elif command == "add-contact":
                print(add_contact(args, book))
            elif command == "add-phone":
                print(add_phone(args, book))
            elif command == "delete-contact":
                print(delete_contact(args, book))
            elif command == "change-phone":
                print(change_phone(args, book))
            elif command == "show-phone":
                print(show_phone(args, book))
            elif command == "all-contacts":
                print(show_all(book))
            elif command == "search-contact":
                print(search_contacts(args, book))
            elif command == "add-email":
                print(add_email(args, book))
            elif command == "change-email":
                print(change_email(args, book))
            elif command == "add-address":
                print(add_address(args, book))
            elif command == "change-address":
                print(change_address(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))

            # --- NOTES ---
            elif command == "add-note":
                print(add_note(args, notebook))
            elif command == "all-notes":
                print(show_all_notes(notebook))
            elif command == "find-note":
                print(find_note(args, notebook))
            elif command == "edit-note":
                print(edit_note(args, notebook))
            elif command == "delete-note":
                print(delete_note(args, notebook))

            else:
                print("Invalid command. Type 'help' to see all commands.")

    except KeyboardInterrupt:
        print("\nInterrupted. Saving data...")
    finally:
        save_contacts(book)
        save_notes(notebook)
        print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()
