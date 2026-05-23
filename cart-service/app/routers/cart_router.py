from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.application.use_cases import (
    AddToCart,
    CartItemNotFoundError,
    CartLimitExceededError,
    ClearCart,
    GetCart,
    InvalidQuantityError,
    RemoveCartItem,
    StockNotAvailableError,
    UpdateCartItem,
)
from app.infrastructure.clients.inventory_client import InventoryClient
from app.infrastructure.clients.pricing_client import PricingClient
from app.infrastructure.database import get_db
from app.infrastructure.repositories import (
    SQLAlchemyCartItemRepository,
    SQLAlchemyCartRepository,
)

router = APIRouter(prefix="/cart", tags=["Cart"])


class AddCartItemRequest(BaseModel):
    customer_id: str = Field(..., examples=["customer-1"])
    book_id: str = Field(..., examples=["book-1"])
    quantity: int = Field(..., gt=0, examples=[1])


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., gt=0, examples=[2])


class CartItemResponse(BaseModel):
    id: int
    book_id: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class CartResponse(BaseModel):
    id: int
    customer_id: str
    status: str
    items: List[CartItemResponse]
    total: Decimal


def build_cart_response(cart) -> CartResponse:
    return CartResponse(
        id=cart.id,
        customer_id=cart.customer_id,
        status=cart.status,
        items=[
            CartItemResponse(
                id=item.id,
                book_id=item.book_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
            )
            for item in cart.items
        ],
        total=cart.total.amount,
    )


def _repositories(db: Session):
    return SQLAlchemyCartRepository(db), SQLAlchemyCartItemRepository(db)


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    request: AddCartItemRequest,
    db: Session = Depends(get_db),
):
    cart_repository, cart_item_repository = _repositories(db)

    use_case = AddToCart(
        cart_repository=cart_repository,
        cart_item_repository=cart_item_repository,
        inventory_client=InventoryClient(),
        pricing_client=PricingClient(),
    )

    try:
        cart = use_case.execute(
            customer_id=request.customer_id,
            book_id=request.book_id,
            quantity=request.quantity,
        )
        return build_cart_response(cart)

    except StockNotAvailableError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except CartLimitExceededError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except InvalidQuantityError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{customer_id}", response_model=CartResponse)
def get_cart(
    customer_id: str,
    db: Session = Depends(get_db),
):
    cart_repository = SQLAlchemyCartRepository(db)
    cart = GetCart(cart_repository).execute(customer_id)
    return build_cart_response(cart)


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
):
    cart_repository, cart_item_repository = _repositories(db)

    use_case = UpdateCartItem(
        cart_repository=cart_repository,
        cart_item_repository=cart_item_repository,
        inventory_client=InventoryClient(),
    )

    try:
        cart = use_case.execute(item_id=item_id, quantity=request.quantity)
        return build_cart_response(cart)

    except CartItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except StockNotAvailableError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except InvalidQuantityError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/items/{item_id}", response_model=CartResponse)
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    cart_repository, cart_item_repository = _repositories(db)

    try:
        cart = RemoveCartItem(
            cart_repository=cart_repository,
            cart_item_repository=cart_item_repository,
        ).execute(item_id)

        return build_cart_response(cart)

    except CartItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{customer_id}", response_model=CartResponse)
def clear_cart(
    customer_id: str,
    db: Session = Depends(get_db),
):
    cart_repository = SQLAlchemyCartRepository(db)
    cart = ClearCart(cart_repository).execute(customer_id)
    return build_cart_response(cart)
