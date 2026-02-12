
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from datetime import datetime
from spine.chapters.admin.models import Tenant, Organization, TenantStatus, TenantTier

class TenantManager:
    def __init__(self, session: Session):
        self.session = session

    def create_organization(self, name: str) -> Organization:
        org = Organization(name=name)
        self.session.add(org)
        self.session.commit()
        self.session.refresh(org)
        return org

    def create_tenant(self, org_id: UUID, name: str, tier: TenantTier = TenantTier.SOLO) -> Tenant:
        # Validate Org exists
        org = self.session.get(Organization, org_id)
        if not org:
            raise ValueError(f"Organization {org_id} not found")

        tenant = Tenant(organization_id=org_id, name=name, tier=tier)
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        return tenant

    def suspend_tenant(self, tenant_id: UUID) -> Tenant:
        tenant = self.session.get(Tenant, tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        
        tenant.status = TenantStatus.SUSPENDED
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        return tenant

    def list_tenants(self, org_id: Optional[UUID] = None) -> List[Tenant]:
        query = select(Tenant)
        if org_id:
            query = query.where(Tenant.organization_id == org_id)
        return self.session.exec(query).all()

    def get_tenant_hierarchy(self, org_id: UUID) -> dict:
        org = self.session.get(Organization, org_id)
        if not org:
            return {}
        
        return {
            "organization": org,
            "tenants": self.list_tenants(org_id)
        }
