import urllib.request
from PIL import Image

url = "https://danagedumigrate.in/wp-content/uploads/2023/11/country_testimonial_2020110903452664.jpg"
urllib.request.urlretrieve(url, "test_img.jpg")

img = Image.open("test_img.jpg")
print(f"Image format: {img.format}")
print(f"Image size: {img.size}")
print(f"Image mode: {img.mode}")
