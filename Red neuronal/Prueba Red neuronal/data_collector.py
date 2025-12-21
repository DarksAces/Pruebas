import os
import shutil
from PIL import Image
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

class BulkDataCollector:
    def __init__(self, output_dir="dataset"):
        self.output_dir = output_dir
        # MEGA CONFIGURATION: Massively expanded search terms
        self.categories_config = {
            "paintings": [
                # Eras & Styles
                "oil painting masterpiece", "classic art painting", "abstract painting", 
                "renaissance painting", "baroque painting", "impressionist art", 
                "cubism painting", "surrealism art", "pop art painting", "watercolor art",
                "acrylic painting", "digital art painting", "fresco painting", "tempera painting",
                # Famous Artists (style)
                "van gogh style painting", "picasso style art", "monet style painting",
                "da vinci style sketch", "rembrandt style", "dali surrealism",
                # Subjects
                "portrait painting", "landscape oil painting", "still life painting",
                "historical painting", "mythological painting"
            ],
            "plasticine": [
                # General
                "plasticine art", "claymation characters", "modeling clay animals", 
                "plasticine figures", "play doh art", "clay art sculpture",
                # Specifics
                "stop motion clay characters", "polymer clay charms", "plasticine food models",
                "clay world models", "aardman style clay", "plasticine landscape",
                "child clay modeling", "professional clay animation"
            ],
            "graffiti": [
                # Styles
                "street art graffiti", "colorful wall graffiti", "urban graffiti", 
                "graffiti mural", "spray can art", "tagging graffiti", "stencil art graffiti",
                # Locations/Types
                "train graffiti", "subway graffiti", "abandoned building graffiti",
                "3d graffiti art", "wildstyle graffiti", "bubble style graffiti",
                "banksy style art", "large street mural"
            ],
            "others": [
                # Nature
                "landscape photography", "nature photography forest", "mountain photography",
                "ocean waves photo", "flower macro photography", "wildlife photography",
                # Urban
                "city landscape photography", "modern architecture", "skyscraper photo",
                "busy street crowd", "traffic jam", "old building photo",
                # Objects/People
                "portrait photography people", "random objects on table", "cars on street",
                "fruits basket photo", "furniture design", "computer hardware",
                "clothing fashion photo", "kitchen utensils"
            ]
        }
        
    def setup_directories(self):
        for category in self.categories_config.keys():
            path = os.path.join(self.output_dir, category)
            os.makedirs(path, exist_ok=True)
            
    def process_and_compress_image(self, filepath):
        try:
            with Image.open(filepath) as img:
                # Convert to RGB (in case of RGBA/P palette)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too big (Max 640px)
                max_size = (640, 640)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save with compression (Quality 65 is decent but small)
                img.save(filepath, "JPEG", optimize=True, quality=65)
                return True
        except Exception as e:
            # If image is corrupt, delete it using os.remove directly
            try:
                os.remove(filepath)
            except:
                pass
            return False

    def clean_category(self, category_path):
        print(f"Cleaning and Compressing images in {category_path}...")
        files = os.listdir(category_path)
        count = 0
        for f in files:
            full_path = os.path.join(category_path, f)
            if self.process_and_compress_image(full_path):
                count += 1
        print(f"Processed {count} images in {category_path}")

    def run(self, images_per_term=500):
        total_terms = sum(len(terms) for terms in self.categories_config.values())
        print(f"Starting MEGA BULK collection.")
        print(f"Categories: {len(self.categories_config)}")
        print(f"Total Search Terms: {total_terms}")
        print(f"Target per term: {images_per_term} x 3 Crawlers = {images_per_term*3}")
        print(f"POTENTIAL TOTAL: {total_terms * images_per_term * 3} images")
        
        self.setup_directories()
        
        for category, search_terms in self.categories_config.items():
            print(f"\n=== Processing Category: {category} ({len(search_terms)} terms) ===")
            cat_dir = os.path.join(self.output_dir, category)
            
            for term in search_terms:
                print(f"\n>>> Searching for: '{term}'")
                
                # Using 10 Threads for faster download
                # 1. Bing (Usually fast/reliable)
                try:
                    bing = BingImageCrawler(downloader_threads=10, storage={'root_dir': cat_dir})
                    bing.crawl(keyword=term, max_num=images_per_term)
                except Exception as e:
                    print(f"Bing crawler error: {e}")

                # 2. Baidu (Good for diversity)
                try:
                    baidu = BaiduImageCrawler(downloader_threads=10, storage={'root_dir': cat_dir})
                    baidu.crawl(keyword=term, max_num=images_per_term)
                except Exception as e:
                    print(f"Baidu crawler error: {e}")

                # 3. Google (Strict, but high quality)
                try:
                    google = GoogleImageCrawler(downloader_threads=10, storage={'root_dir': cat_dir})
                    google.crawl(keyword=term, max_num=images_per_term)
                except Exception as e:
                    print(f"Google crawler error: {e}")
            
            # Post-process category to save space
            self.clean_category(cat_dir)

if __name__ == "__main__":
    # With 15-20 terms per category, 3 crawlers, and 300 images each...
    # That is ~18,000 images PER CATEGORY = ~72,000 Total.
    # Adjust 'images_per_term' to scale up/down.
    collector = BulkDataCollector()
    collector.run(images_per_term=200)
