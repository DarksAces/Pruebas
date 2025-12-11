import os
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Carpeta de destino
TEST_FOLDER = "mis_pruebas"

# URLs variadas para tener un buen mix
URLS = [
    # Arte
    "https://es.wikipedia.org/wiki/Arte_abstracto",
    "https://es.wikipedia.org/wiki/Pop_art",
    "https://es.wikipedia.org/wiki/Escultura",
    "https://es.wikipedia.org/wiki/Vincent_van_Gogh",
    
    # Monumentos
    "https://es.wikipedia.org/wiki/Torre_Eiffel",
    "https://es.wikipedia.org/wiki/Coliseo",
    "https://es.wikipedia.org/wiki/Taj_Mahal",
    "https://es.wikipedia.org/wiki/Estatua_de_la_Libertad",
    
    # Otros
    "https://es.wikipedia.org/wiki/Gato",
    "https://es.wikipedia.org/wiki/Automóvil",
    "https://es.wikipedia.org/wiki/Bosque",
    "https://es.wikipedia.org/wiki/Teclado_(informática)"
]

def download_test_images():
    if not os.path.exists(TEST_FOLDER):
        os.makedirs(TEST_FOLDER)
        print(f"Carpeta '{TEST_FOLDER}' creada.")

    print(f"Buscando imágenes para '{TEST_FOLDER}'...")
    
    image_count = 1
    # Intentar encontrar el último número usado (por si ya hay fotos)
    existing_files = os.listdir(TEST_FOLDER)
    if existing_files:
        print("Ya existen archivos, buscaré el siguiente número...")
        for f in existing_files:
            name, _ = os.path.splitext(f)
            if name.isdigit():
                num = int(name)
                if num >= image_count:
                    image_count = num + 1
    
    print(f"Empezando por la imagen número: {image_count}")
    
    total_downloaded = 0
    target_per_url = 5 # Descargar 5 de cada URL
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in URLS:
        try:
            print(f"Explorando: {url}")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            
            downloaded_from_url = 0
            
            for img in img_tags:
                if downloaded_from_url >= target_per_url:
                    break
                    
                img_url = img.get('src')
                if not img_url:
                    continue
                    
                img_url = urljoin(url, img_url)
                
                # Ignorar iconos pequeños
                if 'svg' in img_url or 'logo' in img_url.lower():
                    continue

                try:
                    img_data = requests.get(img_url, headers=headers, timeout=5).content
                    if len(img_data) < 10000: # Ignorar imágenes < 10KB
                        continue
                        
                    ext = os.path.splitext(urlparse(img_url).path)[1]
                    if not ext or len(ext) > 5:
                        ext = '.jpg'
                    
                    filename = f"{image_count}{ext}"
                    filepath = os.path.join(TEST_FOLDER, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                    
                    print(f"  [Guardada] {filename} (Origen: {url.split('/')[-1]})")
                    
                    image_count += 1
                    downloaded_from_url += 1
                    total_downloaded += 1
                    
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Error en {url}: {e}")

    print(f"\n¡Listo! {total_downloaded} imágenes nuevas en '{TEST_FOLDER}'.")

if __name__ == "__main__":
    download_test_images()
