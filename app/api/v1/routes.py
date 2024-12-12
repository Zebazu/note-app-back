from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.dto.note_dto import NoteDTO, NoteVersionDTO
from app.services.dto.user_dto import UserDTO
from app.services.note_service import erase_note, get_notes_by_user, getHistory, create_note, update_existing_note
from app.services.user_services import get_current_user, register_user
from app.infrastructure.database import Base, engine
from app.services.user_services import verify_user
from app.utils.auth_service import create_access_token
from app.infrastructure.database import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/register")
def register(user: UserDTO, db: Session = Depends(get_db)):
    try:
        register_user(db, user.username, user.password)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(user: UserDTO, db: Session = Depends(get_db)):
    try:
        verified_user = verify_user(db, user.username, user.password)
        access_token = create_access_token(data={"sub": verified_user.username})
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=e.args)
    


@router.get("/notes")
def get_notes(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = current_user["sub"] 
    notes = get_notes_by_user(db, user_id)
    return {"notes": notes}

@router.post("/notes")
def add_note(note: NoteDTO, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["sub"]
    
    try:
        created_note = create_note(db=db, title=note.title, description=note.description, time=note.time, user_id=user_id)
        return {"message": "Note created successfully",  "note":created_note}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/notes/{note_id}")
def update_note(
    note_id: int, 
    note_data: NoteVersionDTO, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["sub"]
    try:
        update_existing_note(db=db, note_id=note_id, title=note_data.title, description=note_data.description, version=note_data.version, time=note_data.time, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    return {"message": "Note updated successfully"}

@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["sub"]
    try:
        erase_note(db=db,note_id=note_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"message": "Note deleted successfully"}

@router.get("/notes/{note_id}/history")
def get_note_history(note_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    print(note_id)
    user_id = current_user["sub"]
    try:
        history=getHistory(db=db, note_id=note_id, user_id=user_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"history": history}
    