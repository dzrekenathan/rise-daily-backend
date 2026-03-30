from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schema.quote import Quote
from app.schema.category import Category
from sqlalchemy.orm import Session
from app.model import models
from app.schema.quote import QuoteBase, Quote
from app.schema.page import Page
import uuid
from app.core.database import get_db



router = APIRouter()

# Get all quotes
@router.get("/quotes", status_code=status.HTTP_200_OK, operation_id="get_quotes")
async def get_quotes(
    db: Session =Depends(get_db),
    cursor: str = None,
    limit: int = Query(default=10, ge=1)
    ):
    """Retrieve all quotes. Supports optional cursor-based pagination and a limit (default 10, min 1)."""
    quotes = db.query(models.Quote).all()
    return quotes

# Create a new quote
@router.post("/quotes", status_code=status.HTTP_201_CREATED, operation_id="create_quote")
async def create_quote(quote: QuoteBase, db: Session = Depends(get_db)):
    """Create and persist a new quote. Accepts quote fields in the request body and returns the created quote."""
    new_quote = models.Quote(**quote.dict())
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote

# Get a quote by ID
@router.get("/quotes/{quote_id}", response_model=Quote, status_code=status.HTTP_200_OK, operation_id="get_quote")
async def get_quote(quote_id: int, db: Session = Depends(get_db)):
    """Retrieve a single quote by its ID. Returns 404 if the quote does not exist."""
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    return quote


# Update a quote by ID
@router.put("/quotes/{quote_id}", response_model=Quote, status_code=status.HTTP_200_OK, operation_id="update_quote")
async def update_quote(quote_id: int, quote: QuoteBase, db: Session = Depends(get_db)):
    """Update an existing quote by its ID. Replaces all fields with the provided data. Returns 404 if not found."""
    quote_query = db.query(models.Quote).filter(models.Quote.id == quote_id)
    if not quote_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    quote_query.update(quote.dict(), synchronize_session=False)
    db.commit()
    return quote_query.first()


# Delete a quote by ID
@router.delete("/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete_quote")
async def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    """Delete a quote by its ID. Returns 204 on success and 404 if the quote does not exist."""
    quote_query = db.query(models.Quote).filter(models.Quote.id == quote_id)
    if not quote_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    quote_query.delete(synchronize_session=False)
    db.commit()
    return None








# @router.get("/quotes", status_code=status.HTTP_200_OK, operation_id="get_quotes")
# async def get_quotes(
#     db: Session =Depends(get_db),
#     cursor: str = None,
#     limit: int = Query(default=10, ge=1)
#     ):
#     quotes = db.query(models.Quote).all()
#     return quotes

# # Create a new quote
# @router.post("/quotes", status_code=status.HTTP_201_CREATED, operation_id="create_quote")
# async def create_quote(quote: QuoteBase, db: Session = Depends(get_db)):
#     new_quote = models.Quote(**quote.dict())
#     db.add(new_quote)
#     db.commit()
#     db.refresh(new_quote)
#     return new_quote

# # Get a quote by ID
# @router.get("/quotes/{quote_id}", response_model=Quote, status_code=status.HTTP_200_OK, operation_id="get_quote")
# async def get_quote(quote_id: int, db: Session = Depends(get_db)):
#     quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
#     if not quote:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
#     return quote


# # Update a quote by ID
# @router.put("/quotes/{quote_id}", response_model=Quote, status_code=status.HTTP_200_OK, operation_id="update_quote")
# async def update_quote(quote_id: int, quote: QuoteBase, db: Session = Depends(get_db)):
#     quote_query = db.query(models.Quote).filter(models.Quote.id == quote_id)
#     if not quote_query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
#     quote_query.update(quote.dict(), synchronize_session=False)
#     db.commit()
#     return quote_query.first()


# # Delete a quote by ID
# @router.delete("/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete_quote")
# async def delete_quote(quote_id: int, db: Session = Depends(get_db)):
#     quote_query = db.query(models.Quote).filter(models.Quote.id == quote_id)
#     if not quote_query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
#     quote_query.delete(synchronize_session=False)
#     db.commit()
#     return None

