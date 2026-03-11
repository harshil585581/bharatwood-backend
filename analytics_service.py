from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models import SiteVisit
from datetime import datetime

def record_visit(db: Session, ip_address: str, session_id: str, user_agent: str, origin: str):
    # Clean origin to ensure consistent matching (e.g., remove https:// or http:// and trailing slashes)
    if origin:
        origin = origin.replace("https://", "").replace("http://", "").strip("/")

    db_visit = SiteVisit(
        ip_address=ip_address,
        session_id=session_id,
        user_agent=user_agent,
        origin=origin
    )
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def get_monthly_visits(db: Session, year: int = None, origin: str = None):
    if year is None:
        year = datetime.now().year

    # Base query
    query = db.query(
        extract('month', SiteVisit.created_at).label('month'),
        func.count(SiteVisit.id).label('visits')
    ).filter(
        extract('year', SiteVisit.created_at) == year
    )

    if origin:
        # Clean origin to ensure consistent matching
        origin = origin.replace("https://", "").replace("http://", "").strip("/")
        query = query.filter(SiteVisit.origin.ilike(f"%{origin}%"))

    stats = query.group_by(
        extract('month', SiteVisit.created_at)
    ).all()

    # Initialize all months with 0
    monthly_data = {month: 0 for month in range(1, 13)}
    
    for row in stats:
        monthly_data[int(row.month)] = row.visits

    # Format the response
    response_data = []
    month_abbrs = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i in range(1, 13):
        response_data.append({
            "month": month_abbrs[i - 1],
            "visits": monthly_data[i]
        })

    return response_data
