# ReadMe — Funcional 1

Este documento resume qué cambia en **Funcional 1** (renombrado desde Prueba 13) respecto a entregas anteriores del repositorio, además de incluir instrucciones de ejecución, pruebas y resolución de problemas.

## Resumen rápido

Funcional 1 refina la gestión de ventanas (1/4, 1/2 y pantalla completa), mejora la selección y asignación de medios para ventanas de fondo y corrige problemas de UX relacionados con el selector de archivos y la posición de la ventana principal.

Los cambios clave se centran en tres áreas principales:
- Lógica del selector (UI y JS en `html/selector.html`)
- Exposición de API segura (preload en `preload.js`)
- Lógica principal de ventanas y diálogo de archivos (`main.js`)

## ¿Qué cambia respecto a versiones anteriores?

- Selector de archivos:
  - Antes: el handler que abría el diálogo de selección de archivos sólo se ejecutaba cuando un contador/límite (`maxFilesNeeded`) era mayor que 0. Esto provocaba que, en modos como "1/2 pantalla" o "pantalla completa", el botón no hiciera nada y el usuario no pudiera seleccionar archivos.
  - Ahora: el selector permite abrir siempre el diálogo. Si no hay un límite forzado, se pasa un límite grande al main para habilitar multiSelección; cuando existe un requisito, se recorta la lista al número requerido. Se añadieron try/catch, mensajes y logs para facilitar diagnóstico.

- Sincronización de posición (mitades y cuartos):
  - Antes: existían condiciones en las que `posSelect` (el select visual) y la variable interna `mainPosition` podían desincronizarse, provocando que al pulsar "Abrir ventana" la posición enviada al `main.js` fuera incorrecta o siempre la izquierda.
  - Ahora: `mainPosition` se actualiza y se fuerza en el select tras cambios de tamaño; además el envío usa `mainPosition` como fuente de la verdad. Se agregó un indicador de depuración en la UI que muestra `posSelect.value` y `mainPosition` en tiempo real.

- Diálogo de archivos (IPC):
  - `preload.js` sigue exponiendo `electronAPI.selectMediaDialog(maxFiles)` mediante `ipcRenderer.invoke('open-media-dialog', maxFiles)`.
  - `main.js` maneja `open-media-dialog` y activa `multiSelections` cuando `maxFiles > 1`. El mensaje del diálogo ahora refleja el valor pasado y el `defaultPath` apunta al directorio de recursos configurado en `config.json`.

- Distribuciones avanzadas de fondos:
  - Se añadieron esquemas de distribución para 1/4 de pantalla: `none`, `three_individual`, `one_big`, `two_halves`.
  - Para `two_halves` se permite asignar un archivo fusionado que cubrirá dos áreas y un archivo individual para el cuarto restante; los bounds fusionados usan índices especiales (98, 99) para distinguirlos internamente.

## Archivos modificados relevantes

- `html/selector.html` — Ajustes en el flujo de selección, límite de archivos y sincronización de posición; añadido panel de depuración y logs.
- `preload.js` — Exposición de `electronAPI.selectMediaDialog(maxFiles)` y otros canales (sendSelection/onFileChange/onNoFile/onLoadImages).
- `main.js` — Manejo del diálogo (`ipcMain.handle('open-media-dialog')`), cálculo de posiciones (`calculatePositions`) y creación de ventanas (main + fondo), además de lógica de fusión/distribución de fondos.

## Cómo ejecutar (Windows — PowerShell)

Desde la carpeta `Funcional 1`:

```powershell
# Instalar dependencias (si no están instaladas)
npm install

# Ejecutar la app (arranca Electron)
npm start
```

Si estás desarrollando, abre DevTools en la ventana `selector` para ver los logs y la salida de depuración (Ctrl+Shift+I o Menú > Ver > Desarrollador).

## Pruebas y verificación (pasos para reproducir y comprobar corrección)

1. Inicia la app (`npm start`) y espera a que aparezca la ventana `selector`.
2. En "Elige tamaño de la ventana principal" selecciona "1/2 pantalla".
3. En "Elige posición" prueba cada opción: Mitad Izquierda, Mitad Derecha, Mitad Superior, Mitad Inferior.
   - Observa el panel de depuración bajo el selector: debe mostrar "Selector value: X — mainPosition: Y" y actualizarse al cambiar la opción.
4. Haz clic en "Seleccionar Archivos de Imagen/Video".
   - Debe abrirse un diálogo de selección. Si no hay un límite, puedes seleccionar varios archivos; si hay un límite (por ejemplo 2), sólo se tomarán los primeros 2.
   - Revisa DevTools: deberías ver logs que empiezan por `[DEBUG] Llamando a selectMediaDialog...` y el resultado.
5. Pulsa "Abrir ventana".
   - Observa la consola del proceso principal (si la tienes visible al ejecutar `npm start`) y revisa el log `[SELECCION] Recibido:` con `position` igual al valor mostrado en `mainPosition`.
   - Comprueba que la ventana principal aparece en la mitad/posición elegida. Si no, revisa si tienes múltiples monitores (el cálculo usa `screen.getAllDisplays()` y por defecto apunta al segundo monitor si existe).

## Resolución de problemas comunes

- "No se abre el diálogo de selección":
  - Abre DevTools en la ventana selector y revisa si hay un `alert(...)` indicando que `window.electronAPI` no está disponible.
  - Confirma que `preload.js` está correctamente referenciado en `main.js` al crear la ventana selector (propiedad `webPreferences.preload`).

- "Selecciono Mitad Derecha y siempre se abre en la Izquierda":
  - Revisa el panel `Selector value` bajo el select. Si el valor cambia pero la ventana se abre igual, copia el log `[DEBUG] Enviando selección...` y compáralo con el log del proceso principal `[SELECCION] Recibido:`.
  - Si `position` enviado en el evento IPC no coincide con `mainPosition`, informar y adjuntar los logs.

- "Seleccioné archivos pero no aparecen en fondos":
  - Revisa que los caminos de los archivos existan y que `main.js` pueda acceder a ellos (permisos y rutas). `main.js` convierte rutas Windows a URL con `url.pathToFileURL(...)`.

## Notas para desarrolladores

- El límite `maxFiles` que se pasa al diálogo se usa para decidir si habilitar `multiSelections` (cuando `>1`). Para pruebas locales, si la API del sistema de diálogos no acepta `undefined`, desde la UI se pasa un número grande (`100`) cuando no hay límite, para forzar multiSelección.
- La lógica de fusión usa índices especiales (98/99) para distinguir bounds fusionados del resto. Si cambias esa lógica, actualiza también el mapeo `userMediaMap` en `main.js`.

## Siguientes pasos sugeridos

- Añadir tests unitarios para `calculatePositions()` para asegurar comportamiento multi-monitor.
- Añadir validaciones UI que impidan asignar el mismo archivo a dos áreas (actualmente hay un alert, pero puede mejorarse deshabilitando la opción duplicada en el select).
- Mejorar el diálogo de selección para mostrar miniaturas al seleccionar (UX).

---

Si quieres, puedo añadir un pequeño script de prueba o snapshots de logs para automatizar la verificación de la selección y posicionamiento. ¿Te lo preparo?
