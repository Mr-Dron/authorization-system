import asyncio

from datetime import datetime, timezone

from app.tasks import checks

async def scheduler():
    while True:

        now = datetime.now(timezone.utc)

        try:
            if now.minute % 5 == 0:
                await checks.check_user_last_seen()
            
            if now.hour == 3 and now.minute == 0:
                await checks.logout_inactive_users()
        
        except Exception as exc:
            print(f"[SCHEDULER ERROR] {exc}")

        await asyncio.sleep(60)