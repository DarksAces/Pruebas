import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
import random

# Carpeta destino
OUTPUT_FOLDER = "firebase_downloads"

# URLs variadas para probar el modelo (distintas a las de entrenamiento idealmente, o mezclas)
TEST_URLS = [
    "https://es.wikipedia.org/wiki/Museo_del_Prado",
    "https://es.wikipedia.org/wiki/Museo_del_Louvre",
    "https://es.wikipedia.org/wiki/Arte_urbano",
    "https://es.wikipedia.org/wiki/Arquitectura_moderna",
    "https://es.wikipedia.org/wiki/Escultura_contemporánea",
    "https://es.wikipedia.org/wiki/Mosaico",
    "https://es.wikipedia.org/wiki/Arte_textil"
]

def download_test_images(limit_per_url=15):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Carpeta creada: {OUTPUT_FOLDER}")

    print(f"--- DESCARGANDO IMÁGENES DE PRUEBA EN '{OUTPUT_FOLDER}' ---")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    total_downloaded = 0

    for url in TEST_URLS:
        print(f"\nProcesando: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            
            count = 0
            for img in images:
                if count >= limit_per_url:
                    break
                
                img_url = img.get('src') or img.get('data-src')
                if not img_url:
                    continue
                    
                img_url = urljoin(url, img_url)
                
                if img_url.lower().endswith(('.svg', '.gif', 'logo.png', 'icon.png')):
                    continue

                try:
                    img_data = requests.get(img_url, headers=headers, timeout=5).content
                    if len(img_data) < 10000: # Ignorar muy pequeñas (<10KB) para test
                        continue
                        
                    # Hash para nombre único
                    img_hash = hashlib.md5(img_data).hexdigest()
                    ext = os.path.splitext(urlparse(img_url).path)[1]
                    if not ext or len(ext) > 5: ext = '.jpg'
                    
                    filename = f"test_{img_hash}{ext}"
                    filepath = os.path.join(OUTPUT_FOLDER, filename)
                    
                    if not os.path.exists(filepath):
                        with open(filepath, 'wb') as f:
                            f.write(img_data)
                        print(f"  [+] Descargada: {filename}")
                        count += 1
                        total_downloaded += 1
                    else:
                        print(f"  [.] Saltada (ya existe): {filename}")
                        
                except Exception:
                    continue

        except Exception as e:
            print(f"Error accediendo a {url}: {e}")

    print(f"\n✅ ¡LISTO! Se han descargado {total_downloaded} imágenes nuevas en '{OUTPUT_FOLDER}'.")
    print("Ahora puedes probar el modelo con:")
    print(f"python predict_folder.py \"{OUTPUT_FOLDER}\"")

if __name__ == "__main__":
    download_test_images()
