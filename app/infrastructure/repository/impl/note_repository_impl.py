from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.domain.models.note_model import Note, NoteHistory
from app.domain.models.user_model import User
from app.infrastructure.repository.interfaces.user_note_interfaces import CRUDRep

class NoteRepositoryImpl:
    def create_note(self, db: Session, title: str, description: str, time: datetime, user_id: int):
        
        user_id_reference=db.query(User).filter(user_id == User.username).first().id
        db_note = Note(title=title, description=description, timestamp=time, user_id=user_id_reference)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    def erase_note(self, db: Session, note_id: int, user_id:str):
        note = db.query(Note).join(User).filter(User.username.like(user_id),Note.id == note_id).first()
        
        noteHistory= db.query(NoteHistory).filter(note.id == NoteHistory.note_id).all()
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada o acceso denegado")
        
        for history in noteHistory:
            db.delete(history)
        db.commit()

        db.delete(note)
        db.commit()

    def update_existing_note(self, db: Session, note_id: int, title: str, description: str, version:int, time: datetime, user_id: str):

        note = db.query(Note).join(User).filter(Note.id == note_id, User.username.like(user_id)).first()

        history = NoteHistory(
            note_id=note.id,
            previous_title=note.title,
            previous_description=note.description,
            previous_timestamp=note.timestamp
        )
        historyNotes = db.query(NoteHistory).filter(NoteHistory.note_id == note_id).all()
        if(historyNotes and len(historyNotes) != version):
            raise HTTPException(status_code=409, detail="La nota ya ha sido actualizada anteriormente")
        db.add(history)

        note.title = title
        note.description = description
        note.timestamp = datetime.utcnow()

        db.commit()
        db.refresh(note)
        return note
    
    def get_notes_by_user_rep(self, db: Session, user_id: str) -> List[Note]:
        return db.query(Note).join(User).filter(User.username.like(user_id), User.id==Note.user_id ).all()

    def get_notes_history(self, db: Session,  note_id: int, user_id=str):
        return db.query(NoteHistory).filter(NoteHistory.note_id == note_id).all()