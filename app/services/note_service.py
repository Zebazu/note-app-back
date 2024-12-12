from datetime import datetime
from sqlalchemy.orm import Session
from app.infrastructure.repository.impl.note_repository_impl import NoteRepositoryImpl
from app.infrastructure.repository.interfaces.user_note_interfaces import CRUDRep

def get_note_repository() -> CRUDRep:
    return NoteRepositoryImpl()

def create_note(db: Session, title: str, description: str, time: datetime, user_id: int):
    noteRepo=get_note_repository()
    if time is None:
            time = datetime.now()
    noteRepo.create_note(db,title,description,time,user_id)

def get_notes_by_user(db: Session, user_id: str):
    noteRepo=get_note_repository()

    return noteRepo.get_notes_by_user_rep(db, user_id)

def getHistory(db: Session,  note_id: int, user_id=str):
    noteRepo=get_note_repository()

    return noteRepo.get_notes_history(db, note_id, user_id)
def update_existing_note(db: Session, note_id: int, title: str, description: str, version:int, time: datetime, user_id: str):
    noteRepo=get_note_repository()

    return noteRepo.update_existing_note(db=db,note_id=note_id, title=title, description=description, version=version, time=time, user_id=user_id)
def erase_note(db, note_id, user_id):
    noteRepo=get_note_repository()

    noteRepo.erase_note(db=db,note_id=note_id, user_id=user_id)
