#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import HTTPException

app = FastAPI()

# Models

class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str
    state: str
    country: str

class BasePerson(BaseModel): 
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Miguel"
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)
    
class Person(BasePerson):
    password: str = Field(..., min_length=3)
    
class PersonOut(BasePerson):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="donkami04")

fake_id_users = [1, 2, 3]

@app.get("/", status_code=status.HTTP_200_OK, tags=['Persons'])
def home(): 
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new", response_model=PersonOut, tags=['Persons'])
def create_person(person: Person = Body(...)): 
    return person

# Validaciones: Query Parameters

@app.get("/person/detail", tags=['Persons'])
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocío"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
): 
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}", tags=['Persons'])
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
): 

    
    if person_id not in fake_id_users:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "This Person does not exist!!"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}", tags=['Persons'])
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
): 
    results = person.dict()
    results.update(location.dict())
    return results

# Login
@app.post('/login', response_model=LoginOut, tags=['Authentication'])
def login(username: str = Form(...)):
    return LoginOut(username=username)

# Contact
@app.post('/contact', status_code=status.HTTP_200_OK, tags=['Information of contact'])
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
): 
    return user_agent

# Files
@app.post('/post-images', status_code=status.HTTP_200_OK, tags=['Utils'])
def post_images(
    image: UploadFile = File(...)
):
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read())/1024, ndigits=2)
    }