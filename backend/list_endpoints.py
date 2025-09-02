import os
import re

def extract_endpoints_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = r'@router\.(get|post|put|delete|patch)\(["\']([^"\']*)["\']'
        matches = re.findall(pattern, content, re.IGNORECASE)
        return [(method.upper(), path) for method, path in matches]
    except Exception as e:
        return []

router_dir = 'app/routers'
all_endpoints = []
modules = {}

for file in sorted(os.listdir(router_dir)):
    if file.endswith('.py') and file != '__init__.py':
        file_path = os.path.join(router_dir, file)
        endpoints = extract_endpoints_from_file(file_path)
        if endpoints:
            module_name = file.replace('.py', '')
            modules[module_name] = endpoints
            all_endpoints.extend(endpoints)

print('🏛️ IMMIGRATION LAW DASHBOARD - COMPLETE API ENDPOINT LIST')
print('=' * 70)
print()

# Define module order
module_order = ['authentication', 'users', 'lawyers', 'clients', 'cases', 'dashboard', 
                'deadlines', 'documents', 'billing', 'activities']

for module in module_order:
    if module in modules:
        endpoints = modules[module]
        phase = "PHASE 1" if module in ['authentication', 'users', 'lawyers', 'clients', 'cases', 'dashboard'] else "PHASE 2"
        print(f'📋 {module.upper()} MODULE - {phase} ({len(endpoints)} endpoints):')
        for method, path in endpoints:
            # Add /api prefix if not present
            if not path.startswith('/api/'):
                if path.startswith('/'):
                    full_path = '/api' + path
                else:
                    full_path = '/api/' + path
            else:
                full_path = path
            print(f'   {method:<6} {full_path}')
        print()

print(f'📊 SUMMARY:')
print(f'   Total Endpoints: {len(all_endpoints)}')
print(f'   Total Modules: {len(modules)}')
print(f'   Phase 1 Modules: 6 (Authentication, Users, Lawyers, Clients, Cases, Dashboard)')
print(f'   Phase 2 Modules: 4 (Deadlines, Documents, Billing, Activities)')
