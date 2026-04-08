import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.domain.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.application.use_cases import RegisterUser, LoginUser, GetCurrentUser
from app.application.auth_middleware import validate_jwt
from app.infrastructure.repositories import UserRepositoryPostgres
from app.infrastructure.hashing import BCryptHashingService
from app.infrastructure.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


def get_register_use_case(db: Session = Depends(get_db)) -> RegisterUser:
    return RegisterUser(
        repository=UserRepositoryPostgres(db),
        hashing=BCryptHashingService(),
    )


def get_login_use_case(db: Session = Depends(get_db)) -> LoginUser:
    return LoginUser(
        repository=UserRepositoryPostgres(db),
        hashing=BCryptHashingService(),
    )


def get_current_user_use_case(db: Session = Depends(get_db)) -> GetCurrentUser:
    return GetCurrentUser(repository=UserRepositoryPostgres(db))


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    use_case: RegisterUser = Depends(get_register_use_case),
):
    try:
        return use_case.execute(request.email, request.password, request.role)
    except ValueError as e:
        if str(e) == "EMAIL_ALREADY_EXISTS":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    use_case: LoginUser = Depends(get_login_use_case),
):
    try:
        return use_case.execute(request.email, request.password)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.get("/me", response_model=UserResponse)
def get_me(
    payload: dict = Depends(validate_jwt),
    use_case: GetCurrentUser = Depends(get_current_user_use_case),
):
    try:
        user_id = uuid.UUID(payload["user_id"])
        return use_case.execute(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
