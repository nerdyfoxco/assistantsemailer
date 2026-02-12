
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from typing import List

from spine.db import get_session
from spine.chapters.admin.tenants import TenantManager
from spine.chapters.admin.models import Organization, Tenant, TenantTier

router = APIRouter(prefix="/admin", tags=["admin"])

def get_tenant_manager(session: Session = Depends(get_session)) -> TenantManager:
    return TenantManager(session)

@router.post("/orgs", response_model=Organization)
def create_organization(name: str, mgr: TenantManager = Depends(get_tenant_manager)):
    return mgr.create_organization(name)

@router.post("/tenants", response_model=Tenant)
def create_tenant(org_id: UUID, name: str, tier: TenantTier = TenantTier.SOLO, mgr: TenantManager = Depends(get_tenant_manager)):
    try:
        return mgr.create_tenant(org_id, name, tier)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/tenants/{tenant_id}/suspend", response_model=Tenant)
def suspend_tenant(tenant_id: UUID, mgr: TenantManager = Depends(get_tenant_manager)):
    try:
        return mgr.suspend_tenant(tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/orgs/{org_id}/hierarchy")
def get_hierarchy(org_id: UUID, mgr: TenantManager = Depends(get_tenant_manager)):
    return mgr.get_tenant_hierarchy(org_id)

# --- Safety Controls ---
from spine.chapters.admin.safety import SafetyManager

def get_safety_manager(session: Session = Depends(get_session)) -> SafetyManager:
    return SafetyManager(session)

@router.get("/safety/status")
def get_system_status(mgr: SafetyManager = Depends(get_safety_manager)):
    return mgr.get_status()

@router.post("/safety/kill")
def engage_kill_switch(mgr: SafetyManager = Depends(get_safety_manager)):
    # In real app, get user from auth context
    return mgr.engage_kill_switch(user_email="admin@system.local")

@router.post("/safety/resume")
def disengage_kill_switch(mgr: SafetyManager = Depends(get_safety_manager)):
    return mgr.disengage_kill_switch(user_email="admin@system.local")

# --- Billing ---
from spine.chapters.admin.reconciliation import Ledger
from spine.chapters.admin.billing import PLANS

def get_ledger(session: Session = Depends(get_session)) -> Ledger:
    return Ledger(session)

@router.get("/billing/plans")
def list_plans():
    return {k.value: v.dict() for k, v in PLANS.items()}

@router.get("/billing/{tenant_id}/ledger")
def get_tenant_ledger(tenant_id: str, ledger: Ledger = Depends(get_ledger)):
    history = ledger.get_history(tenant_id)
    balance = ledger.get_balance(tenant_id)
    return {
        "balance": balance,
        "currency": "usd",
        "history": history
    }
