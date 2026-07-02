from typing import List, Optional
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="GigHub Nairobi - Freelance Gigs API C027-01-0846/2024",
    description="Custom assignment backend tracking localized gig listings.",
    version="1.0.0"
)

ASSIGNED_CATEGORIES = ["Development", "Design", "Writing"]
ASSIGNED_CURRENCY = "KES"
VALID_STATUSES = ["Open", "In Progress", "Closed"]


gigs_db = [
    {
        "id": 1,
        "title": "Build a React Dashboard",
        "description": "Build a responsive React dashboard for a local Nairobi fintech startup.",
        "category": "Development",
        "budget": 45000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Logo Design for E-commerce",
        "description": "Create a modern, sleek logo and brand identity kit for an online fashion store.",
        "category": "Design",
        "budget": 12500.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "John Omwamba"
    },
    {
        "id": 3,
        "title": "Technical Blog Post Writing",
        "description": "Write three comprehensive technical articles about cloud computing optimizations.",
        "category": "Writing",
        "budget": 18000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Alice Koech"
    },
    {
        "id": 4,
        "title": "Mobile App UI/UX Redesign",
        "description": "Redesign the user experience and user interface profiles for a delivery mobile application.",
        "category": "Design",
        "budget": 35000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Otieno"
    },
    {
        "id": 5,
        "title": "Python Script Automation",
        "description": "Develop a robust Python script to scrape daily real estate market pricing from local listings.",
        "category": "Development",
        "budget": 22000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Mercy Kamau"
    },
    {
        "id": 6,
        "title": "Copywriting for Landing Page",
        "description": "High-converting sales copy rewrite for an agro-tech startup landing page platform.",
        "category": "Writing",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Mwangi"
    },
    {
        "id": 7,
        "title": "E-commerce Website Setup",
        "description": "Full setup of a WooCommerce multi-vendor market website with local M-Pesa payment gateways.",
        "category": "Development",
        "budget": 65000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Grace Kendi"
    },
    {
        "id": 8,
        "title": "Social Media Graphic Kits",
        "description": "Design a package of 30 reusable social media templates for a local fitness brand campaign.",
        "category": "Design",
        "budget": 20000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Brian Omondi"
    },
    {
        "id": 9,
        "title": "API Documentation Writing",
        "description": "Review clean backend code structures and write complete clear Markdown format technical documentations.",
        "category": "Writing",
        "budget": 28000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Emmanuel Kiprop"
    },
    {
        "id": 10,
        "title": "Flutter Cross-Platform App",
        "description": "Build an MVP version for a localized ride-hailing tracking application using Flutter frameworks.",
        "category": "Development",
        "budget": 95000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Sylvia Wanjiku"
    },
    {
        "id": 11,
        "title": "Packaging Graphic Designs",
        "description": "Creative visual concept designs for a premium eco-friendly coffee manufacturing business package.",
        "category": "Design",
        "budget": 40000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Patrick Juma"
    }
]

# Track the next auto-increment ID state dynamically
current_id_counter = len(gigs_db)
class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, json_schema_extra={"example": "Build a React dashboard"})
    description: str = Field(..., min_length=20, max_length=500, json_schema_extra={"example": "Build a React dashboard for a fintech startup..."})
    category: str = Field(..., json_schema_extra={"example": "Development"})
    budget: float = Field(..., gt=0, json_schema_extra={"example": 15000.0})
    client_name: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "Jane Muthoni"})

    @field_validator('category')
    @classmethod
    def validate_category(cls, value: str) -> str:
        if value not in ASSIGNED_CATEGORIES:
            raise ValueError(f"Category must be one of your assigned categories: {', '.join(ASSIGNED_CATEGORIES)}")
        return value


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0, json_schema_extra={"example": 17500.0})
    status: Optional[str] = Field(None, json_schema_extra={"example": "In Progress"})

    @field_validator('status')
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return value


@app.get("/gigs", response_model=List[dict])
def get_gigs(
    category: Optional[str] = Query(None, description="Filter gigs by category"),
    min_budget: Optional[float] = Query(None, description="Minimum budget filter"),
    max_budget: Optional[float] = Query(None, description="Maximum budget filter")
):
    filtered_gigs = gigs_db
    
    if category:
        filtered_gigs = [g for g in filtered_gigs if g["category"].lower() == category.lower()]
        
    if min_budget is not None:
        filtered_gigs = [g for g in filtered_gigs if g["budget"] >= min_budget]
        
    if max_budget is not None:
        filtered_gigs = [g for g in filtered_gigs if g["budget"] <= max_budget]
        
    return filtered_gigs


@app.get("/gigs/search", response_model=List[dict])
def search_gigs(q: str = Query(..., description="Query parameter matching text inside gig titles")):
    results = [g for g in gigs_db if q.lower() in g["title"].lower()]
    return results


@app.get("/gigs/{gig_id}", response_model=dict)
def get_gig_by_id(gig_id: int = Path(..., description="Target numerical unique gig ID")):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    raise HTTPException(status_code=404, detail=f"Gig with ID {gig_id} not found")


@app.post("/gigs", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_gig(gig_data: GigCreate):
    global current_id_counter
    current_id_counter += 1
    
    new_gig = {
        "id": current_id_counter,
        "title": gig_data.title,
        "description": gig_data.description,
        "category": gig_data.category,
        "budget": gig_data.budget,
        "currency": ASSIGNED_CURRENCY,  # Enforced matching parameter rule
        "status": "Open",               # Instantiated state configuration
        "client_name": gig_data.client_name
    }
    
    gigs_db.append(new_gig)
    return new_gig


@app.put("/gigs/{gig_id}", response_model=dict)
def update_gig(gig_id: int, update_data: GigUpdate):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            if update_data.budget is not None:
                gig["budget"] = update_data.budget
            if update_data.status is not None:
                gig["status"] = update_data.status
            return gig
            
    raise HTTPException(status_code=404, detail=f"Gig with ID {gig_id} not found")


@app.delete("/gigs/{gig_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gig(gig_id: int):
    global gigs_db
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            gigs_db.pop(index)
            return
            
    raise HTTPException(status_code=404, detail=f"Gig with ID {gig_id} not found")