content = """server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
"""
with open("frontend-bookflow/nginx.conf", "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print("Done")
