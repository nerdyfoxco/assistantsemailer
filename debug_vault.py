
import asyncio
import logging
import uuid
import sys
from spine.db.database import AsyncSessionLocal
from spine.chapters.action.vault import Vault
from spine.core.config import settings
from spine.db.models import UserVault
from sqlalchemy import select, delete

# Setup Logging to Console
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("visual_seal")

async def run_visual_audit():
    print("=== VISUAL SEAL AUDIT: UMP-60-03 (THE VAULT) ===")
    
    async with AsyncSessionLocal() as db:
        vault = Vault(db)
        user_id = f"visual_test_user_{uuid.uuid4().hex[:8]}"
        key_name = "secret_visual_key"
        plaintext = "CONFIDENTIAL_DATA_12345"
        
        print(f"\n[1] SETUP")
        print(f"User ID: {user_id}")
        print(f"Key: {key_name}")
        print(f"Plaintext: {plaintext}")
        
        # 1. ENCRYPT & STORE
        print(f"\n[2] ACTION: Store (Encrypt)")
        await vault.stored_set(user_id, key_name, plaintext)
        
        # Verify Raw DB Content
        stmt = select(UserVault).where(UserVault.user_id == user_id, UserVault.key_name == key_name)
        result = await db.execute(stmt)
        record = result.scalars().first()
        
        if record:
            print(f"-> DB STATUS: RECORD FOUND")
            # Show masked encrypted value
            enc_val = record.encrypted_value
            masked_enc = enc_val[:10] + "..." + enc_val[-10:]
            print(f"-> RAW ENCRYPTED: {masked_enc} (Length: {len(enc_val)})")
            
            if enc_val == plaintext:
                print("!! CRITICAL FAILURE: PLAYINTEXT STORED IN DB !!")
                return
            else:
                print("-> SECURITY CHECK: PASS (Value is encrypted)")
        else:
            print("!! FAILURE: Record not found in DB !!")
            return

        # 2. RETRIEVE & DECRYPT
        print(f"\n[3] ACTION: Retrieve (Decrypt)")
        decrypted = await vault.stored_get(user_id, key_name)
        print(f"-> DECRYPTED VALUE: {decrypted}")
        
        if decrypted == plaintext:
            print("-> INTEGRITY CHECK: PASS (Roundtrip successful)")
        else:
            print(f"!! FAILURE: Decrypted value mismatch. Got '{decrypted}' !!")
            
        # 3. CLEANUP
        print(f"\n[4] CLEANUP")
        await vault.stored_delete(user_id, key_name)
        check = await vault.stored_get(user_id, key_name)
        if check is None:
            print("-> DELETION CHECK: PASS")
        else:
            print("!! FAILURE: Record still exists !!")
            
    print("\n=== AUDIT COMPLETE ===")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(run_visual_audit())
    except Exception as e:
        print(f"!! EXCEPTION: {e}")
