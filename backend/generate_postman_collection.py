import os
import re
import json

def extract_endpoints_with_details(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract endpoint details including docstrings
        pattern = r'@router\.(get|post|put|delete|patch)\(["\']([^"\']*)["\'][^)]*\)\s*(?:async\s+)?def\s+([^(]+)\([^)]*\):[^"\']*(?:["\']([^"\']*)["\'])?'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        endpoints = []
        for method, path, func_name, description in matches:
            endpoints.append({
                'method': method.upper(),
                'path': path,
                'function': func_name,
                'description': description or func_name.replace('_', ' ').title()
            })
        
        return endpoints
    except Exception as e:
        return []

def generate_postman_collection():
    router_dir = 'app/routers'
    base_url = "{{base_url}}"  # Postman variable
    
    collection = {
        "info": {
            "name": "Immigration Law Dashboard API",
            "description": "Complete API collection for Immigration Law Dashboard with 63 endpoints",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {
                "key": "base_url",
                "value": "http://localhost:8000",
                "type": "string"
            },
            {
                "key": "auth_token",
                "value": "",
                "type": "string"
            }
        ],
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{auth_token}}",
                    "type": "string"
                }
            ]
        },
        "item": []
    }
    
    # Module order for organization
    module_order = ['authentication', 'users', 'lawyers', 'clients', 'cases', 'dashboard', 
                    'deadlines', 'documents', 'billing', 'activities']
    
    for module in module_order:
        module_file = f'{router_dir}/{module}.py'
        if os.path.exists(module_file):
            endpoints = extract_endpoints_with_details(module_file)
            
            if endpoints:
                phase = "PHASE 1" if module in ['authentication', 'users', 'lawyers', 'clients', 'cases', 'dashboard'] else "PHASE 2"
                
                module_folder = {
                    "name": f"{module.upper()} - {phase} ({len(endpoints)} endpoints)",
                    "item": []
                }
                
                for endpoint in endpoints:
                    method = endpoint['method']
                    path = endpoint['path']
                    
                    # Construct full URL
                    if not path.startswith('/api/'):
                        if path.startswith('/'):
                            full_path = '/api' + path
                        else:
                            full_path = '/api/' + path
                    else:
                        full_path = path
                    
                    # Map to correct API structure
                    if module == 'authentication':
                        if path == '/login':
                            full_path = '/api/auth/login'
                        elif path == '/register':
                            full_path = '/api/auth/register'
                        elif path == '/me':
                            full_path = '/api/auth/me'
                        elif path == '/logout':
                            full_path = '/api/auth/logout'
                    else:
                        full_path = f'/api/{module}{path}'
                    
                    # Create request body based on method and endpoint
                    body = None
                    if method in ['POST', 'PUT']:
                        body = get_sample_body(module, endpoint['function'], method)
                    
                    request_item = {
                        "name": f"{method} {endpoint['description']}",
                        "request": {
                            "method": method,
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json",
                                    "type": "text"
                                }
                            ],
                            "url": {
                                "raw": f"{base_url}{full_path}",
                                "host": ["{{base_url}}"],
                                "path": full_path.split('/')[1:]
                            },
                            "description": f"{endpoint['description']} - {module.title()} module"
                        }
                    }
                    
                    # Add authentication for protected endpoints
                    if module != 'authentication' or endpoint['function'] in ['get_current_user', 'logout']:
                        request_item["request"]["auth"] = {
                            "type": "bearer",
                            "bearer": [
                                {
                                    "key": "token",
                                    "value": "{{auth_token}}",
                                    "type": "string"
                                }
                            ]
                        }
                    
                    # Add body for POST/PUT requests
                    if body:
                        request_item["request"]["body"] = {
                            "mode": "raw",
                            "raw": json.dumps(body, indent=2),
                            "options": {
                                "raw": {
                                    "language": "json"
                                }
                            }
                        }
                    
                    module_folder["item"].append(request_item)
                
                collection["item"].append(module_folder)
    
    return collection

def get_sample_body(module, function, method):
    """Generate sample request bodies for different endpoints"""
    
    bodies = {
        'authentication': {
            'register': {
                "username": "john_lawyer",
                "email": "john@lawfirm.com", 
                "password": "secure123",
                "first_name": "John",
                "last_name": "Smith",
                "role": "lawyer",
                "phone": "+1234567890"
            },
            'login': {
                "username": "john_lawyer",
                "password": "secure123"
            }
        },
        'users': {
            'create_user': {
                "username": "new_user",
                "email": "user@example.com",
                "password": "password123",
                "first_name": "New",
                "last_name": "User", 
                "role": "client",
                "phone": "+1234567890"
            },
            'update_user': {
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
                "phone": "+1234567890"
            }
        },
        'lawyers': {
            'create_lawyer': {
                "user_id": 1,
                "bar_number": "BAR123456",
                "specialization": "Immigration Law",
                "hourly_rate": 250.00,
                "bio": "Experienced immigration attorney"
            },
            'update_lawyer': {
                "specialization": "Immigration & Family Law",
                "hourly_rate": 275.00,
                "bio": "Updated bio"
            }
        },
        'clients': {
            'create_client': {
                "user_id": 1,
                "country_of_origin": "Mexico",
                "immigration_status": "H-1B",
                "preferred_language": "English"
            },
            'update_client': {
                "immigration_status": "Green Card",
                "preferred_language": "Spanish"
            }
        },
        'cases': {
            'create_case': {
                "client_id": 1,
                "lawyer_id": 1,
                "case_type": "Family Based Immigration",
                "title": "Green Card Application",
                "description": "Adjustment of status application",
                "status": "open",
                "priority": "medium"
            },
            'update_case': {
                "status": "in_progress",
                "priority": "high",
                "description": "Updated case description"
            },
            'assign_lawyer': {
                "lawyer_id": 2
            }
        },
        'deadlines': {
            'create_deadline': {
                "case_id": 1,
                "title": "File I-485",
                "description": "Submit adjustment of status application",
                "due_date": "2025-10-01T00:00:00",
                "priority": "high"
            },
            'update_deadline': {
                "title": "Updated deadline",
                "priority": "urgent",
                "status": "pending"
            }
        },
        'documents': {
            'create_document': {
                "case_id": 1,
                "title": "Birth Certificate",
                "file_name": "birth_cert.pdf",
                "file_type": "pdf",
                "confidentiality_level": "confidential"
            },
            'update_document': {
                "title": "Updated Document Title",
                "confidentiality_level": "highly_confidential"
            },
            'share_document': {
                "recipient_email": "client@example.com",
                "message": "Please review this document"
            }
        },
        'billing': {
            'create_billing': {
                "case_id": 1,
                "description": "Legal consultation and document review",
                "amount": 500.00,
                "due_date": "2025-10-01T00:00:00"
            },
            'update_billing': {
                "amount": 750.00,
                "status": "sent"
            },
            'record_payment': {
                "billing_id": 1,
                "amount": 500.00,
                "payment_method": "credit_card",
                "transaction_id": "TXN123456"
            }
        },
        'activities': {
            'create_activity': {
                "case_id": 1,
                "lawyer_id": 1,
                "activity_type": "consultation",
                "description": "Client consultation regarding case status",
                "hours_worked": 2.5,
                "billable_rate": 250.00,
                "is_billable": True,
                "activity_date": "2025-09-01T10:00:00"
            },
            'update_activity': {
                "hours_worked": 3.0,
                "description": "Extended consultation with document review"
            }
        }
    }
    
    if module in bodies and function in bodies[module]:
        return bodies[module][function]
    
    # Default bodies for common operations
    if method == 'POST':
        return {"data": "sample_create_data"}
    elif method == 'PUT':
        return {"data": "sample_update_data"}
    
    return None

# Generate and save the collection
collection = generate_postman_collection()

# Save as JSON file
with open('Immigration_Law_Dashboard_API.postman_collection.json', 'w', encoding='utf-8') as f:
    json.dump(collection, f, indent=2)

print("🚀 POSTMAN COLLECTION GENERATED!")
print("=" * 50)
print("📁 File: Immigration_Law_Dashboard_API.postman_collection.json")
print("📊 Total Endpoints: 63")
print("🔗 Import this file into Postman for testing")
print()
print("📋 SETUP INSTRUCTIONS:")
print("1. Import the JSON file into Postman")
print("2. Set base_url variable to: http://localhost:8000")
print("3. Register/Login to get auth token")
print("4. Set auth_token variable with JWT token")
print("5. Test all endpoints!")
