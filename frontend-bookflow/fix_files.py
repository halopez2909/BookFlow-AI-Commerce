content = open('src/components/inventory/FileUploader.tsx', 'r', encoding='utf-8').read()
content = content.replace('showError(File size exceeds MB limit.)', 'showError("File size exceeds " + String(maxSizeMB) + "MB limit.")')
open('src/components/inventory/FileUploader.tsx', 'w', encoding='utf-8').write(content)
print('Fixed FileUploader')
