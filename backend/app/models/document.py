"""
Document model for case document management
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Document details
    document_name = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False)  # passport, visa, application, etc.
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger)  # Size in bytes
    mime_type = Column(String(100))
    
    # Security and access
    access_level = Column(String(20), nullable=False, default="case")  # public, case, lawyer, admin
    is_confidential = Column(Boolean, default=False)
    password_protected = Column(Boolean, default=False)
    
    # Metadata
    description = Column(Text)
    tags = Column(String(500))  # Comma-separated tags
    version = Column(Integer, default=1)
    
    # Status
    status = Column(String(20), nullable=False, default="active")  # active, archived, deleted
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    case = relationship("Case", backref="documents")
    uploader = relationship("User", backref="uploaded_documents")
    
    @property
    def id(self):
        return self.document_id
    
    @property
    def file_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
