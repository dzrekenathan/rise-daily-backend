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
@router.get("/quotes", status_code=status.HTTP_200_OK)
async def get_quotes(
    db: Session =Depends(get_db),
    cursor: str = None,
    limit: int = Query(default=10, ge=1)
    ):
    quotes = db.query(models.Quote).all()
    return quotes

# Create a new quote
@router.post("/quotes", response_model=Quote, status_code=status.HTTP_201_CREATED)
async def create_quote(quote: QuoteBase, db: Session = Depends(get_db)):
    new_quote = models.Quote(**quote.dict())
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote

# Get a quote by ID
@router.get("/quotes/{quote_id}", response_model=Quote, status_code=status.HTTP_200_OK)
async def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    return quote


# Update a quote by ID
@router.put("/quotes/{quote_id}", response_model=Quote, status_code=status.HTTP_200_OK)
async def update_quote(quote_id: int, quote: QuoteBase, db: Session = Depends(get_db)):
    quote_query = db.query(models.Quote).filter(models.Quote.id == quote_id)
    if not quote_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    quote_query.update(quote.dict(), synchronize_session=False)
    db.commit()
    return quote_query.first()


# Delete a quote by ID
@router.delete("/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    quote_query = db.query(models.Quote).filter(models.Quote.id == quote_id)
    if not quote_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    quote_query.delete(synchronize_session=False)
    db.commit()
    return None

