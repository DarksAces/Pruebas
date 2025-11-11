# Prueba 14 - Editor de Texto Interactivo (Versión Modular)

Esta versión implementa una arquitectura completamente modular del editor de texto interactivo, separando las responsabilidades en módulos especializados y mejorando significativamente la estructura del código.

## Resumen de Mejoras

La versión 14 representa una reescritura completa enfocada en la modularidad y mantenibilidad:

### Nueva Estructura de Carpetas
```
Prueba14/
├── config/
│   └── config.json       # Configuración centralizada
├── html/                 # Interfaces de usuario
│   ├── background.html   # Ventana de fondo
│   ├── index.html       # Ventana principal
│   └── selector.html    # Selector de configuración
└── JavaScript/          # Lógica modular
    ├── appState.js      # Estado global
    ├── configManager.js  # Gestión de config
    ├── inactivityManager.js
    ├── ipcHandlers.js   # Comunicación IPC
    ├── main.js         # Punto de entrada
    ├── pathManager.js   # Gestión de rutas
    ├── positionCalculator.js
    ├── preload.js      # API segura
    └── windowManager.js # Gestión ventanas
```

### Módulos Principales

## Módulos JavaScript y sus Responsabilidades

1. **Estado y Configuración**:
   - `appState.js`: Gestiona el estado global de la aplicación
   - `configManager.js`: Carga/guarda configuración y última sesión
   - `pathManager.js`: Resuelve rutas de recursos y archivos

2. **Gestión de Ventanas**:
   - `windowManager.js`: Creación y control de ventanas
   - `positionCalculator.js`: Cálculo preciso de posiciones
   - `inactivityManager.js`: Timer de inactividad y reset

3. **Comunicación**:
   - `ipcHandlers.js`: Gestión centralizada de IPC
   - `preload.js`: API segura para renderers

4. **Punto de Entrada**:
   - `main.js`: Orquestación y lifecycle de la app

## Mejoras Principales

1. **Modularización Completa**:
   - Separación clara de responsabilidades
   - Mejor testabilidad y mantenimiento
   - Reducción de acoplamiento

2. **Gestión de Estado**:
   - Estado centralizado en `appState`
   - Configuración unificada
   - Persistencia mejorada

3. **Cálculo de Posiciones**:
   - Soporte multi-monitor mejorado
   - Cálculos precisos para cada modo
   - Mejor manejo de bordes

4. **Sistema de Archivos**:
   - Rutas multiplataforma
   - Vigilancia eficiente
   - Mejor gestión de recursos

## Instalación y Uso

```powershell
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Ejecutar en modo producción
npm start
```

Para desarrollo, usa las DevTools (Ctrl+Shift+I) para ver logs detallados.

## Funcionalidades Principales

1. **Gestión de Ventanas**
   - Pantalla completa
   - Mitades (horizontal/vertical)
   - Cuartos de pantalla
   - Soporte multi-monitor
   - Posicionamiento preciso

2. **Gestión de Medios**
   - Selección múltiple
   - Vista previa
   - Distribución automática
   - Sincronización de fondos

3. **Sistema de Archivos**
   - Vigilancia de cambios
   - Auto-reset por inactividad
   - Persistencia de config
   - Logs detallados

## Pruebas y Verificación

1. **Selector de Ventanas**:
   - Elige tamaño (1/4, 1/2, completa)
   - Prueba cada posición
   - Verifica cálculos en DevTools

2. **Gestión de Archivos**:
   - Selección múltiple
   - Límites según modo
   - Asignación a áreas

3. **Ventanas**:
   - Posicionamiento correcto
   - Fondos sincronizados
   - Reset automático

## Solución de Problemas

1. **Selector no Responde**:
   - Verificar `ipcHandlers.js`
   - Comprobar logs en DevTools
   - Validar config.json

2. **Ventanas Mal Posicionadas**:
   - Revisar `positionCalculator.js`
   - Verificar monitor activo
   - Comprobar bounds calculados

3. **Archivos No Cargan**:
   - Validar rutas en `pathManager.js`
   - Comprobar permisos
   - Verificar formatos soportados

## Desarrollo

1. **Convenciones**:
   - ES6+ modern JavaScript
   - Modularización estricta
   - Logging consistente

2. **Testing**:
   ```powershell
   # Tests unitarios
   npm test

   # Lint
   npm run lint
   
   # Dev con hot-reload
   npm run dev
   ```

3. **Mantenimiento**:
   - Seguir estructura modular
   - Documentar cambios
   - Actualizar tests

## Siguientes Pasos

1. **Mejoras Planificadas**:
   - Tests E2E
   - Sistema de plugins
   - UI/UX mejorada
   - Más configuraciones

2. **Bugs Conocidos**:
   - Reporte y tracking en GitHub
   - Priorización de fixes
   - Updates regulares

