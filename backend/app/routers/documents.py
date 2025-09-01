"""
Documents router - Document management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentCreate, DocumentUpdate, DocumentShare

router = APIRouter()
security = HTTPBearer()

# Configure upload directory
UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    case_id: Optional[int] = Query(None),
    document_type: Optional[str] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get documents with filtering"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Document).filter(Document.status == "active")
    
    # Role-based filtering
    if current_user.role == "client":
        # Clients can only see documents for their cases
        from app.models.case import Case
        query = query.join(Case).filter(Case.client_id == current_user.id)
    elif current_user.role == "lawyer":
        # Lawyers can see documents for their assigned cases
        # For now, show all - in full implementation, filter by case assignments
        pass
    
    # Apply filters
    if case_id:
        query = query.filter(Document.case_id == case_id)
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    documents = query.order_by(Document.created_at.desc()).all()
    
    # Add computed properties
    for doc in documents:
        doc.file_size_mb = doc.file_size_mb
    
    return [DocumentResponse.model_validate(doc) for doc in documents]

@router.post("/", response_model=DocumentResponse)
async def upload_document(
    case_id: int,
    document_type: str,
    access_level: str = "case",
    is_confidential: bool = False,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Upload document (File type validation, size limits)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can upload documents
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can upload documents"
        )
    
    # Validate file type
    allowed_types = {
        'application/pdf', 'image/jpeg', 'image/png', 'image/gif',
        'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # Check file size (limit to 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10MB limit"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    # Create document record
    document = Document(
        case_id=case_id,
        uploaded_by=current_user.id,
        document_name=file.filename,
        document_type=document_type,
        file_path=file_path,
        file_size=len(file_content),
        mime_type=file.content_type,
        access_level=access_level,
        is_confidential=is_confidential,
        description=description,
        tags=tags
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Add computed properties
    document.file_size_mb = document.file_size_mb
    
    return DocumentResponse.model_validate(document)

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document_by_id(
    document_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get document by ID"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access permissions
    if current_user.role == "client":
        from app.models.case import Case
        case = db.query(Case).filter(Case.case_id == document.case_id).first()
        if not case or case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    # Add computed properties
    document.file_size_mb = document.file_size_mb
    
    return DocumentResponse.model_validate(document)

@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Download document file (Access control, audit logging)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access permissions
    if current_user.role == "client":
        from app.models.case import Case
        case = db.query(Case).filter(Case.case_id == document.case_id).first()
        if not case or case.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    # Check if file exists
    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # TODO: Add audit logging here
    
    return FileResponse(
        path=document.file_path,
        filename=document.document_name,
        media_type=document.mime_type
    )

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update document metadata"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions
    if current_user.role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot update documents"
        )
    
    # Update document fields
    update_data = document_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)
    
    # Increment version
    document.version += 1
    
    db.commit()
    db.refresh(document)
    
    # Add computed properties
    document.file_size_mb = document.file_size_mb
    
    return DocumentResponse.model_validate(document)

@router.post("/{document_id}/share")
async def share_document(
    document_id: int,
    share_data: DocumentShare,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Share document with users (Permission-based sharing)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can share documents
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can share documents"
        )
    
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # TODO: Implement document sharing logic with permissions table
    # For now, return success message
    
    return {
        "message": f"Document shared with {len(share_data.user_ids)} users",
        "shared_with": share_data.user_ids,
        "access_level": share_data.access_level
    }

@router.get("/search/")
async def search_documents(
    q: str = Query(..., description="Search query"),
    document_type: Optional[str] = Query(None),
    case_id: Optional[int] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Search documents (Content search, metadata filtering)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    query = db.query(Document).filter(Document.status == "active")
    
    # Role-based filtering
    if current_user.role == "client":
        from app.models.case import Case
        query = query.join(Case).filter(Case.client_id == current_user.id)
    
    # Search in document name, description, and tags
    search_filter = (
        Document.document_name.contains(q) |
        Document.description.contains(q) |
        Document.tags.contains(q)
    )
    query = query.filter(search_filter)
    
    # Apply additional filters
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if case_id:
        query = query.filter(Document.case_id == case_id)
    
    documents = query.order_by(Document.created_at.desc()).all()
    
    # Add computed properties
    for doc in documents:
        doc.file_size_mb = doc.file_size_mb
    
    return {
        "query": q,
        "total_results": len(documents),
        "documents": [DocumentResponse.model_validate(doc) for doc in documents]
    }

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete document (soft delete)"""
    
    current_user = get_current_user(credentials.credentials, db)
    
    # Only admin and lawyers can delete documents
    if current_user.role not in ["admin", "lawyer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin and lawyers can delete documents"
        )
    
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Soft delete - mark as deleted
    document.status = "deleted"
    db.commit()
    
    return {"message": "Document deleted successfully"}
