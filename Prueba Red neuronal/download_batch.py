from download_images import download_images_from_url

# Diccionario de Categoría -> Lista de URLs
# ¡AMPLIACIÓN CULTURAL MASSIVE UPDATE V10.0 - DEEP SEARCH EDITION!
sites = {
    # 1. PINTURAS (Paintings)
    'paintings': [
        # Movimientos Artísticos Principales
        "https://es.wikipedia.org/wiki/Pintura",
        "https://es.wikipedia.org/wiki/Impresionismo",
        "https://es.wikipedia.org/wiki/Postimpresionismo",
        "https://es.wikipedia.org/wiki/Expresionismo",
        "https://es.wikipedia.org/wiki/Cubismo",
        "https://es.wikipedia.org/wiki/Surrealismo",
        "https://es.wikipedia.org/wiki/Arte_abstracto",
        "https://es.wikipedia.org/wiki/Barroco",
        "https://es.wikipedia.org/wiki/Rococó",
        "https://es.wikipedia.org/wiki/Neoclasicismo",
        "https://es.wikipedia.org/wiki/Romanticismo",
        "https://es.wikipedia.org/wiki/Realismo_(arte)",
        "https://es.wikipedia.org/wiki/Renacimiento",
        "https://es.wikipedia.org/wiki/Manierismo",
        "https://es.wikipedia.org/wiki/Dadaísmo",
        "https://es.wikipedia.org/wiki/Fauvismo",
        "https://es.wikipedia.org/wiki/Futurismo",
        "https://es.wikipedia.org/wiki/Pop_art",
        "https://es.wikipedia.org/wiki/Simbolismo",
        "https://es.wikipedia.org/wiki/Art_déco",
        "https://es.wikipedia.org/wiki/Art_nouveau",
        # Listas de Obras Maestras y Museos
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Leonardo_da_Vinci",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Vincent_van_Gogh",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Rembrandt",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Velázquez",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Francisco_de_Goya",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Salvador_Dalí",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Pablo_Picasso_1889-1900",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Frida_Kahlo",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Joaquín_Sorolla",
        "https://es.wikipedia.org/wiki/Anexo:Obra_de_Gustav_Klimt",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Artemisia_Gentileschi",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Caravaggio",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_El_Greco",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Paul_Cézanne",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Claude_Monet",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Pierre-Auguste_Renoir",
        "https://es.wikipedia.org/wiki/Mona_Lisa",
        "https://es.wikipedia.org/wiki/La_noche_estrellada",
        "https://es.wikipedia.org/wiki/Guernica_(cuadro)",
        "https://es.wikipedia.org/wiki/Las_meninas"
    ],

    # 2. ESCULTURAS (Sculptures)
    'sculptures': [
        "https://es.wikipedia.org/wiki/Escultura",
        "https://es.wikipedia.org/wiki/Escultura_del_Renacimiento",
        "https://es.wikipedia.org/wiki/Escultura_barroca",
        "https://es.wikipedia.org/wiki/Escultura_neoclásica",
        "https://es.wikipedia.org/wiki/Escultura_griega",
        "https://es.wikipedia.org/wiki/Escultura_romana",
        "https://es.wikipedia.org/wiki/Escultura_etrusca",
        "https://es.wikipedia.org/wiki/Escultura_gótica",
        "https://es.wikipedia.org/wiki/Escultura_románica",
        "https://es.wikipedia.org/wiki/Escultura_maya",
        "https://es.wikipedia.org/wiki/Escultura_azteca",
        # Artistas famosos
        "https://es.wikipedia.org/wiki/Gian_Lorenzo_Bernini",
        "https://es.wikipedia.org/wiki/Miguel_Ángel",
        "https://es.wikipedia.org/wiki/Auguste_Rodin",
        "https://es.wikipedia.org/wiki/Donatello",
        "https://es.wikipedia.org/wiki/Antonio_Canova",
        "https://es.wikipedia.org/wiki/Constantin_Brâncuși",
        "https://es.wikipedia.org/wiki/Alberto_Giacometti",
        "https://es.wikipedia.org/wiki/Henry_Moore",
        "https://es.wikipedia.org/wiki/Louise_Bourgeois",
        "https://es.wikipedia.org/wiki/Alexander_Calder",
        # Obras específicas
        "https://es.wikipedia.org/wiki/David_(Miguel_Ángel)",
        "https://es.wikipedia.org/wiki/La_Piedad_(Miguel_Ángel)",
        "https://es.wikipedia.org/wiki/Venus_de_Milo",
        "https://es.wikipedia.org/wiki/Victoria_de_Samotracia",
        "https://es.wikipedia.org/wiki/El_pensador",
        "https://es.wikipedia.org/wiki/Estatua_de_la_Libertad",
        "https://es.wikipedia.org/wiki/Cristo_Redentor",
        "https://es.wikipedia.org/wiki/Moái",
        "https://es.wikipedia.org/wiki/Guerreros_de_terracota",
        "https://es.wikipedia.org/wiki/Gran_Esfinge_de_Guiza"
    ],

    # 3. DIBUJOS (Drawings)
    'drawings': [
        "https://es.wikipedia.org/wiki/Dibujo",
        "https://es.wikipedia.org/wiki/Boceto",
        "https://es.wikipedia.org/wiki/Apunte",
        "https://es.wikipedia.org/wiki/Carboncillo",
        "https://es.wikipedia.org/wiki/Sanguina",
        "https://es.wikipedia.org/wiki/Pastel_(técnica)",
        "https://es.wikipedia.org/wiki/Lápiz_de_color",
        "https://es.wikipedia.org/wiki/Tinta_china",
        "https://es.wikipedia.org/wiki/Plumilla",
        "https://es.wikipedia.org/wiki/Ilustración",
        "https://es.wikipedia.org/wiki/Grabado",
        "https://es.wikipedia.org/wiki/Aguafuerte",
        "https://es.wikipedia.org/wiki/Xilografía",
        "https://es.wikipedia.org/wiki/Litografía",
        "https://es.wikipedia.org/wiki/Hombre_de_Vitruvio",
        "https://es.wikipedia.org/wiki/Dibujo_técnico",
        "https://es.wikipedia.org/wiki/Caricatura",
        "https://es.wikipedia.org/wiki/Cómic",
        "https://es.wikipedia.org/wiki/Manga",
        "https://es.wikipedia.org/wiki/Anime",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Drawing",
        "https://en.wikipedia.org/wiki/Sketch_(drawing)",
        "https://en.wikipedia.org/wiki/Figure_drawing",
        "https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
        "https://en.wikipedia.org/wiki/Michelangelo",
        "https://en.wikipedia.org/wiki/Albrecht_D%C3%BCrer"
    ],

    # 4. GRAFFITI (Graffiti)
    'graffiti': [
        "https://es.wikipedia.org/wiki/Graffiti",
        "https://es.wikipedia.org/wiki/Arte_urbano",
        "https://es.wikipedia.org/wiki/Muralismo",
        "https://es.wikipedia.org/wiki/Esténcil",
        "https://es.wikipedia.org/wiki/Banksy",
        "https://es.wikipedia.org/wiki/Jean-Michel_Basquiat",
        "https://es.wikipedia.org/wiki/Keith_Haring",
        "https://es.wikipedia.org/wiki/Shepard_Fairey",
        "https://es.wikipedia.org/wiki/Os_Gêmeos",
        "https://es.wikipedia.org/wiki/Blu_(artista)",
        "https://es.wikipedia.org/wiki/Blek_le_Rat",
        "https://es.wikipedia.org/wiki/Invader_(artista)",
        "https://es.wikipedia.org/wiki/Kaws",
        "https://es.wikipedia.org/wiki/Lady_Pink",
        "https://es.wikipedia.org/wiki/Tag_(graffiti)",
        "https://es.wikipedia.org/wiki/Hip_hop_(cultura)",
        "https://es.wikipedia.org/wiki/Sticker_art",
        "https://es.wikipedia.org/wiki/Wheatpaste",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Graffiti",
        "https://en.wikipedia.org/wiki/Street_art",
        "https://en.wikipedia.org/wiki/Banksy",
        "https://en.wikipedia.org/wiki/List_of_works_by_Banksy",
        "https://en.wikipedia.org/wiki/Stencil",
        "https://en.wikipedia.org/wiki/Wheatpaste",
        # New High-Density Sources (Categories)
        "https://en.wikipedia.org/wiki/Category:Graffiti_in_New_York_City",
        "https://en.wikipedia.org/wiki/Category:Graffiti_in_London",
        "https://en.wikipedia.org/wiki/Category:Graffiti_in_Berlin",
        "https://en.wikipedia.org/wiki/Category:Graffiti_in_Spain",
        "https://en.wikipedia.org/wiki/Category:Street_art_festivals",
        "https://en.wikipedia.org/wiki/Category:Stencil_graffiti",
        "https://en.wikipedia.org/wiki/Category:Murals_in_Northern_Ireland",
        "https://en.wikipedia.org/wiki/Category:Street_artist_stubs"
    ],

    # 5. ARQUITECTURA (Architecture)
    'architecture': [
        # Estilos Arquitectónicos
        "https://es.wikipedia.org/wiki/Arquitectura",
        "https://es.wikipedia.org/wiki/Arquitectura_del_Antiguo_Egipto",
        "https://es.wikipedia.org/wiki/Arquitectura_de_la_Antigua_Grecia",
        "https://es.wikipedia.org/wiki/Arquitectura_de_la_Antigua_Roma",
        "https://es.wikipedia.org/wiki/Arquitectura_bizantina",
        "https://es.wikipedia.org/wiki/Arquitectura_islámica",
        "https://es.wikipedia.org/wiki/Arquitectura_románica",
        "https://es.wikipedia.org/wiki/Arquitectura_gótica",
        "https://es.wikipedia.org/wiki/Arquitectura_del_Renacimiento",
        "https://es.wikipedia.org/wiki/Arquitectura_barroca",
        "https://es.wikipedia.org/wiki/Arquitectura_neoclásica",
        "https://es.wikipedia.org/wiki/Arquitectura_moderna",
        "https://es.wikipedia.org/wiki/Arquitectura_posmoderna",
        "https://es.wikipedia.org/wiki/Arquitectura_brutalista",
        "https://es.wikipedia.org/wiki/Art_Deco_architecture", # A veces la URL es en ingles si no hay buena en es
        "https://es.wikipedia.org/wiki/Arquitectura_high-tech",
        "https://es.wikipedia.org/wiki/Deconstructivismo",
        # Tipos de Edificios
        "https://es.wikipedia.org/wiki/Rascacielos",
        "https://es.wikipedia.org/wiki/Catedral",
        "https://es.wikipedia.org/wiki/Castillo",
        "https://es.wikipedia.org/wiki/Palacio",
        "https://es.wikipedia.org/wiki/Mezquita",
        "https://es.wikipedia.org/wiki/Templo_hinduista",
        "https://es.wikipedia.org/wiki/Pagoda",
        # Edificios Famosos
        "https://es.wikipedia.org/wiki/Catedral_de_Notre_Dame",
        "https://es.wikipedia.org/wiki/Coliseo",
        "https://es.wikipedia.org/wiki/Partenón",
        "https://es.wikipedia.org/wiki/Taj_Mahal",
        "https://es.wikipedia.org/wiki/Torre_Eiffel",
        "https://es.wikipedia.org/wiki/Ópera_de_Sídney",
        "https://es.wikipedia.org/wiki/Sagrada_Familia",
        "https://es.wikipedia.org/wiki/Empire_State_Building",
        "https://es.wikipedia.org/wiki/Burj_Khalifa"
    ],

    # 6. MOSAICOS (Mosaics)
    'mosaics': [
        "https://es.wikipedia.org/wiki/Mosaico",
        "https://es.wikipedia.org/wiki/Mosaico_romano",
        "https://es.wikipedia.org/wiki/Mosaico_bizantino",
        "https://es.wikipedia.org/wiki/Mosaico_helenístico",
        "https://es.wikipedia.org/wiki/Tesela",
        "https://es.wikipedia.org/wiki/Iglesia_de_San_Vitale_en_Rávena",
        "https://es.wikipedia.org/wiki/Basílica_de_San_Marcos",
        "https://es.wikipedia.org/wiki/Park_Güell",
        "https://es.wikipedia.org/wiki/Trencadís",
        "https://es.wikipedia.org/wiki/Gaudí",
        "https://es.wikipedia.org/wiki/Villa_romana_del_Casale",
        "https://es.wikipedia.org/wiki/Mosaico_de_Issos",
        "https://es.wikipedia.org/wiki/Mosaicos_de_la_catedral_de_Monreale",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Mosaic",
        "https://en.wikipedia.org/wiki/Roman_mosaic",
        "https://en.wikipedia.org/wiki/Byzantine_mosaics",
        "https://en.wikipedia.org/wiki/Ravenna",
        "https://en.wikipedia.org/wiki/Hagia_Sophia",
        # New High-Density Sources (Categories)
        "https://en.wikipedia.org/wiki/Category:Roman_mosaics_in_the_United_Kingdom",
        "https://en.wikipedia.org/wiki/Category:Byzantine_mosaics",
        "https://en.wikipedia.org/wiki/Category:Mosaics_in_Italy",
        "https://en.wikipedia.org/wiki/Category:Mosaics_in_Spain",
        "https://en.wikipedia.org/wiki/Category:Mosaics_in_Delos",
        "https://en.wikipedia.org/wiki/Category:Mosaics_in_Cyprus",
        "https://en.wikipedia.org/wiki/Category:Mosaics_in_Turkey",
        "https://en.wikipedia.org/wiki/Category:Mosaics_of_Jesus"
    ],

    # 7. CERÁMICA (Ceramics)
    'ceramics': [
        "https://es.wikipedia.org/wiki/Cerámica",
        "https://es.wikipedia.org/wiki/Alfarería",
        "https://es.wikipedia.org/wiki/Porcelana",
        "https://es.wikipedia.org/wiki/Cerámica_griega",
        "https://es.wikipedia.org/wiki/Cerámica_de_figuras_negras",
        "https://es.wikipedia.org/wiki/Cerámica_de_figuras_rojas",
        "https://es.wikipedia.org/wiki/Cerámica_china",
        "https://es.wikipedia.org/wiki/Cerámica_Ming",
        "https://es.wikipedia.org/wiki/Cerámica_japonesa",
        "https://es.wikipedia.org/wiki/Loza",
        "https://es.wikipedia.org/wiki/Azulejo",
        "https://es.wikipedia.org/wiki/Mayólica",
        "https://es.wikipedia.org/wiki/Talavera_de_la_Reina",
        "https://es.wikipedia.org/wiki/Terracota",
        "https://es.wikipedia.org/wiki/Guerreros_de_terracota",
        "https://es.wikipedia.org/wiki/Jarrón",
        "https://es.wikipedia.org/wiki/Ánfora",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Ceramic_art",
        "https://en.wikipedia.org/wiki/Pottery",
        "https://en.wikipedia.org/wiki/Porcelain",
        "https://en.wikipedia.org/wiki/Chinese_ceramics",
        "https://en.wikipedia.org/wiki/Greek_pottery",
        "https://en.wikipedia.org/wiki/Islamic_pottery",
        "https://en.wikipedia.org/wiki/Delftware",
        # New High-Density Sources (Categories)
        "https://en.wikipedia.org/wiki/Category:Ancient_Greek_pottery",
        "https://en.wikipedia.org/wiki/Category:Maiolica",
        "https://en.wikipedia.org/wiki/Category:Islamic_pottery",
        "https://en.wikipedia.org/wiki/Category:Porcelain",
        "https://en.wikipedia.org/wiki/Category:Studio_pottery",
        "https://en.wikipedia.org/wiki/Category:Ceramic_art_by_country",
        "https://en.wikipedia.org/wiki/Category:British_pottery",
        "https://en.wikipedia.org/wiki/Category:Japanese_pottery"
    ],

    # 8. TEXTILES (Textiles)
    'textiles': [
        "https://es.wikipedia.org/wiki/Arte_textil",
        "https://es.wikipedia.org/wiki/Tejido_(textil)",
        "https://es.wikipedia.org/wiki/Tapiz",
        "https://es.wikipedia.org/wiki/Alfombra",
        "https://es.wikipedia.org/wiki/Alfombra_persa",
        "https://es.wikipedia.org/wiki/Alfombra_oriental",
        "https://es.wikipedia.org/wiki/Bordado",
        "https://es.wikipedia.org/wiki/Encaje",
        "https://es.wikipedia.org/wiki/Seda",
        "https://es.wikipedia.org/wiki/Batik",
        "https://es.wikipedia.org/wiki/Patchwork",
        "https://es.wikipedia.org/wiki/Quilt",
        "https://es.wikipedia.org/wiki/Macramé",
        "https://es.wikipedia.org/wiki/Telar",
        "https://es.wikipedia.org/wiki/Diseño_de_modas",
        "https://es.wikipedia.org/wiki/Vestimenta_indígena",
        "https://es.wikipedia.org/wiki/Traje_típico",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Textile",
        "https://en.wikipedia.org/wiki/List_of_fabrics",
        "https://en.wikipedia.org/wiki/Weaving",
        "https://en.wikipedia.org/wiki/Knitting",
        "https://en.wikipedia.org/wiki/Embroidery",
        "https://en.wikipedia.org/wiki/Tapestry",
        "https://en.wikipedia.org/wiki/Carpet",
        "https://en.wikipedia.org/wiki/Silk",
        # New High-Density Sources (Categories)
        "https://en.wikipedia.org/wiki/Category:Textile_arts",
        "https://en.wikipedia.org/wiki/Category:Rugs_and_carpets",
        "https://en.wikipedia.org/wiki/Category:Tapestries",
        "https://en.wikipedia.org/wiki/Category:Embroidery",
        "https://en.wikipedia.org/wiki/Category:Quilting",
        "https://en.wikipedia.org/wiki/Category:Indigenous_textile_art_of_the_Americas",
        "https://en.wikipedia.org/wiki/Category:Textile_arts_of_India",
        "https://en.wikipedia.org/wiki/Category:Coptic_textiles"
    ],

    # 9. FOTOGRAFÍA (Photography)
    'photography': [
        "https://es.wikipedia.org/wiki/Fotografía",
        "https://es.wikipedia.org/wiki/Historia_de_la_fotografía",
        "https://es.wikipedia.org/wiki/Fotografía_de_paisaje",
        "https://es.wikipedia.org/wiki/Fotografía_de_retrato",
        "https://es.wikipedia.org/wiki/Fotoperiodismo",
        "https://es.wikipedia.org/wiki/Fotografía_de_naturaleza",
        "https://es.wikipedia.org/wiki/Fotografía_de_calle",
        "https://es.wikipedia.org/wiki/Fotografía_artística",
        "https://es.wikipedia.org/wiki/Daguerrotipo",
        "https://es.wikipedia.org/wiki/Cámara_fotográfica",
        "https://es.wikipedia.org/wiki/Ansel_Adams",
        "https://es.wikipedia.org/wiki/Henri_Cartier-Bresson",
        "https://es.wikipedia.org/wiki/Robert_Capa",
        "https://es.wikipedia.org/wiki/Dorothea_Lange",
        "https://es.wikipedia.org/wiki/Sebastião_Salgado",
        "https://es.wikipedia.org/wiki/Annie_Leibovitz",
        "https://es.wikipedia.org/wiki/Steve_McCurry",
        "https://es.wikipedia.org/wiki/Fotografía_en_blanco_y_negro",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Photography",
        "https://en.wikipedia.org/wiki/History_of_photography",
        "https://en.wikipedia.org/wiki/Monochrome_photography",
        "https://en.wikipedia.org/wiki/Street_photography",
        "https://en.wikipedia.org/wiki/Landscape_photography",
        "https://en.wikipedia.org/wiki/Portrait_photography",
        # New High-Density Sources (Categories)
        "https://en.wikipedia.org/wiki/Category:Documentary_photography",
        "https://en.wikipedia.org/wiki/Category:War_photography",
        "https://en.wikipedia.org/wiki/Category:Landscape_photography",
        "https://en.wikipedia.org/wiki/Category:Street_photography",
        "https://en.wikipedia.org/wiki/Category:Fashion_photography",
        "https://en.wikipedia.org/wiki/Category:Wildlife_photography",
        "https://en.wikipedia.org/wiki/Category:Architectural_photography",
        "https://en.wikipedia.org/wiki/Category:Black-and-white_photography"
    ],

    # 10. FRESCOS (Frescoes)
    'frescoes': [
        "https://es.wikipedia.org/wiki/Fresco",
        "https://es.wikipedia.org/wiki/Pintura_mural",
        "https://es.wikipedia.org/wiki/Capilla_Sixtina",
        "https://es.wikipedia.org/wiki/La_creación_de_Adán",
        "https://es.wikipedia.org/wiki/Juicio_Final_(Miguel_Ángel)",
        "https://es.wikipedia.org/wiki/La_última_cena_(Leonardo_da_Vinci)",
        "https://es.wikipedia.org/wiki/La_escuela_de_Atenas",
        "https://es.wikipedia.org/wiki/Giotto",
        "https://es.wikipedia.org/wiki/Capilla_de_los_Scrovegni",
        "https://es.wikipedia.org/wiki/Fra_Angelico",
        "https://es.wikipedia.org/wiki/Masaccio",
        "https://es.wikipedia.org/wiki/Piero_della_Francesca",
        "https://es.wikipedia.org/wiki/Diego_Rivera",
        "https://es.wikipedia.org/wiki/David_Alfaro_Siqueiros",
        "https://es.wikipedia.org/wiki/José_Clemente_Orozco",
        "https://es.wikipedia.org/wiki/Muralismo_mexicano",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Fresco",
        "https://en.wikipedia.org/wiki/Sistine_Chapel_ceiling",
        "https://en.wikipedia.org/wiki/Giotto",
        "https://en.wikipedia.org/wiki/Masaccio",
        "https://en.wikipedia.org/wiki/Fra_Angelico",
        "https://en.wikipedia.org/wiki/Raphael_Rooms",
        # New High-Density Sources (Categories)
        "https://en.wikipedia.org/wiki/Category:Frescoes_in_Florence",
        "https://en.wikipedia.org/wiki/Category:Frescoes_in_Rome",
        "https://en.wikipedia.org/wiki/Category:Baroque_frescoes",
        "https://en.wikipedia.org/wiki/Category:Minoan_frescoes",
        "https://en.wikipedia.org/wiki/Category:Frescoes_by_artist",
        "https://en.wikipedia.org/wiki/Category:Renaissance_frescoes"
    ],

    # 11. OTROS (Others)
    'others': [
        "https://es.wikipedia.org/wiki/Arte_digital",
        "https://es.wikipedia.org/wiki/Videoarte",
        "https://es.wikipedia.org/wiki/Instalación_artística",
        "https://es.wikipedia.org/wiki/Performance_(arte)",
        "https://es.wikipedia.org/wiki/Happening",
        "https://es.wikipedia.org/wiki/Collage",
        "https://es.wikipedia.org/wiki/Fotomontaje",
        "https://es.wikipedia.org/wiki/Origami",
        "https://es.wikipedia.org/wiki/Vidriera",
        "https://es.wikipedia.org/wiki/Grabado",
        "https://es.wikipedia.org/wiki/Arte_cinético",
        "https://es.wikipedia.org/wiki/Land_art",
        "https://es.wikipedia.org/wiki/Arte_conceptual",
        "https://es.wikipedia.org/wiki/Minimalismo",
        "https://es.wikipedia.org/wiki/Arte_povera",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Origami",
        "https://en.wikipedia.org/wiki/Calligraphy",
        "https://en.wikipedia.org/wiki/Collage",
        "https://en.wikipedia.org/wiki/Printmaking",
        "https://en.wikipedia.org/wiki/Installation_art",
        "https://en.wikipedia.org/wiki/Performance_art"
    ]
}

def batch_download():
    print("Iniciando MEGA-DESCARGA de ARTE (Deep Search Complete)... ¡Prepárate!")
    total_sites = sum(len(urls) for urls in sites.values())
    processed = 0
    
    for category, urls in sites.items():
        print(f"\n>>> INICIANDO CATEGORÍA: {category.upper()} <<<")
        for url in urls:
            processed += 1
            print(f"--- [{processed}/{total_sites}] Procesando: {url} ---")
            try:
                # Limitamos a 100 para MAXIMIZAR datos (User Request)
                download_images_from_url(url, category, limit=10000)
            except Exception as e:
                print(f"Error procesando sitio {url}: {e}")

    print("\n\n¡MEGA-DESCARGA completada! Tu dataset debería ser enorme ahora.")
    print("Revisa la carpeta 'dataset/' para ver el tesoro acumulado.")

if __name__ == "__main__":
    batch_download()