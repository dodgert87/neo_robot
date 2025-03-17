from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.cache_service import CacheService
from app.core.error_codes import ErrorCode

router = APIRouter()

### ---------------- PERSON ROUTES ---------------- ###
class PersonRequest(BaseModel):
    personId: str
    firstName: str
    lastName: str

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
