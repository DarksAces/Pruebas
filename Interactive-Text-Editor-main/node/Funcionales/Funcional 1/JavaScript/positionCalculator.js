// JavaScript/positionCalculator.js

const { screen } = require('electron');

/*
 * positionCalculator.js
 *
 * Contiene la función calculatePositions(size, selectedPos) que devuelve los bounds
 * (x,y,width,height) para la ventana principal y, cuando proceda, un array con los
 * bounds de las ventanas de fondo.
 *
 * Entrada:
 *  - size: '1'|'2'|'3' (1 => quarter layout, 2 => half, 3 => full)
 *  - selectedPos: número (1..4) que indica la posición elegida por el usuario
 *
 * Salida: { mainBounds: {...}, otherBounds: [...] }
 *  - mainBounds tiene al menos x,y,width,height y un campo index
 *  - otherBounds es un array de bounds para las ventanas de fondo; en layouts fusionados
 *    estos bounds pueden combinarse posteriormente (p.ej. indices 98/99 en ipcHandlers)
 */

function calculatePositions(size, selectedPos) {
    // Seleccionamos display: preferencia por segundo display si existe (configurable en el futuro)
    const displays = screen.getAllDisplays();
    const targetDisplay = displays.length > 1 ? displays[1] : displays[0];

    const { width: sw, height: sh, x: sx, y: sy } = targetDisplay.bounds;

    console.log(`[DIAGNOSTICO] Display Target - X:${sx}, Y:${sy}, W:${sw}, H:${sh}`);

    // Posiciones base para quarter (1..4)
    const quarterPositionsBase = [
        { x: sx, y: sy, width: sw/2, height: sh/2, index: 1 },
        { x: sx + sw/2, y: sy, width: sw/2, height: sh/2, index: 2 },
        { x: sx, y: sy + sh/2, width: sw/2, height: sh/2, index: 3 },
        { x: sx + sw/2, y: sy + sh/2, width: sw/2, height: sh/2, index: 4 }
    ];
    
    // Fullscreen: la ventana principal ocupa todo el display; no hay fondos
    if (size === "3") {
        return {
            mainBounds: { x: sx, y: sy, width: sw, height: sh, index: 0 }, 
            otherBounds: []
        };
    }
    
    // Half layouts: definimos 4 opciones (left/right/top/bottom)
    if (size === "2") {
        const halfPositions = [
             { x: sx, y: sy, width: sw/2, height: sh, index: 1 },
             { x: sx + sw/2, y: sy, width: sw/2, height: sh, index: 2 },
             { x: sx, y: sy, width: sw, height: sh/2, index: 3 },
             { x: sx, y: sy + sh/2, width: sw, height: sh/2, index: 4 }
        ];

        const mainPos = halfPositions[selectedPos - 1];
        
        // Determinar la "otra" mitad disponible según la seleccion
        let otherIndex;
        if (selectedPos === 1) otherIndex = 2; 
        else if (selectedPos === 2) otherIndex = 1; 
        else if (selectedPos === 3) otherIndex = 4; 
        else if (selectedPos === 4) otherIndex = 3; 
        
        const otherPos = halfPositions[otherIndex - 1];

        return { mainBounds: mainPos, otherBounds: [otherPos] };
    }
    
    // Quarter layout: ajustamos 1px para evitar solapes y devolvemos las 3 otras regiones
    if (size === "1") {
        const mainPosBase = quarterPositionsBase[selectedPos - 1];
        const pixelAdj = 1; // ajuste pequeño para evitar bordes compartidos

        let mainBounds = { ...mainPosBase };
        
        // Ajustes de píxeles para evitar bordes exactos que generen problemas de rendering
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

        const others = quarterPositionsBase
            .filter(pos => pos.index !== selectedPos)
            .map(pos => pos);

        return { mainBounds: mainBounds, otherBounds: others };
    }
}

module.exports = {
    calculatePositions
};