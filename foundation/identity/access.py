from .models import User, Resource

class AccessDeniedError(Exception):
    pass

class TenantMismatchError(AccessDeniedError):
    pass

def validate_access(actor: User, resource: Resource):
    """
    The Core Check.
    1. Actor must be Active.
    2. Actor.tenant_id must match Resource.tenant_id.
    """
    if not actor.is_active:
        raise AccessDeniedError(f"User {actor.id} is inactive.")

    if actor.tenant_id != resource.tenant_id:
        raise TenantMismatchError(
            f"Isolation Violation: User {actor.id} (Tenant {actor.tenant_id}) "
            f"attempted access to Resource {resource.id} (Tenant {resource.tenant_id})"
        )

    return True

def validate_admin_access(actor: User, resource: Resource):
    """
    Checks if actor is admin AND belongs to same tenant.
    """
    validate_access(actor, resource)
    
    if actor.role not in ["OWNER", "ADMIN"]:
        raise AccessDeniedError(f"User {actor.id} lacks ADMIN privs.")
        
    return True
