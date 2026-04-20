content = open('src/services/apiClient.ts', 'r', encoding='utf-8').read()
content = content.replace('config.headers.Authorization = Bearer', 'config.headers.Authorization = Bearer ')
open('src/services/apiClient.ts', 'w', encoding='utf-8').write(content)
print('Fixed')
