@echo off
echo ===========================================
echo INICIANDO PROCESO AUTOMATICO (ARTE AI)
echo ===========================================

echo.
echo [1/3] DESCARGANDO IMAGENES (Esto puede tardar)...
.\venv\Scripts\python.exe download_batch.py
if %errorlevel% neq 0 (
    echo ERROR en la descarga. Deteniendo.
    pause
    exit /b %errorlevel%
)

echo.
echo [1.5/3] DESCARGANDO DE JOVI (FIREBASE LEGACY)...
.\venv\Scripts\python.exe download_firebase.py

echo.
echo [2/3] LIMPIANDO DATASET (Borrando imagenes corruptas)...
.\venv\Scripts\python.exe clean_dataset.py
if %errorlevel% neq 0 (
    echo ERROR en la limpieza. Deteniendo.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/3] ENTRENANDO MODELO...
.\venv\Scripts\python.exe train_model.py
if %errorlevel% neq 0 (
    echo ERROR en el entrenamiento.
    pause
    exit /b %errorlevel%
)

echo.
echo ===========================================
echo PROCESO COMPLETADO CON EXITO!
echo ===========================================

echo.
echo [4/3] SUBIENDO DATASET A NUBE (REDTRAIN - COMPRESION)...
.\venv\Scripts\python.exe upload_dataset.py
if %errorlevel% neq 0 (
    echo ERROR en la subida a nube. (No critico)
)

echo.
echo TODO TERMINADO.
echo ===========================================
pause
