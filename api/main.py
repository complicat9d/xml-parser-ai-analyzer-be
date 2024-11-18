import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Response, status, Request
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
from celery.result import AsyncResult

from api.routes.test import test_router
from celery_tasks.tasks import fetch_and_process_sales_data
from celery_tasks.conf import app as celery_app  # noqa


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
router.include_router(test_router)


@router.get("/process-data", status_code=status.HTTP_200_OK)
async def fetch_data_from_xml():
    task = fetch_and_process_sales_data.apply_async()
    return JSONResponse({"task_id": task.id})


@router.get("/task-status/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_status(task_id: str):
    """Интеграция эндпоинта для просмотра таски по заданному task_id, также эту информацию можно просматривать в celery flower"""
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return JSONResponse({"task_id": task_id, "status": "PENDING", "result": None})
    elif task_result.state == "SUCCESS":
        return JSONResponse(
            {"task_id": task_id, "status": "SUCCESS", "result": task_result.result}
        )
    elif task_result.state == "FAILURE":
        return JSONResponse(
            {"task_id": task_id, "status": "FAILURE", "result": str(task_result.result)}
        )
    else:
        return JSONResponse(
            {"task_id": task_id, "status": task_result.state, "result": None}
        )


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
