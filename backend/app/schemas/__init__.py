"""
Immigration Law Dashboard Schemas
"""

from .user import UserCreate, UserUpdate, UserResponse
from .lawyer import LawyerCreate, LawyerUpdate, LawyerResponse
from .client import ClientCreate, ClientUpdate, ClientResponse
from .case import CaseCreate, CaseUpdate, CaseResponse
from .deadline import DeadlineCreate, DeadlineUpdate, DeadlineResponse
from .document import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentUpload, DocumentShare
from .billing import BillingCreate, BillingUpdate, BillingResponse, BillingSend, PaymentCreate, PaymentResponse
from .activity import ActivityCreate, ActivityUpdate, ActivityResponse

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse",
    "LawyerCreate", "LawyerUpdate", "LawyerResponse",
    "ClientCreate", "ClientUpdate", "ClientResponse", 
    "CaseCreate", "CaseUpdate", "CaseResponse",
    "DeadlineCreate", "DeadlineUpdate", "DeadlineResponse",
    "DocumentCreate", "DocumentUpdate", "DocumentResponse", "DocumentUpload", "DocumentShare",
    "BillingCreate", "BillingUpdate", "BillingResponse", "BillingSend", "PaymentCreate", "PaymentResponse",
    "ActivityCreate", "ActivityUpdate", "ActivityResponse"
]