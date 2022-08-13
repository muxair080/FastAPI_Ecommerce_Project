from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
import scheema, database, models
from config import setting 
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='login')


def create_access_taken(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes= setting.access_token_expire_minutes)
    to_encode.update({'exp' : expire})
    encode_jwt = jwt.encode(to_encode, setting.secret_key, algorithm= setting.algorithm)
    return encode_jwt

def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        id : str = payload.get('user_id')
        if id is None:
            # print('Id', id)
            raise credentials_exception
        
        token_data = scheema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
        
    return token_data


def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentails", headers = {"WWW-Authenticate" : "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.user_id == token.id).first()
    return user