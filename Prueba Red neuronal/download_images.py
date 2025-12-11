import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import hashlib

def download_images_from_url(url, category, limit=50):
    # Validar categoría
    valid_categories = ['monuments', 'artworks', 'others']
    if category not in valid_categories:
        print(f"Error: Categoría no válida. Usa una de: {', '.join(valid_categories)}")
        return

    # Directorios de destino (80% train, 20% validation)
    train_dir = os.path.join('dataset', 'train', category)
    val_dir = os.path.join('dataset', 'validation', category)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"Conectando a {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        
        print(f"Encontradas {len(images)} etiquetas de imagen.")
        
        count = 0
        img_hashes = set() # Para evitar duplicados idénticos

        for img in images:
            if count >= limit:
                break
                
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue
                
            # Convertir URL relativa a absoluta
            img_url = urljoin(url, img_url)
            
            # Filtrar iconos pequeños o imágenes irrelevantes por extensión
            if img_url.lower().endswith(('.svg', '.gif')):
                continue

            try:
                img_data = requests.get(img_url, headers=headers, timeout=5).content
                
                # Filtrar por tamaño (bytes) - ignorar imágenes muy pequeñas (< 5KB)
                if len(img_data) < 5120: 
                    continue
                    
                # Generar hash para nombre único y evitar duplicados
                img_hash = hashlib.md5(img_data).hexdigest()
                if img_hash in img_hashes:
                    continue
                img_hashes.add(img_hash)
                
                # Decidir destino (80% train, 20% validation)
                # Usamos un contador simple: cada 5ta imagen va a validación
                if count % 5 == 0:
                    save_dir = val_dir
                    split_name = "validation"
                else:
                    save_dir = train_dir
                    split_name = "train"
                
                ext = os.path.splitext(urlparse(img_url).path)[1]
                if not ext or len(ext) > 5:
                    ext = '.jpg' # Default extension
                    
                filename = f"{category}_{img_hash}{ext}"
                filepath = os.path.join(save_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                    
                print(f"[{count+1}/{limit}] Guardada en {split_name}: {filename}")
                count += 1
                
            except Exception as e:
                # print(f"Error descargando imagen: {e}")
                continue
                
        print(f"\nDescarga completada. {count} imágenes guardadas para la categoría '{category}'.")
        
    except Exception as e:
        print(f"Error accediendo a la URL: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python download_images.py <URL> <CATEGORIA> [LIMITE]")
        print("Categorías: monuments, artworks, others")
        print("Ejemplo: python download_images.py \"https://es.wikipedia.org/wiki/Mona_Lisa\" artworks")
    else:
        url = sys.argv[1]
        category = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        download_images_from_url(url, category, limit)
