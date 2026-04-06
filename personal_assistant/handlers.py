from typing import List
from personal_assistant.models import AddressBook, Record
from personal_assistant.notes import NoteBook


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            msg = str(e)
            if "not enough values to unpack" in msg:
                return "❌ Please provide all required arguments."
            return f"❌ {msg}"
        except KeyError as e:
            msg = str(e).strip("'\"")
            return f"❌ {msg}" if msg else "❌ Not found."
        except IndexError:
            return "❌ Please provide all required arguments."
    return inner


# =================== CONTACTS ===================

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    if not args:
        raise IndexError
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    record = book.find(name)
    message = f"✅ Phone added to existing contact '{name}'."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"✅ Contact '{name}' added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_phone(args: List[str], book: AddressBook) -> str:
    name, phone = args
    record = book.get(name)
    record.add_phone(phone)
    return f"✅ Phone {phone} added to '{name}'."


@input_error
def delete_contact(args: List[str], book: AddressBook) -> str:
    name = args[0]
    book.delete(name)
    return f"✅ Contact '{name}' deleted."


@input_error
def change_phone(args: List[str], book: AddressBook) -> str:
    name, old_phone, new_phone = args
    record = book.get(name)
    record.edit_phone(old_phone, new_phone)
    return f"✅ Phone updated for '{name}': {old_phone} → {new_phone}."


@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.get(name)
    if not record.phones:
        return f"📭 '{name}' has no phone numbers."
    return f"📞 {name}'s phones: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "📭 Address book is empty."
    lines = []
    for i, record in enumerate(book.data.values(), 1):
        lines.append(f"{i}. {record}")
    return "\n".join(lines)


@input_error
def search_contacts(args: List[str], book: AddressBook) -> str:
    query = " ".join(args)
    if not query.strip():
        raise ValueError("Enter a search query.")
    results = book.search(query)
    if not results:
        return f"🔍 No contacts found matching '{query}'."
    header = f"🔍 Found {len(results)} contact(s) matching '{query}':\n"
    return header + "\n".join(str(r) for r in results)


@input_error
def add_email(args: List[str], book: AddressBook) -> str:
    name, email = args
    record = book.get(name)
    record.add_email(email)
    return f"✅ Email {email} added to '{name}'."


@input_error
def change_email(args: List[str], book: AddressBook) -> str:
    name, email = args
    record = book.get(name)
    record.add_email(email)
    return f"✅ Email updated for '{name}': {email}."


@input_error
def add_address(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Please provide name and address.")
    name = args[0]
    address = " ".join(args[1:])
    record = book.get(name)
    record.add_address(address)
    return f"✅ Address added to '{name}'."


@input_error
def change_address(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Please provide name and address.")
    name = args[0]
    address = " ".join(args[1:])
    record = book.get(name)
    record.add_address(address)
    return f"✅ Address updated for '{name}'."


@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, date = args
    record = book.get(name)
    record.add_birthday(date)
    return f"✅ Birthday {date} added to '{name}'."


@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.get(name)
    if record.birthday is None:
        return f"📭 No birthday set for '{name}'."
    return f"🎂 {name}'s birthday: {record.birthday}."


@input_error
def birthdays(args: List[str], book: AddressBook) -> str:
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"📭 No upcoming birthdays in the next {days} days."
    lines = [f"🎂 Upcoming birthdays in the next {days} days:"]
    lines += [f"  🎉 {b['name']}: {b['congratulation_date']}" for b in upcoming]
    return "\n".join(lines)


# =================== NOTES ===================

@input_error
def add_note(args: List[str], notebook: NoteBook) -> str:
    text = " ".join(args)
    if not text.strip():
        raise ValueError("Note text cannot be empty.")
    note = notebook.add_note(text)
    return f"✅ Note added. (ID: {note.id})"


@input_error
def show_all_notes(notebook: NoteBook) -> str:
    if not notebook.data:
        return "📭 No notes saved."
    lines = [str(note) for note in notebook.data.values()]
    return "📝 Your notes:\n" + "\n".join(lines)


@input_error
def find_note(args: List[str], notebook: NoteBook) -> str:
    query = " ".join(args)
    if not query.strip():
        raise ValueError("Enter a search query.")
    results = notebook.search(query)
    if not results:
        return f"🔍 No notes found matching '{query}'."
    return f"🔍 Found {len(results)} note(s):\n" + "\n".join(str(n) for n in results)


@input_error
def edit_note(args: List[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Please provide note ID and new text.")
    note_id = int(args[0])
    new_text = " ".join(args[1:])
    note = notebook.find_by_id(note_id)
    if note is None:
        raise KeyError(f"Note with ID {note_id} not found.")
    note.edit(new_text)
    return f"✅ Note {note_id} updated."


@input_error
def delete_note(args: List[str], notebook: NoteBook) -> str:
    note_id = int(args[0])
    notebook.delete(note_id)
    return f"✅ Note {note_id} deleted."


# =================== HELP ===================

def show_help() -> str:
    return """
📖 Available commands:

👤 CONTACTS
  add-contact [name] [phone]          : Add contact (phone optional)
  add-phone [name] [phone]            : Add phone to existing contact
  delete-contact [name]               : Delete a contact
  change-phone [name] [old] [new]     : Change phone number
  show-phone [name]                   : Show contact's phones
  all-contacts                        : Show all contacts
  search-contact [query]              : Search by name, phone, email or address
  add-email [name] [email]            : Add email
  change-email [name] [email]         : Update email
  add-address [name] [address...]     : Add address
  change-address [name] [address...]  : Update address
  add-birthday [name] [DD.MM.YYYY]    : Add birthday
  show-birthday [name]                : Show birthday
  birthdays [days]                    : Upcoming birthdays (default: 7 days)

📝 NOTES
  add-note [text...]                  : Add a new note
  all-notes                           : Show all notes
  find-note [query]                   : Search notes by text
  edit-note [id] [new text...]        : Edit a note
  delete-note [id]                    : Delete a note

⚙️  SYSTEM
  help                                : Show this message
  close / exit                        : Save data and exit
"""