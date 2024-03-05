from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create_students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@app.post("/create_labor_categories/", response_model=schemas.LaborCategory)
def create_labor_category(labor_category: schemas.LaborCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_labor_category(db=db, labor_category=labor_category)

@app.post("/register_labor/", response_model=schemas.LaborRecord)
def create_labor_record(labor_record: schemas.LaborRecordCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_labor_record(db=db, labor_record=labor_record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students/{student_name}/cleaning-count/", response_model=int)
def get_student_cleaning_count(student_name: str, db: Session = Depends(get_db)):
    return crud.get_cleaning_count_by_student_name(db, student_name)

@app.get("/get_labor_categories/", response_model=List[schemas.LaborCategory])
def list_labor_categories(db: Session = Depends(get_db)):
    categories = crud.get_all_labor_categories(db)
    return categories

@app.get("/get_students_list/", response_model=List[schemas.Student])
def list_students(db: Session = Depends(get_db)):
    students = crud.get_all_students(db)
    return students
