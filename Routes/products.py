from typing import List, Optional
from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter,UploadFile,File

import models, scheema, oauth
from database import get_db
from sqlalchemy.orm import Session
import os, shutil,hashlib
router = APIRouter()



@router.get('/allcategories', response_model= List[scheema.CategoryOut], tags= ["category"])
def getCategories(db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    
    query = db.query(models.Categories).all()

    if not query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Category table is empty")
    
    return query

@router.post('/newcategory', tags= ["category"])
def addNewCategory(category : scheema.Category , db : Session = Depends(get_db)):
    new_category = models.Categories(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.put('/updatecategory/{id}', tags= ["category"])
def updateCategory(id : int, category : scheema.Category, db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    update_query = db.query(models.Categories).filter(models.Categories.category_id == id)
    result = update_query.first()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with {id} this id not found")
    
    if result.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action.")
    
    update_query.update(category.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()


@router.delete('/deletecategory/{id}', tags= ["category"])
def deleteCategory(id : int, db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    query = db.query(models.Categories).filter(models.Categories.category_id == id)
    delete_category = query.first()
    if delete_category  == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Category with Id {id} dose not exist")
    if delete_category.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
    
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




# ********************************Products Images***********************************************

@router.post('/addimages',response_model=scheema.productImage, status_code=status.HTTP_201_CREATED,tags=['porductImages'])
async def addImage(id : int, image : UploadFile = File(...), db  : Session = Depends(get_db)):
    imgs_ext = ['.jpg', '.jpeg', '.jpe' '.jif', '.jfif', '.jfi','.png','.gif','.webp','.tiff','.tif','.psd','.bmp','.dib','.heif','.heic','.ind','.indd','.indt', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2','.svg','.svgz','.ai']
    image_data = os.path.splitext(image.filename)
    contents = await image.read()
    # hashed_content = hashlib.sha256(contents).hexdigest()
    if(image_data[1] in imgs_ext):
        with open(f"Media\ {image.filename}",'wb') as imagefile:
            shutil.copyfileobj(image.file, imagefile)
            size = str(round(len(contents)/1024))+'kbs'
            data = {"image_name" : image_data[0], "image_ext" : image_data[1],"image_size" : size , "Product_id" : id}
            add_query = models.ProductsImage(**data)
            db.add(add_query)
            db.commit()
            db.refresh(add_query)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The given file is not image")

    return add_query

@router.delete('/deleteimage/{id}',tags=["porductImages"])
def delete_images(id : int, db : Session = Depends(get_db)):
    query = db.query(models.ProductsImage).filter(models.ProductsImage.image_id == id)
    delete_image = query.first()

    if not delete_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Image dose not exist with this {id} id")
    
    print("image name : ",delete_image.image_name)
    os.remove( f"Media\ {delete_image.image_name}{delete_image.image_ext}")
    query.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.put('/updateimage{id}',tags=["porductImages"])
async def update_images(id : int, image : UploadFile = File(...), db : Session = Depends(get_db)):
    imgs_ext = ['.jpg', '.jpeg', '.jpe' '.jif', '.jfif', '.jfi','.png','.gif','.webp','.tiff','.tif','.psd','.bmp','.dib','.heif','.heic','.ind','.indd','.indt', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2','.svg','.svgz','.ai']
    
    query = db.query(models.ProductsImage).filter(models.ProductsImage.image_id == id)
    update_query = query.first()

    print("productL iid", update_query.Product_id)
    image_data = os.path.splitext(image.filename)
    contents = await image.read()
    if(image_data[1] in imgs_ext):
        os.remove( f"Media\ {update_query.image_name}{update_query.image_ext}")
        with open(f"Media\ {image.filename}",'wb') as imagefile:
            shutil.copyfileobj(image.file, imagefile)
            size = str(round(len(contents)/1024))+'kbs'
            data = {"image_name" : image_data[0], "image_ext" : image_data[1],"image_size" : size , "Product_id" : update_query.Product_id}


            if update_query is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with {id} this id not found")
            
            # if result.owner_id != current_user.user_id:
            #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action.")

            query.update(data, synchronize_session=False)
            db.commit()
            db.refresh(update_query)
            
            return update_query
    
# # ************************************ products crud*****************************************

@router.post('/newproduct', response_model= scheema.productOut, status_code = status.HTTP_201_CREATED, tags= ["products"])
def addNewProduct(product : scheema.ProductIn, db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    
    owner_id = current_user.user_id
    product = product.dict()
    product['owner_id'] = owner_id
    # print('product : ',type(product))
    
    new_product = models.Products(**product)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get('/allproducts', status_code=status.HTTP_200_OK, response_model=List[scheema.productOut], tags= ["products"])
def getProducts(db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):

    # query = db.query(models.Products).all()
    query = db.query(models.Products).all()

    if not query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Products table is empty. ")

    return query

@router.get('/productsfetch')
def fetchProducts(db : Session = Depends(get_db)):
    query = db.query(models.Products).all()

    if not query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Products table is empty. ")

    return query

@router.get('/singleproduct/{id}', response_model= scheema.productOut, tags= ["products"])
def singleProduct(id : int, db : Session = Depends(get_db)):
    
    query = db.query(models.Products).filter(models.Products.product_id == id).first()
    
    if not query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"Item dose not exist with {id} this id ")
    
    return query
    
@router.put('/updateproducts/{id}', response_model= scheema.productOut, status_code=status.HTTP_200_OK, tags=["products"])
def updateProduct(id : int, product : scheema.ProductIn, db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):

    update_query = db.query(models.Products).filter(models.Products.product_id == id)
    result = update_query.first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with {id} this id not found")
    
    if result.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform this action.")

    update_query.update(product.dict(), synchronize_session=False)
    db.commit()
    db.refresh(result)
    return result



@router.delete('/deleteproduct/{id}', tags= ["products"])
def deleteProduct(id : int, db : Session = Depends(get_db), current_user : int = Depends(oauth.get_current_user)):
    delete_query = db.query(models.Products).filter(models.Products.product_id == id)
    result = delete_query.first()
    """delete the product with the specific id from the database """
    if result  == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Product with Id {id} dose not exist")
    if result.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
        


