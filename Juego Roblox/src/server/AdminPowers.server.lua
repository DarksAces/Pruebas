--[[
    AdminPowers.server.lua
    Otorga poderes temporales cuando empieza el turno de Admin.
]]

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local Players = game:GetService("Players")

local AdminTurnStarted = ReplicatedStorage:WaitForChild("AdminTurnStarted")
local AdminTurnEnded = ReplicatedStorage:WaitForChild("AdminTurnEnded")

-- Carpeta donde guardaremos las herramientas poderosas
local adminToolsFolder = ServerStorage:FindFirstChild("AdminTools")
if not adminToolsFolder then
    adminToolsFolder = Instance.new("Folder")
    adminToolsFolder.Name = "AdminTools"
    adminToolsFolder.Parent = ServerStorage
    
    -- Creamos una herramienta de prueba "Martillo de Ban" (solo visual por ahora)
    local hammer = Instance.new("Tool")
    hammer.Name = "BanHammer"
    hammer.RequiresHandle = true
    local handle = Instance.new("Part", hammer)
    handle.Name = "Handle"
    handle.Size = Vector3.new(1, 4, 1)
    handle.BrickColor = BrickColor.new("Really red")
    hammer.Parent = adminToolsFolder
end

local function givePowers(player)
    if not player then return end
    print("⚡ OTORGANDO PODERES A " .. player.Name)
    
    -- 1. Dar Herramientas
    for _, tool in ipairs(adminToolsFolder:GetChildren()) do
        local clone = tool:Clone()
        clone.Parent = player.Backpack
    end
    
    -- 2. Efectos Visuales (Hacerlo gigante, brillo, etc)
    local char = player.Character
    if char then
        local humanoid = char:FindFirstChild("Humanoid")
        if humanoid then
            humanoid.WalkSpeed = 32 -- Más rápido
            humanoid.MaxHealth = 500
            humanoid.Health = 500
        end
        
        -- Sparkles
        local root = char:FindFirstChild("HumanoidRootPart")
        if root then
            local sparkles = Instance.new("Sparkles")
            sparkles.Name = "AdminSparkles"
            sparkles.SparkleColor = Color3.fromRGB(255, 215, 0) -- Dorado
            sparkles.Parent = root
        end
    end
    
    -- 3. Mensaje Global
    local msg = Instance.new("Message")
    msg.Text = "👑 ¡LARGA VIDA AL NUEVO ADMIN: " .. player.Name .. "! 👑"
    msg.Parent = workspace
    task.delay(5, function() msg:Destroy() end)
end

local function removePowers(player)
    if not player then return end
    print("❌ QUITANDO PODERES A " .. player.Name)
    
    -- 1. Quitar Herramientas
    player.Backpack:ClearAllChildren()
    if player.Character then 
        -- También quitar si la tiene equipada
        for _, obj in pairs(player.Character:GetChildren()) do
            if obj:IsA("Tool") then obj:Destroy() end
        end
        
        -- Quitamos efectos
        local root = player.Character:FindFirstChild("HumanoidRootPart")
        if root and root:FindFirstChild("AdminSparkles") then
            root.AdminSparkles:Destroy()
        end
        
        player.Character.Humanoid.WalkSpeed = 16
    end
end

AdminTurnStarted.OnServerEvent:Connect(function(clientWhoFired) 
    -- IMPORTANTE: Este evento lo dispara el servidor hacia el cliente en QueueManager
    -- Pero aquí queremos escuchar CUANDO el servidor decida. 
    -- Corrección: QueueManager debe usar BindableEvent para comunicarse con este script del servidor, 
    -- o simplemente invocamos la función si unificamos scripts.
    -- Dado que están separados, usaremos los RemoteEvents como señales "internas" si las disparamos a nosotros mismos?
    -- No, mejor usamos un BindableEvent para comunicación Server-Server seguro.
end)

-- Mejor enfoque: Escuchar los mismos RemoteEvents pero "OnClient" no funciona en Server.
-- CAMBIO DE ESTRATEGIA: Usar BindableEvent en ServerStorage para comunicación interna
local ServerEvents = ReplicatedStorage:FindFirstChild("ServerEvents") or Instance.new("Folder", ReplicatedStorage)
ServerEvents.Name = "ServerEvents"

local InternalTurnStart = Instance.new("BindableEvent")
InternalTurnStart.Name = "InternalTurnStart"
InternalTurnStart.Parent = ServerEvents

local InternalTurnEnd = Instance.new("BindableEvent")
InternalTurnEnd.Name = "InternalTurnEnd"
InternalTurnEnd.Parent = ServerEvents

-- Modificar QueueManager para que dispare estos Bindables
-- (Nota: Tendré que actualizar QueueManager, pero por ahora dejo este listo)

InternalTurnStart.Event:Connect(givePowers)
InternalTurnEnd.Event:Connect(removePowers)
