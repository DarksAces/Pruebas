import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import hashlib
from PIL import Image
import io

def download_images_from_url(url, category, limit=50):
    # Validar categoría
    valid_categories = [
        'paintings', 'sculptures', 'drawings', 'graffiti', 'architecture',
        'mosaics', 'ceramics', 'textiles', 'photography', 'frescoes', 'others',
        'concept_art', 'ukiyo_e', 'pixel_art', 'scientific_illustration',
        'cyberpunk', 'steampunk', 'low_poly',
        'watercolor', 'oil_painting', '3d_render', 'vaporwave', 'fractal_art',
        'african_art', 'islamic_art', 'tattoo_art', 'origami', 'stained_glass',
        'comics_manga', 'fashion', 'textures', 'vehicles', 'non_art', 'video_art'
    ]
    if category not in valid_categories:
        print(f"Error: Categoría no válida. Usa una de: {', '.join(valid_categories)}")
        return

    # Directorios de destino (80% train, 20% validation)
    train_dir = os.path.join('dataset', 'train', category)
    val_dir = os.path.join('dataset', 'validation', category)

    # Crear directorios si no existen
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

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
            
            # Filtrar por extensión
            if not img_url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue

            # Filtros ANTI-RUIDO (Nombre del archivo/URL)
            forbidden_terms = ['logo', 'icon', 'button', 'user', 'avatar', 'profile', 'symbol', 'sprite', 'pixel', 'search', 'menu', 'footer', 'header', 'nav']
            if any(term in img_url.lower() for term in forbidden_terms):
                continue

            try:
                img_data = requests.get(img_url, headers=headers, timeout=5).content
                
                if len(img_data) < 15360: # 15KB min
                    continue
                
                # --- ANÁLISIS DE IMAGEN CON PILLOW (Dimensiones y Ratio) ---
                try:
                    image_obj = Image.open(io.BytesIO(img_data))
                    width, height = image_obj.size
                    
                    # 1. Filtro de Dimensiones Mínimas (Pixel)
                    if width < 200 or height < 200:
                        continue
                        
                    # 2. Filtro de Aspect Ratio (Evitar banners alargados)
                    ratio = width / height
                    if ratio > 2.5 or ratio < 0.4: # Muy ancho o muy alto
                        continue
                        
                    # Conversión a RGB para asegurar compatibilidad (quita transparencia/paletas raras)
                    if image_obj.mode in ('RGBA', 'P'):
                         image_obj = image_obj.convert('RGB')
                         
                except Exception as e:
                    # Si PIL falla al abrir (no es imagen válida), descartar
                    continue
                    
                # Generar hash
                img_hash = hashlib.md5(img_data).hexdigest()
                if img_hash in img_hashes:
                    continue
                img_hashes.add(img_hash)
                
                # Decidir destino (80/20)
                if count % 5 == 0:
                    save_dir = val_dir
                else:
                    save_dir = train_dir
                
                # Guardar siempre como JPG para estandarizar
                filename = f"{category}_{img_hash}.jpg"
                filepath = os.path.join(save_dir, filename)
                
                if os.path.exists(filepath):
                    count += 1
                    continue

                # Guardamos usando PIL para asegurar el formato correcto
                image_obj.save(filepath, "JPEG", quality=90)
                # with open(filepath, 'wb') as f: f.write(img_data) # OLD WAY

                    
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
