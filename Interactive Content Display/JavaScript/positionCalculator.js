// JavaScript/positionCalculator.js

const { screen } = require('electron');
const logManager = require('./logManager'); 

function calculatePositions(size, selectedPos) {
    try {
        // Obtiene todas las pantallas conectadas
        const displays = screen.getAllDisplays();
        
        if (displays.length === 0) {
             throw new Error("No display found to calculate positions.");
        }
        
        // Selecciona la segunda pantalla si existe (proyector/TV), si no, usa la principal
        const targetDisplay = displays.length > 1 ? displays[1] : displays[0];

        // Obtiene coordenadas y dimensiones de la pantalla objetivo
        const { width: sw, height: sh, x: sx, y: sy } = targetDisplay.bounds;

        console.log(`[DIAGNOSTICO] Display Target - X:${sx}, Y:${sy}, W:${sw}, H:${sh}`);

        // Define la cuadrícula base (dividiendo la pantalla en 4 cuadrantes)
        const quarterPositionsBase = [
            { x: sx, y: sy, width: sw/2, height: sh/2, index: 1 },         // Arriba-Izq
            { x: sx + sw/2, y: sy, width: sw/2, height: sh/2, index: 2 },  // Arriba-Der
            { x: sx, y: sy + sh/2, width: sw, height: sh/2, index: 3 },    // Abajo-Izq
            { x: sx + sw/2, y: sy + sh/2, width: sw/2, height: sh/2, index: 4 } // Abajo-Der
        ];
        
        // --- LÓGICA DE TAMAÑOS ---

        // CASO 3: Pantalla Completa
        if (size === "3") {
            return {
                mainBounds: { x: sx, y: sy, width: sw, height: sh, index: 0 }, 
                otherBounds: [] // No hay fondos
            };
        }
        
        // CASO 2: Media Pantalla (Vertical)
        if (size === "2") {
            // Definimos mitades verticales y horizontales
            const halfPositions = [
                 { x: sx, y: sy, width: sw/2, height: sh, index: 1 },
                 { x: sx + sw/2, y: sy, width: sw/2, height: sh, index: 2 },
                 { x: sx, y: sy, width: sw, height: sh/2, index: 3 },
                 { x: sx, y: sy + sh/2, width: sw, height: sh/2, index: 4 }
            ];

            const mainPos = halfPositions[selectedPos - 1];
            
            // Calculamos la posición "opuesta" para poner el fondo
            let otherIndex;
            if (selectedPos === 1) otherIndex = 2; 
            else if (selectedPos === 2) otherIndex = 1; 
            else if (selectedPos === 3) otherIndex = 4; 
            else if (selectedPos === 4) otherIndex = 3; 
            
            const otherPos = halfPositions[otherIndex - 1];

            return { mainBounds: mainPos, otherBounds: [otherPos] };
        }
        
        // CASO 1: Un Cuarto de Pantalla
        if (size === "1") {
            const mainPosBase = quarterPositionsBase[selectedPos - 1];
            const pixelAdj = 1; // Ajuste fino para evitar líneas negras entre ventanas

            let mainBounds = { ...mainPosBase };
            
            // Ajustes de superposición por píxel para bordes
            if (selectedPos === 1 || selectedPos === 3) {
                mainBounds.width += pixelAdj; 
            }
            if (selectedPos === 1 || selectedPos === 2) {
                mainBounds.height += pixelAdj;
            }
            if (selectedPos === 2 || selectedPos === 4) {
                mainBounds.x -= pixelAdj;
                mainBounds.width += pixelAdj;
            }
            if (selectedPos === 3 || selectedPos === 4) {
                mainBounds.y -= pixelAdj;
                mainBounds.height += pixelAdj;
            }

            // El resto de cuadrantes son "otros" (fondos)
            const others = quarterPositionsBase
                .filter(pos => pos.index !== selectedPos)
                .map(pos => pos);

            return { mainBounds: mainBounds, otherBounds: others };
        }

    } catch (error) {
        logManager.logFatal('POSITION_CALCULATION', error);
        console.error('[FATAL] Error en el cálculo de posiciones.', error);
        throw error;
    }
}

module.exports = {
    calculatePositions
};