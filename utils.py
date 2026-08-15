import datetime as dtm

from tluser import UserOnlineStatus, User


def get_time_ago(status: UserOnlineStatus):
    now_utc = dtm.datetime.now(dtm.timezone.utc)
    delta: dtm.timedelta = now_utc - status.was_online
    
    total_seconds = max(0, int(delta.total_seconds()))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0:
        time_ago = f"{hours} hours {minutes} minutes ago"
    else:
        time_ago = f"{minutes} minutes ago"
    return time_ago


def get_fullname(user: User, target_phone_or_id: str | None = None) -> str | None:
    return " ".join(
        [user.first_name or "", user.last_name or ""]
    ).strip() or target_phone_or_id
