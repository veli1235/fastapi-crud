from sqlalchemy.orm import Session
from scheme import *
from models import User
from fastapi import HTTPException
from exception import UserNotFound

def create_user_in_db(data: USerCreateSchema,db:Session):
    new_user = User(username=data.username, password= data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"new user is created"}


def delete_user_in_db(*,data:UserDeleteSchema,db:Session):
    user_in_db = db.query(User).filter(User.username==data.username).first()
    if  not user_in_db :
        raise HTTPException(status_code=404,detail="user has been deleted")
    db.delete(user_in_db)
    db.commit()
    return {"msg":"user is deleted"}

def update_user_in_db(*,username,data:UserUpdateSchema,db:Session):
    is_correct = db.query(User).filter_by(username=username,password=data.password).first()
    if not is_correct :
        raise UserNotFound()
    db.query(User).update({"password": data.new_password})
    db.commit()
    return {"msg":"user is updated"}
    
    
def get_user_from_db(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user :
        raise UserNotFound()
    return {"username":user.username}