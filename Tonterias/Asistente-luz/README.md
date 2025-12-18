# Consulta Luz & Control de Aires Automático

Este proyecto en **Python** permite consultar el precio de la luz desde [Energía XXI](https://www.energiaxxi.com/) y controlar automáticamente los aires acondicionados conectados a **Home Assistant**.

- Si el precio baja de un umbral definido, el aire se enciende.  
- Si el precio sube por encima del umbral, el aire se apaga.  
- Se soportan múltiples aires automáticamente.  


---

## 🛠️ Requisitos

- Python 3.9+  
- [Playwright](https://playwright.dev/python/) para la consulta web.  
- [Requests](https://pypi.org/project/requests/) para interactuar con Home Assistant.  
- Home Assistant con **token long-lived** y aires registrados como `climate`.  

---

## ⚙️ Instalación

1. Clonar o descargar el repositorio:

```bash
git clone https://github.com/usuario/consulta-luz.git
cd consulta-luz
```

2. Instalar dependencias:
3. 
```bash
pip install playwright requests
python -m playwright install
```

Editar el script consulta_luz.py:

HOME_ASSISTANT_URL_BASE → IP o dominio de tu Home Assistant.

TOKEN → tu token long-lived.

UMBRAL → precio en €/kWh que activa el encendido/apagado de los aires.
