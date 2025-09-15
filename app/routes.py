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

@router.post("/applications", response_model=schemas.Application)
def create_application(app: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    new_app = models.JobApplication(**app.dict())
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

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