from fastapi import FastAPI,Depends
from db import get_db
from sqlalchemy.orm import Session
from scheme  import USerCreateSchema,UserDeleteSchema,UserUpdateSchema
from service import *


app = FastAPI() 
@app.get("/")
def health_check():
    return {"msg":"okey"}


@app.post("/user")
def create_user(item : USerCreateSchema, db:Session = Depends(get_db)):
    message = create_user_in_db(data=item,db=db)
    return message



@app.delete("/user")
def delete_user(item: UserDeleteSchema, db: Session = Depends(get_db)):
    message = delete_user_in_db(data=item,db=db)
    return message
    

@app.put("/password")
def update_user(username, item: UserUpdateSchema, db: Session = Depends(get_db)):
    message = update_password_in_db(username = username,data=item,db=db)
    return message

@app.get("/user")
def get_user(username: str, db: Session = Depends(get_db)):
    message = get_user_from_db(username = username, db = db)
    return message


@app.delete("/users")
def delete_all_user( db: Session = Depends(get_db)):
    message = delete_all_user_in_db(db=db)
    return message
