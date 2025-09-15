# app/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# Applications
# -------------------------------
@router.get("/applications", response_model=list[schemas.Application])
def list_applications(db: Session = Depends(get_db)):
    return db.query(models.JobApplication).all()

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload
from fastapi import HTTPException

@router.put("/applications/{app_id}", response_model=schemas.Application)
def update_application(app_id: int, updated_app: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    db_app = db.query(models.JobApplication).filter(models.JobApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")

    # Only update fields that are provided in request
    for field, value in updated_app.dict(exclude_unset=True).items():
        setattr(db_app, field, value)

    db.commit()
    db.refresh(db_app)

    # Reload with company + source for response
    db_app = (
        db.query(models.JobApplication)
        .options(joinedload(models.JobApplication.company),
                 joinedload(models.JobApplication.source))
        .filter(models.JobApplication.id == app_id)
        .first()
    )

    return db_app
# -------------------------------
# Companies
# -------------------------------
@router.get("/companies", response_model=list[schemas.Company])
def list_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()

@router.post("/companies", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    new_company = models.Company(**company.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

# -------------------------------
# Sources
# -------------------------------
@router.get("/sources", response_model=list[schemas.Source])
def list_sources(db: Session = Depends(get_db)):
    return db.query(models.Source).all()

@router.post("/sources", response_model=schemas.Source)
def create_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    new_source = models.Source(**source.dict())
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    return new_source

from fastapi import HTTPException

# -------------------------------
# Update Application
# -------------------------------
@router.put("/applications/{app_id}", response_model=schemas.Application)
def update_application(app_id: int, updated_app: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    db_app = db.query(models.JobApplication).filter(models.JobApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")

    # Update only provided fields
    for field, value in updated_app.dict(exclude_unset=True).items():
        setattr(db_app, field, value)

    db.commit()
    db.refresh(db_app)
    return db_app

# -------------------------------
# Delete Application
# -------------------------------
@router.delete("/applications/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    db_app = db.query(models.JobApplication).filter(models.JobApplication.id == app_id).first()
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(db_app)
    db.commit()
    return {"message": f"Application {app_id} deleted successfully"}