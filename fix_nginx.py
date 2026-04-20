content = """server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files \ \/ /index.html;
    }
}
"""
with open('frontend-bookflow/nginx.conf', 'w', encoding='utf-8') as f:
    f.write(content)
print('nginx.conf fixed')
