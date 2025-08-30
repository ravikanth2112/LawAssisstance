# Import all models
from .user import User, UserType
from .lawyer import Lawyer
from .client import Client
from .case import Case, CaseStatus, CasePriority

# Update relationships
from sqlalchemy.orm import relationship

# Add relationships to User model
User.lawyer = relationship("Lawyer", back_populates="user", uselist=False)
User.client = relationship("Client", back_populates="user", uselist=False)

# Add relationships to Client model
Client.cases = relationship("Case", back_populates="client")

# Add relationships to Lawyer model
Lawyer.primary_cases = relationship("Case", back_populates="primary_lawyer")

__all__ = [
    "User", "UserType",
    "Lawyer", 
    "Client", 
    "Case", "CaseStatus", "CasePriority"
]
