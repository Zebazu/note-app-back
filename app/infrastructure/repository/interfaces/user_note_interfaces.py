from abc import ABC, abstractmethod

class CRUDRep(ABC):
    @abstractmethod
    def create_user(self, db, username, hashed_password):
        pass
    @abstractmethod
    def create_note(self, db, title, description, time, user_id):
        pass
    @abstractmethod
    def erase_note(self, db, note_id, user_id):
        pass
    @abstractmethod
    def update_existing_note(self, db, note_id, title, description, version, time, user_id):
        pass
    @abstractmethod
    def verify_user(self, db, username, password):
        pass
    @abstractmethod
    def get_notes_by_user_rep(self, db, user_id):
        pass
    @abstractmethod
    def get_notes_history(self, db,  note_id, user_id):
        pass
