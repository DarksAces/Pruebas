# Clasificador de Imágenes: Monumentos, Arte y Otros

Este proyecto utiliza una Red Neuronal Convolucional (CNN) para clasificar imágenes en tres categorías.

## Estructura de Carpetas

Antes de empezar, debes colocar tus imágenes en las carpetas correspondientes dentro de `dataset/`.

```
Prueba Red neuronal/
├── dataset/
│   ├── train/              <-- 80% de tus imágenes aquí
│   │   ├── monuments/
│   │   ├── artworks/
│   │   └── others/
│   └── validation/         <-- 20% de tus imágenes aquí
│       ├── monuments/
│       ├── artworks/
│       └── others/
├── train_model.py
├── predict.py
├── requirements.txt
└── README.md
```

## Instrucciones

### 1. Instalación
He creado un entorno virtual para ti que usa Python 3.10. Para activarlo:

**En PowerShell:**
```powershell
.\venv\Scripts\activate
```
Verás que aparece `(venv)` al principio de la línea. ¡Eso significa que estás listo!

### 2. Preparar Datos
Coloca muchas imágenes (mínimo 50-100 por categoría para probar) en las carpetas de `dataset/train` y `dataset/validation`.

### 3. Entrenar el Modelo
Asegúrate de tener el entorno activado `(venv)` y ejecuta:
```bash
python train_model.py
```
*(Si no quieres activar el entorno, puedes usar directamente `.\venv\Scripts\python train_model.py`)*

Esto creará un archivo `model.h5` al finalizar.

### 4. Probar / Predecir
Para clasificar una nueva imagen:
```bash
python predict.py "ruta/a/tu/imagen.jpg"
```
