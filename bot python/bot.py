# ingesta_bot_ultra.py

import firebase_admin
from firebase_admin import credentials, firestore
import time
import random
import datetime
import json
from io import StringIO

# --- CONFIGURACIÓN DE CREDENCIALES DIRECTAS ---
# 🚨 ESTE DICCIONARIO CONTIENE TUS CREDENCIALES PRIVADAS. MANTÉNELO SEGURO.
SERVICE_ACCOUNT_INFO = {
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "universe_domain": ""
}

# Atribución solicitada
ADMIN_BOT_AUTHOR = "DarkAce" 
ADMIN_BOT_ID = "DarkAceID" 

# --- DATOS GLOBALES PARA INGESTAR (35+ EJEMPLOS VARIADOS) ---
SITIOS_FAMOSOS_PARA_INGESTAR = [
 ]

# Inicializar Firebase
try:
    # 💡 CAMBIO CLAVE: Cargar las credenciales del diccionario
    cred = credentials.Certificate(SERVICE_ACCOUNT_INFO) 
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Conexión a Firebase Admin establecida directamente.")
except Exception as e:
    print(f"❌ Error al inicializar Firebase Admin: {e}")
    print("VERIFICA que el DICCIONARIO SERVICE_ACCOUNT_INFO esté COMPLETO y CORRECTO.")
    exit()

def is_duplicated(lat, lng):
    """Verifica si ya existe un sitio en Firestore con coordenadas similares."""
    epsilon = 0.00001
    
    query = db.collection('sitios') \
        .where('lat', '>', lat - epsilon) \
        .where('lat', '<', lat + epsilon) \
        .where('lng', '>', lng - epsilon) \
        .where('lng', '<', lng + epsilon) \
        .limit(1)

    return query.get()

def upload_site_to_firestore(site_data):
    """Añade un documento a la colección 'sitios' con un ID generado automáticamente."""
    
    # 1. Verificar duplicados
    existing_sites = is_duplicated(site_data['lat'], site_data['lng'])
    if existing_sites:
        print(f"⚠️ SITIO IGNORADO (DUPLICADO): '{site_data['title']}' ya existe.")
        return False

    # 2. El ID es generado automáticamente con .document()
    doc_ref = db.collection('sitios').document() 
    
    data = {
        'title': site_data['title'],
        'lat': site_data['lat'],
        'lng': site_data['lng'],
        'type': site_data['type'],
        'imageUrl': site_data['imageUrl'],
        
        # Atribución solicitada
        'author': ADMIN_BOT_AUTHOR, 
        'authorId': ADMIN_BOT_ID, 
        
        'createdAt': firestore.SERVER_TIMESTAMP,
    }

    try:
        doc_ref.set(data)
        print(f"✅ SITIO SUBIDO: '{site_data['title']}' - ID automático: {doc_ref.id}")
        return True
    except Exception as e:
        print(f"❌ ERROR al subir {site_data['title']}: {e}")
        return False


# --- INGESTA PRINCIPAL ---
if __name__ == "__main__":
    print(f"\n--- Iniciando Ingestión Ultra Masiva de {len(SITIOS_FAMOSOS_PARA_INGESTAR)} Sitios ---")
    
    successful_uploads = 0
    for site in SITIOS_FAMOSOS_PARA_INGESTAR:
        if upload_site_to_firestore(site):
            successful_uploads += 1
        
        # Pausa para evitar sobrecargar Firestore
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"\n--- Proceso Finalizado. {successful_uploads} sitios subidos por {ADMIN_BOT_AUTHOR}. ---")