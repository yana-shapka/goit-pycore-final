from collections import UserDict
from datetime import datetime
from typing import Optional


class Note:
    _counter = 0

    def __init__(self, text: str):
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty.")
        Note._counter += 1
        self.id = Note._counter
        self.text = text.strip()
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    def edit(self, new_text: str):
        if not new_text or not new_text.strip():
            raise ValueError("Note text cannot be empty.")
        self.text = new_text.strip()

    def __str__(self) -> str:
        return f"[{self.id}] {self.created_at} | {self.text}"


class NoteBook(UserDict):

    def add_note(self, text: str) -> Note:
        note = Note(text)
        self.data[note.id] = note
        return note

    def find_by_id(self, note_id: int) -> Optional[Note]:
        return self.data.get(note_id)

    def delete(self, note_id: int):
        if note_id not in self.data:
            raise KeyError(f"Note with ID {note_id} not found.")
        del self.data[note_id]

    def search(self, query: str) -> list:
        query = query.lower()
        return [note for note in self.data.values() if query in note.text.lower()]

    def __str__(self) -> str:
        if not self.data:
            return "No notes saved."
        return "\n".join(str(note) for note in self.data.values())
