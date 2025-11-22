import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from schemas import Review
from database import db, create_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# -----------------------------
# Reviews API
# -----------------------------

class ReviewOut(Review):
    id: str
    created_at: Optional[str] = None

@app.get("/api/reviews", response_model=List[ReviewOut])
def list_reviews(limit: int = Query(20, ge=1, le=100)):
    """Return recent reviews (newest first)"""
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    # Sort by created_at desc if present else by _id desc
    cursor = db["review"].find({}).sort([("created_at", -1), ("_id", -1)]).limit(limit)
    items = []
    for doc in cursor:
        items.append(ReviewOut(
            id=str(doc.get("_id")),
            name=doc.get("name", ""),
            rating=int(doc.get("rating", 0)),
            message=doc.get("message", ""),
            event_type=doc.get("event_type"),
            instagram=doc.get("instagram"),
            created_at=str(doc.get("created_at")) if doc.get("created_at") else None,
        ))
    return items

@app.post("/api/reviews", status_code=201)
def create_review(review: Review):
    """Create a new review"""
    try:
        inserted_id = create_document("review", review)
        return {"id": inserted_id, "message": "Review submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
