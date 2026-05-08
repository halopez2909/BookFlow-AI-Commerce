# Add pricing and external routers to BFF
content = open('bff-bookflow/app/routers/pricing_router.py', 'r', encoding='utf-8').read()
print('pricing_router exists:', len(content) > 0)

content = open('bff-bookflow/main.py', 'r', encoding='utf-8').read()
print('Current BFF routers:')
for line in content.split('\n'):
    if 'router' in line.lower():
        print(' ', line.strip())
