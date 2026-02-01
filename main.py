from fastapi import FastAPI
from app.api.v1.routers import quote, health, category
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.model import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(quote.router, prefix="/api/v1", tags=["Quotes"])
app.include_router(category.router, prefix="/api/v1", tags=["Categories"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)



