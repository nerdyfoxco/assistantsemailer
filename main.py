from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chapters.api.router import router as api_router

app = FastAPI(title="Email System Vertical Slice", version="0.1.0")

# CORS for Frontend (Vite @ 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from spine.chapters.public.auth import router as auth_router
from spine.chapters.developer.api import router as developer_router
from spine.db.database import engine
from sqlmodel import SQLModel

app.include_router(api_router)
app.include_router(auth_router)
app.include_router(developer_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Vertical Slice Operational"}

@app.post("/seed")
def seed_data():
    from chapters.api.deps import get_container
    from chapters.connectors.gmail.service import EmailIngested
    from chapters.brain.service import BrainService
    
    container = get_container()
    manager = container.work_manager
    manager._store.clear()

    # Seed 1
    event1 = EmailIngested(
        tenant_id="demo", message_id="msg_1", snippet="Urgent Help", payload={"subject": "Urgent", "from": "client@co.com"}
    )
    manager.handle_email_ingested(event1)
    
    # Seed 2 (Drafted)
    event2 = EmailIngested(
        tenant_id="demo", message_id="msg_2", snippet="Meeting?", payload={"subject": "Sync", "from": "boss@co.com"}
    )
    item2 = manager.handle_email_ingested(event2)
    BrainService().generate_draft(item2, "Casual")
    
    return {"status": "seeded", "items": 2}
