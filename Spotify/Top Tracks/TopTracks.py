import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- CONFIGURACIÓN Y AUTENTICACIÓN ---



CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=(CLIENT_ID),
        client_secret=(CLIENT_SECRET),
        redirect_uri=(REDIRECT_URI),
        scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
    ))
usuario_id = sp.current_user()['id']

# --- CONFIGURACIÓN DE LÍMITES ---
MAX_CANCIONES_PLAYLIST = 9900  # Dejamos margen antes del límite de 10,000
MAX_CANCIONES_POR_ARTISTA = 20  # Límite por artista (ajustable)

print(f"⚙️ Configuración actual:")
print(f"   - Máximo de canciones en playlist: {MAX_CANCIONES_PLAYLIST}")
print(f"   - Máximo de canciones por artista: {MAX_CANCIONES_POR_ARTISTA}")
cambiar = input("\n¿Quieres cambiar estos límites? [S/N]: ").strip().upper()
if cambiar == "S":
    try:
        MAX_CANCIONES_PLAYLIST = int(input("Nuevo límite total de playlist: "))
        MAX_CANCIONES_POR_ARTISTA = int(input("Nuevo límite por artista: "))
    except ValueError:
        print("Entrada inválida. Se mantienen los límites por defecto.")

# --- FILTROS DE CANCIONES (EN VIVO, REMIXES, ETC.) ---

# Lista de palabras clave a excluir (en minúsculas)
PALABRAS_CLAVE_EXCLUIR = ["live", "en vivo", "directo", "concierto", "acoustic", "acústico", "remix", "versión"] 

def es_cancion_valida(track, filtrar=False):
    """Verifica si la canción es válida, aplicando filtros si 'filtrar' es True."""
    # Verificar estructura mínima
    if not track or not track.get('name'):
        return False
    
    # Si no se quiere filtrar, siempre es válida
    if not filtrar:
        return True 

    nombre_track = track['name'].lower()
    
    # El nombre del álbum puede no estar presente en algunas llamadas (e.g., sp.artist_top_tracks)
    nombre_album = track.get('album', {}).get('name', '').lower()
    
    for palabra in PALABRAS_CLAVE_EXCLUIR:
        if palabra in nombre_track or palabra in nombre_album:
            return False
            
    return True

FILTRAR_CANCIONES = False
print(f"\n🚫 Filtros de exclusión:")
print(f"   Se excluirán canciones que contengan: {', '.join(PALABRAS_CLAVE_EXCLUIR)}")
preguntar_filtro = input("¿Quieres HABILITAR estos filtros para evitar canciones 'en vivo', 'remixes', etc.? [S/N]: ").strip().upper()
if preguntar_filtro == "S":
    FILTRAR_CANCIONES = True
    print("   ✅ Filtros de exclusión ACTIVADOS.")
else:
    print("   ❌ Filtros de exclusión DESACTIVADOS.")

# --- SELECCIÓN DE PLAYLIST ---

# Crear nueva playlist o usar existente
opcion = input("\n¿Quieres crear una nueva playlist (C) o usar una existente (E)? [C/E]: ").strip().upper()

if opcion == "C":
    nombre_playlist = input("Ingresa el nombre de la nueva playlist: ").strip()
    playlist = sp.user_playlist_create(usuario_id, nombre_playlist, public=True)
elif opcion == "E":
    playlists = sp.current_user_playlists(limit=50)['items']
    if not playlists:
        print("⚠️ No tienes playlists. Creando una nueva por defecto.")
        nombre_playlist = input("Ingresa el nombre de la nueva playlist: ").strip()
        playlist = sp.user_playlist_create(usuario_id, nombre_playlist, public=True)
    else:
        print("\nPlaylists existentes:")
        for i, pl in enumerate(playlists, 1):
            print(f"{i}. {pl['name']} ({pl['tracks']['total']} canciones)")
        
        while True:
            try:
                eleccion = int(input("Selecciona el número de la playlist: "))
                if 1 <= eleccion <= len(playlists):
                    playlist = playlists[eleccion - 1]
                    break
                else:
                    print("Número fuera de rango. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
else:
    print("Opción no válida. Creando una nueva playlist.")
    nombre_playlist = input("Ingresa el nombre de la nueva playlist: ").strip()
    playlist = sp.user_playlist_create(usuario_id, nombre_playlist, public=True)

playlist_id = playlist['id']
print(f"Usando playlist: {playlist['name']} (ID: {playlist_id})")

# --- PROCESAMIENTO DE ARTISTAS Y CANCIONES ---

# Solicitar artistas
entrada = input("\nIngresa los nombres de los artistas separados por coma: ")
artistas_lista = [nombre.strip() for nombre in entrada.split(",") if nombre.strip()]

todas_canciones_uris = []
contador_artistas_procesados = 0

for nombre_artista in artistas_lista:
    # Verificar si ya alcanzamos el límite total
    if len(todas_canciones_uris) >= MAX_CANCIONES_PLAYLIST:
        print(f"\n⚠️ Se alcanzó el límite de {MAX_CANCIONES_PLAYLIST} canciones. Deteniendo el proceso.")
        break
    
    resultados = sp.search(q=f'artist:"{nombre_artista}"', type="artist", limit=5)
    artista = None
    # Buscar una coincidencia exacta de nombre (insensible a mayúsculas/minúsculas)
    for a in resultados['artists']['items']:
        if a['name'].lower() == nombre_artista.lower():
            artista = a
            break

    if artista is None:
        print(f"⚠️ Artista '{nombre_artista}' no encontrado exactamente. Saltando.")
        continue

    artista_id = artista['id']
    artista_nombre = artista['name']
    
    canciones_artista = []
    
    # 1. Top tracks (la respuesta ya contiene info de álbum para usar el filtro)
    try:
        top_tracks = sp.artist_top_tracks(artista_id)['tracks']
        # Aplicar el filtro aquí
        valid_top_tracks = [track['uri'] for track in top_tracks if es_cancion_valida(track, FILTRAR_CANCIONES)]
        canciones_artista.extend(valid_top_tracks)
    except Exception as e:
        print(f"Error al obtener Top Tracks de {artista_nombre}: {e}")
    
    # 2. Si queremos más canciones, añadimos de álbumes populares
    if len(canciones_artista) < MAX_CANCIONES_POR_ARTISTA:
        try:
            albumes = sp.artist_albums(artista_id, album_type='album', limit=5)['items']
            for album in albumes:
                if len(canciones_artista) >= MAX_CANCIONES_POR_ARTISTA:
                    break
                
                # Obtener pistas del álbum
                pistas_album = sp.album_tracks(album['id'])['items']
                
                for pista in pistas_album:
                    if len(canciones_artista) >= MAX_CANCIONES_POR_ARTISTA:
                        break
                    
                    # Para el filtro, necesitamos la info del álbum, que a veces falta en 'album_tracks'
                    # Creamos una estructura de track temporal para el filtro
                    track_para_filtro = {
                        'name': pista['name'],
                        'album': {'name': album['name']} # Usamos el nombre del álbum que obtuvimos antes
                    }
                    
                    if es_cancion_valida(track_para_filtro, FILTRAR_CANCIONES):
                        canciones_artista.append(pista['uri'])
        except Exception as e:
            print(f"Error al obtener canciones de álbumes de {artista_nombre}: {e}")
    
    # Limitar canciones por artista
    canciones_artista = canciones_artista[:MAX_CANCIONES_POR_ARTISTA]
    todas_canciones_uris.extend(canciones_artista)
    
    contador_artistas_procesados += 1
    print(f"🎶 {contador_artistas_procesados}/{len(artistas_lista)}: {artista_nombre} - {len(canciones_artista)} canciones añadidas")

# Limitar al máximo de la playlist (en caso de que la suma exceda)
if len(todas_canciones_uris) > MAX_CANCIONES_PLAYLIST:
    print(f"\n⚠️ Recortando de {len(todas_canciones_uris)} a {MAX_CANCIONES_PLAYLIST} canciones por límite total.")
    todas_canciones_uris = todas_canciones_uris[:MAX_CANCIONES_PLAYLIST]

# --- AÑADIR CANCIONES A LA PLAYLIST ---

# Obtener canciones actuales de la playlist
canciones_existentes = []
offset = 0
print("\nObteniendo canciones existentes en la playlist...")
while True:
    response = sp.playlist_items(playlist_id, offset=offset, fields="items.track.uri,next", limit=100)
    if not response['items']:
        break
    # Filtrar items nulos
    canciones_existentes.extend([item['track']['uri'] for item in response['items'] if item['track']])
    if not response['next']:
        break
    offset += len(response['items'])

# Filtrar solo canciones nuevas
canciones_a_añadir = [uri for uri in todas_canciones_uris if uri not in canciones_existentes]

# Verificar que no excedamos el límite con las nuevas canciones
total_final = len(canciones_existentes) + len(canciones_a_añadir)
if total_final > MAX_CANCIONES_PLAYLIST:
    exceso = total_final - MAX_CANCIONES_PLAYLIST
    print(f"\n⚠️ Al añadir todas las canciones se excedería el límite por {exceso} canciones")
    canciones_a_añadir = canciones_a_añadir[:len(canciones_a_añadir) - exceso]
    print(f"   Se añadirán solo {len(canciones_a_añadir)} canciones nuevas")

# Añadir canciones nuevas en lotes de 100
print(f"Añadiendo {len(canciones_a_añadir)} canciones nuevas en lotes de 100...")
for i in range(0, len(canciones_a_añadir), 100):
    try:
        sp.playlist_add_items(playlist_id, canciones_a_añadir[i:i+100])
    except Exception as e:
        print(f"Error al añadir lote {i//100 + 1}: {e}")

# --- RESUMEN FINAL ---
total_final = len(canciones_existentes) + len(canciones_a_añadir)
print(f"\n✅ Proceso completado:")
print(f"   Canciones añadidas nuevas: {len(canciones_a_añadir)}")
print(f"   Total en playlist: {total_final}")
print(f"   Espacio restante: {MAX_CANCIONES_PLAYLIST - total_final}")

# --- MEZCLAR PLAYLIST (OPCIONAL) ---

# Mezclar playlist con restricciones suaves (opcional)
mezclar = input("\n¿Quieres mezclar la playlist ahora para evitar artistas/albúm consecutivos? [S/N]: ").strip().upper()
if mezclar == "S":
    # Obtener todas las canciones con info básica
    canciones_info = []
    offset = 0
    print("Obteniendo información de canciones para la mezcla...")
    while True:
        response = sp.playlist_items(playlist_id, offset=offset, fields="items.track(uri,name,artists,album(name)),next", limit=100)
        if not response['items']:
            break
        for item in response['items']:
            track = item['track']
            if track and track.get('artists'): # Asegurarse de que el track y los artistas existen
                canciones_info.append({
                    "uri": track['uri'],
                    "artist": track['artists'][0]['name'],
                    "album": track['album']['name'],
                    "name": track['name']
                })
        if not response['next']:
            break
        offset += len(response['items'])

    # Función de mezcla suave
    def mezclar_suave(tracks, max_intentos=5000):
        print(f"Iniciando mezcla suave de {len(tracks)} canciones...")
        best_tracks = list(tracks) # Inicializar con el orden actual por si falla
        
        for intento in range(max_intentos):
            temp_tracks = list(tracks)
            random.shuffle(temp_tracks)
            
            valido = True
            for i in range(1, len(temp_tracks)):
                # Comprobar artista consecutivo O álbum consecutivo
                if temp_tracks[i]['artist'] == temp_tracks[i-1]['artist'] or \
                   temp_tracks[i]['album'] == temp_tracks[i-1]['album']:
                    valido = False
                    break
            
            if valido:
                print(f"  ✓ Mezcla perfecta encontrada en intento {intento + 1}")
                return temp_tracks
            
            if intento % 1000 == 0 and intento > 0:
                print(f"  Intento {intento}/{max_intentos}. No se encontró mezcla perfecta aún.")

        print("  ⚠️ No se encontró una mezcla perfecta sin repeticiones. Usando una mezcla aleatoria.")
        return best_tracks # Retorna la última mezcla intentada o la inicial si no hubo intentos

    canciones_mezcladas = mezclar_suave(canciones_info)

    # Reemplazar playlist con la mezcla final (en lotes de 100)
    print("Aplicando la mezcla a la playlist...")
    
    # La API de Spotify permite reemplazar/añadir hasta 100 items por llamada.
    # Usamos replace_items para el primer lote y add_items para los subsiguientes.
    track_uris_mezcladas = [t['uri'] for t in canciones_mezcladas]
    
    if track_uris_mezcladas:
        # Primer lote: Reemplazar (vacía y añade)
        sp.playlist_replace_items(playlist_id, track_uris_mezcladas[0:100])
        print("  - Lote 1 aplicado (Reemplazo total)")

        # Lotes subsiguientes: Añadir
        for i in range(100, len(track_uris_mezcladas), 100):
            sp.playlist_add_items(playlist_id, track_uris_mezcladas[i:i+100])
            print(f"  - Lote {(i//100) + 1} aplicado")

        print(f"✅ Playlist mezclada con {len(canciones_mezcladas)} canciones.")
    else:
        print("No hay canciones para mezclar/reemplazar.")