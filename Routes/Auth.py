from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import models, utils, scheema, oauth 
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter() 

@router.post('/login', response_model=scheema.Token, tags= ["Login"])
def Login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    user  = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print("user id : ",user.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Found")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "You have enterd wrong password try again")
    

    access_token = oauth.create_access_taken(data= {"user_id" : user.user_id})
    return {"access_token" : access_token, "token_type" : "bearer"}