from download_images import download_images_from_url

# Diccionario de Categoría -> Lista de URLs
# ¡AMPLIACIÓN MASIVA v3.0 - EL SUPER DATASET!
sites = {
    'artworks': [
        # --- GRAFFITI Y ARTE URBANO (Prioridad para corrección) ---
        "https://es.wikipedia.org/wiki/Graffiti",
        "https://es.wikipedia.org/wiki/Arte_urbano",
        "https://es.wikipedia.org/wiki/Muralismo",
        "https://es.wikipedia.org/wiki/Keith_Haring",
        "https://es.wikipedia.org/wiki/Jean-Michel_Basquiat",
        "https://es.wikipedia.org/wiki/Banksy",
        "https://es.wikipedia.org/wiki/Stencil",
        "https://es.wikipedia.org/wiki/Tag_(graffiti)",

        # --- MAESTROS DEL ARTE (Renacimiento a Moderno) ---
        "https://es.wikipedia.org/wiki/Leonardo_da_Vinci",
        "https://es.wikipedia.org/wiki/Miguel_Ángel",
        "https://es.wikipedia.org/wiki/Rafael_Sanzio",
        "https://es.wikipedia.org/wiki/Caravaggio",
        "https://es.wikipedia.org/wiki/Rembrandt",
        "https://es.wikipedia.org/wiki/Diego_Velázquez",
        "https://es.wikipedia.org/wiki/Francisco_de_Goya",
        "https://es.wikipedia.org/wiki/Eugène_Delacroix",
        "https://es.wikipedia.org/wiki/Claude_Monet",
        "https://es.wikipedia.org/wiki/Pierre-Auguste_Renoir",
        "https://es.wikipedia.org/wiki/Vincent_van_Gogh",
        "https://es.wikipedia.org/wiki/Paul_Cézanne",
        "https://es.wikipedia.org/wiki/Paul_Gauguin",
        "https://es.wikipedia.org/wiki/Pablo_Picasso",
        "https://es.wikipedia.org/wiki/Vasili_Kandinsky",
        "https://es.wikipedia.org/wiki/Kazimir_Malévich",
        "https://es.wikipedia.org/wiki/Salvador_Dalí",
        "https://es.wikipedia.org/wiki/René_Magritte",
        "https://es.wikipedia.org/wiki/Andy_Warhol",
        "https://es.wikipedia.org/wiki/Jackson_Pollock",
        "https://es.wikipedia.org/wiki/Frida_Kahlo",
        "https://es.wikipedia.org/wiki/Tamara_de_Lempicka",

        # --- ARTES VISUALES AVANZADAS Y DE NICHO ---
        "https://es.wikipedia.org/wiki/Arte_cinético",
        "https://es.wikipedia.org/wiki/Op_art",
        "https://es.wikipedia.org/wiki/Arte_sonoro",
        "https://es.wikipedia.org/wiki/Arte_generativo",
        "https://es.wikipedia.org/wiki/Fractal",
        "https://es.wikipedia.org/wiki/Land_Art",
        "https://es.wikipedia.org/wiki/Arte_textil",
        "https://es.wikipedia.org/wiki/Tejido",
        "https://es.wikipedia.org/wiki/Vidrio_de_Murano",
        "https://es.wikipedia.org/wiki/Vitrales",
        "https://es.wikipedia.org/wiki/Manuscrito_iluminado",
        "https://es.wikipedia.org/wiki/Libro_de_horas",
        
        # --- MOVIMIENTOS Y ESTILOS ---
        "https://es.wikipedia.org/wiki/Arte_contemporáneo",
        "https://es.wikipedia.org/wiki/Arte_abstracto",
        "https://es.wikipedia.org/wiki/Cubismo",
        "https://es.wikipedia.org/wiki/Pop_art",
        "https://es.wikipedia.org/wiki/Impresionismo",
        "https://es.wikipedia.org/wiki/Surrealismo",
        "https://es.wikipedia.org/wiki/Renacimiento",
        "https://es.wikipedia.org/wiki/Pintura_del_Barroco",
        "https://es.wikipedia.org/wiki/Gótico",
        "https://es.wikipedia.org/wiki/Rococó",
        "https://es.wikipedia.org/wiki/Neoclasicismo",
        "https://es.wikipedia.org/wiki/Romanticismo",
        "https://es.wikipedia.org/wiki/Postimpresionismo",
        "https://es.wikipedia.org/wiki/Fauvismo",
        "https://es.wikipedia.org/wiki/Expresionismo",
        "https://es.wikipedia.org/wiki/Dadaísmo",
        "https://es.wikipedia.org/wiki/Futurismo",
        "https://es.wikipedia.org/wiki/Constructivismo",
        "https://es.wikipedia.org/wiki/Minimalismo",
        "https://es.wikipedia.org/wiki/Arte_conceptual",
        "https://es.wikipedia.org/wiki/Art_nouveau",
        "https://es.wikipedia.org/wiki/Art_déco",
        "https://es.wikipedia.org/wiki/Hiperrealismo",
        "https://es.wikipedia.org/wiki/Videoarte",

        # --- TIPOS Y FORMATOS ---
        "https://es.wikipedia.org/wiki/Escultura_contemporánea",
        "https://es.wikipedia.org/wiki/Retrato_pictórico",
        "https://es.wikipedia.org/wiki/Pintura_del_paisaje",
        "https://es.wikipedia.org/wiki/Bodegón",
        "https://es.wikipedia.org/wiki/Mural",
        "https://es.wikipedia.org/wiki/Grabado",
        "https://es.wikipedia.org/wiki/Fotografía_artística",
        "https://es.wikipedia.org/wiki/Diseño_gráfico",
        "https://es.wikipedia.org/wiki/Mosaico",
        "https://es.wikipedia.org/wiki/Cerámica",
        
        # --- CULTURA POP Y DIGITAL ---
        "https://es.wikipedia.org/wiki/Anime",
        "https://es.wikipedia.org/wiki/Manga",
        "https://es.wikipedia.org/wiki/Cómic",
        "https://es.wikipedia.org/wiki/Novela_gráfica",
        "https://es.wikipedia.org/wiki/Superhéroe",
        "https://es.wikipedia.org/wiki/Arte_de_videojuegos",
        "https://es.wikipedia.org/wiki/Pixel_art",
        "https://es.wikipedia.org/wiki/Gráficos_3D_por_computadora",
        "https://es.wikipedia.org/wiki/Concept_art",
        "https://es.wikipedia.org/wiki/Arte_fantástico",
        "https://es.wikipedia.org/wiki/Ciencia_ficción",
        "https://es.wikipedia.org/wiki/Cyberpunk",
        "https://es.wikipedia.org/wiki/Steampunk",
        "https://es.wikipedia.org/wiki/Tatuaje",
        "https://es.wikipedia.org/wiki/Origami",
        "https://es.wikipedia.org/wiki/Caligrafía"
    ],
    'monuments': [
        # --- ESTRUCTURAS HISTÓRICAS Y PATRIMONIO ---
        "https://es.wikipedia.org/wiki/Fortificación",
        "https://es.wikipedia.org/wiki/Alcázar",
        "https://es.wikipedia.org/wiki/Acueducto",
        "https://es.wikipedia.org/wiki/Ingeniería_romana",
        "https://es.wikipedia.org/wiki/Faro",
        "https://es.wikipedia.org/wiki/Necrópolis",
        "https://es.wikipedia.org/wiki/Mausoleo",
        "https://es.wikipedia.org/wiki/Mercado_(establecimiento)",
        "https://es.wikipedia.org/wiki/Arquitectura_vernácula",
        "https://es.wikipedia.org/wiki/Pagoda",
        "https://es.wikipedia.org/wiki/Torre_del_reloj",
        "https://es.wikipedia.org/wiki/Reloj_astronómico",

        # --- ARQUITECTURA CLÁSICA Y RELIGIOSA ---
        "https://es.wikipedia.org/wiki/Pirámides_de_Egipto",
        "https://es.wikipedia.org/wiki/Antigua_Roma",
        "https://es.wikipedia.org/wiki/Templo_griego",
        "https://es.wikipedia.org/wiki/Megalito",
        "https://es.wikipedia.org/wiki/Zigurat",
        "https://es.wikipedia.org/wiki/Arquitectura_precolombina",
        "https://es.wikipedia.org/wiki/Estela_(monumento)",
        "https://es.wikipedia.org/wiki/Castillo",
        "https://es.wikipedia.org/wiki/Catedral_gótica",
        "https://es.wikipedia.org/wiki/Arquitectura_románica",
        "https://es.wikipedia.org/wiki/Mezquita",
        "https://es.wikipedia.org/wiki/Monasterio",
        "https://es.wikipedia.org/wiki/Arquitectura_mudéjar",
        
        # --- ARQUITECTURA MODERNA Y PÚBLICA ---
        "https://es.wikipedia.org/wiki/Rascacielos",
        "https://es.wikipedia.org/wiki/Puente",
        "https://es.wikipedia.org/wiki/Arquitectura_moderna",
        "https://es.wikipedia.org/wiki/Estilo_internacional_(arquitectura)",
        "https://es.wikipedia.org/wiki/Arquitectura_brutalista",
        "https://es.wikipedia.org/wiki/Arquitectura_sustentable",
        "https://es.wikipedia.org/wiki/Arquitectura_deconstructivista",
        "https://es.wikipedia.org/wiki/Estadio_de_fútbol",
        "https://es.wikipedia.org/wiki/Ópera_(edificio)",
        "https://es.wikipedia.org/wiki/Teatro",
        "https://es.wikipedia.org/wiki/Biblioteca",
        "https://es.wikipedia.org/wiki/Museo",
        "https://es.wikipedia.org/wiki/Palacio",
        "https://es.wikipedia.org/wiki/Muralla",
        "https://es.wikipedia.org/wiki/Puerta_de_la_ciudad",
        "https://es.wikipedia.org/wiki/Plaza",
        "https://es.wikipedia.org/wiki/Fuente_(arquitectura)",
        "https://es.wikipedia.org/wiki/Parque_urbano",
        
        # --- CATEGORÍAS GENERALES ---
        "https://es.wikipedia.org/wiki/Monumento",
        "https://es.wikipedia.org/wiki/Arco_de_triunfo",
        "https://es.wikipedia.org/wiki/Obelisco",
        "https://es.wikipedia.org/wiki/Patrimonio_de_la_Humanidad"
    ],
    'others': [
        # --- ESCENAS SOCIALES Y ENTORNOS (Falsos Positivos) ---
        "https://es.wikipedia.org/wiki/Fotografía_documental",
        "https://es.wikipedia.org/wiki/Fotoperiodismo",
        "https://es.wikipedia.org/wiki/Interfaz_de_usuario",
        "https://es.wikipedia.org/wiki/Logotipo",
        "https://es.wikipedia.org/wiki/Oficina",
        "https://es.wikipedia.org/wiki/Mobiliario_de_oficina",
        "https://es.wikipedia.org/wiki/Hospital",
        "https://es.wikipedia.org/wiki/Equipo_médico",
        "https://es.wikipedia.org/wiki/Deporte_de_equipo",
        "https://es.wikipedia.org/wiki/Competición",
        "https://es.wikipedia.org/wiki/Plato_preparado", # Food porn/Comida
        "https://es.wikipedia.org/wiki/Multitud",
        "https://es.wikipedia.org/wiki/Retrato_(fotografía)",
        
        # --- INFRAESTRUCTURA Y SISTEMAS ---
        "https://es.wikipedia.org/wiki/Ingeniería_civil",
        "https://es.wikipedia.org/wiki/Obra_pública",
        "https://es.wikipedia.org/wiki/Central_eléctrica",
        "https://es.wikipedia.org/wiki/Subestación",
        "https://es.wikipedia.org/wiki/Aeropuerto",
        "https://es.wikipedia.org/wiki/Terminal_de_autobuses",
        "https://es.wikipedia.org/wiki/Fábrica",
        "https://es.wikipedia.org/wiki/Automatización",
        "https://es.wikipedia.org/wiki/Extintor",
        "https://es.wikipedia.org/wiki/Cámara_de_seguridad",
        "https://es.wikipedia.org/wiki/Cableado_estructurado",
        "https://es.wikipedia.org/wiki/Circuito_impreso",
        "https://es.wikipedia.org/wiki/Estación_de_ferrocarril",
        "https://es.wikipedia.org/wiki/Edificio_residencial",
        
        # --- CIENCIA, NATURALEZA Y NO-ARTÍSTICO ---
        "https://es.wikipedia.org/wiki/Telescopio",
        "https://es.wikipedia.org/wiki/Observatorio_astronómico",
        "https://es.wikipedia.org/wiki/Roca_sedimentaria",
        "https://es.wikipedia.org/wiki/Mineral",
        "https://es.wikipedia.org/wiki/Microscopía",
        "https://es.wikipedia.org/wiki/Célula",
        "https://es.wikipedia.org/wiki/Radiografía",
        "https://es.wikipedia.org/wiki/Resonancia_magnética",
        "https://es.wikipedia.org/wiki/Fauna",
        "https://es.wikipedia.org/wiki/Hábitat",
        "https://es.wikipedia.org/wiki/Desastre_natural",
        "https://es.wikipedia.org/wiki/Inundación",
        "https://es.wikipedia.org/wiki/Bosque",
        "https://es.wikipedia.org/wiki/Playa",
        "https://es.wikipedia.org/wiki/Montaña",
        "https://es.wikipedia.org/wiki/Volcán",
        
        # --- OBJETOS COTIDIANOS Y TECNOLOGÍA ---
        "https://es.wikipedia.org/wiki/Computadora",
        "https://es.wikipedia.org/wiki/Teléfono_inteligente",
        "https://es.wikipedia.org/wiki/Electrodoméstico",
        "https://es.wikipedia.org/wiki/Herramienta_eléctrica",
        "https://es.wikipedia.org/wiki/Robótica",
        "https://es.wikipedia.org/wiki/Vehículo",
        "https://es.wikipedia.org/wiki/Automóvil",
        "https://es.wikipedia.org/wiki/Bicicleta",
        "https://es.wikipedia.org/wiki/Ropa",
        "https://es.wikipedia.org/wiki/Mueble"
    ]
}

def batch_download():
    print("Iniciando descarga masiva... Esto puede tardar unos minutos.")
    total_sites = sum(len(urls) for urls in sites.values())
    processed = 0
    
    for category, urls in sites.items():
        for url in urls:
            processed += 1
            print(f"\n--- [{processed}/{total_sites}] Procesando: {url} ({category}) ---")
            try:
                # Descargamos hasta 100 imágenes por sitio para tener variedad
                download_images_from_url(url, category, limit=100)
            except Exception as e:
                print(f"Error procesando sitio {url}: {e}")

    print("\n\n¡Descarga masiva completada!")
    print("Ahora ejecuta: python train_model.py")

if __name__ == "__main__":
    batch_download()