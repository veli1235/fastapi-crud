from sqlalchemy.orm import Session
from scheme import *
from models import User
from fastapi import HTTPException
from exception import *
import psycopg2
from settings import DATABASE_URL
import bcrypt

def create_user_in_db(data: USerCreateSchema,db:Session):
    hashed_password=bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
    new_user=User(username=data.username,password=hashed_password.decode("utf-8"))
    user=db.query(User).filter_by(username=new_user.username).first()
    if user:
        raise UserIsExists()
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

def update_password_in_db(*,username,data:UserUpdateSchema,db:Session):
    hashed_password1=bcrypt.hashpw(data.new_password.encode("utf-8"),bcrypt.gensalt())
    user = db.query(User).filter_by(username=username).first()

  
    if not user:
        raise UserNotFound()

    if not bcrypt.checkpw(data.password.encode("utf-8"),user.password.encode("utf-8")):
        raise UserNotFound()
    
    db.query(User).filter_by(username=username).update({"password":hashed_password1.decode("utf-8")})
    db.commit()
    return {"msg":"password is updated"}
    
    
def get_user_from_db(*,username:str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user :
        raise UserNotFound()
    return {"username":user.username}

def delete_all_user_in_db(*,db:Session):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM users;")

    cur.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    conn.commit()
    cur.close()
    conn.close()
    return {"msg":"all users deleted"}