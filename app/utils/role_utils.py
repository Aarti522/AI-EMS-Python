from fastapi import HTTPException


VALID_ROLES = {
    "ADMIN",
    "HR",
    "MANAGER",
    "EMPLOYEE"
}


def validate_role(role: str) -> str:
    normalized_role = str(role).strip().upper()

    if normalized_role not in VALID_ROLES:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "data": None,
                "message": "Invalid role"
            }
        )

    return normalized_role


def require_role(role: str, allowed_roles: set) -> str:
    normalized_role = validate_role(role)

    if normalized_role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "data": None,
                "message": "Access denied for this role"
            }
        )

    return normalized_role