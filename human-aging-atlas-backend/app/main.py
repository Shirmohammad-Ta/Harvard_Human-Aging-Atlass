from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import genes, search, stats
from .config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="REST API for Human Aging Atlas - Multi-omics aging evidence database"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثبت روت‌ها
app.include_router(genes.router)
app.include_router(search.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "genes": "/genes",
            "search": "/search?q=TP53",
            "stats": "/stats"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}