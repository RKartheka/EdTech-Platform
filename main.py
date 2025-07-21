
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth, database
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    return crud.create_user(db, user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_access_token({"id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/assignments", response_model=schemas.AssignmentOut)
def create_assignment(assignment: schemas.AssignmentCreate, user=Depends(auth.RoleChecker("teacher")), db: Session = Depends(auth.get_db)):
    return crud.create_assignment(db, assignment, user.id)

@app.post("/assignments/{assignment_id}/submit")
def submit_assignment(assignment_id: int, submission: schemas.SubmissionCreate, user=Depends(auth.RoleChecker("student")), db: Session = Depends(auth.get_db)):
    return crud.submit_assignment(db, assignment_id, user.id, submission)

@app.get("/assignments/{assignment_id}/submissions", response_model=list[schemas.SubmissionOut])
def view_submissions(assignment_id: int, user=Depends(auth.RoleChecker("teacher")), db: Session = Depends(auth.get_db)):
    return crud.get_submissions(db, assignment_id)
