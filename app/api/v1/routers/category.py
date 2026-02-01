from fastapi import APIRouter, Depends, HTTPException, status
from app.model import models
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schema.category import CategoryCreate


router = APIRouter()

# Region: Category Endpoints
# Return list of categories

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

# endregion



# Create a new category
@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get a specific category by ID

@router.get("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

# Update a specific category by ID

@router.put("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(category_id: int, updated_category: CategoryCreate, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == category_id)
    if not category_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()
    return category_query.first()

# Delete a specific category by ID

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == category_id)
    if not category_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_query.delete(synchronize_session=False)
    db.commit()
    return None

# End of Category Endpoints