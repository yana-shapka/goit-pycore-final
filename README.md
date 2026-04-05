# 🤖 Personal Assistant CLI

A command-line personal assistant for managing contacts and notes.
Data is saved automatically and restored on next launch.

---

## Installation

1. Clone the repository:

```bash
   git clone https://github.com/yana-shapka/goit-pycore-final
   cd goit-pycore-final
```

2. Install as a package:

```bash
   pip install -e .
```

3. Run from anywhere:

```bash
   assistant
```

Or directly:

```bash
   python -m personal_assistant.main
```

---

## Commands

### Contacts

| Command                              | Description                          |
| ------------------------------------ | ------------------------------------ |
| `add-contact [name] [phone]`         | Add contact (phone optional)         |
| `add-phone [name] [phone]`           | Add phone to existing contact        |
| `delete-contact [name]`              | Delete a contact                     |
| `change-phone [name] [old] [new]`    | Change phone number                  |
| `show-phone [name]`                  | Show contact's phones                |
| `all-contacts`                       | Show all contacts                    |
| `search-contact [query]`             | Search by name, phone or email       |
| `add-email [name] [email]`           | Add email                            |
| `change-email [name] [email]`        | Update email                         |
| `add-address [name] [address...]`    | Add address                          |
| `change-address [name] [address...]` | Update address                       |
| `add-birthday [name] [DD.MM.YYYY]`   | Add birthday                         |
| `show-birthday [name]`               | Show birthday                        |
| `birthdays [days]`                   | Upcoming birthdays (default: 7 days) |

### Notes

| Command                        | Description          |
| ------------------------------ | -------------------- |
| `add-note [text...]`           | Add a new note       |
| `all-notes`                    | Show all notes       |
| `find-note [query]`            | Search notes by text |
| `edit-note [id] [new text...]` | Edit a note          |
| `delete-note [id]`             | Delete a note        |

### System

| Command          | Description        |
| ---------------- | ------------------ |
| `help`           | Show all commands  |
| `close` / `exit` | Save data and exit |

---

## Data Storage

All data is saved automatically to:

- `addressbook.pkl` — contacts
- `notebook.pkl` — notes

Data is restored automatically on next launch.

---

## Project Structure

```
goit-pycore-final/
├── personal_assistant/
│   ├── __init__.py
│   ├── models.py       # AddressBook, Record, Field classes
│   ├── notes.py        # NoteBook, Note classes
│   ├── handlers.py     # Command handler functions
│   ├── storage.py      # Save/load data
│   └── main.py         # Entry point, main loop
├── setup.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore
```
