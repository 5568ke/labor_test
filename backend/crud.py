from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name,student_id=student.student_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_labor_category_id_by_name(db: Session, labor_category_name: str):
    return db.query(models.LaborCategory).filter(models.LaborCategory.name == labor_category_name).first()

def get_student_id_by_name(db: Session, student_name: str):
    return db.query(models.Student).filter(models.Student.name == student_name).first()

def create_labor_record(db: Session, labor_record: schemas.LaborRecordCreate):
    student = get_student_id_by_name(db, labor_record.student_name)
    if not student:
        raise Exception("Student not found")
    
    labor_category = get_labor_category_id_by_name(db, labor_record.labor_category_name)
    if not labor_category:
        raise Exception("Labor category not found")
    
    current_time = datetime.now()
    db_record = models.LaborRecord(
        student_id=student.id,
        labor_category_id=labor_category.id,
        date=current_time.strftime("%Y-%m-%d"),
        time=current_time.strftime("%H:%M:%S")
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def create_labor_category(db: Session, labor_category: schemas.LaborCategoryCreate):
    db_category = models.LaborCategory(name=labor_category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_cleaning_count_by_student_name(db: Session, student_name: str) -> int:
    return db.query(models.LaborRecord).join(models.Student).filter(models.Student.name == student_name).count()

def get_all_labor_categories(db: Session):
    return db.query(models.LaborCategory).all()

def get_all_students(db: Session):
    return db.query(models.Student).all()
