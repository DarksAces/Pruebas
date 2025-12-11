@echo off
echo ==========================================
echo   INICIANDO PROCESO AUTOMATICO COMPLETO
echo   1. Descargar Dataset
echo   2. Entrenar Modelo
echo   3. Subir a GitHub
echo   4. APAGAR PC
echo ==========================================
echo.

cd /d "c:\Users\Daniel\Documents\GitHub\Scripts-Prueba\Prueba Red neuronal"

echo [1/4] Activando entorno y descargando imagenes...
call venv\Scripts\activate
python download_batch.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo en la descarga. Se cancela el apagado.
    pause
    exit /b
)

echo.
echo [2/4] Entrenando modelo (Esto tardara un rato)...
python train_model.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo en el entrenamiento. Se cancela el apagado.
    pause
    exit /b
)

echo.
echo [3/4] Subiendo a GitHub...
cd ..
git add .
git commit -m "Auto: Dataset massive update + New Model trained"
git push
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al subir a GitHub. Se cancela el apagado.
    pause
    exit /b
)

echo.
echo [4/4] TAREA FINALIZADA CON EXITO.
echo ==========================================
echo   EL ORDENADOR SE APAGARA EN 60 SEGUNDOS
echo   Para cancelar, abre una terminal y escribe: shutdown /a
echo ==========================================
shutdown /s /t 60
