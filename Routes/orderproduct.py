from typing import List, Optional
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter

import models, scheema, oauth
from database import get_db
from sqlalchemy.orm import Session
import httpx
router = APIRouter()



@router.post('/allcustomers', response_model= List[scheema.CustomerOut], status_code= status.HTTP_200_OK, tags= ["Orders"])
def allCustomer(db : Session = Depends(get_db)):

    customer_query = db.query(models.Customer).all()

    if not customer_query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Item dose not exist with {id} this id ")
    
    return customer_query


# @router.get('/customers', tags=['customer'])
# def customer():
#     return {"customer : ": "welcome to customers"}

@router.post('/addcustomerinfo', response_model=scheema.CustomerOut, tags= ["Orders"])
def CustomerInfo(customer : scheema.CustomerIn, db : Session = Depends(get_db)):
    query = models.Customer(**customer.dict())
    db.add(query)
    db.commit()
    db.refresh(query)


    # new_order = scheema.Order(query.cust_id)
    # print("query.Customer_id : ",query.cust_id)
    # new_order = {"customer_id" : query.cust_id}
    # print("new_order : ",new_order)
    # print("new_order : ",type(new_order))

    # order_query = models.Orders(**new_order)
    # db.add(order_query)
    # db.commit()
    # db.refresh(order_query)

    return query


# ************************* Orders***************************

@router.post('/neworder', response_model=scheema.OrderOut, tags=["Orders"], status_code=status.HTTP_201_CREATED)

def newOrder(order : scheema.Order ,db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    new_order = models.Orders(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.post('/allorders', response_model=List[scheema.OrderOut], tags=["Orders"])
def getOrders(db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    query = db.query(models.Orders).all()

    if not query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Not Found")
    
    return query

        



# ************************** add orderd items in db*************************

@router.post('/orderitems', response_model= scheema.orderItemsOut, status_code=status.HTTP_201_CREATED, tags= ["OrdersItems"])
async def addItem(item : scheema.orderItems, db : Session = Depends(get_db)):
    
    # order_item = item.dict();
    print("item.product_id : ",item.product_id)
    # product = await httpx.get('http://127.0.0.1:8000/productsfetch')
    product = db.query(models.Products).filter(models.Products.product_id == item.product_id)
    product_result  = product.first()
    # product_result = scheema.productOut(product_result)

  

    if not product_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this product dose not exist")
    

    if product_result.quantity < item.order_quantity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avalible quantity is less than your demand")


    new_item = models.OrderITems(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    product_result.quantity = product_result.quantity - item.order_quantity
    update_product = {"product_id" :product_result.product_id, "category_id" :product_result.category_id, "product_name" : product_result.product_name , "price" : product_result.price, "sale_price": product_result.sale_price,"quantity": product_result.quantity, "owner_id" : product_result.owner_id}

    product.update(update_product, synchronize_session=False)
    db.commit()
    db.refresh(product_result)
    print("product : ", product_result)

    return new_item


@router.post('/orderItems', response_model=List[scheema.orderItemsOut], tags=["OrdersItems"])
def getOrderItems(db : Session = Depends(get_db)):
    
    query = db.query(models.OrderITems).all()
    if not query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Item dose not exist with {id} this id ")
    
    return query






    