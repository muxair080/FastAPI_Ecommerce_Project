from fastapi import FastAPI
from database import engine
app = FastAPI()
from database import engine
import models
import Routes.products, Routes.users, Routes.Auth, Routes.orderproduct, Routes.payment
from fastapi.middleware.cors import CORSMiddleware

# this is the ecommerce website


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
models.Base.metadata.create_all(bind= engine)
@app.get('/')
def index():
    return {"Ecom : " : "Welcome to Ecommerce website"}



# @app.get('/allcustomers', response_model= List[scheema.CustomerOut], status_code= status.HTTP_200_OK, tags= ["Main"])
# def allCustomer(db : Session = Depends(get_db)):

#     customer_query = db.query(models.Customer).all()

#     if not customer_query:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Item dose not exist with {id} this id ")
    
#     return customer_query

app.include_router(Routes.products.router)
app.include_router(Routes.users.router)
app.include_router(Routes.Auth.router)
app.include_router(Routes.orderproduct.router)
app.include_router(Routes.payment.router)


