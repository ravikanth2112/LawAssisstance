"""
Document schemas for API requests and responses
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    case_id: int
    document_name: str
    document_type: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    access_level: str = "case"  # public, case, lawyer, admin
    is_confidential: bool = False
    description: Optional[str] = None
    tags: Optional[str] = None

class DocumentUpdate(BaseModel):
    document_name: Optional[str] = None
    document_type: Optional[str] = None
    access_level: Optional[str] = None
    is_confidential: Optional[bool] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    status: Optional[str] = None

class DocumentUpload(BaseModel):
    case_id: int
    document_name: str
    document_type: str
    access_level: str = "case"  # public, case, lawyer, admin
    is_confidential: bool = False
    description: Optional[str] = None
    tags: Optional[str] = None

class DocumentShare(BaseModel):
    user_ids: list[int]
    access_level: str = "view"  # view, edit, download
    expires_at: Optional[datetime] = None

class DocumentResponse(BaseModel):
    document_id: int
    case_id: int
    uploaded_by: int
    document_name: str
    document_type: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    access_level: str
    is_confidential: bool
    password_protected: bool
    description: Optional[str] = None
    tags: Optional[str] = None
    version: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Computed properties
    file_size_mb: float = 0
    
    # Related objects (if populated)
    case: Optional['CaseResponse'] = None
    uploader: Optional['UserResponse'] = None

    class Config:
        from_attributes = True
        
    @property
    def id(self):
        return self.document_id

# Import here to avoid circular import
from app.schemas.case import CaseResponse
from app.schemas.user import UserResponse
DocumentResponse.model_rebuild()
