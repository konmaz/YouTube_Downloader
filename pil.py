
url = 'https://img.youtube.com/vi/UK8HH3_q4yI/maxresdefault.jpg'

import requests
from PIL import Image

response = requests.get(url, stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)
image.show()
requests image()
