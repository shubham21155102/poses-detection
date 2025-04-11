import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

def fetch_filtered_images(page_url, download_folder):
    os.makedirs(download_folder, exist_ok=True)

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    count = 1
    for img in img_tags:
        img_url = img.get('src') or img.get('data-src')
        if not img_url:
            continue

        full_url = urljoin(page_url, img_url)

        try:
            # Get image content
            img_response = requests.get(full_url, timeout=10)
            img_bytes = BytesIO(img_response.content)
            img_obj = Image.open(img_bytes)

            # Filter by aspect ratio
            width, height = img_obj.size
            if width > 4 * height:
                print(f"Skipped (too wide): {full_url}")
                continue

            # Save the image
            img_path = os.path.join(download_folder, f"{count}.jpg")
            img_obj.save(img_path)
            print(f"Saved: {full_url}")
            count += 1

        except Exception as e:
            print(f"Error with {full_url}: {e}")

# search_term = "person-balancing"
# url = f"https://unsplash.com/s/collections/{search_term}"
# download_folder = "dataset/test/balancing"
search_terms=["person-balancing","person-falling","person-hugging","person-lookingup","person-sitting","person-standing"]
download_folders=["balancing","falling","hugging","lookingup","sitting","standing"]
for i in range(6):
    search_term=search_terms[i]
    download_folder=f"dataset/test/{download_folders[i]}"
    url= f"https://unsplash.com/s/collections/{search_term}"
    fetch_filtered_images(url, download_folder)
