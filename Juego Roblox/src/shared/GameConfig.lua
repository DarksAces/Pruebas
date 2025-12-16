--[[
    Configuración Principal del Juego
    Aquí defines los IDs de tus productos, tiempos y nombres de objetos.
]]

local GameConfig = {}

-- === MONETIZACIÓN ===
-- Reemplaza estos 0 con los IDs reales de Roblox cuando los crees
GameConfig.Products = {
    SkipQueue = 0,         -- ID de Developer Product (se puede comprar muchas veces)
    InstantAdmin = 0,      -- ID de Developer Product (para saltar directo al trono)
}

GameConfig.Gamepasses = {
    VIP = 0,               -- ID de Gamepass (Nombre dorado, prioridad, etc.)
    PermAdmin = 0          -- ID de Gamepass (Admin para siempre, no necesita cola)
}

-- === CONFIGURACIÓN DE LA COLA ===
GameConfig.Queue = {
    UserTurnDuration = 60, -- Segundos que dura el turno de admin antes de echarlo
    MaxQueueSize = 50,     -- Máximo de jugadores en la cola visual
    AFKTimeout = 120,      -- Si no se mueve en X segundos, fuera de la cola
}

-- === NOMBRES EN EL WORKSPACE ===
-- Asegúrate de que existan Partes en el Workspace con estos nombres exactos
GameConfig.Locations = {
    AdminThrone = "AdminThrone",   -- Donde se teletransporta al Admin actual
    ExitLocation = "ExitSpawn",    -- Donde va al terminar su turno
    QueueStart = "QueuePt_1"       -- El primer punto de la cola
}

return GameConfig
