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

class Application(BaseModel):
    id: int
    role: str
    referral: bool
    status: ApplicationStatus
    date_applied: datetime.date
    company_id: int
    source_id: int
    company: Company | None = None
    source: Source | None = None

    class Config:
        orm_mode = True

class ApplicationUpdate(BaseModel):
    role: str | None = None
    referral: bool | None = None
    status: ApplicationStatus | None = None
    date_applied: datetime.date | None = None
    company_id: int | None = None
    source_id: int | None = None

    class Config:
        orm_mode = True