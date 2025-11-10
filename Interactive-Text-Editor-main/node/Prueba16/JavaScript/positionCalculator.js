// JavaScript/positionCalculator.js

const { screen } = require('electron');
const windowManager = require('./windowManager'); // Para obtener el display primario

function calculatePositions(size, selectedPos) {
    // Usamos el display PRIMARIO para la ventana principal
    const targetDisplay = windowManager.getPrimaryDisplay();
    if (!targetDisplay) {
        console.error('[CALCULATOR] No se pudo obtener el display principal.');
        return { mainBounds: { x: 0, y: 0, width: 800, height: 600, index: 0 }, otherBounds: [] };
    }

    const { width: sw, height: sh, x: sx, y: sy } = targetDisplay.bounds;

    console.log(`[DIAGNOSTICO] Display Target (MAIN) - X:${sx}, Y:${sy}, W:${sw}, H:${sh}`);

    // Solo se calcula la posición de la ventana principal (index.html)
    // Las ventanas de fondo se gestionarán de forma diferente en ipcHandlers.js

    const quarterPositionsBase = [
        { x: sx, y: sy, width: sw/2, height: sh/2, index: 1 },
        { x: sx + sw/2, y: sy, width: sw/2, height: sh/2, index: 2 },
        { x: sx, y: sy + sh/2, width: sw/2, height: sh/2, index: 3 },
        { x: sx + sw/2, y: sy + sh/2, width: sw/2, height: sh/2, index: 4 }
    ];
    
    if (size === "3") {
        return {
            mainBounds: { x: sx, y: sy, width: sw, height: sh, index: 0 }, 
            otherBounds: [] // No hay otros bounds en el display principal
        };
    }
    
    if (size === "2") {
        const halfPositions = [
             { x: sx, y: sy, width: sw/2, height: sh, index: 1 },
             { x: sx + sw/2, y: sy, width: sw/2, height: sh, index: 2 },
             { x: sx, y: sy, width: sw, height: sh/2, index: 3 },
             { x: sx, y: sy + sh/2, width: sw, height: sh/2, index: 4 }
        ];

        const mainPos = halfPositions[selectedPos - 1];
        
        return { mainBounds: mainPos, otherBounds: [] }; // No hay otros bounds en el display principal
    }
    
    if (size === "1") {
        const mainPosBase = quarterPositionsBase[selectedPos - 1];
        const pixelAdj = 1;

        let mainBounds = { ...mainPosBase };
        
        // Ajustes por pixel (se mantienen)
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

        return { mainBounds: mainBounds, otherBounds: [] }; // No hay otros bounds en el display principal
    }
}

module.exports = {
    calculatePositions
};