from http import HTTPStatus

from api.v1.queries.search import query_film_by_title
from api.v1.schemas.search import SearchDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException, Request
from services.collection import CollectionService
from utils.pagination import paginate_response
from utils.service import get_collection_service

CONFIG = Settings().dict()

router = APIRouter()


@router.get("/", response_model=dict)
async def search_collection(
    title: str, search_service: CollectionService = Depends(get_collection_service),
    page: int = 1, size: int = 10
) -> dict:
    """Search films with title."""
    search = await search_service.get_items(
        query_film_by_title(
            title), SearchDetailSchema, CONFIG["ELASTIC_FILM_INDEX"]
    )
    if not search:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="film not found")
    return paginate_response(search, page, size)
