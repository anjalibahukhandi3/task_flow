from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth, tasks

app = FastAPI(
    title="Task Manager API (Python)",
    description="Scalable REST API built with FastAPI, SQLAlchemy, and JWT Authentication",
    version="1.0.0",
    docs_url="/docs", # Built-in Swagger UI
)

@app.on_event("startup")
def startup_event():
    # Create database tables
    models.Base.metadata.create_all(bind=engine)

# Configure CORS so React app can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API is running!"}
