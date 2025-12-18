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
    print(f"\n[*] Escaneando archivos basura comunes en: {device}...")
    
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

def scan_large_folders(device):
    """Escanea carpetas que suelen ocupar mucho espacio (WhatsApp, Telegram, etc)."""
    print("\n[*] Realizando escaneo profundo de carpetas grandes...")
    
    # Rutas probables de WhatsApp (varían según versión de Android)
    wa_paths = [
        "/sdcard/WhatsApp/Media/WhatsApp Video/Sent",
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Video/Sent",
        "/sdcard/WhatsApp/Media/WhatsApp Images/Sent",
        "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images/Sent",
        "/sdcard/Telegram/Telegram Video",
        "/sdcard/Telegram/Telegram Audio",
    ]
    
    found_heavy = []
    
    for path in wa_paths:
        kb, paths = get_size_and_paths(device, path)
        if kb > 1024: # Solo mostrar si ocupa más de 1MB
            desc = f"Archivos enviados de {path.split('/')[-2]} ({path.split('/')[-1]})"
            found_heavy.append({
                "path": path,
                "desc": desc,
                "size_kb": kb,
                "real_paths": paths,
                "is_dangerous": True # Marcar como requiere cuidado
            })
            
    # Escaneo de nivel superior para ver qué ocupa más espacio
    print("   -> Analizando uso de almacenamiento general (Top 5 carpetas)...")
    cmd = f"adb -s {device} shell du -d 1 -k /sdcard/ 2>/dev/null"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    top_dirs = []
    for line in res.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try:
                kb = int(parts[0])
                path = " ".join(parts[1:])
                if path.strip() == "/sdcard/": continue
                if kb > 100 * 1024: # Más de 100MB
                     top_dirs.append((kb, path))
            except:
                pass
                
    top_dirs.sort(key=lambda x: x[0], reverse=True)
    
    return found_heavy, top_dirs

def clean_item(device, item):
    """Limpia un item específico con los métodos apropiados."""
    cmd_list = []
    
    # Decidir método de borrado
    if "*" in item['path']:
         cmd_list.append(f"adb -s {device} shell rm -rf \"{item['path']}\"")
    elif "Thumbnails" in item['desc']:
         for p in item['real_paths']:
             if ".thumbnails" in p:
                 cmd_list.append(f"adb -s {device} shell rm -rf \"{p}\"")
    else:
         # Carpeta directa
         cmd_list.append(f"adb -s {device} shell rm -rf \"{item['path']}\"")

    cleaned_kb = 0
    success = True
    
    for cmd in cmd_list:
        res = subprocess.run(cmd, shell=True, capture_output=True)
        if res.returncode != 0:
            success = False
            # print(f"Error: {res.stderr.decode()}")
    
    if success:
        return item['size_kb']
    return 0

def main():
    print("=== Limpiador de Móvil Android ===")
    
    if not check_adb():
        print("[Error] ADB no se encuentra. Asegúrate de tener instalado 'platform-tools' compruébalo.")
        input("Presiona Enter para salir...")
        return

    devices = get_devices()
    if not devices:
        print("[!] No se detectan dispositivos.")
        input("Presiona Enter para salir...")
        return

    device = devices[0]
    print(f"[*] Dispositivo conectado: {device}")

    # 1. Escaneo de Basura Estándar
    junk_list, junk_kb = scan_junk(device)
    
    # 2. Escaneo Profundo
    heavy_list, top_dirs = scan_large_folders(device)
    
    total_cleaned = 0
    
    print("\n=== Resultados del Análisis ===")
    
    # Procesar Basura Común
    if junk_list:
        print("\n--- Archivos Basura (Seguro de borrar) ---")
        for item in junk_list:
            size_str = human_readable_size(item['size_kb'])
            print(f"\nEncontrado: {item['desc']}")
            print(f"Ubicación: {item['path']}")
            print(f"Tamaño: {size_str}")
            
            resp = input(f"¿Quieres eliminar esto? ({size_str}) (s/n): ").lower()
            if resp == 's':
                cleaned = clean_item(device, item)
                total_cleaned += cleaned
                print(" -> Eliminado.")
            else:
                print(" -> Omitido.")
    else:
        print("\nNo se encontró basura común.")

    # Procesar Carpetas Pesadas (Deep Scan)
    if heavy_list:
        print("\n--- Carpetas Grandes (Archivos Enviados de WhatsApp/Telegram) ---")
        print("NOTA: Esto borrará archivos que HAS ENVIADO (videos, fotos).")
        for item in heavy_list:
            size_str = human_readable_size(item['size_kb'])
            print(f"\nEncontrado: {item['desc']}")
            print(f"Ubicación: {item['path']}")
            print(f"Tamaño: {size_str}")
            
            resp = input(f"¿Quieres eliminar esto? ({size_str}) (s/n): ").lower()
            if resp == 's':
                cleaned = clean_item(device, item)
                total_cleaned += cleaned
                print(" -> Eliminado.")
            else:
                print(" -> Omitido.")

    # Mostrar carpetas grandes informativas
    if top_dirs:
        print("\n--- ¿Dónde están tus 12GB? (Top Carpetas) ---")
        print("Estas carpetas ocupan mucho espacio. Revisa manualmente.")
        for size_kb, path in top_dirs[:5]:
             print(f" - {path}: {human_readable_size(size_kb)}")

    print(f"\n========================================")
    print(f"Limpieza finalizada.")
    print(f"Espacio total liberado: {human_readable_size(total_cleaned)}")
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
