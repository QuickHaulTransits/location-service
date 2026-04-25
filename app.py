"""
Location Service API for Indian States, Districts, and Centers
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import json
from datetime import timedelta
import sys
from pathlib import Path
from data.indian_locations import get_all_states, get_districts_by_state, get_centers_by_district

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.config import settings

app = FastAPI(title="Location Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client = redis.from_url(settings.redis_url, db=0, decode_responses=True)

# Cache TTL (1 hour)
CACHE_TTL = timedelta(hours=1)

@app.get("/states")
async def get_states():
    """Get all Indian states"""
    cache_key = "states"
    
    try:
        # Try to get from cache
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        print(f"Redis error in get_states: {e}")
    
    # Get from data source
    states = get_all_states()
    
    try:
        # Cache the result
        redis_client.setex(cache_key, CACHE_TTL, json.dumps(states))
    except Exception as e:
        print(f"Redis error in set_states: {e}")
    
    return states

@app.get("/districts")
async def get_districts(state: str):
    """Get districts by state ID"""
    if not state:
        raise HTTPException(status_code=400, detail="State parameter is required")
    
    cache_key = f"districts:{state}"
    
    try:
        # Try to get from cache
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        print(f"Redis error in get_districts: {e}")
    
    # Get from data source
    districts = get_districts_by_state(state)
    
    if not districts:
        raise HTTPException(status_code=404, detail="State not found")
    
    try:
        # Cache the result
        redis_client.setex(cache_key, CACHE_TTL, json.dumps(districts))
    except Exception as e:
        print(f"Redis error in set_districts: {e}")
    
    return districts

@app.get("/centers")
async def get_centers(state: str, district: str):
    """Get centers by state and district IDs"""
    if not state or not district:
        raise HTTPException(status_code=400, detail="State and district parameters are required")
    
    cache_key = f"centers:{state}:{district}"
    
    try:
        # Try to get from cache
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        print(f"Redis error in get_centers: {e}")
    
    # Get from data source
    centers = get_centers_by_district(state, district)
    
    if not centers:
        raise HTTPException(status_code=404, detail="No centers found for the specified state and district")
    
    try:
        # Cache the result
        redis_client.setex(cache_key, CACHE_TTL, json.dumps(centers))
    except Exception as e:
        print(f"Redis error in set_centers: {e}")
    
    return centers

@app.delete("/cache")
async def clear_cache():
    """Clear all location cache (for development/testing)"""
    keys = redis_client.keys("states*") + redis_client.keys("districts*") + redis_client.keys("centers*")
    if keys:
        redis_client.delete(*keys)
    return {"message": f"Cleared {len(keys)} cache entries"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except:
        return {"status": "unhealthy", "redis": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
