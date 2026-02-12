
from sqlmodel import Session, select
from datetime import datetime
from spine.chapters.admin.models import SystemFlag

class SafetyManager:
    KILL_SWITCH_KEY = "global_kill_switch"

    def __init__(self, session: Session):
        self.session = session

    def is_kill_switch_active(self) -> bool:
        """
        Returns True if Kill Switch is ACTIVE (System Halted).
        Defaults to False (System Running) if flag missing.
        """
        flag = self.session.get(SystemFlag, self.KILL_SWITCH_KEY)
        return flag is not None and flag.value == "ACTIVE"

    def engage_kill_switch(self, user_email: str) -> SystemFlag:
        """
        STOPS all email sending immediately.
        """
        flag = self.session.get(SystemFlag, self.KILL_SWITCH_KEY)
        if not flag:
            flag = SystemFlag(key=self.KILL_SWITCH_KEY, value="ACTIVE")
        else:
            flag.value = "ACTIVE"
        
        flag.updated_at = datetime.utcnow()
        flag.updated_by = user_email
        self.session.add(flag)
        self.session.commit()
        self.session.refresh(flag)
        return flag

    def disengage_kill_switch(self, user_email: str) -> SystemFlag:
        """
        RESUMES email sending.
        """
        flag = self.session.get(SystemFlag, self.KILL_SWITCH_KEY)
        if not flag:
            flag = SystemFlag(key=self.KILL_SWITCH_KEY, value="INACTIVE")
        else:
            flag.value = "INACTIVE"
        
        flag.updated_at = datetime.utcnow()
        flag.updated_by = user_email
        self.session.add(flag)
        self.session.commit()
        self.session.refresh(flag)
        return flag

    def get_status(self) -> dict:
        active = self.is_kill_switch_active()
        flag = self.session.get(SystemFlag, self.KILL_SWITCH_KEY)
        last_update = flag.updated_at if flag else None
        updated_by = flag.updated_by if flag else None
        
        return {
            "kill_switch_active": active,
            "status": "HALTED" if active else "OPERATIONAL",
            "last_updated": last_update,
            "updated_by": updated_by
        }
