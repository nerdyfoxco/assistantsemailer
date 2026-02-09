import functools
import inspect

class VerificationFault(Exception):
    pass

class Guarantee:
    """Base class for all runtime guarantees."""
    def check(self, *args, **kwargs) -> bool:
        raise NotImplementedError

class G_Allow(Guarantee):
    """Always passes (for testing)."""
    def check(self, *args, **kwargs):
        return True

class G_Deny(Guarantee):
    """Always fails (to prove veto power)."""
    def check(self, *args, **kwargs):
        raise VerificationFault("Explicit G_Deny triggered.")

class G_Auth_Token_Present(Guarantee):
    """Ensures an 'auth_token' kwarg is present and not empty."""
    def check(self, *args, **kwargs):
        token = kwargs.get("auth_token")
        if not token:
            raise VerificationFault("G_AUTH Violation: No auth_token provided.")
        return True

def verify(guarantees):
    """
    The Phase 15.H Decorator.
    Executes ALL guarantees BEFORE the target function.
    """
    def decorator_verify(func):
        @functools.wraps(func)
        def wrapper_verify(*args, **kwargs):
            # Bind arguments to parameter names for easier inspection
            sig = inspect.signature(func)
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            all_args = bound.arguments

            for g in guarantees:
                # Pass the context (arguments) to the guarantee
                # We instantiate if it's a class, or use if instance
                check_obj = g() if isinstance(g, type) else g
                check_obj.check(**all_args)
            
            return func(*args, **kwargs)
        return wrapper_verify
    return decorator_verify
