from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine
import pandas as pd
import os

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

@app.post("/add_students_by_file/")
def create_students(file: UploadFile = File(...),db: Session = Depends(get_db)):
    try:
        db.query(models.Student).delete()
        db.commit()

        file_location = f"{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        process_student_file(file_location, db)
        return {"message": "Students have been successfully added."}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=400, content={"message": str(e)})

@app.post("/add_labor_categories_by_file/")
def create_labor_categories(file: UploadFile = File(...),db: Session = Depends(get_db)):
    try:
        db.query(models.LaborCategory).delete()
        db.commit()

        file_location = f"{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        process_labor_category_file(file_location, db)
        return {"message": "Labor categories have been successfully added."}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=400, content={"message": str(e)})

def process_student_file(file_path: str, db: Session):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        student = schemas.StudentCreate(name=row['Name'], student_number=row['Student Number'])
        crud.create_student(db=db, student=student)

def process_labor_category_file(file_path: str, db: Session):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        category = schemas.LaborCategoryCreate(name=row['Name'])
        crud.create_labor_category(db=db, labor_category=category)


# def fetch_student_data(db: Session):
#     data = db.query(
#         models.Student.name, 
#         func.count(models.LaborRecord.id).label("cleaning_count")
#     ).join(models.LaborRecord).group_by(models.Student.id).all()
#     return data
#
# @app.get("/students/export/")
# async def export_students():
#     db = SessionLocal()
#     try:
#         students_data = fetch_student_data(db)
#         df = pd.DataFrame(students_data, columns=["Name", "Student Number", "Cleaning Count"])
#         file_path = "students_data.xlsx"
#         df.to_excel(file_path, index=False)
#         
#         return FileResponse(path=file_path, filename="students_data.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     finally:
#         db.close()
#         # os.remove(file_path)
