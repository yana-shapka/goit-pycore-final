import pickle
from personal_assistant.models import AddressBook
from personal_assistant.notes import NoteBook, Note


def save_contacts(book: AddressBook, filename: str = "addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_contacts(filename: str = "addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def save_notes(notebook: NoteBook, filename: str = "notebook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


def load_notes(filename: str = "notebook.pkl") -> NoteBook:
    try:
        with open(filename, "rb") as f:
            notebook = pickle.load(f)
            if notebook.data:
                Note._counter = max(notebook.data.keys())
            return notebook
    except FileNotFoundError:
        return NoteBook()
