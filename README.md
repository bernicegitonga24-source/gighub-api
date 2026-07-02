 GigHub Nairobi - Freelance Gigs API

GigHub is a lightweight, localized backend REST API built using **FastAPI** and **Pydantic**. The platform is designed for a Nairobi-based freelancing platform to connect local clients (posting short-term jobs/gigs) with freelancers like developers, designers, and writers.

This project was built adhering to specific dataset constraints mapped to Admission Number: **C027-01-0846/2024**.

 Project Specifications (Admission Parameters)
Based on the admission criteria rules, this API configuration operates under the following hardcoded constraints:
* **Total Initial Gigs:** 11 (`5 + last digit 6`)
* **Assigned Categories:** `["Development", "Design", "Writing"]` (Derived from even index `0846`)
* **Currency:** `KES` (Derived from leading digits `08` being less than 10)


 Features & Core Functionalities
1. **List & Filter Gigs:** Fetch all gigs with functional query filtering for `category`, `min_budget`, and `max_budget`.
2. **Search Ecosystem:** Search listings dynamically by matching string queries inside gig titles.
3. **Pydantic Data Validation:** Strict type-checking and validation logic preventing bad entries (e.g. invalid categories or negative budgets).
4. **CRUD Actions:** Complete support to view individual records, append new listings, update status/budgets, or drop rows.



 Tech Stack
* **Language:** Python 3.11+
* **Framework:** FastAPI
* **Validation:** Pydantic v2
* **Server Gateway:** Uvicorn (ASGI)


 Installation & Setup

1. Clone or Open the Directory
Ensure you are inside your project repository folder:
```bash
cd C:\Users\bernice\Desktop\Assignment\gighub_api