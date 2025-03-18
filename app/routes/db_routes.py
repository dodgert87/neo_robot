from fastapi import APIRouter, HTTPException, Query
from app.services.cache_service import CacheService
from app.core.error_codes import ErrorCode
from app.models.api_models import PersonRequest, NewsArticleRequest

router = APIRouter()

### ---------------- PERSON ROUTES ---------------- ###

@router.post("/person")
async def store_person(person: PersonRequest):
    """
    Stores a person's information in the database.
    """
    try:
        CacheService.store_person(person.personId, person.firstName, person.lastName)
        return {"status": "success", "message": "Person stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing person: {str(e)}")

@router.get("/person/{person_id}")
async def retrieve_person(person_id: str):
    """
    Retrieves a person's information from the database.
    """
    person = CacheService.retrieve_person(person_id)
    if "error" in person:
        raise HTTPException(status_code=404, detail=person["error"])
    return person

@router.get("/persons")
async def retrieve_all_persons():
    """
    Retrieves all persons stored in the database.
    """
    try:
        persons = CacheService.retrieve_all_persons()
        return {"status": "success", "data": persons}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving persons: {str(e)}")


### ---------------- CACHE QUERY ROUTES ---------------- ###
@router.get("/cache")
async def retrieve_cached_query(
    query_id: str = Query(None, description="Filter by query ID"),
    command: str = Query(None, description="Filter by command"),
    tag: str = Query(None, description="Filter by tag"),
    parameters: str = Query(None, description="Filter by parameters (JSON format)")
):
    """
    Retrieves cached queries based on query_id, command, tag, or parameters.
    """
    try:
        # Convert parameters string to dictionary if provided
        param_dict = None
        if parameters:
            import json
            try:
                param_dict = json.loads(parameters)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format for parameters")

        queries = CacheService.retrieve_query(query_id=query_id, command=command, tag=tag, parameters=param_dict)
        if not queries:
            return {"status": "success", "message": "No matching queries found", "data": []}

        return {"status": "success", "data": queries}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cache: {str(e)}")


### ---------------- NEWS ROUTES ---------------- ###


@router.post("/news")
async def store_news_article(article: NewsArticleRequest):
    """
    Stores a news article in the database.
    """
    try:
        CacheService.store_news_article(article.model_dump())
        return {"status": "success", "message": "News article stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing news article: {str(e)}")


@router.get("/news")
async def fetch_news_articles(
    article_id: str = Query(None, description="Filter by article ID"),
    title: str = Query(None, description="Filter by article title"),
    keywords: str = Query(None, description="Filter by keywords"),
    category: str = Query(None, description="Filter by category"),
    country: str = Query(None, description="Filter by country"),
    source_id: str = Query(None, description="Filter by source ID")
):
    """
    Fetches news articles based on filters (title, keywords, category, country, etc.).
    """
    try:
        keywords_list = keywords.split(",") if keywords else None
        category_list = category.split(",") if category else None
        country_list = country.split(",") if country else None

        articles = CacheService.fetch_articles(
            article_id=article_id,
            title=title,
            keywords=keywords_list,
            category=category_list,
            country=country_list,
            source_id=source_id
        )

        if not articles:
            return {"status": "success", "message": "No matching articles found", "data": []}

        return {"status": "success", "data": articles}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")


@router.post("/news/{article_id}/increment")
async def increment_news_query_count(article_id: str):
    """
    Increments the query count for a news article.
    """
    try:
        CacheService.increment_query_count(article_id)
        return {"status": "success", "message": f"Query count incremented for article {article_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating query count: {str(e)}")