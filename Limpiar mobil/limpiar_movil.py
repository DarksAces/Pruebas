import subprocess
import os
import sys

# Agregar ruta de ADB explícitamente por si no está en el PATH del sistema o no se ha refrescado
adb_path = r"C:\Users\Daniel\Downloads\platform-tools-latest-windows\platform-tools"
if os.path.isdir(adb_path) and adb_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + adb_path


def check_adb():
    """Verifica si ADB está instalado y disponible."""
    try:
        subprocess.run(["adb", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_devices():
    """Obtiene la lista de dispositivos conectados."""
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    devices = [line.split('\t')[0] for line in lines if '\tdevice' in line]
    return devices

def get_size_and_paths(device, path):
    """Obtiene el tamaño total y archivos de un patrón (soporta comodines)."""
    # du -s -k devuelve el tamaño en kilobytes por archivo/carpeta coincidente
    cmd = f"adb -s {device} shell du -a -k \"{path}\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    total_kb = 0
    found_paths = []
    
    if result.returncode != 0:
        return 0, []

    for line in result.stdout.strip().split('\n'):
        parts = line.split()
        if len(parts) >= 2:
            try:
                size = int(parts[0])
                file_path = " ".join(parts[1:]) # recosntruir ruta por si tiene espacios
                total_kb += size
                found_paths.append(file_path)
            except ValueError:
                continue
                
    return total_kb, found_paths

def human_readable_size(size_kb):
    """Convierte KB a MB o GB."""
    if size_kb > 1024 * 1024:
        return f"{size_kb / (1024 * 1024):.2f} GB"
    elif size_kb > 1024:
        return f"{size_kb / 1024:.2f} MB"
    else:
        return f"{size_kb} KB"

def find_thumbnails(device):
    """Busca carpetas .thumbnails en lugares comunes."""
    candidates = [
        "/sdcard/DCIM/.thumbnails",
        "/sdcard/DCIM/Camera/.thumbnails",
        "/sdcard/Pictures/.thumbnails",
        "/sdcard/.thumbnails"
    ]
    
    found_kb = 0
    paths = []
    
    for cand in candidates:
        kb, p = get_size_and_paths(device, cand)
        if kb > 0:
            found_kb += kb
            paths.extend(p)
            
    # Si no encuentra nada, intentar búsqueda con 'find' (puede ser lento)
    if found_kb == 0:
        print("   -> Buscando thumbnails profundamente (puede tardar)...")
        cmd = f"adb -s {device} shell find /sdcard/DCIM -name \".thumbnails\" -type d 2>/dev/null"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        for line in res.stdout.splitlines():
            kb, p = get_size_and_paths(device, line.strip())
            found_kb += kb
            paths.extend(p)
            
    return found_kb, paths

def scan_junk(device):
    """Busca archivos basura conocidos."""
    print(f"\n[*] Escaneando dispositivo: {device}...")
    
    # Rutas comunes de basura
    targets = [
        ("/sdcard/Android/data/*/cache", "Caché de Aplicaciones"),
        ("/sdcard/LOST.DIR", "Archivos corruptos/perdidos"),
        ("/sdcard/Download/*.tmp", "Archivos temporales de descargas"),
        ("/sdcard/Download/*.apk", "Instaladores APK antiguos"),
        ("/sdcard/*.log", "Archivos de registro (Logs)"),
        ("/sdcard/tmp", "Archivos temporales"),
    ]

    found_junk = []
    total_kb = 0

    for path, description in targets:
        size, paths = get_size_and_paths(device, path)
        if size > 0:
            found_junk.append({
                "path": path, # Ruta original del patrón para mostrar
                "desc": description,
                "size_kb": size,
                "real_paths": paths # Para borrar después
            })
            total_kb += size

    # Búsqueda especial para thumbnails
    thumb_kb, thumb_paths = find_thumbnails(device)
    if thumb_kb > 0:
         found_junk.append({
            "path": "Thumbnails detectados",
            "desc": "Miniaturas de Galería",
            "size_kb": thumb_kb,
            "real_paths": thumb_paths
         })
         total_kb += thumb_kb

    return found_junk, total_kb

def clean_junk(device, junk_list):
    """Elimina los archivos detectados."""
    print(f"\n[!] Iniciando limpieza en {device}...")
    cleaned_kb = 0
    
    for item in junk_list:
        print(f"  -> Eliminando: {item['desc']} ({human_readable_size(item['size_kb'])})")
        
        # En vez de borrar el patrón, borramos las rutas encontradas (más seguro con wildcards)
        # Ojo: si hay miles de archivos, el comando puede ser muy largo.
        # Mejor borrar el directorio padre si es caché completas, o usar rm con wildcard si es seguro.
        
        # Estrategia híbrida:
        # Si 'real_paths' son muchos, intentamos borrar el patrón original si es seguro.
        # Caso: /sdcard/Download/*.apk -> rm /sdcard/Download/*.apk funciona.
        
        target_path = item['path']
        
        if "*" in target_path:
             # Borrado con wildcard
             # Aseguramos comillas
             cmd = f"adb -s {device} shell rm -rf \"{target_path}\""
             subprocess.run(cmd, shell=True)
             # Asumimos borrado correcto
             cleaned_kb += item['size_kb']
             
        elif "Thumbnails" in target_path:
             # Borrar cada carpeta de thumbnails encontrada
             for p in item['real_paths']:
                 # Solo borrar si es carpeta de .thumbnails o contenido
                 if ".thumbnails" in p:
                     # rm -rf de la carpeta
                     cmd = f"adb -s {device} shell rm -rf \"{p}\""
                     subprocess.run(cmd, shell=True)
             cleaned_kb += item['size_kb']
        else:
             # Carpeta directa
             cmd = f"adb -s {device} shell rm -rf \"{target_path}\""
             subprocess.run(cmd, shell=True)
             cleaned_kb += item['size_kb']

            
    print(f"\n[OK] Limpieza completada.")
    return cleaned_kb


def main():
    print("=== Limpiador de Móvil Android ===")
    
    if not check_adb():
        print("[Error] ADB no se encuentra. Asegúrate de tener instalado 'platform-tools' y agregado al PATH.")
        print("Puedes descargarlo aquí: https://developer.android.com/studio/releases/platform-tools")
        input("Presiona Enter para salir...")
        return

    devices = get_devices()
    if not devices:
        print("[!] No se detectan dispositivos.")
        print(" Asegúrate de:")
        print("  1. Conectar el móvil por USB.")
        print("  2. Activar 'Depuración USB' en Opciones de Desarrollador.")
        print("  3. Aceptar la huella digital RSA en la pantalla del móvil si aparece.")
        input("Presiona Enter para salir...")
        return

    device = devices[0]
    if len(devices) > 1:
        print(f"[!] Múltiples dispositivos detectados. Usando el primero: {device}")
    else:
        print(f"[*] Dispositivo conectado: {device}")

    print("\nBuscando archivos inútiles...")
    junk_list, total_kb = scan_junk(device)

    if total_kb == 0:
        print("[*] Tu móvil parece estar limpio o no tenemos acceso a las carpetas de sistema.")
        return

    print("\n--- Resumen de Basura Encontrada ---")
    for item in junk_list:
        print(f" - {item['desc']}: {human_readable_size(item['size_kb'])}")
    
    print(f"\nTotal a liberar: {human_readable_size(total_kb)}")
    
    confirm = input("\n¿Deseas eliminar estos archivos? (s/n): ").lower()
    if confirm == 's':
        cleaned = clean_junk(device, junk_list)
        print(f"\nEspacio liberado: {human_readable_size(cleaned)}")
        
        # Opción extra: Limpiar caché de apps genérico (Comando peligroso si no se tiene cuidado, pero rm -rf de caché es seguro)
        print("\n¿Quieres intentar limpiar la caché de TODAS las aplicaciones en /Android/data/?")
        print("Nota: En Android 11+ puede fallar por permisos.")
        deep_clean = input("¿Limpieza profunda de caché de apps? (s/n): ").lower()
        if deep_clean == 's':
            print("Limpiando /sdcard/Android/data/*/cache ...")
            subprocess.run(f"adb -s {device} shell rm -rf /sdcard/Android/data/*/cache", shell=True)
            print("Comando enviado.")

    else:
        print("Operación cancelada.")

if __name__ == "__main__":
    main()
