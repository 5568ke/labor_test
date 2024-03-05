from pydantic import BaseModel
from typing import List, Optional


class LaborRecordBase(BaseModel):
      pass

class LaborRecordCreate(LaborRecordBase):
    student_name: str  
    labor_category_name: str

class LaborRecord(LaborRecordBase):
    id: int
    student_id: int  
    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    labor_records: List[LaborRecord] = []
    class Config:
        orm_mode = True

class LaborCategoryBase(BaseModel):
    name: str

class LaborCategoryCreate(LaborCategoryBase):
    pass

class LaborCategory(LaborCategoryBase):
    id: int
    class Config:
        orm_mode = True

