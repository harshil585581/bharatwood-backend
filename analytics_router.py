from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from database import get_db
import analytics_service
from schemas import MonthlyVisitStats
import uuid

router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"],
)

from pydantic import BaseModel

class VisitRequest(BaseModel):
    origin: str = None

@router.post("/visit")
async def record_visit(request: Request, response: Response, visit_data: VisitRequest, db: Session = Depends(get_db)):
    # Get IP address
    client_host = request.client.host
    forwarded_for = request.headers.get("X-Forwarded-For")
    ip_address = forwarded_for.split(',')[0] if forwarded_for else client_host

    # Get User Agent
    user_agent = request.headers.get("User-Agent")
    
    # Get Origin (Explicit from body, fallback to Headers)
    origin = visit_data.origin or request.headers.get("Origin") or request.headers.get("Referer")

    # Get session ID from cookies or generate a new one
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        # Set cookie so subsequent requests from the same user have the same session_id
        # Usually frontend will need to send credentials for this if CORS is involved
        response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="lax", max_age=31536000) 

    analytics_service.record_visit(db, ip_address, session_id, user_agent, origin)

    return {"message": "Visit recorded", "session_id": session_id}

@router.get("/monthly", response_model=list[MonthlyVisitStats])
def get_monthly_visits(year: int = None, origin: str = None, db: Session = Depends(get_db)):
    return analytics_service.get_monthly_visits(db, year, origin)
