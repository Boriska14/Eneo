from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import EneoData
from app.routers.auth import get_db


router = APIRouter()

@router.get("/data_by_date")
async def get_data_by_date(date: str = None, db: Session = Depends(get_db)):
    """
    Fetches EneoData records for a given date (without considering hour).

    Parameters:
        date (str, optional): Date in YYYY-MM-DD format. Defaults to None.
        db (Session): Database session object.

    Returns:
        List[EneoData]: List of EneoData objects.
    """

    if not date:
        return {"error": "Please provide a date in YYYY-MM-DD format."}

    date_column = func.left(EneoData.date, 10)
    query = db.query(EneoData).filter(date_column == date)

    results = await query.all()
    return results
