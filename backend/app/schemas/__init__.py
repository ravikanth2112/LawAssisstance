# Import all schemas
from .user import UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenData, UserType
from .lawyer import LawyerCreate, LawyerUpdate, LawyerResponse, LawyerWithUser
from .client import ClientCreate, ClientUpdate, ClientResponse, ClientWithUser
from .case import CaseCreate, CaseUpdate, CaseResponse, CaseWithDetails, CaseStatus, CasePriority

__all__ = [
    # User schemas
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin", "Token", "TokenData", "UserType",
    # Lawyer schemas
    "LawyerCreate", "LawyerUpdate", "LawyerResponse", "LawyerWithUser",
    # Client schemas
    "ClientCreate", "ClientUpdate", "ClientResponse", "ClientWithUser",
    # Case schemas
    "CaseCreate", "CaseUpdate", "CaseResponse", "CaseWithDetails", "CaseStatus", "CasePriority"
]
