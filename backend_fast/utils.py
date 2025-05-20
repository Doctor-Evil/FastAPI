import bcrypt
from fastapi import HTTPException, status

# Хеширование пароля
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )

def check_user_admin(current_user: dict) -> bool:
    """
    Check if the current user is an admin.
    """
    if not current_user.role.value == "admin":
        return False
    
    return True