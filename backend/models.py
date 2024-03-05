from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    student_id = Column(String, index=True)

    labor_records = relationship("LaborRecord", back_populates="student")

class LaborCategory(Base):
    __tablename__ = "labor_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)

class LaborRecord(Base):
    __tablename__ = "labor_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    labor_category_id = Column(Integer, ForeignKey("labor_categories.id"))
    date = Column(String, index=True)
    time = Column(String, index=True)

    student = relationship("Student", back_populates="labor_records")
    labor_category = relationship("LaborCategory")

