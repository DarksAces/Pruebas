--[[
    QueueManager.server.lua
    Gestiona la lógica central de la cola y los turnos.
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")

local GameConfig = require(ReplicatedStorage.Shared.GameConfig)

-- Estado del Servidor
local currentAdmin = nil
local queue = {} -- Lista de UserIds: {12345, 67890, ...}
local turnTimer = 0

-- Eventos Remotos (Rojo no crea las instancias, asumimos que se crearán o las creamos por código)
local function getRemote(name)
    local remote = ReplicatedStorage:FindFirstChild(name)
    if not remote then
        remote = Instance.new("RemoteEvent")
        remote.Name = name
        remote.Parent = ReplicatedStorage
    end
    return remote
end

local UpdateQueueEvent = getRemote("UpdateQueueEvent")
local AdminTurnStarted = getRemote("AdminTurnStarted")
local AdminTurnEnded = getRemote("AdminTurnEnded")

-- === FUNCIONES DE LA COLA ===

local function updateQueueVisuals()
    -- Envía la info de la cola a todos los clientes para actualizar su UI
    UpdateQueueEvent:FireAllClients(queue, currentAdmin)
    
    -- Teletransportar físicamente a los jugadores en la cola (Opcional, si quieres cola física)
    for i, userId in ipairs(queue) do
        local player = Players:GetPlayerByUserId(userId)
        if player and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
            -- Mover al jugador al punto "QueuePt_i" si existe
            local pointName = "QueuePt_" .. i
            local point = Workspace:FindFirstChild(pointName) or Workspace:FindFirstChild("QueueStart")
            
            if point then
                -- Lógica simple de movimiento: Un pequeño offset para que no se amontonen si es el mismo punto
                local targetCFrame = point.CFrame
                if not Workspace:FindFirstChild("QueuePt_" .. i) then 
                     targetCFrame = targetCFrame * CFrame.new(0, 0, i * 3) -- Fila india hacia atrás
                end
                
                -- Usamos MoveTo o PivotTo
                player.Character:PivotTo(targetCFrame)
            end
        end
    end
end

local function endTurn()
    if currentAdmin then
        local player = Players:GetPlayerByUserId(currentAdmin)
        if player then
            print("👑 El turno de " .. player.Name .. " ha terminado.")
            AdminTurnEnded:FireClient(player)
            
            -- Teletransportar fuera
            local exit = Workspace:FindFirstChild(GameConfig.Locations.ExitLocation)
            if player.Character and exit then
                player.Character:PivotTo(exit.CFrame + Vector3.new(0, 3, 0))
            else
                 player:LoadCharacter() -- Respawn simple si no hay salida
            end
        end
    end
    
    currentAdmin = nil
    turnTimer = 0
    
    -- Siguiente en la cola
    if #queue > 0 then
        local nextUserId = table.remove(queue, 1)
        local nextPlayer = Players:GetPlayerByUserId(nextUserId)
        
        if nextPlayer then
            currentAdmin = nextUserId
            turnTimer = GameConfig.Queue.UserTurnDuration
            
            print("👑 ¡Nuevo Admin: " .. nextPlayer.Name .. "!")
            AdminTurnStarted:FireClient(nextPlayer)
            
            -- Teletransportar al trono
            local throne = Workspace:FindFirstChild(GameConfig.Locations.AdminThrone)
            if nextPlayer.Character and throne then
                nextPlayer.Character:PivotTo(throne.CFrame + Vector3.new(0, 3, 0))
            end
        else
            -- Si el jugador se desconectó justo antes, intentamos con el siguiente
            endTurn() 
        end
    end
    
    updateQueueVisuals()
end

local function addToQueue(player)
    -- Verificar si ya está en la cola o es el admin actual
    if currentAdmin == player.UserId then return end
    for _, id in ipairs(queue) do
        if id == player.UserId then return end
    end
    
    table.insert(queue, player.UserId)
    print("➕ " .. player.Name .. " se unió a la cola. Posición: " .. #queue)
    updateQueueVisuals()
    
    -- Si no hay nadie en el trono, empieza el turno inmediatamente
    if not currentAdmin then
        endTurn() -- Esto iniciará el turno del primero (que acaba de entrar)
    end
end

local function removeFromQueue(player)
    for i, id in ipairs(queue) do
        if id == player.UserId then
            table.remove(queue, i)
            break
        end
    end
    updateQueueVisuals()
    
    if currentAdmin == player.UserId then
        endTurn()
    end
end

-- === BUCLE PRINCIPAL (TIMER) ===
task.spawn(function()
    while true do
        task.wait(1)
        if currentAdmin then
            turnTimer = turnTimer - 1
            if turnTimer <= 0 then
                endTurn()
            end
        end
    end
end)

-- === CONEXIONES ===

-- Detectar cuando un jugador toca la zona de "Unirse a Cola"
-- Esto requiere una Parte en Workspace llamada 'JoinQueuePad'
local joinPad = Workspace:FindFirstChild("JoinQueuePad")
if not joinPad then
    -- Creamos una de prueba si no existe para que no falle el script
    joinPad = Instance.new("Part")
    joinPad.Name = "JoinQueuePad"
    joinPad.Size = Vector3.new(10, 1, 10)
    joinPad.Position = Vector3.new(0, 0, 20)
    joinPad.Anchored = true
    joinPad.BrickColor = BrickColor.new("Lime green")
    joinPad.Parent = Workspace
    
    local txt = Instance.new("SurfaceGui", joinPad)
    local lbl = Instance.new("TextLabel", txt)
    lbl.Size = UDim2.new(1,0,1,0)
    lbl.Text = "TOCA PARA ENTRAR A LA COLA"
    lbl.TextScaled = true
end

joinPad.Touched:Connect(function(hit)
    local player = Players:GetPlayerFromCharacter(hit.Parent)
    if player then
        addToQueue(player)
    end
end)

Players.PlayerRemoving:Connect(removeFromQueue)

-- API Pública para otros scripts (como monetización)
_G.QueueSystem = {
    SkipToFront = function(player)
        removeFromQueue(player)
        table.insert(queue, 1, player.UserId) -- Poner el primero
        updateQueueVisuals()
        
        -- Si no hay admin, entra ya
        if not currentAdmin then
            endTurn()
        end
    end,
    
    ForceTurnEnd = function()
        endTurn()
    end
}
