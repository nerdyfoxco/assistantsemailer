import unittest
from engine import verify, VerificationFault, G_Allow, G_Deny, G_Auth_Token_Present

class TestPhase15H(unittest.TestCase):

    def test_01_allow_pass(self):
        """G_Allow should let function execute."""
        @verify([G_Allow])
        def sensitive_op():
            return "SUCCESS"
        self.assertEqual(sensitive_op(), "SUCCESS")

    def test_02_deny_block(self):
        """G_Deny should raise VerificationFault."""
        @verify([G_Deny])
        def sensitive_op():
            return "SHOULD_NOT_RUN"
        with self.assertRaises(VerificationFault):
            sensitive_op()

    def test_03_multiple_guarantees_all_pass(self):
        """All guarantees must pass."""
        @verify([G_Allow, G_Allow])
        def op(): return "OK"
        self.assertEqual(op(), "OK")

    def test_04_multiple_guarantees_one_fail(self):
        """If any guarantee fails, block execution."""
        @verify([G_Allow, G_Deny])
        def op(): return "NO"
        with self.assertRaises(VerificationFault):
            op()

    def test_05_auth_token_check_pass(self):
        """G_Auth passes when token provided."""
        @verify([G_Auth_Token_Present])
        def send_email(auth_token=None):
            return "SENT"
        self.assertEqual(send_email(auth_token="valid_token"), "SENT")

    def test_06_auth_token_check_fail_none(self):
        """G_Auth fails when token is None."""
        @verify([G_Auth_Token_Present])
        def send_email(auth_token=None):
            return "SENT"
        with self.assertRaises(VerificationFault):
            send_email(auth_token=None)

    def test_07_auth_token_check_fail_missing_kwarg(self):
        """G_Auth fails when kwarg missing entirely."""
        @verify([G_Auth_Token_Present])
        def send_email():
            return "SENT"
        with self.assertRaises(VerificationFault):
            send_email()

    def test_08_decorator_preserves_metadata(self):
        """Decorator should preserve function name/doc."""
        @verify([G_Allow])
        def my_func():
            """My Docstring"""
            pass
        self.assertEqual(my_func.__name__, "my_func")
        self.assertEqual(my_func.__doc__, "My Docstring")

    def test_09_args_inspection(self):
        """Guarantee can inspect positional args mapped to kwargs."""
        class G_InspectArg(unittest.TestCase): # misuse of TestCase just for class structure in this inline test
            def check(self, x=None, **kwargs):
                if x != 10: raise VerificationFault("x must be 10")
        
        # We need to adapt G_InspectArg to match the Guarantee interface protocol expectation of `check`
        class G_CheckX:
            def check(self, x=None, **kwargs):
                if x != 10: raise VerificationFault("x must be 10")

        @verify([G_CheckX])
        def logic(x): return x * 2

        self.assertEqual(logic(10), 20)
        with self.assertRaises(VerificationFault):
            logic(5)

    def test_10_execution_order(self):
        """Guarantees run BEFORE function."""
        side_effects = []
        class G_Log:
            def check(self, **kwargs):
                side_effects.append("CHECK")
        
        @verify([G_Log])
        def run():
            side_effects.append("RUN")
        
        run()
        self.assertEqual(side_effects, ["CHECK", "RUN"])

if __name__ == '__main__':
    unittest.main()
