import requests
import os

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

# Sample image URLs (replace these with actual image URLs)
image_urls = {
    'jlf.jpg': 'https://example.com/jlf.jpg',
    'heritage.jpg': 'https://example.com/heritage.jpg',
    'tech.jpg': 'https://example.com/tech.jpg',
    'diwali.jpg': 'https://example.com/diwali.jpg',
    'marathon.jpg': 'https://example.com/marathon.jpg',
    'art.jpg': 'https://example.com/art.jpg'
}

# Create directory if it doesn't exist
os.makedirs('static/images/events', exist_ok=True)

# Download images
for filename, url in image_urls.items():
    filepath = os.path.join('static/images/events', filename)
    download_image(url, filepath) 