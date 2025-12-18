import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyOauthError
from collections import defaultdict

# ------------------- AUTENTICACIÓN -------------------
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
    ))
except SpotifyOauthError as e:
    print(f"\n❌ Error de autenticación: {e}")
    print("Revisa tus credenciales o variables de entorno (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI).")
    exit()

# ------------------- SELECCIÓN DE FUENTE -------------------
print("\n¿Dónde quieres buscar duplicados?")
print("1️⃣  En una playlist")
print("2️⃣  En tus canciones favoritas (Liked Songs)")

choice = input("\nElige una opción (1 o 2): ").strip()

tracks = []
playlist_id = None
playlist_name = "Tus canciones favoritas ❤️"

if choice == "2":
    print("\n🔍 Obteniendo tus canciones favoritas...")
    offset = 0
    while True:
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        tracks.extend(results['items'])
        if len(results['items']) < 50:
            break
        offset += 50
else:
    playlist_url = input("\nIntroduce la URL o el ID de la playlist: ").strip()
    playlist_id = playlist_url.split("playlist/")[1].split("?")[0] if "playlist/" in playlist_url else playlist_url

    try:
        playlist = sp.playlist(playlist_id, fields="name")
        playlist_name = playlist["name"]
    except Exception as e:
        print(f"❌ Error al obtener la playlist: {e}")
        exit()

    print(f"\n🔍 Obteniendo canciones de la playlist '{playlist_name}'...")
    offset = 0
    while True:
        results = sp.playlist_items(
            playlist_id,
            offset=offset,
            fields="items.track.id,items.track.name,items.track.artists(name),next"
        )
        tracks.extend(results["items"])
        if results["next"] is None:
            break
        offset += len(results["items"])

# ------------------- DETECTAR DUPLICADOS -------------------
print(f"\nAnalizando {len(tracks)} canciones de '{playlist_name}'...")

duplicados_grupos = defaultdict(list)

for idx, item in enumerate(tracks):
    track = item["track"]
    if not track:
        continue
    name = track["name"].strip().lower()
    artists = ", ".join([a["name"].strip().lower() for a in track["artists"]])
    clave = (name, artists)
    duplicados_grupos[clave].append({"track": track, "pos": idx + 1})

duplicados_grupos = {k: v for k, v in duplicados_grupos.items() if len(v) > 1}

# ------------------- MOSTRAR Y GESTIONAR -------------------
if not duplicados_grupos:
    print("\n✅ No se encontraron duplicados. Todo limpio y ordenado 🎶")
else:
    print(f"\n⚠️ Se encontraron {len(duplicados_grupos)} grupos de duplicados.")

    # Preguntar si borrar todas manteniendo solo la primera copia
    borrar_todas = input("¿Quieres borrar todas las duplicadas manteniendo solo la primera copia? (S (mantener solo uan copia) /n (Revisar manualmente)): ").strip().lower()
    
    tracks_to_delete = []

    if borrar_todas == "s":
        for group in duplicados_grupos.values():
            # Mantener la primera canción, borrar el resto
            for item in group[1:]:
                tracks_to_delete.append(item['track']['id'])
    else:
        # Opción manual por grupo
        for clave, group in duplicados_grupos.items():
            track_info = group[0]["track"]
            print(f"\n🎵 {track_info['name']} - {', '.join([a['name'] for a in track_info['artists']])}")
            print("Duplicados encontrados:")
            for i, t in enumerate(group, 1):
                print(f"  {i}. Posición {t['pos']}: {t['track']['name']} - {', '.join([a['name'] for a in t['track']['artists']])}")
            to_delete = input("👉 Introduce los números de las canciones a borrar (ej. 1,3) o 'ninguna': ").strip()
            if to_delete.lower() != "ninguna":
                indices = [int(x.strip()) - 1 for x in to_delete.split(",") if x.strip().isdigit()]
                for i in indices:
                    if 0 <= i < len(group):
                        tracks_to_delete.append(group[i]["track"]["id"])

    # ------------------- ELIMINAR -------------------
    if tracks_to_delete:
        if playlist_id:
            # Eliminar en bloques de 100 canciones
            for i in range(0, len(tracks_to_delete), 100):
                sp.playlist_remove_all_occurrences_of_items(playlist_id, tracks_to_delete[i:i+100])
            print(f"\n✅ Se eliminaron {len(tracks_to_delete)} duplicados de '{playlist_name}', manteniendo una copia de cada canción.")
        else:
            print("\n⚠️ No se pueden eliminar canciones directamente de tus Favoritos.")
            print("Puedes crear una playlist nueva sin duplicados si lo deseas.")
            create = input("\n¿Quieres crear una nueva playlist limpia? (s/n): ").strip().lower()
            if create == "s":
                user_id = sp.me()['id']
                new_playlist = sp.user_playlist_create(user_id, f"{playlist_name} (sin duplicados)")
                unique_tracks = []
                seen = set()
                for item in tracks:
                    t = item['track']
                    if t and t['id'] not in seen:
                        seen.add(t['id'])
                        unique_tracks.append(t['id'])
                for i in range(0, len(unique_tracks), 100):
                    sp.playlist_add_items(new_playlist['id'], unique_tracks[i:i+100])
                print(f"\n✅ Playlist creada: {playlist_name} (sin duplicados)")
            else:
                print("\n👌 No se hicieron cambios.")
    else:
        print("\n❌ No se eliminó ninguna canción.")
