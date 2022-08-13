from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models, scheema
from typing import List
import json


router = APIRouter()

@router.post('/paymentdata', response_model= scheema.PaymentOut, status_code=status.HTTP_201_CREATED,  tags=["Payment"])
def addPaymentData(payment : scheema.Payment, db : Session = Depends(get_db)):
    
    add_payment = models.Payments(**payment.dict())
    db.add(add_payment)
    db.commit()
    db.refresh(add_payment)

    order_query = db.query(models.Orders).filter(models.Orders.order_id == payment.order_id)
    order = order_query.first();
    if order:
        # print("ordre id : ", order.)
        order_set = {"order_id" :order.order_id ,"customer_id" :order.customer_id,"status": "paid","cost":order.cost}

        order_query.update(order_set, synchronize_session=False)
        db.commit()
    else:
        print("some thing went worng")
    return add_payment

@router.post('/getpaymentdata', response_model= List[scheema.PaymentOut], status_code = status.HTTP_200_OK, tags=["Payment"])
def getPaymentData(db : Session = Depends(get_db)):
    payment_query = db.query(models.Payments).all()

    if not payment_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found")
    
    return payment_query




