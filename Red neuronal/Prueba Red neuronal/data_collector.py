import os
import shutil
import time
from PIL import Image
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler

class BulkDataCollector:
    def __init__(self, output_dir="dataset"):
        self.output_dir = output_dir
        # MEGA EXPANSION V2: 60,000+ Image Target
        self.categories_config = {
            "paintings": [
                # Movements
                "Italian Renaissance painting", "Northern Renaissance art", "Mannerism painting", 
                "Baroque art painting", "Rococo style painting", "Neoclassicism art", "Romanticism painting", 
                "Realism art painting", "Impressionism painting", "Post-Impressionism art", 
                "Fauvism painting", "Expressionism art", "Cubism painting", "Futurism art", 
                "Dadaism art", "Surrealism painting", "Abstract Expressionism", "Pop Art painting", 
                "Minimalism art", "Contemporary art painting", "Art Nouveau painting", "Art Deco painting",
                # Artists (Styles)
                "Leonardo da Vinci style", "Michelangelo painting", "Raphael artist", "Caravaggio style", 
                "Rembrandt painting", "Vermeer painting", "Francisco Goya art", "J.M.W. Turner painting", 
                "Edouard Manet painting", "Claude Monet painting", "Pierre-Auguste Renoir", "Edgar Degas art", 
                "Paul Cezanne painting", "Vincent Van Gogh painting", "Paul Gauguin art", "Gustav Klimt art", 
                "Edvard Munch painting", "Henri Matisse art", "Pablo Picasso painting", "Salvador Dali art", 
                "Jackson Pollock art", "Andy Warhol art", "Jean-Michel Basquiat", "Frida Kahlo painting",
                # Subjects & Techniques
                "oil portrait painting", "landscape oil painting", "seascape watercolor", "cityscape painting", 
                "still life flower painting", "still life fruit painting", "historical scene painting", 
                "mythological scene painting", "gouache painting", "ink wash painting", "pastel drawing art", 
                "encaustic painting", "tempera painting", "fresco wall painting"
            ],
            "plasticine": [
                # General & Characters
                "plasticine art", "plasticine figures", "plasticine animals", "plasticine people", 
                "plasticine monsters", "plasticine food", "plasticine flowers", "plasticine trees", 
                "plasticine cars", "plasticine house", "claymation characters", "stop motion clay art",
                # Specific Styles & Materials
                "Aardman style clay", "Wallace and Gromit style", "Sean the Sheep style", 
                "Gumby style clay", "polymer clay charms", "polymer clay sculpture", 
                "fimo clay art", "sculpey clay figures", "play-doh creations", "children play-doh art",
                "modeling clay diorama", "clay animation set"
            ],
            "graffiti": [
                # Styles
                "tagging graffiti", "throw-up graffiti", "blockbuster graffiti", "wildstyle graffiti", 
                "stencil art graffiti", "sticker bombing street art", "3d graffiti art", 
                "bubble letters graffiti", "calligraffiti", "wheatpaste art",
                # Locations & Themes
                "train graffiti whole car", "subway graffiti art", "large wall mural graffiti", 
                "street art portrait", "abandoned factory graffiti", "bridge graffiti", 
                "skatepark graffiti", "urban street art", "political street art", 
                "psychedelic graffiti", "colorful graffiti background"
            ],
            "others": [
                # Photography Types
                "portrait photography", "landscape photography", "architectural photography", 
                "wildlife photography", "macro photography flowers", "macro photography insects", 
                "aerial photography nature", "aerial photography city", "street photography black and white", 
                "fashion photography editorial", "sports photography action", "night photography city", 
                "long exposure photography light trails", "underwater photography coral", 
                "food photography professional", "product photography", "travel photography", 
                "pet photography dogs", "pet photography cats", "minimalist photography",
                # Scenes
                "busy market street", "crowded subway station", "highway traffic jam", 
                "forest path hiking", "mountain peak snow", "desert sand dunes", 
                "ocean waves storm", "tropical beach sunset", "old library interior", 
                "modern office interior", "industrial warehouse interior"
            ]
        }
        
    def setup_directories(self):
        for category in self.categories_config.keys():
            path = os.path.join(self.output_dir, category)
            os.makedirs(path, exist_ok=True)
            
    def process_and_compress_image(self, filepath):
        try:
            with Image.open(filepath) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                max_size = (800, 800) # Increased resolution slightly
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                img.save(filepath, "JPEG", optimize=True, quality=70)
                return True
        except Exception:
            try:
                os.remove(filepath)
            except:
                pass
            return False

    def clean_category(self, category_path):
        print(f"   > Cleaning {category_path}...")
        try:
            files = os.listdir(category_path)
            count = 0
            for f in files:
                full_path = os.path.join(category_path, f)
                if os.path.isfile(full_path):
                    if self.process_and_compress_image(full_path):
                        count += 1
            print(f"   > Validated {count} images in {category_path}")
        except Exception as e:
            print(f"   > Error cleaning {category_path}: {e}")

    def run(self, images_per_term=800):
        total_terms = sum(len(terms) for terms in self.categories_config.values())
        print(f"=== MEGA DATA COLLECTOR STARTED ===")
        print(f"Target: {images_per_term} images per term per crawler")
        print(f"Total Terms: {total_terms}")
        print(f"Theoretical Max: {total_terms * images_per_term * 3}")
        
        self.setup_directories()
        
        for category, search_terms in self.categories_config.items():
            print(f"\n--- Category: {category.upper()} ---")
            cat_dir = os.path.join(self.output_dir, category)
            
            for term in search_terms:
                print(f"Search: '{term}'")
                
                # Bing
                try:
                    bing = BingImageCrawler(downloader_threads=10, storage={'root_dir': cat_dir}, log_level='ERROR')
                    bing.crawl(keyword=term, max_num=images_per_term)
                except: pass

                # Baidu
                try:
                    baidu = BaiduImageCrawler(downloader_threads=10, storage={'root_dir': cat_dir}, log_level='ERROR')
                    baidu.crawl(keyword=term, max_num=images_per_term)
                except: pass

                # Google (Try/Except because it fails often)
                try:
                    google = GoogleImageCrawler(downloader_threads=10, storage={'root_dir': cat_dir}, log_level='ERROR')
                    google.crawl(keyword=term, max_num=images_per_term)
                except: pass
            
            # Clean immediately after category is done to free up temp handles/memory
            self.clean_category(cat_dir)

if __name__ == "__main__":
    collector = BulkDataCollector()
    # Increased to 800 to ensure we hit the 60k target even with duplicates/failures
    collector.run(images_per_term=800)
