from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import blog

app = FastAPI(
    title="Quality Playbook API",
    description="Backend API for Quality Playbook blog",
    version="1.0.0"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
        "https://qualityplaybook.dev",
        "https://www.qualityplaybook.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include blog router
app.include_router(blog.router)


@app.get("/")
async def root():
    return {
        "message": "Quality Playbook API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
