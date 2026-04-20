content = open('bff-bookflow/main.py', 'r', encoding='utf-8').read()

new_imports = """from app.routers.normalization_router import router as normalization_router
from app.routers.pricing_router import router as pricing_router
from app.routers.audit_router import router as audit_router
from app.routers.integration_router import router as integration_router
from app.routers.system_router import router as system_router
"""

new_includes = """app.include_router(normalization_router)
app.include_router(pricing_router)
app.include_router(audit_router)
app.include_router(integration_router)
app.include_router(system_router)
"""

# Add imports after existing imports
content = content.replace(
    'from app.routers.config_router import router as config_router',
    'from app.routers.config_router import router as config_router\n' + new_imports
)

# Add includes after existing includes
content = content.replace(
    'app.include_router(config_router)',
    'app.include_router(config_router)\n' + new_includes
)

with open('bff-bookflow/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('main.py updated')
