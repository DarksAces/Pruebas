import asyncio
from playwright.async_api import async_playwright
import requests

# Configuración
URL_LUZ = "https://www.energiaxxi.com/es/facturas/como-saber-cual-es-el-precio-de-la-luz"
UMBRAL = 0.15  # Precio en €/kWh

# Home Assistant
HOME_ASSISTANT_URL_BASE = "http://IP_DE_HOME_ASSISTANT:8123/api/services/climate/"
TOKEN = "TU_TOKEN_AQUI"
AIRES = ["climate.aire_salon", "climate.aire_habitacion"]  # lista de aires
estado_aires = {aire: False for aire in AIRES}  # False = apagado, True = encendido

# Función para encender/apagar aires
def controlar_aires(encender):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    for aire in AIRES:
        if estado_aires[aire] != encender:  # solo enviar si hay cambio
            accion = "turn_on" if encender else "turn_off"
            url = HOME_ASSISTANT_URL_BASE + accion
            data = {"entity_id": aire}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"{'Encendido' if encender else 'Apagado'} {aire}")
                estado_aires[aire] = encender
            else:
                print(f"Error {accion} {aire}: {response.status_code} {response.text}")

# Función principal para obtener precio
async def obtener_precio():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL_LUZ)
        try:
            await page.wait_for_selector("p.price", timeout=15000)
            precio_elemento = await page.query_selector("p.price")
            if precio_elemento:
                precio_texto = (await precio_elemento.text_content()).strip()
                print(f"Precio actual de la luz: {precio_texto}")
                
                # Convertir a float
                precio_num = float(precio_texto.replace("€/kWh", "").replace(",", ".").strip())
                
                # Controlar aires según precio
                if precio_num < UMBRAL:
                    controlar_aires(True)
                else:
                    controlar_aires(False)
            else:
                print("No se pudo encontrar el precio de la luz.")
        except Exception as e:
            print(f"Error al obtener el precio: {e}")
        await browser.close()

# Bucle principal
async def main():
    while True:
        await obtener_precio()
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
