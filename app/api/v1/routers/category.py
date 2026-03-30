from fastapi import APIRouter, Depends, HTTPException, status
from app.model import models
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schema.category import CategoryCreate


from sqlalchemy import func
from sqlalchemy.orm import Session

def get_categories_with_quote_count(db: Session):
    """Query all categories with an aggregated count of their associated quotes using a left outer join."""
    return (
        db.query(
            models.Category,
            func.count(models.Quote.id).label("number_of_quote")
        )
        .outerjoin(models.Quote, models.Quote.category_id == models.Category.id)
        .group_by(models.Category.id)
        .all()
    )


router = APIRouter()

# Region: Category Endpoints
# Return list of categories

@router.get("/categories", status_code=status.HTTP_200_OK, operation_id="get_categories")
def get_categories(db: Session = Depends(get_db)):
    """Retrieve all categories, each including its metadata and the total number of associated quotes."""
    results = get_categories_with_quote_count(db)

    return [
        {
            "id": category.id,
            "name": category.name,
            "image_url": category.image_url,
            "description": category.description,
            "number_of_quote": number_of_quote,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
        for category, number_of_quote in results
    ]


# endregion



# Create a new category
@router.post("/categories", status_code=status.HTTP_201_CREATED, operation_id="create_category")
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create and persist a new category. Accepts category fields in the request body and returns the created category."""
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get a specific category by ID

@router.get("/categories/{category_id}", status_code=status.HTTP_200_OK, operation_id="get_category")
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieve a single category by its ID. Returns 404 if the category does not exist."""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

# Update a specific category by ID

@router.put("/categories/{category_id}", status_code=status.HTTP_200_OK, operation_id="update_category")
async def update_category(category_id: int, updated_category: CategoryCreate, db: Session = Depends(get_db)):
    """Update an existing category by its ID. Replaces all fields with the provided data. Returns 404 if not found."""
    category_query = db.query(models.Category).filter(models.Category.id == category_id)
    if not category_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()
    return category_query.first()

# Delete a specific category by ID

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="delete_category")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category by its ID. Returns 204 on success.
    Returns 404 if the category does not exist.
    Returns 400 if the category has one or more associated quotes — remove all quotes in the category before deleting it.
    """
    category_query = db.query(models.Category).filter(models.Category.id == category_id)
    if not category_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_query.delete(synchronize_session=False)
    db.commit()
    return None

# End of Category Endpoints