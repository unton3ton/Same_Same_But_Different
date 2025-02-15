import requests

url = 'http://127.0.0.1:5005/neurogenerate-0_neuro.png'

response = requests.get(url)

with open('output-0.0.1.png', 'wb') as f:
	f.write(response.content)

# $ python -m http.server
# Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
# 127.0.0.1 - - [12/Feb/2025 09:39:24] "GET /output-0.0.png HTTP/1.1" 200 -
