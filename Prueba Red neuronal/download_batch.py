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
        "https://es.wikipedia.org/wiki/Busto_(escultura)",
        "https://es.wikipedia.org/wiki/Estatua",
        "https://es.wikipedia.org/wiki/Relieve_(arte)",
        "https://es.wikipedia.org/wiki/Talla_de_madera",
        "https://es.wikipedia.org/wiki/Bronce_(escultura)",
        "https://es.wikipedia.org/wiki/Mármol",
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
        "https://es.wikipedia.org/wiki/Gran_Esfinge_de_Guiza",
        # Reinforcement to distinguish from Graffiti/Paintings
        "https://en.wikipedia.org/wiki/Statue",
        "https://en.wikipedia.org/wiki/Bust_(sculpture)",
        "https://en.wikipedia.org/wiki/Bronze_sculpture",
        "https://en.wikipedia.org/wiki/Marble_sculpture",
        "https://en.wikipedia.org/wiki/Wood_carving"
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
        "https://en.wikipedia.org/wiki/Category:Street_artist_stubs",
        # Reinforcement to distinguish from Paintings
        "https://en.wikipedia.org/wiki/Throw_up_(graffiti)",
        "https://en.wikipedia.org/wiki/Wildstyle",
        "https://en.wikipedia.org/wiki/Graffiti_fandom",
        "https://en.wikipedia.org/wiki/Anti-graffiti_coating"
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
        "https://en.wikipedia.org/wiki/Performance_art"
    ],

    # 12. PLASTILINA (Plasticine/Clay)
    'plasticine': [
        "https://es.wikipedia.org/wiki/Plastilina",
        "https://es.wikipedia.org/wiki/Arcilla_polimérica",
        "https://es.wikipedia.org/wiki/Stop_motion",
        "https://es.wikipedia.org/wiki/Claymation",
        "https://es.wikipedia.org/wiki/Aardman_Animations",
        "https://es.wikipedia.org/wiki/Wallace_y_Gromit",
        "https://es.wikipedia.org/wiki/Pingu",
        "https://es.wikipedia.org/wiki/Celebrity_Deathmatch",
        "https://es.wikipedia.org/wiki/Robot_Chicken",
        "https://es.wikipedia.org/wiki/Modelado",
        # Balance URLs (English)
        "https://en.wikipedia.org/wiki/Plasticine",
        "https://en.wikipedia.org/wiki/Clay_animation",
        "https://en.wikipedia.org/wiki/Modelling_clay",
        "https://en.wikipedia.org/wiki/Polymer_clay",
        "https://en.wikipedia.org/wiki/Gumby",
        "https://en.wikipedia.org/wiki/Morph_(character)",
        "https://en.wikipedia.org/wiki/Play-Doh",
        # Categories
        "https://en.wikipedia.org/wiki/Category:Clay_animation",
        "https://en.wikipedia.org/wiki/Category:Stop-motion_animated_characters",
        "https://en.wikipedia.org/wiki/Category:Aardman_Animations",
        "https://en.wikipedia.org/wiki/Category:Clay_animators"
    ]
}

# =================================================================================================
#  MEGA-EXPANSIÓN DE ENLACES (V20 - V80 ULTRA PACK)
# =================================================================================================

# --- V20 ULTRA EXPANSION ---
sites['paintings'] += [
    "https://es.wikipedia.org/wiki/Anexo:Pintores_por_orden_cronológico",
    "https://es.wikipedia.org/wiki/Anexo:Pintores_del_Renacimiento",
    "https://es.wikipedia.org/wiki/Anexo:Pintores_del_Barroco",
    "https://es.wikipedia.org/wiki/Anexo:Pintores_del_Impresionismo",
    "https://es.wikipedia.org/wiki/Anexo:Pintores_del_Surrealismo",
    "https://es.wikipedia.org/wiki/Anexo:Pintores_por_nacionalidad",
    "https://es.wikipedia.org/wiki/Anexo:Pinturas_más_caras",
    "https://es.wikipedia.org/wiki/Anexo:Museo_del_Prado",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Tiziano",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Rubens",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Botticelli",
    "https://es.wikipedia.org/wiki/Sandro_Botticelli",
    "https://en.wikipedia.org/wiki/List_of_painters_by_name",
    "https://en.wikipedia.org/wiki/List_of_art_movements",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Leonardo_da_Vinci",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Picasso",
    "https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_the_arts",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Raphael",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Titian",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Peter_Paul_Rubens",
    "https://en.wikipedia.org/wiki/List_of_paintings_in_the_Louvre",
    "https://en.wikipedia.org/wiki/Category:Famous_paintings",
    "https://en.wikipedia.org/wiki/Category:Renaissance_paintings",
    "https://en.wikipedia.org/wiki/Category:Baroque_paintings",
    "https://en.wikipedia.org/wiki/Category:Impressionist_paintings",
    "https://en.wikipedia.org/wiki/Category:Expressionist_paintings",
    "https://en.wikipedia.org/wiki/Category:Cubist_paintings",
    "https://en.wikipedia.org/wiki/Category:Abstract_paintings",
    "https://en.wikipedia.org/wiki/Category:Pop_art",
    "https://en.wikipedia.org/wiki/Category:Symbolist_paintings",
    "https://en.wikipedia.org/wiki/Category:Modern_paintings",
]

sites['sculptures'] += [
    "https://es.wikipedia.org/wiki/Anexo:Escultores",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Miguel_Ángel",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Bernini",
    "https://es.wikipedia.org/wiki/Arte_mobiliario",
    "https://en.wikipedia.org/wiki/List_of_sculptors",
    "https://en.wikipedia.org/wiki/List_of_statues_by_height",
    "https://en.wikipedia.org/wiki/List_of_colossal_sculptures",
    "https://en.wikipedia.org/wiki/List_of_statues",
    "https://en.wikipedia.org/wiki/List_of_equestrian_statues",
    "https://en.wikipedia.org/wiki/Category:Sculptures_in_Italy",
    "https://en.wikipedia.org/wiki/Category:Sculptures_in_Greece",
    "https://en.wikipedia.org/wiki/Category:Sculptures_in_Rome",
    "https://en.wikipedia.org/wiki/Category:Sculptures_in_the_Louvre",
    "https://en.wikipedia.org/wiki/Category:Modern_sculpture",
    "https://en.wikipedia.org/wiki/Category:Bronze_sculptures",
    "https://en.wikipedia.org/wiki/Category:Marble_sculptures",
    "https://en.wikipedia.org/wiki/Category:Stone_sculptures",
    "https://en.wikipedia.org/wiki/Category:Wooden_sculptures",
]

sites['drawings'] += [
    "https://es.wikipedia.org/wiki/Dibujo_artístico",
    "https://es.wikipedia.org/wiki/Dibujo_a_lápiz",
    "https://es.wikipedia.org/wiki/Dibujo_infográfico",
    "https://en.wikipedia.org/wiki/List_of_drawings_by_Leonardo_da_Vinci",
    "https://en.wikipedia.org/wiki/List_of_drawings_by_Michelangelo",
    "https://en.wikipedia.org/wiki/Category:Drawings",
    "https://en.wikipedia.org/wiki/Category:Ink_drawings",
    "https://en.wikipedia.org/wiki/Category:Pencil_drawings",
    "https://en.wikipedia.org/wiki/Category:Sketches",
    "https://en.wikipedia.org/wiki/Category:Illustrators",
]

sites['graffiti'] += [
    "https://es.wikipedia.org/wiki/Arte_mural",
    "https://es.wikipedia.org/wiki/Bombing_(graffiti)",
    "https://es.wikipedia.org/wiki/Graffiti_latinoamericano",
    "https://en.wikipedia.org/wiki/List_of_street_artists",
    "https://en.wikipedia.org/wiki/List_of_graffiti_artists",
    "https://en.wikipedia.org/wiki/Category:Graffiti_by_city",
    "https://en.wikipedia.org/wiki/Category:Graffiti_artists",
    "https://en.wikipedia.org/wiki/Category:Street_art_by_country",
    "https://en.wikipedia.org/wiki/Category:Muralists",
    "https://en.wikipedia.org/wiki/Category:Urban_art",
]

sites['architecture'] += [
    "https://es.wikipedia.org/wiki/Historia_de_la_arquitectura",
    "https://es.wikipedia.org/wiki/Arquitectura_contemporánea",
    "https://es.wikipedia.org/wiki/Arquitectura_sostenible",
    "https://en.wikipedia.org/wiki/List_of_architectural_styles",
    "https://en.wikipedia.org/wiki/List_of_palaces",
    "https://en.wikipedia.org/wiki/List_of_cathedrals",
    "https://en.wikipedia.org/wiki/List_of_mosques",
    "https://en.wikipedia.org/wiki/List_of_skyscrapers",
    "https://en.wikipedia.org/wiki/List_of_modernist_architecture",
    "https://en.wikipedia.org/wiki/Category:World_Heritage_Sites",
    "https://en.wikipedia.org/wiki/Category:Architectural_styles",
    "https://en.wikipedia.org/wiki/Category:Ancient_architecture",
    "https://en.wikipedia.org/wiki/Category:Castles_by_country",
]

sites['mosaics'] += [
    "https://es.wikipedia.org/wiki/Mosaico_moderno",
    "https://en.wikipedia.org/wiki/List_of_mosaics",
    "https://en.wikipedia.org/wiki/Category:Roman_mosaics",
    "https://en.wikipedia.org/wiki/Category:Greek_mosaics",
    "https://en.wikipedia.org/wiki/Category:Byzantine_mosaics_in_Turkey",
    "https://en.wikipedia.org/wiki/Category:Mosaic_artists",
]

sites['ceramics'] += [
    "https://es.wikipedia.org/wiki/Alfarería_indígena",
    "https://en.wikipedia.org/wiki/List_of_ceramic_artists",
    "https://en.wikipedia.org/wiki/List_of_pottery_styles",
    "https://en.wikipedia.org/wiki/Category:Pottery_by_country",
    "https://en.wikipedia.org/wiki/Category:Porcelain_by_country",
    "https://en.wikipedia.org/wiki/Category:Ceramics_museums",
]

sites['textiles'] += [
    "https://es.wikipedia.org/wiki/Arte_têxtil_andino",
    "https://en.wikipedia.org/wiki/List_of_textile_artists",
    "https://en.wikipedia.org/wiki/List_of_textile_patterns",
    "https://en.wikipedia.org/wiki/Category:Textile_museums",
    "https://en.wikipedia.org/wiki/Category:Traditional_textile_art",
    "https://en.wikipedia.org/wiki/Category:Weaving",
]

sites['photography'] += [
    "https://es.wikipedia.org/wiki/Fotografía_documental",
    "https://es.wikipedia.org/wiki/Fotografía_aérea",
    "https://es.wikipedia.org/wiki/Fotografía_nocturna",
    "https://en.wikipedia.org/wiki/List_of_photographers",
    "https://en.wikipedia.org/wiki/List_of_photojournalists",
    "https://en.wikipedia.org/wiki/List_of_landscape_photographers",
    "https://en.wikipedia.org/wiki/Category:Photography_by_genre",
    "https://en.wikipedia.org/wiki/Category:Photographs",
]

sites['frescoes'] += [
    "https://es.wikipedia.org/wiki/Frescos_renacentistas",
    "https://en.wikipedia.org/wiki/List_of_frescoes",
    "https://en.wikipedia.org/wiki/Category:Fresco_by_country",
    "https://en.wikipedia.org/wiki/Category:Renaissance_fresco_paintings",
    "https://en.wikipedia.org/wiki/Category:Murals",
]

sites['others'] += [
    "https://es.wikipedia.org/wiki/Arte_sonoro",
    "https://es.wikipedia.org/wiki/Holografía",
    "https://en.wikipedia.org/wiki/List_of_contemporary_artists",
    "https://en.wikipedia.org/wiki/List_of_installation_artists",
    "https://en.wikipedia.org/wiki/Category:Digital_art",
    "https://en.wikipedia.org/wiki/Category:Kinetic_art",
    "https://en.wikipedia.org/wiki/Category:Land_art",
]

sites['plasticine'] += [
    "https://en.wikipedia.org/wiki/List_of_clay_animators",
    "https://en.wikipedia.org/wiki/List_of_Aardman_Animations_films",
    "https://en.wikipedia.org/wiki/Category:Claymation_films",
    "https://en.wikipedia.org/wiki/Category:Stop_motion_techniques",
    "https://en.wikipedia.org/wiki/Category:Stop-motion_films",
]

# --- V30 ULTRA EXPANSION ---
sites['paintings'] += [
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Rafael",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Tiziano",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Pieter_Brueghel",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Sandro_Botticelli",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Giorgione",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Paul_Gauguin",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Rodin",
    "https://es.wikipedia.org/wiki/Anexo:Obras_de_Marcel_Duchamp",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_El_Greco",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Caravaggio",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Vermeer",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Goya",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Rubens",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Rembrandt",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_Wassily_Kandinsky",
    "https://en.wikipedia.org/wiki/List_of_Impressionist_artists",
    "https://en.wikipedia.org/wiki/List_of_Baroque_artists",
    "https://en.wikipedia.org/wiki/List_of_Abstract_artists",
    "https://en.wikipedia.org/wiki/List_of_Expressionist_artists",
    "https://en.wikipedia.org/wiki/List_of_Surrealist_artists",
    "https://en.wikipedia.org/wiki/List_of_Cubists",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Vatican_Museums",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Prado_Museum",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Louvre_by_artist",
    "https://en.wikipedia.org/wiki/Category:Renaissance_art",
    "https://en.wikipedia.org/wiki/Category:18th-century_paintings",
    "https://en.wikipedia.org/wiki/Category:19th-century_paintings",
    "https://en.wikipedia.org/wiki/Category:20th-century_paintings",
    "https://en.wikipedia.org/wiki/Category:Italian_paintings",
    "https://en.wikipedia.org/wiki/Category:French_paintings",
    "https://en.wikipedia.org/wiki/Category:German_paintings",
]

sites['sculptures'] += [
    "https://es.wikipedia.org/wiki/Escultura_moderna",
    "https://es.wikipedia.org/wiki/Escultura_contemporánea",
    "https://es.wikipedia.org/wiki/Anexo:Escultores_del_Renacimiento",
    "https://es.wikipedia.org/wiki/Anexo:Escultores_modernos",
    "https://es.wikipedia.org/wiki/Arte_megalítico",
    "https://en.wikipedia.org/wiki/List_of_colossal_statues",
    "https://en.wikipedia.org/wiki/List_of_Hellenistic_sculptures",
    "https://en.wikipedia.org/wiki/List_of_Roman_sculptures",
    "https://en.wikipedia.org/wiki/List_of_Egyptian_sculptures",
    "https://en.wikipedia.org/wiki/Category:Sculptures_by_country",
    "https://en.wikipedia.org/wiki/Category:Sculptures_in_Museums",
    "https://en.wikipedia.org/wiki/Category:Ancient_Greek_sculpture",
    "https://en.wikipedia.org/wiki/Category:Roman_sculpture",
    "https://en.wikipedia.org/wiki/Category:Neoclassical_sculpture",
    "https://en.wikipedia.org/wiki/Category:Modern_sculptors",
    "https://en.wikipedia.org/wiki/Category:Stone_sculpture",
    "https://en.wikipedia.org/wiki/Category:Metal_sculpture",
    "https://en.wikipedia.org/wiki/Category:Outdoor_sculptures",
]

sites['drawings'] += [
    "https://es.wikipedia.org/wiki/Dibujo_barroco",
    "https://es.wikipedia.org/wiki/Dibujo_renacentista",
    "https://en.wikipedia.org/wiki/List_of_draughtsmen",
    "https://en.wikipedia.org/wiki/List_of_illustrators_by_name",
    "https://en.wikipedia.org/wiki/List_of_children%27s_book_illustrators",
    "https://en.wikipedia.org/wiki/Category:Ink_art",
    "https://en.wikipedia.org/wiki/Category:Pencil_art",
    "https://en.wikipedia.org/wiki/Category:Charcoal_drawings",
    "https://en.wikipedia.org/wiki/Category:Sketch_artists",
]

sites['graffiti'] += [
    "https://es.wikipedia.org/wiki/Graffiti_latino",
    "https://es.wikipedia.org/wiki/Graffiti_argentino",
    "https://es.wikipedia.org/wiki/Graffiti_mexicano",
    "https://es.wikipedia.org/wiki/Graffiti_español",
    "https://en.wikipedia.org/wiki/List_of_street_art_museums",
    "https://en.wikipedia.org/wiki/List_of_street_art_festivals",
    "https://en.wikipedia.org/wiki/List_of_street_artists_by_city",
    "https://en.wikipedia.org/wiki/Category:Graffiti_art_by_country",
    "https://en.wikipedia.org/wiki/Category:Muralists_by_country",
    "https://en.wikipedia.org/wiki/Category:Urban_culture",
]

sites['architecture'] += [
    "https://es.wikipedia.org/wiki/Arquitectura_precolombina",
    "https://es.wikipedia.org/wiki/Arquitectura_preclásica_maya",
    "https://es.wikipedia.org/wiki/Arquitectura_incaica",
    "https://en.wikipedia.org/wiki/List_of_architectural_heritage_sites",
    "https://en.wikipedia.org/wiki/List_of_modernist_buildings",
    "https://en.wikipedia.org/wiki/List_of_ancient_monuments",
    "https://en.wikipedia.org/wiki/List_of_world%27s_most_visited_palaces",
    "https://en.wikipedia.org/wiki/List_of_Barcelona_landmarks",
    "https://en.wikipedia.org/wiki/List_of_Paris_landmarks",
    "https://en.wikipedia.org/wiki/List_of_Roman_monuments",
    "https://en.wikipedia.org/wiki/List_of_architects_by_nationality",
    "https://en.wikipedia.org/wiki/Category:Architectural_sites",
    "https://en.wikipedia.org/wiki/Category:Ancient_buildings",
    "https://en.wikipedia.org/wiki/Category:Castles_in_Spain",
    "https://en.wikipedia.org/wiki/Category:Castles_in_France",
]

sites['mosaics'] += [
    "https://en.wikipedia.org/wiki/List_of_Byzantine_mosaics",
    "https://en.wikipedia.org/wiki/List_of_Roman_sites_with_mosaics",
    "https://en.wikipedia.org/wiki/List_of_ancient_mosaics",
    "https://en.wikipedia.org/wiki/Category:Mosaic_artists_by_nationality",
    "https://en.wikipedia.org/wiki/Category:Islamic_mosaics",
]

sites['ceramics'] += [
    "https://es.wikipedia.org/wiki/Cerámica_ibérica",
    "https://es.wikipedia.org/wiki/Cerámica_romana",
    "https://es.wikipedia.org/wiki/Cerámica_islámica",
    "https://en.wikipedia.org/wiki/List_of_pottery_styles",
    "https://en.wikipedia.org/wiki/List_of_Chinese_pottery_and_porcelain",
    "https://en.wikipedia.org/wiki/List_of_Islamic_pottery",
    "https://en.wikipedia.org/wiki/Category:Porcelain_museums",
]

sites['textiles'] += [
    "https://es.wikipedia.org/wiki/Textil_precolombino",
    "https://es.wikipedia.org/wiki/Arte_textil_maya",
    "https://en.wikipedia.org/wiki/List_of_fashion_designers",
    "https://en.wikipedia.org/wiki/List_of_fabric_names",
    "https://en.wikipedia.org/wiki/Category:Traditional_clothing",
    "https://en.wikipedia.org/wiki/Category:Historic_textiles",
]

sites['photography'] += [
    "https://es.wikipedia.org/wiki/Fotografía_urbana",
    "https://en.wikipedia.org/wiki/List_of_photography_awards",
    "https://en.wikipedia.org/wiki/List_of_landmark_photographs",
    "https://en.wikipedia.org/wiki/List_of_fashion_photographers",
    "https://en.wikipedia.org/wiki/Category:Photography_museums",
    "https://en.wikipedia.org/wiki/Category:Iconic_photographs",
]

sites['frescoes'] += [
    "https://en.wikipedia.org/wiki/List_of_fresco_cycles",
    "https://en.wikipedia.org/wiki/Category:Renaissance_fresco_artists",
    "https://en.wikipedia.org/wiki/Category:Greek_frescoes",
    "https://en.wikipedia.org/wiki/Category:Roman_frescoes",
]

sites['others'] += [
    "https://es.wikipedia.org/wiki/Arte_lumínico",
    "https://es.wikipedia.org/wiki/Arte_interactivo",
    "https://en.wikipedia.org/wiki/List_of_contemporary_art_museums",
    "https://en.wikipedia.org/wiki/List_of_installation_artists",
    "https://en.wikipedia.org/wiki/List_of_conceptual_artists",
    "https://en.wikipedia.org/wiki/Category:Digital_sculptures",
]

sites['plasticine'] += [
    "https://en.wikipedia.org/wiki/List_of_stop-motion_series",
    "https://en.wikipedia.org/wiki/List_of_stop-motion_films",
    "https://en.wikipedia.org/wiki/Category:Stop_motion_animation",
    "https://en.wikipedia.org/wiki/Category:Claymation_artists",
]

# --- V40 MEGA DROP ---
sites['paintings'] += [
    "https://en.wikipedia.org/wiki/List_of_Italian_paintings",
    "https://en.wikipedia.org/wiki/List_of_French_paintings",
    "https://en.wikipedia.org/wiki/List_of_German_paintings",
    "https://en.wikipedia.org/wiki/List_of_Spanish_paintings",
    "https://en.wikipedia.org/wiki/List_of_Russian_paintings",
    "https://en.wikipedia.org/wiki/List_of_Japanese_paintings",
    "https://en.wikipedia.org/wiki/List_of_Chinese_paintings",
    "https://en.wikipedia.org/wiki/List_of_Persian_paintings",
    "https://en.wikipedia.org/wiki/List_of_Indian_paintings",
    "https://en.wikipedia.org/wiki/List_of_American_paintings",
    "https://en.wikipedia.org/wiki/List_of_modernist_artworks",
    "https://en.wikipedia.org/wiki/List_of_expressionist_paintings",
    "https://en.wikipedia.org/wiki/List_of_post-impressionist_artists",
    "https://en.wikipedia.org/wiki/List_of_national_treasures_of_Japan_(paintings)",
    "https://en.wikipedia.org/wiki/List_of_Korean_paintings",
    "https://en.wikipedia.org/wiki/List_of_cave_art",
    "https://en.wikipedia.org/wiki/List_of_medieval_paintings",
    "https://en.wikipedia.org/wiki/List_of_Renaissance_artists",
    "https://en.wikipedia.org/wiki/List_of_art_movements",
    "https://en.wikipedia.org/wiki/Category:Famous_paintings",
    "https://en.wikipedia.org/wiki/Category:Painting_collections",
    "https://en.wikipedia.org/wiki/Category:Portraits_by_artist",
    "https://en.wikipedia.org/wiki/Category:Landscape_paintings",
    "https://en.wikipedia.org/wiki/Category:Religious_paintings",
    "https://en.wikipedia.org/wiki/Category:Mythological_paintings",
]

sites['sculptures'] += [
    "https://en.wikipedia.org/wiki/List_of_ancient_statues",
    "https://en.wikipedia.org/wiki/List_of_colossal_statues_in_Egypt",
    "https://en.wikipedia.org/wiki/List_of_Greek_statues",
    "https://en.wikipedia.org/wiki/List_of_Roman_statues",
    "https://en.wikipedia.org/wiki/List_of_Egyptian_monuments",
    "https://en.wikipedia.org/wiki/List_of_Norse_artifacts",
    "https://en.wikipedia.org/wiki/List_of_pre-Columbian_art",
    "https://en.wikipedia.org/wiki/List_of_medieval_sculpture",
    "https://en.wikipedia.org/wiki/List_of_modern_sculptures",
    "https://en.wikipedia.org/wiki/Category:Sculptures_by_period",
    "https://en.wikipedia.org/wiki/Category:Sculptures_by_material",
    "https://en.wikipedia.org/wiki/Category:Marble_sculptures",
    "https://en.wikipedia.org/wiki/Category:Bronze_sculptures",
    "https://en.wikipedia.org/wiki/Category:Stone_sculptures",
    "https://en.wikipedia.org/wiki/Category:Sculpture_collections",
]

sites['drawings'] += [
    "https://en.wikipedia.org/wiki/List_of_artists_known_for_drawing",
    "https://en.wikipedia.org/wiki/List_of_lithographs",
    "https://en.wikipedia.org/wiki/List_of_watercolor_art",
    "https://en.wikipedia.org/wiki/Category:Sketches",
    "https://en.wikipedia.org/wiki/Category:Pencil_drawings",
    "https://en.wikipedia.org/wiki/Category:Charcoal_art",
    "https://en.wikipedia.org/wiki/Category:Ink_drawings",
    "https://en.wikipedia.org/wiki/Category:Illustration_collections",
]

sites['graffiti'] += [
    "https://en.wikipedia.org/wiki/List_of_Banksy_works",
    "https://en.wikipedia.org/wiki/List_of_street_art_murals",
    "https://en.wikipedia.org/wiki/List_of_street_artists",
    "https://en.wikipedia.org/wiki/List_of_graffiti_terms",
    "https://en.wikipedia.org/wiki/Category:Street_art_by_city",
    "https://en.wikipedia.org/wiki/Category:Graffiti_art_by_year",
]

sites['architecture'] += [
    "https://en.wikipedia.org/wiki/List_of_famous_buildings",
    "https://en.wikipedia.org/wiki/List_of_Hindu_temples",
    "https://en.wikipedia.org/wiki/List_of_Buddhist_temples",
    "https://en.wikipedia.org/wiki/List_of_mosques",
    "https://en.wikipedia.org/wiki/List_of_cathedrals",
    "https://en.wikipedia.org/wiki/List_of_palaces",
    "https://en.wikipedia.org/wiki/List_of_castles",
    "https://en.wikipedia.org/wiki/List_of_ancient_structures",
    "https://en.wikipedia.org/wiki/List_of_pyramids",
    "https://en.wikipedia.org/wiki/List_of_Mayan_sites",
    "https://en.wikipedia.org/wiki/List_of_Aztec_sites",
    "https://en.wikipedia.org/wiki/List_of_Inca_sites",
    "https://en.wikipedia.org/wiki/List_of_Roman_sites",
    "https://en.wikipedia.org/wiki/List_of_Greek_temples",
    "https://en.wikipedia.org/wiki/Category:Architecture_by_period",
    "https://en.wikipedia.org/wiki/Category:Architecture_by_country",
]

sites['mosaics'] += [
    "https://en.wikipedia.org/wiki/List_of_ancient_mosaics",
    "https://en.wikipedia.org/wiki/List_of_Baroque_mosaics",
    "https://en.wikipedia.org/wiki/List_of_Islamic_mosaics",
    "https://en.wikipedia.org/wiki/List_of_Roman_mosaics",
    "https://en.wikipedia.org/wiki/Category:Mosaic_art_by_period",
]

sites['ceramics'] += [
    "https://en.wikipedia.org/wiki/List_of_ceramic_artists",
    "https://en.wikipedia.org/wiki/List_of_pottery_styles",
    "https://en.wikipedia.org/wiki/List_of_pre-Columbian_pottery",
    "https://en.wikipedia.org/wiki/List_of_Japanese_pottery_and_porcelain",
    "https://en.wikipedia.org/wiki/List_of_Chinese_porcelain",
    "https://en.wikipedia.org/wiki/Category:Ceramics_by_country",
]

sites['textiles'] += [
    "https://en.wikipedia.org/wiki/List_of_traditional_textiles",
    "https://en.wikipedia.org/wiki/List_of_fabrics",
    "https://en.wikipedia.org/wiki/List_of_tapestries",
    "https://en.wikipedia.org/wiki/Category:Embroidery",
    "https://en.wikipedia.org/wiki/Category:African_textiles",
]

sites['photography'] += [
    "https://en.wikipedia.org/wiki/List_of_iconic_photographs",
    "https://en.wikipedia.org/wiki/List_of_famous_photographers",
    "https://en.wikipedia.org/wiki/List_of_photo_collections",
    "https://en.wikipedia.org/wiki/List_of_photojournalists",
    "https://en.wikipedia.org/wiki/Category:Photography_by_country",
    "https://en.wikipedia.org/wiki/Category:Historical_photographs",
]

sites['frescoes'] += [
    "https://en.wikipedia.org/wiki/List_of_frescoes",
    "https://en.wikipedia.org/wiki/List_of_Renaissance_frescoes",
    "https://en.wikipedia.org/wiki/List_of_Baroque_frescoes",
    "https://en.wikipedia.org/wiki/Category:Fresco_painters",
]

# --- V80 OVERKILL (GENERATED LINKS) ---
sites['paintings'] += [
    "https://en.wikipedia.org/wiki/List_of_paintings",
    "https://en.wikipedia.org/wiki/List_of_paintings_by_artist",
    "https://en.wikipedia.org/wiki/Category:Paintings_by_artist",
    "https://en.wikipedia.org/wiki/Category:Paintings_by_country",
    "https://en.wikipedia.org/wiki/Category:Paintings_by_century",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Louvre",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Metropolitan_Museum_of_Art",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_Rijksmuseum",
    "https://en.wikipedia.org/wiki/Category:Paintings_in_the_National_Gallery,_London",
    "https://en.wikipedia.org/wiki/Category:Renaissance_paintings",
    "https://en.wikipedia.org/wiki/Category:Baroque_paintings",
    "https://en.wikipedia.org/wiki/Category:Impressionist_paintings",
    "https://en.wikipedia.org/wiki/Category:Modern_paintings",
]

sites['sculptures'] += [
    "https://en.wikipedia.org/wiki/Category:Sculptures_by_artist",
    "https://en.wikipedia.org/wiki/Category:Sculptures_by_period",
    "https://en.wikipedia.org/wiki/Category:Ancient_Greek_sculpture",
    "https://en.wikipedia.org/wiki/Category:Roman_sculpture",
    "https://en.wikipedia.org/wiki/Category:Egyptian_sculpture",
    "https://en.wikipedia.org/wiki/Category:Outdoor_sculptures",
    "https://en.wikipedia.org/wiki/List_of_statues",
    "https://en.wikipedia.org/wiki/List_of_colossal_statues",
    "https://en.wikipedia.org/wiki/Category:Sculptures_by_museum",
]

sites['drawings'] += [
    "https://en.wikipedia.org/wiki/Category:Drawings_by_artist",
    "https://en.wikipedia.org/wiki/Category:Sketches",
    "https://en.wikipedia.org/wiki/Category:Pencil_drawings",
    "https://en.wikipedia.org/wiki/Category:Ink_drawings",
    "https://en.wikipedia.org/wiki/List_of_drawings",
]

sites['graffiti'] += [
    "https://en.wikipedia.org/wiki/Category:Graffiti",
    "https://en.wikipedia.org/wiki/Category:Street_art",
    "https://en.wikipedia.org/wiki/Category:Murals_by_city",
    "https://en.wikipedia.org/wiki/List_of_street_artists",
    "https://en.wikipedia.org/wiki/List_of_murals",
]

sites['architecture'] += [
    "https://en.wikipedia.org/wiki/Category:Architectural_styles",
    "https://en.wikipedia.org/wiki/Category:Buildings_and_structures_by_country",
    "https://en.wikipedia.org/wiki/Category:Temples_by_country",
    "https://en.wikipedia.org/wiki/Category:Palaces_by_country",
    "https://en.wikipedia.org/wiki/Category:Castles_by_country",
    "https://en.wikipedia.org/wiki/Category:Archaeological_sites_by_country",
    "https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites",
    "https://en.wikipedia.org/wiki/List_of_ancient_cities",
    "https://en.wikipedia.org/wiki/List_of_archaeological_sites_sorted_by_country",
]

sites['mosaics'] += [
    "https://en.wikipedia.org/wiki/Category:Mosaics_by_period",
    "https://en.wikipedia.org/wiki/Category:Mosaics_by_country",
    "https://en.wikipedia.org/wiki/List_of_mosaics",
]

sites['ceramics'] += [
    "https://en.wikipedia.org/wiki/Category:Pottery_by_country",
    "https://en.wikipedia.org/wiki/Category:Ceramics_by_period",
    "https://en.wikipedia.org/wiki/Category:Porcelain",
    "https://en.wikipedia.org/wiki/Category:Chinese_pottery",
    "https://en.wikipedia.org/wiki/List_of_pottery_and_porcelain_terms",
]

sites['textiles'] += [
    "https://en.wikipedia.org/wiki/Category:Textiles_by_country",
    "https://en.wikipedia.org/wiki/Category:Embroidery",
    "https://en.wikipedia.org/wiki/Category:Tapestries",
    "https://en.wikipedia.org/wiki/List_of_textile_artists",
]

sites['photography'] += [
    "https://en.wikipedia.org/wiki/Category:Photography_collections",
    "https://en.wikipedia.org/wiki/Category:Historic_photographs",
    "https://en.wikipedia.org/wiki/List_of_photographers",
    "https://en.wikipedia.org/wiki/List_of_photojournalists",
    "https://en.wikipedia.org/wiki/Category:Press_photographs",
]

sites['frescoes'] += [
    "https://en.wikipedia.org/wiki/Category:Fresco_painters",
    "https://en.wikipedia.org/wiki/Category:Fresco_cycles",
    "https://en.wikipedia.org/wiki/List_of_frescoes",
]

sites['plasticine'] += [
    "https://en.wikipedia.org/wiki/Category:Stop_motion_films",
    "https://en.wikipedia.org/wiki/Category:Clay_animation",
    "https://en.wikipedia.org/wiki/List_of_stop-motion_animated_television_series",
]

# --- AUTO-GENERATED ARTIST LISTS (BY LETTER) ---
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
sites['paintings'] += [f"https://en.wikipedia.org/wiki/Category:Painters_by_name:?from={l}" for l in letters]
sites['sculptures'] += [f"https://en.wikipedia.org/wiki/Category:Sculptors_by_name:?from={l}" for l in letters]
sites['photography'] += [f"https://en.wikipedia.org/wiki/Category:Photographers_by_name:?from={l}" for l in letters]



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