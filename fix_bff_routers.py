import os
import shutil

# Lista de routers que deben estar en el BFF
routers_needed = [
    'normalization_router.py',
    'pricing_router.py', 
    'audit_router.py',
    'integration_router.py',
    'system_router.py',
]

# Verificar cuales existen
bff_routers = 'bff-bookflow/app/routers'
for router in routers_needed:
    path = os.path.join(bff_routers, router)
    if os.path.exists(path):
        print(f'EXISTS: {router}')
    else:
        print(f'MISSING: {router}')
