from fastapi import FastAPI, Response, APIRouter, status,HTTPException, Depends
import models,scheema, utils
from database import get_db
from sqlalchemy.orm import Session
from typing import List
router = APIRouter()
# ,response_model=scheema.User
# ********************************Create Usertype***********************************
@router.post('/create_usertype',status_code=status.HTTP_201_CREATED, response_model=scheema.UserTypeOut,tags=['usertype'])
def create_Usertype(usertype : scheema.UserType, db : Session = Depends(get_db)):
    new_usertype = models.userType(**usertype.dict())
    db.add(new_usertype)
    db.commit()
    db.refresh(new_usertype)

    return new_usertype

@router.get('/allusertypes', status_code=status.HTTP_200_OK, response_model=List[scheema.UserTypeOut],tags=['usertype'])
def get_allusertypes(db : Session = Depends(get_db)):
    query = db.query(models.userType).all()

    if not query:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"usertype database is empty")
    
    return query

@router.put('/updateusertype/{id}', status_code=status.HTTP_201_CREATED, response_model=scheema.UserTypeOut,tags=['usertype'])
def updateUsertype(id : int, usertype : scheema.UserTypeIn, db : Session = Depends(get_db)):
    query = db.query(models.userType).filter(models.userType.usertype_id == id)
    query_update = query.first()
    
    if not query_update:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user at  {id} this id dose not exist")  
    query.update(usertype.dict(),synchronize_session=False)
    db.commit()
    db.refresh(query_update)
    return query_update

# ********************************Create User***********************************
@router.post('/create_user',status_code = status.HTTP_201_CREATED, response_model=scheema.UserOut,tags=["Create User"])
def create_user(user : scheema.UserIn, db : Session = Depends(get_db)):
    hash_password = utils.hash(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    # return {"user : " : new_user}
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=scheema.UserOut,status_code=status.HTTP_200_OK,tags=["Create User"])
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user at  {id} this id dose not exist")
    return user