from fastapi import FastAPI
from routes import all_routes
from fastapi.middleware.cors import CORSMiddleware
from middleware.config import settings
import uvicorn
app = FastAPI()


# ✅ CORS setup using config.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(all_routes.router)

@app.get("/")
async def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


