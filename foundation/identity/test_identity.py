import unittest
from models import User, Tenant, Resource
from access import validate_access, validate_admin_access, AccessDeniedError, TenantMismatchError

class TestIdentityIsolation(unittest.TestCase):

    def setUp(self):
        self.tenant_a = Tenant(name="Corp A")
        self.tenant_b = Tenant(name="Corp B")
        
        self.user_a = User(email="a@a.com", tenant_id=self.tenant_a.id, role="MEMBER")
        self.admin_a = User(email="admin@a.com", tenant_id=self.tenant_a.id, role="ADMIN")
        self.user_b = User(email="b@b.com", tenant_id=self.tenant_b.id, role="MEMBER")
        
        self.res_a = Resource(id="doc_1", tenant_id=self.tenant_a.id)
        self.res_b = Resource(id="doc_2", tenant_id=self.tenant_b.id)

    def test_01_same_tenant_access_allowed(self):
        """User A can access Resource A."""
        self.assertTrue(validate_access(self.user_a, self.res_a))

    def test_02_cross_tenant_access_blocked(self):
        """User A CANNOT access Resource B."""
        with self.assertRaises(TenantMismatchError):
            validate_access(self.user_a, self.res_b)

    def test_03_user_b_access_own_resource(self):
        """User B can access Resource B."""
        self.assertTrue(validate_access(self.user_b, self.res_b))

    def test_04_user_b_fail_access_resource_a(self):
        """User B CANNOT access Resource A."""
        with self.assertRaises(TenantMismatchError):
            validate_access(self.user_b, self.res_a)

    def test_05_inactive_user_blocked(self):
        """Inactive user blocked even if tenant matches."""
        self.user_a.is_active = False
        with self.assertRaises(AccessDeniedError):
            validate_access(self.user_a, self.res_a)

    def test_06_admin_check_success(self):
        """Admin can access resource in same tenant with admin check."""
        self.assertTrue(validate_admin_access(self.admin_a, self.res_a))

    def test_07_member_fails_admin_check(self):
        """Member fails admin check even if tenant matches."""
        with self.assertRaises(AccessDeniedError):
            validate_admin_access(self.user_a, self.res_a)

    def test_08_admin_fails_cross_tenant(self):
        """Admin A cannot access Admin B resource."""
        with self.assertRaises(TenantMismatchError):
            validate_admin_access(self.admin_a, self.res_b)

    def test_09_resource_integrity(self):
        """Ensure resource actually stores tenant_id."""
        self.assertEqual(self.res_a.tenant_id, self.tenant_a.id)

    def test_10_uuid_generation(self):
        """Ensure IDs are unique."""
        u1 = User()
        u2 = User()
        self.assertNotEqual(u1.id, u2.id)

if __name__ == '__main__':
    unittest.main()
