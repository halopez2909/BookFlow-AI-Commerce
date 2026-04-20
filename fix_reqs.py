content = open('normalization-service/requirements.txt', 'r', encoding='utf-8').read()
content = content.replace('stdnum==1.20', 'python-stdnum==1.19')
open('normalization-service/requirements.txt', 'w', encoding='utf-8').write(content)
print('Fixed requirements.txt')
