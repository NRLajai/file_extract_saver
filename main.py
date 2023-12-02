from fastapi import FastAPI, Request, File, UploadFile
from fastapi import Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Path
import magic
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import csv
import sqlite3
import os
import shutil

from models import Users, UsersResponse, DataBasesetup



class App:
    def __init__(self) -> None:        
        app = FastAPI()
        app.mount("/static", StaticFiles(directory="static"), name="static")        
        
        self.app = app
        self.templates = Jinja2Templates(directory="templates")      



class Handler:
    def __init__(self) -> None:
        app = FastAPI()
        app.mount("/static", StaticFiles(directory="static"), name="static")        
        self.templates = Jinja2Templates(directory="templates")    

        db_setup = DataBasesetup()
        self.app = app
        self.db = db_setup.db

        UPLOAD_FOLDER = "./uploaded_files"

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        self.upload_folder = UPLOAD_FOLDER

    
    def get_db(self):
        if self.db is None:
            db = self.db_setup.db
            return db
        else:
            return self.db


    def get_mime_type(self, file):
        mime = magic.Magic()
        return mime.from_buffer(file.file.read())


    def get_file_contents(self, file):
        for row in file:
            yield {key.strip(): value.strip() for key, value in row.items()}
    

    async def homepage(self, request: Request):
        content = {
            "request": request,
            "title": "File Upload",
            "choice": "Choose a File:"
            }
        return self.templates.TemplateResponse("upload_page.html", content)
    

    async def create_upload_file(self, uploaded_file: UploadFile = File(...)):
        try:
            mime_type = self.get_mime_type(uploaded_file)

            if not mime_type.startswith("CSV text"):
                    return {"error": "Upload appropriate file type, Example as [.csv]"}
            
            uploaded_file.file.seek(0)
            file_path = os.path.join(self.upload_folder, uploaded_file.filename)

            with open(file_path, "wb") as file:
                shutil.copyfileobj(uploaded_file.file, file)

            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                for row in self.get_file_contents(csv_reader):                
                    user = Users(name=str(row["name"]), age=int(row["age"]))
                    db = self.get_db()
                    db.add(user)
                    db.commit()
                    db.refresh(user)
                db.close()

            return {"success": "Uploaded successfully."}
        except Exception as e:
            return {"error": "An error occurred while processing uploaded file."}


    async def read_user(self, user_id: int = Path(...)):
        try:
            db = self.get_db()
            user = db.query(Users).filter(Users.id == user_id).first()
            
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_response = UsersResponse(id=user.id, name=user.name, age=user.age)
            
            return user_response
        except Exception as e:
            return {"error": "Somwthing went wrong, Could not fetch data."}




handler = Handler()

router = APIRouter()
router.add_api_route("/", handler.homepage, methods=["GET"])
router.add_api_route("/users/{user_id}", handler.read_user, methods=["GET"])
router.add_api_route("/uploadfile", handler.create_upload_file, methods=["POST"])
handler.app.include_router(router)



# uvicorn main:handler.app --reload

# @app.get("/", response_class=HTMLResponse)
# async def homepage(request: Request):
#     return templates.TemplateResponse("upload_page.html", {"request": request})


# @app.post("/uploadfile/")
# async def create_upload_file(uploaded_file: UploadFile = File(...)):
#     try:
#         mime_type = get_mime_type(uploaded_file)

#         if not mime_type.startswith("CSV text"):
#                 return {"error": "Upload appropriate file type, Example as [.csv]"}
        
#         uploaded_file.file.seek(0)
#         file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)

#         with open(file_path, "wb") as file:
#             shutil.copyfileobj(uploaded_file.file, file)

#         with open(file_path, mode='r', newline='', encoding='utf-8') as file:
#             csv_reader = csv.DictReader(file)

#             for row in get_file_contents(csv_reader):                
#                 user = Users(name=str(row["name"]), age=int(row["age"]))
#                 db = SessionLocal()
#                 db.add(user)
#                 db.commit()
#                 db.refresh(user)
#             db.close()

#         return {"success": "Uploaded successfully."}
#     except Exception as e:
#         return {"error": f"An error occurred while processing uploaded file.{e}"}

    

# @app.get("/users/{user_id}")
# def read_user(user_id: int = Path(...), db: Session = Depends(get_db)):
#     try:
#         user = db.query(Users).filter(Users.id == user_id).first()
        
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
        
#         user_response = UsersResponse(id=user.id, name=user.name, age=user.age)
        
#         return user_response
#     except:
#         return {"error": "Somwthing went wrong, Could not fetch data"}
