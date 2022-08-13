from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional,List




class UserType(BaseModel):
    usertype : str
class UserTypeIn(UserType):
    pass
class UserTypeOut(UserType):
    usertype_id : int
    class Config:
        orm_mode=True

class User(BaseModel):
    email : EmailStr

class UserOut(User):  
    user_id : int  
    created_at : datetime
    class Config:
        orm_mode = True

class UserIn(User):
    password : str

# token
class Token(BaseModel):
    access_token : str
    token_type : str
    
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : Optional[str] = None
    


class Customer(BaseModel):
    name : str
    email : EmailStr
    phone_no : str
    Address : str
    
class CustomerIn(Customer):
    pass



# class categories(BaseModel):
#     name : str
#     cat_type : str

class Product(BaseModel):
    category_id : int
    product_name : str
    price : float
    sale_price : float
    quantity : int 

class ProductIn(Product):
    pass

class productImage(BaseModel):
    image_id : int
    image_name : str
    image_ext : str 
    image_size : str
    class Config:
        orm_mode=True

class productOut(Product):
    product_id : int
    owner_id : int
    owner : UserOut
    images : List[productImage]
    class Config:
        orm_mode = True

class Category(BaseModel):
    category_name : str
    category_type : str
    owner_id : int

class CategoryOut(Category):
    category_id : int
    owner  : UserOut
    class Config:
        orm_mode = True

class Order(BaseModel):
    customer_id : Optional[int] = None
    cost : float


    
class CustomerOut(Customer):
    cust_id : int
    # orders : OrderOut
    class Config:
        orm_mode=True
        
class OrderOut(Order):
    order_id : int
    customer : CustomerOut
    class Config:
        orm_mode = True

class orderItems(BaseModel):
    order_id : int
    product_id : int
    order_quantity : int
# 
# class OrderItemsOut(orderItems):
    

class orderItemsOut(orderItems):
    order_item_id : int
    order : OrderOut
    class Config:
        orm_mode = True


class Payment(BaseModel):
    order_id : int
    transaction_id  : str

class PaymentOut(Payment):
    payment_id : int
    orders : OrderOut
    class Config:
        orm_mode= True
