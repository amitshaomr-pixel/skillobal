from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from routes import all_routes
from fastapi.middleware.cors import CORSMiddleware
from middleware.config import settings
import uvicorn
import traceback
from starlette.exceptions import HTTPException as StarletteHTTPException
from middleware.exceptions import CustomError


app = FastAPI()


# ======================================================================================
# 1. Custom Application Errors
# ======================================================================================
@app.exception_handler(CustomError)
async def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_message": exc.message
        }
    )


# ======================================================================================
# 2. FastAPI HTTPException Errors (404, 401, etc.)
# ======================================================================================
@app.exception_handler(StarletteHTTPException)
async def global_404_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "error_message": "Not found"
            }
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_message": exc.detail
        }
    )


# ======================================================================================
# 3. Pydantic Validation Errors (Request body validation)
# ======================================================================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    cleaned = []
    for err in exc.errors():
        err_copy = err.copy()
        if "ctx" in err_copy and "error" in err_copy["ctx"]:
            err_copy["ctx"]["error"] = str(err_copy["ctx"]["error"])
        cleaned.append(err_copy)

    return JSONResponse(
        status_code=422,
        content={
            "error_message": "Validation error",
            "errors": cleaned
        }
    )



# ======================================================================================
# 4. Handle all other Python errors (500 server errors)
# ======================================================================================
@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):

    # Log the stack trace for debugging (optional)
    print("\n--- INTERNAL SERVER ERROR ---")
    traceback.print_exc()
    print("-----------------------------\n")

    return JSONResponse(
        status_code=500,
        content={
            "error_message": str(exc) # Remove in production
        }
    )





# ---------------------------------------------------------------
# CORS
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)


# Routes
app.include_router(all_routes.router)


# Root
@app.get("/")
async def root():
    return {"message": "API is running"}


# Run
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
