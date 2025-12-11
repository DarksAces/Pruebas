from download_images import download_images_from_url

# Diccionario de Categoría -> Lista de URLs
# ¡AMPLIACIÓN MASIVA v5.0 - EL DATASET SUPREMO (10 CLASES)!
sites = {
    # 1. MONUMENTOS (Histórico y Turístico)
    'monuments': [
        # Listas de Patrimonio Mundial
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_España",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Italia",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Francia",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_México",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_China",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Alemania",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_el_Perú",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_la_India",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Japón",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Reino_Unido",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Grecia",
        "https://es.wikipedia.org/wiki/Anexo:Patrimonio_de_la_Humanidad_en_Egipto",
        "https://es.wikipedia.org/wiki/Anexo:Maravillas_del_mundo",
        "https://es.wikipedia.org/wiki/Siete_maravillas_del_mundo_antiguo",
        "https://es.wikipedia.org/wiki/Nuevas_siete_maravillas_del_mundo_moderno",
        # Tipos específicos
        "https://es.wikipedia.org/wiki/Pirámide",
        "https://es.wikipedia.org/wiki/Castillo",
        "https://es.wikipedia.org/wiki/Catedral",
        "https://es.wikipedia.org/wiki/Estatua",
        "https://es.wikipedia.org/wiki/Ruinas",
        "https://es.wikipedia.org/wiki/Templo",
        "https://es.wikipedia.org/wiki/Arco_de_triunfo",
        "https://es.wikipedia.org/wiki/Obelisco",
        "https://es.wikipedia.org/wiki/Fortificación",
        "https://es.wikipedia.org/wiki/Acueducto",
        "https://es.wikipedia.org/wiki/Anfiteatro",
        "https://es.wikipedia.org/wiki/Pagoda",
        "https://es.wikipedia.org/wiki/Mezquita",
        "https://es.wikipedia.org/wiki/Sinagoga"
    ],

    # 2. OBRAS DE ARTE (Museo)
    'artworks': [
        # Listas de Autores (Anexos masivos)
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Vincent_van_Gogh",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Leonardo_da_Vinci",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Miguel_Ángel_Buonarroti",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Rembrandt",
        "https://es.wikipedia.org/wiki/Anexo:Cuadros_de_Velázquez",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Francisco_de_Goya",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Salvador_Dalí",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Pablo_Picasso_1889-1900",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Frida_Kahlo",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Joaquín_Sorolla",
        "https://es.wikipedia.org/wiki/Anexo:Obras_de_Artemisia_Gentileschi",
        "https://es.wikipedia.org/wiki/Anexo:Obra_de_Gustav_Klimt",
        # Movimientos y Técnicas
        "https://es.wikipedia.org/wiki/Pintura_al_óleo",
        "https://es.wikipedia.org/wiki/Retrato_pictórico",
        "https://es.wikipedia.org/wiki/Escultura_del_Renacimiento",
        "https://es.wikipedia.org/wiki/Impresionismo",
        "https://es.wikipedia.org/wiki/Cubismo",
        "https://es.wikipedia.org/wiki/Surrealismo",
        "https://es.wikipedia.org/wiki/Arte_abstracto",
        "https://es.wikipedia.org/wiki/Arte_pop",
        "https://es.wikipedia.org/wiki/Bodegón",
        # Museos
        "https://es.wikipedia.org/wiki/Museo_del_Louvre",
        "https://es.wikipedia.org/wiki/Museo_del_Prado",
        "https://es.wikipedia.org/wiki/Galería_Uffizi",
        "https://es.wikipedia.org/wiki/Museo_Hermitage",
        "https://es.wikipedia.org/wiki/Museo_Metropolitano_de_Arte"
    ],

    # 3. GRAFFITI (Arte Urbano)
    'graffiti': [
        "https://es.wikipedia.org/wiki/Graffiti",
        "https://es.wikipedia.org/wiki/Arte_urbano",
        "https://es.wikipedia.org/wiki/Muralismo",
        "https://es.wikipedia.org/wiki/Banksy",
        "https://es.wikipedia.org/wiki/Jean-Michel_Basquiat",
        "https://es.wikipedia.org/wiki/Keith_Haring",
        "https://es.wikipedia.org/wiki/Shepard_Fairey",
        "https://es.wikipedia.org/wiki/Os_Gêmeos",
        "https://es.wikipedia.org/wiki/Blu_(artista)",
        "https://es.wikipedia.org/wiki/Tag_(graffiti)",
        "https://es.wikipedia.org/wiki/Hip_hop_(cultura)",
        "https://es.wikipedia.org/wiki/Arte_callejero",
        "https://es.wikipedia.org/wiki/Intervención_artística",
        "https://es.wikipedia.org/wiki/Sticker_art",
        "https://es.wikipedia.org/wiki/Wheatpaste"
    ],

    # 4. EDIFICIOS (Arquitectura no monumental)
    'buildings': [
        "https://es.wikipedia.org/wiki/Rascacielos",
        "https://es.wikipedia.org/wiki/Edificio_residencial",
        "https://es.wikipedia.org/wiki/Casa",
        "https://es.wikipedia.org/wiki/Oficina",
        "https://es.wikipedia.org/wiki/Apartamento",
        "https://es.wikipedia.org/wiki/Fachada",
        "https://es.wikipedia.org/wiki/Arquitectura_moderna",
        "https://es.wikipedia.org/wiki/Centro_comercial",
        "https://es.wikipedia.org/wiki/Escuela",
        "https://es.wikipedia.org/wiki/Hospital",
        "https://es.wikipedia.org/wiki/Fábrica",
        "https://es.wikipedia.org/wiki/Estadio",
        "https://es.wikipedia.org/wiki/Aeropuerto",
        "https://es.wikipedia.org/wiki/Estación_de_ferrocarril",
        "https://es.wikipedia.org/wiki/Banco_(institución)",
        "https://es.wikipedia.org/wiki/Hotel",
        "https://es.wikipedia.org/wiki/Biblioteca",
        "https://es.wikipedia.org/wiki/Teatro"
    ],

    # 5. NATURALEZA (Paisajes)
    'nature': [
        "https://es.wikipedia.org/wiki/Paisaje",
        "https://es.wikipedia.org/wiki/Bosque",
        "https://es.wikipedia.org/wiki/Selva",
        "https://es.wikipedia.org/wiki/Montaña",
        "https://es.wikipedia.org/wiki/Cordillera",
        "https://es.wikipedia.org/wiki/Playa",
        "https://es.wikipedia.org/wiki/Río",
        "https://es.wikipedia.org/wiki/Lago",
        "https://es.wikipedia.org/wiki/Desierto",
        "https://es.wikipedia.org/wiki/Cascada",
        "https://es.wikipedia.org/wiki/Volcán",
        "https://es.wikipedia.org/wiki/Glaciar",
        "https://es.wikipedia.org/wiki/Cueva",
        "https://es.wikipedia.org/wiki/Acantilado",
        "https://es.wikipedia.org/wiki/Arrecife_de_coral",
        "https://es.wikipedia.org/wiki/Parque_nacional",
        "https://es.wikipedia.org/wiki/Árbol",
        "https://es.wikipedia.org/wiki/Flor",
        "https://es.wikipedia.org/wiki/Nube",
        "https://es.wikipedia.org/wiki/Puesta_de_sol"
    ],

    # 6. DOCUMENTOS (Papel y Pantallas)
    'documents': [
        "https://es.wikipedia.org/wiki/Documento",
        "https://es.wikipedia.org/wiki/Manuscrito",
        "https://es.wikipedia.org/wiki/Periódico",
        "https://es.wikipedia.org/wiki/Revista",
        "https://es.wikipedia.org/wiki/Factura",
        "https://es.wikipedia.org/wiki/Captura_de_pantalla",
        "https://es.wikipedia.org/wiki/Libro",
        "https://es.wikipedia.org/wiki/Página_web",
        "https://es.wikipedia.org/wiki/Texto",
        "https://es.wikipedia.org/wiki/Mapa",
        "https://es.wikipedia.org/wiki/Diagrama",
        "https://es.wikipedia.org/wiki/Plano_(arquitectura)",
        "https://es.wikipedia.org/wiki/Pasaporte",
        "https://es.wikipedia.org/wiki/Documento_de_identidad",
        "https://es.wikipedia.org/wiki/Carta_(comunicación)",
        "https://es.wikipedia.org/wiki/Sobre",
        "https://es.wikipedia.org/wiki/Billete",
        "https://es.wikipedia.org/wiki/Sello_postal"
    ],

    # 7. GENTE (Personas)
    'people': [
        "https://es.wikipedia.org/wiki/Retrato_fotográfico",
        "https://es.wikipedia.org/wiki/Selfie",
        "https://es.wikipedia.org/wiki/Multitud",
        "https://es.wikipedia.org/wiki/Familia",
        "https://es.wikipedia.org/wiki/Turista",
        "https://es.wikipedia.org/wiki/Manifestación",
        "https://es.wikipedia.org/wiki/Equipo_deportivo",
        "https://es.wikipedia.org/wiki/Oficinista",
        "https://es.wikipedia.org/wiki/Niño",
        "https://es.wikipedia.org/wiki/Anciano",
        "https://es.wikipedia.org/wiki/Mujer",
        "https://es.wikipedia.org/wiki/Hombre",
        "https://es.wikipedia.org/wiki/Rostro",
        "https://es.wikipedia.org/wiki/Cuerpo_humano",
        "https://es.wikipedia.org/wiki/Bailarín",
        "https://es.wikipedia.org/wiki/Músico"
    ],

    # 8. ANIMALES (Fauna)
    'animals': [
        "https://es.wikipedia.org/wiki/Animalia",
        "https://es.wikipedia.org/wiki/Perro",
        "https://es.wikipedia.org/wiki/Gato",
        "https://es.wikipedia.org/wiki/Ave",
        "https://es.wikipedia.org/wiki/Mamífero",
        "https://es.wikipedia.org/wiki/Reptil",
        "https://es.wikipedia.org/wiki/Anfibio",
        "https://es.wikipedia.org/wiki/Pez",
        "https://es.wikipedia.org/wiki/Insecto",
        "https://es.wikipedia.org/wiki/Animal_de_compañía",
        "https://es.wikipedia.org/wiki/Animal_de_granja",
        "https://es.wikipedia.org/wiki/Fauna_de_África",
        "https://es.wikipedia.org/wiki/Zoológico",
        "https://es.wikipedia.org/wiki/León",
        "https://es.wikipedia.org/wiki/Tigre",
        "https://es.wikipedia.org/wiki/Elefante",
        "https://es.wikipedia.org/wiki/Caballo",
        "https://es.wikipedia.org/wiki/Vaca"
    ],

    # 9. COMIDA (Alimentos)
    'food': [
        "https://es.wikipedia.org/wiki/Gastronomía",
        "https://es.wikipedia.org/wiki/Plato_principal",
        "https://es.wikipedia.org/wiki/Postre",
        "https://es.wikipedia.org/wiki/Fruta",
        "https://es.wikipedia.org/wiki/Verdura",
        "https://es.wikipedia.org/wiki/Comida_rápida",
        "https://es.wikipedia.org/wiki/Restaurante",
        "https://es.wikipedia.org/wiki/Pan",
        "https://es.wikipedia.org/wiki/Queso",
        "https://es.wikipedia.org/wiki/Carne",
        "https://es.wikipedia.org/wiki/Pescado",
        "https://es.wikipedia.org/wiki/Ensalada",
        "https://es.wikipedia.org/wiki/Sopa",
        "https://es.wikipedia.org/wiki/Pizza",
        "https://es.wikipedia.org/wiki/Hamburguesa",
        "https://es.wikipedia.org/wiki/Sushi",
        "https://es.wikipedia.org/wiki/Pasta",
        "https://es.wikipedia.org/wiki/Chocolate",
        "https://es.wikipedia.org/wiki/Pastel"
    ],

    # 10. OTROS (Objetos y Varios)
    'others': [
        "https://es.wikipedia.org/wiki/Automóvil",
        "https://es.wikipedia.org/wiki/Bicicleta",
        "https://es.wikipedia.org/wiki/Motocicleta",
        "https://es.wikipedia.org/wiki/Avión",
        "https://es.wikipedia.org/wiki/Barco",
        "https://es.wikipedia.org/wiki/Tren",
        "https://es.wikipedia.org/wiki/Mueble",
        "https://es.wikipedia.org/wiki/Silla",
        "https://es.wikipedia.org/wiki/Mesa",
        "https://es.wikipedia.org/wiki/Herramienta",
        "https://es.wikipedia.org/wiki/Electrodoméstico",
        "https://es.wikipedia.org/wiki/Computadora",
        "https://es.wikipedia.org/wiki/Teléfono_inteligente",
        "https://es.wikipedia.org/wiki/Ropa",
        "https://es.wikipedia.org/wiki/Calzado",
        "https://es.wikipedia.org/wiki/Juguete",
        "https://es.wikipedia.org/wiki/Instrumento_musical",
        "https://es.wikipedia.org/wiki/Reloj"
    ]
}

def batch_download():
    print("Iniciando descarga masiva para 10 CATEGORÍAS... Esto será épico.")
    total_sites = sum(len(urls) for urls in sites.values())
    processed = 0
    
    for category, urls in sites.items():
        print(f"\n>>> INICIANDO CATEGORÍA: {category.upper()} <<<")
        for url in urls:
            processed += 1
            print(f"--- [{processed}/{total_sites}] Procesando: {url} ---")
            try:
                # Descargamos hasta 100 imágenes por sitio
                download_images_from_url(url, category, limit=100)
            except Exception as e:
                print(f"Error procesando sitio {url}: {e}")

    print("\n\n¡Descarga masiva de 10 clases completada!")
    print("Ahora ejecuta: python train_model.py")

if __name__ == "__main__":
    batch_download()