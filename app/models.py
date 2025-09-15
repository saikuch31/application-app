# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import enum
import datetime

Base = declarative_base()

class ApplicationStatus(str, enum.Enum):
    applied = "Applied"
    interviewing = "Interviewing"
    offer = "Offer"
    rejected = "Rejected"

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    applications = relationship("JobApplication", back_populates="company")

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    applications = relationship("JobApplication", back_populates="source")

class JobApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    referral = Column(Boolean, default=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied)
    date_applied = Column(Date, default=datetime.date.today)

    company_id = Column(Integer, ForeignKey("companies.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))

    company = relationship("Company", back_populates="applications")
    source = relationship("Source", back_populates="applications")