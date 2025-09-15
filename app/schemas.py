# app/schemas.py
from pydantic import BaseModel
import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = "Applied"
    interviewing = "Interviewing"
    offer = "Offer"
    rejected = "Rejected"

# -------------------------------
# Company Schemas
# -------------------------------
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True

# -------------------------------
# Source Schemas
# -------------------------------
class SourceBase(BaseModel):
    name: str

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int

    class Config:
        orm_mode = True

# -------------------------------
# Application Schemas
# -------------------------------
class ApplicationBase(BaseModel):
    role: str
    referral: bool = False
    status: ApplicationStatus = ApplicationStatus.applied
    date_applied: datetime.date = datetime.date.today()

class ApplicationCreate(ApplicationBase):
    company_id: int
    source_id: int

class Application(ApplicationBase):
    id: int
    company: Company   # nested object instead of just ID
    source: Source     # nested object instead of just ID

    class Config:
        orm_mode = True