import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Response, status, Request
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

from database.session import session_dep
from utils.db.sale import create_sale, add_report
from utils.db.product import save_products
from utils.xml_utils import parse_xml, fetch_xml_data
from utils.report import generate_report


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback

    return Response(
        content="".join(
            traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
        )
    )


router = APIRouter(prefix="/api")


@router.get("/process-data", status_code=status.HTTP_200_OK)
async def fetch_data_from_xml(session: session_dep):
    from celery_tasks.tasks import fetch_and_process_sales_data

    task = fetch_and_process_sales_data.apply_async(session)
    return JSONResponse({"task_id": task.id})


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
