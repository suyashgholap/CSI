from fastapi import APIRouter
from models.request import ProductRequest, ProductUpdateRequest
from models.responce import Response
from models.models import Product
from db.database import Database
from sqlalchemy import and_, desc

# APIRouter creates path operations for product module
router = APIRouter(
    prefix="/products",
    tags=["Product"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.post("/add", response_description="Product data added into the database")
async def add_product(product_req: ProductRequest):
    new_product = Product()
    new_product.name = product_req.name
    new_product.price = product_req.price
    new_product.seller_email = product_req.seller_email
    new_product.is_available = product_req.is_available
    new_product.created_by = product_req.created_by
    new_product_id = None
    session = database.get_db_session(engine)
    session.add(new_product)
    session.flush()
    # get id of the inserted product
    session.refresh(new_product, attribute_names=['id'])
    data = {"product_id": new_product.id}
    session.commit()
    session.close()
    return Response(data, 200, "Product added successfully.", False)


@router.put("/update")
async def update_product(product_update_req: ProductUpdateRequest):
    product_id = product_update_req.product_id
    session = database.get_db_session(engine)
    try:
        is_product_updated = session.query(Product).filter(Product.id == product_id).update({
            Product.name: product_update_req.name, Product.price: product_update_req.price,
            Product.seller_email: product_update_req.seller_email,
            Product.is_available: product_update_req.is_available,
            Product.updated_by: product_update_req.updated_by
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Product updated successfully"
        response_code = 200
        error = False
        if is_product_updated == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Product).filter(
                Product.id == product_id).one()

        elif is_product_updated == 0:
            response_msg = "Product not updated. No product found with this id :" + \
                str(product_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.delete("/{product_id}/delete")
async def delete_product(product_id: str):
    session = database.get_db_session(engine)
    try:
        is_product_updated = session.query(Product).filter(and_(Product.id == product_id, Product.deleted == False)).update({
            Product.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Product deleted successfully"
        response_code = 200
        error = False
        data = {"product_id": product_id}
        if is_product_updated == 0:
            response_msg = "Product not deleted. No product found with this id :" + \
                str(product_id)
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.get("/{product_id}")
async def read_product(product_id: str):
    session = database.get_db_session(engine)
    response_message = "Product retrieved successfully"
    data = None
    try:
        data = session.query(Product).filter(
            and_(Product.id == product_id, Product.deleted == False)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Product Not found"
    error = False
    return Response(data, 200, response_message, error)


@router.get("/")
async def read_all_products(created_by: str, page_size: int, page: int):
    session = database.get_db_session(engine)
    data = session.query(Product).filter(and_(Product.created_by == created_by, Product.deleted == False)).order_by(
        desc(Product.created_at)).limit(page_size).offset((page-1)*page_size).all()
    return Response(data, 200, "Products retrieved successfully.", False)