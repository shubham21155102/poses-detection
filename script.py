import requests
import os
import spacy
import time
from PIL import Image
from io import BytesIO

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

search_terms = ["person-balancing", "person-falling", "person-hugging",
                "person-lookingup", "person-sitting", "person-standing"]
download_folders = ["balancing", "falling", "hugging",
                    "lookingup", "sitting", "standing"]

def download_image(url, download_folder, count):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Verify and process image
        img = Image.open(BytesIO(response.content))
        img.verify()
        img = Image.open(BytesIO(response.content))  # Reopen after verification
        
        # Save as JPEG
        img_path = os.path.join(download_folder, f"{count}.jpg")
        img.convert('RGB').save(img_path, 'JPEG')
        print(f"Downloaded: {img_path}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def contains_target_lemma(text, target_lemma):
    """Check if text contains any form of the target lemma using spaCy"""
    doc = nlp(text.lower())
    for token in doc:
        if token.lemma_ == target_lemma:
            return True
    return False

def process_search_term(search_term, download_folder):
    # Extract action word and get its lemma
    action_word = search_term.split("-")[1]
    target_lemma = nlp(action_word)[0].lemma_
    
    count = 1
    total_downloaded = 0
    
    # Iterate through 10 pages
    for page in range(1, 11):
        print(f"Processing {search_term} - Page {page}")
        
        # Create API query parameters
        params = {
            "page": page,
            "per_page": 20,
            "query": search_term.replace("-", " ")
        }
        
        try:
            # Add delay to avoid rate limiting
            time.sleep(1)
            response = requests.get("https://unsplash.com/napi/search/photos", params=params)
            response.raise_for_status()
            
            results = response.json().get('results', [])
            
            for photo in results:
                alt_text = photo.get('alt_description', '')
                if not alt_text:
                    continue
                    
                if contains_target_lemma(alt_text, target_lemma):
                    image_url = photo['urls']['regular']
                    if download_image(image_url, download_folder, count):
                        count += 1
                        total_downloaded += 1
                        
        except Exception as e:
            print(f"Error processing page {page}: {e}")
            continue
            
    print(f"Total downloaded for {search_term}: {total_downloaded}")

# Create directories and process all search terms
for i in range(len(search_terms)):
    term = search_terms[i]
    folder = os.path.join("dataset/test", download_folders[i])
    os.makedirs(folder, exist_ok=True)
    
    print(f"\nStarting processing for: {term}")
    print(f"Target lemma: {nlp(term.split('-')[1])[0].lemma_}")
    process_search_term(term, folder)

print("\nImage download completed!")