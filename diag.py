import sys
import os

print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    import spine
    print(f"Spine: {spine}")
    # print(f"Spine file: {spine.__file__}") # might fail if namespace

    import spine.api
    print(f"Spine API: {spine.api}")

    import spine.api.v1
    print(f"Spine API V1: {spine.api.v1}")

    import spine.api.v1.api
    print(f"Spine API V1 API: {spine.api.v1.api}")
    
    from spine.api.v1.api import api_router
    print(f"Router: {api_router}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
