from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from ..dependencies import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_todo = models.Todo(**todo.dict(), owner_id=user.id)
    db.add(new_todo)
    db.commit()
    return new_todo

@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)

    db.commit()
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"msg": "Todo deleted"}

@router.patch("/{todo_id}/complete")
def mark_completed(todo_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = True
    db.commit()
    return todo
