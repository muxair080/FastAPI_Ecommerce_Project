from  sqlalchemy import Column, ForeignKey, Integer, String,Boolean ,Float 
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"
    cust_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_no = Column(String, nullable=False)
    Address = Column(String, nullable=False)
    orders = relationship("Orders", back_populates="customer")
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))


class Categories(Base):
    __tablename__  = "categories"
    category_id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String, nullable=False)
    category_type = Column(String, nullable=False)
    owner_id = Column(Integer , ForeignKey("users.user_id" , ondelete= "CASCADE") , nullable=False, default=0)
    owner = relationship("User")

class Products(Base):
    __tablename__ = "products"

    product_id =Column(Integer, primary_key=True, nullable=False)
    category_id =  Column(Integer, ForeignKey("categories.category_id" , ondelete= "CASCADE") , nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Float,  nullable=False)
    sale_price = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    owner_id = Column(Integer , ForeignKey("users.user_id" , ondelete= "CASCADE") , nullable=False)
    owner = relationship("User")
    orderItems = relationship("OrderITems")
    images = relationship('ProductsImage', back_populates='products')

class ProductsImage(Base):
    __tablename__="productsimage"
    image_id = Column(Integer, primary_key=True, nullable=False)
    image_name = Column(String, nullable=False)
    image_ext = Column(String, nullable=False)
    image_size = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    Product_id = Column(Integer , ForeignKey("products.product_id" , ondelete= "CASCADE") , nullable=False)
    products = relationship("Products", back_populates='images')
    


class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, nullable=False)
    customer_id =  Column(Integer, ForeignKey("customer.cust_id" , ondelete= "CASCADE") , nullable=False)
    status = Column(String, default="Not Paid")
    cost = Column(Float, nullable=False)
    customer = relationship("Customer")
    date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    payments = relationship("Payments", back_populates="orders", uselist=False)

    # orders_items = relationship("OrderItems")


class OrderITems(Base):
    __tablename__ = "orderitems"
    order_item_id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    product_id =  Column(Integer, ForeignKey("products.product_id" , ondelete= "CASCADE") , nullable=False)
    order_quantity = Column(Integer,  default=0)
    products = relationship("Products")
    order = relationship("Orders", uselist=False)


class Payments(Base):
    
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id" , ondelete= "CASCADE") , nullable=False, unique=True)
    orders = relationship("Orders", back_populates="payments", uselist=False)
    # orders = relationship("Orders", backref="payments")
    transaction_id = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))


class Deliveries(Base):
    
    __tablename__ = "deliveries"

    delivery_id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, nullable=False)
    date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))


# payment -> category relation many to one

class userType(Base):
    __tablename__ = "usertype"
    usertype_id = Column(Integer, primary_key=True, nullable=False)
    usertype = Column(String, nullable=False)
    user = relationship('User', back_populates='usertype')
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    usertype_id = Column(Integer, ForeignKey("usertype.usertype_id" , ondelete= "CASCADE") , nullable=False, unique=True)
    usertype = relationship('userType', back_populates='user')