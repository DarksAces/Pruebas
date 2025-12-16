--[[
    QueueManager.server.lua (STRICT VERSION)
    - Bloquea movimiento.
    - Soporta skip de 1 en 1.
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")

local GameConfig = require(ReplicatedStorage.Shared.GameConfig)

-- Estado
local currentAdmin = nil
local queue = {} -- {UserId1, UserId2, ...}
local turnTimer = 0

-- Comunicación Interna
local ServerEvents = ReplicatedStorage:FindFirstChild("ServerEvents")
if not ServerEvents then
    ServerEvents = Instance.new("Folder", ReplicatedStorage)
    ServerEvents.Name = "ServerEvents"
end

local InternalTurnStart = Instance.new("BindableEvent", ServerEvents)
InternalTurnStart.Name = "InternalTurnStart"
local InternalTurnEnd = Instance.new("BindableEvent", ServerEvents)
InternalTurnEnd.Name = "InternalTurnEnd"

local UpdateQueueEvent = ReplicatedStorage:FindFirstChild("UpdateQueueEvent") or Instance.new("RemoteEvent", ReplicatedStorage)
UpdateQueueEvent.Name = "UpdateQueueEvent"
local AdminTurnStarted = ReplicatedStorage:FindFirstChild("AdminTurnStarted") or Instance.new("RemoteEvent", ReplicatedStorage)
AdminTurnStarted.Name = "AdminTurnStarted"
local AdminTurnEnded = ReplicatedStorage:FindFirstChild("AdminTurnEnded") or Instance.new("RemoteEvent", ReplicatedStorage)
AdminTurnEnded.Name = "AdminTurnEnded"

-- === FUNCIONES DE MOVIMIENTO ===

local function lockPlayer(player, targetPart)
    if player.Character and player.Character:FindFirstChild("HumanoidRootPart") and targetPart then
        local hrp = player.Character.HumanoidRootPart
        local hum = player.Character.Humanoid
        
        -- Opción 1: Teleport + Anchor (Más seguro)
        hrp.CFrame = targetPart.CFrame + Vector3.new(0, 3, 0)
        -- hrp.Anchored = true -- Descomentar si quieres que sea IMPOSIBLE moverse (puede causar lag visual)
        
        -- Opción 2: WalkSpeed 0 (Más suave)
        hum.WalkSpeed = 0
        hum.JumpPower = 0
    end
end

local function unlockPlayer(player)
    if player.Character and player.Character:FindFirstChild("Humanoid") then
        local hum = player.Character.Humanoid
        hum.WalkSpeed = 16
        hum.JumpPower = 50
        player.Character.HumanoidRootPart.Anchored = false
    end
end

local function updateQueueVisuals()
    UpdateQueueEvent:FireAllClients(queue, currentAdmin)
    
    -- Mover a cada jugador a su plataforma correspondiente
    local queueFolder = Workspace:FindFirstChild("QueueSystem")
    
    for i, userId in ipairs(queue) do
        local player = Players:GetPlayerByUserId(userId)
        if player then
            local platName = "QueuePt_" .. i
            local plat = queueFolder and queueFolder:FindFirstChild(platName)
            
            if plat then
                lockPlayer(player, plat)
            else
                -- Si hay más gente que plataformas, se quedan en la última
                local lastPlat = queueFolder:FindFirstChild("QueuePt_" .. #queueFolder:GetChildren())
                if lastPlat then lockPlayer(player, lastPlat) end
            end
        end
    end
end

local function endTurn()
    if currentAdmin then
        local player = Players:GetPlayerByUserId(currentAdmin)
        if player then
            print("👑 Fin de turno: " .. player.Name)
            AdminTurnEnded:FireClient(player)
            InternalTurnEnd:Fire(player)
            unlockPlayer(player)
            
            local exit = Workspace:FindFirstChild("QueueSystem") and Workspace.QueueSystem:FindFirstChild("ExitSpawn")
            if exit then
                player.Character:PivotTo(exit.CFrame + Vector3.new(0, 3, 0))
            else
                player:LoadCharacter()
            end
        end
    end
    
    currentAdmin = nil
    turnTimer = 0
    
    if #queue > 0 then
        local nextUserId = table.remove(queue, 1)
        local nextPlayer = Players:GetPlayerByUserId(nextUserId)
        
        if nextPlayer then
            currentAdmin = nextUserId
            turnTimer = GameConfig.Queue.UserTurnDuration
            
            print("👑 Nuevo Admin: " .. nextPlayer.Name)
            AdminTurnStarted:FireClient(nextPlayer)
            InternalTurnStart:Fire(nextPlayer)
            
            local throne = Workspace:FindFirstChild("QueueSystem") and Workspace.QueueSystem:FindFirstChild("AdminThrone")
            if throne then
                unlockPlayer(nextPlayer) -- En el trono sí puede moverse
                nextPlayer.Character:PivotTo(throne.CFrame + Vector3.new(0, 3, 0))
            end
        else
            endTurn()
        end
    end
    updateQueueVisuals()
end

local function addToQueue(player)
    -- Validación simple
    if currentAdmin == player.UserId then return end
    for _, id in ipairs(queue) do if id == player.UserId then return end end
    
    table.insert(queue, player.UserId)
    updateQueueVisuals()
    
    if not currentAdmin then endTurn() end
end

local function removeFromQueue(player)
    for i, id in ipairs(queue) do
        if id == player.UserId then
            table.remove(queue, i)
            unlockPlayer(player)
            break
        end
    end
    updateQueueVisuals()
    if currentAdmin == player.UserId then endTurn() end
end

-- === SKIP LOGIC (INTERCAMBIO) ===
_G.QueueSystem = {
    SkipOneSpot = function(player)
        -- Buscar posición actual
        local myIndex = nil
        for i, id in ipairs(queue) do
            if id == player.UserId then
                myIndex = i
                break
            end
        end
        
        if myIndex and myIndex > 1 then
            -- Intercambiar con el de delante (myIndex - 1)
            local targetIndex = myIndex - 1
            local otherUserId = queue[targetIndex]
            
            queue[targetIndex] = player.UserId
            queue[myIndex] = otherUserId
            
            print("🔀 " .. player.Name .. " saltó del puesto " .. myIndex .. " al " .. targetIndex)
            updateQueueVisuals() -- Esto recalculará las posiciones físicas
            return true
        elseif myIndex == 1 then
             -- Si ya es primero, quizás quiera forzar el fin del turno del admin para entrar YA?
             -- Por ahora, no hace nada si ya eres primero
             return false
        end
    end,
    ForceTurnEnd = function() endTurn() end -- Para el pase de Admin Instantáneo
}

-- === LOOP & LISTENERS ===
task.spawn(function()
    while true do
        task.wait(1)
        if currentAdmin then
            turnTimer = turnTimer - 1
            if turnTimer <= 0 then endTurn() end
        end
    end
end)

local joinPad = Workspace:WaitForChild("JoinQueuePad", 10)
if joinPad then
    joinPad.Touched:Connect(function(hit)
        local player = Players:GetPlayerFromCharacter(hit.Parent)
        if player then addToQueue(player) end
    end)
end

Players.PlayerRemoving:Connect(removeFromQueue)
