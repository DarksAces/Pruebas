--[[
    QueueUI.client.lua
    Muestra la posición en la cola y botones de compra.
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local MarketplaceService = game:GetService("MarketplaceService")

local GameConfig = require(ReplicatedStorage.Shared.GameConfig)
local player = Players.LocalPlayer

local UpdateQueueEvent = ReplicatedStorage:WaitForChild("UpdateQueueEvent")

-- === CREAR GUI (Por Código) ===
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "QueueHUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = player:WaitForChild("PlayerGui")

local frame = Instance.new("Frame", screenGui)
frame.Size = UDim2.new(0, 300, 0, 150)
frame.Position = UDim2.new(0.5, -150, 0.8, -150) -- Abajo centro
frame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
frame.BorderSizePixel = 0
frame.BackgroundTransparency = 0.2

local uiCorner = Instance.new("UICorner", frame)
uiCorner.CornerRadius = UDim.new(0, 12)

local statusLabel = Instance.new("TextLabel", frame)
statusLabel.Size = UDim2.new(1, 0, 0.4, 0)
statusLabel.BackgroundTransparency = 1
statusLabel.TextColor3 = Color3.new(1, 1, 1)
statusLabel.Font = Enum.Font.GothamBold
statusLabel.TextSize = 20
statusLabel.Text = "Esperando info..."

local currentAdminLabel = Instance.new("TextLabel", frame)
currentAdminLabel.Size = UDim2.new(1, 0, 0.2, 0)
currentAdminLabel.Position = UDim2.new(0, 0, 0.4, 0)
currentAdminLabel.BackgroundTransparency = 1
currentAdminLabel.TextColor3 = Color3.fromRGB(255, 215, 0) -- Gold
currentAdminLabel.Font = Enum.Font.Gotham
statusLabel.TextSize = 16
currentAdminLabel.Text = "Admin Actual: Nadie"

-- BOTÓN SKIP (Solo aparece si estás en cola)
local skipBtn = Instance.new("TextButton", frame)
skipBtn.Size = UDim2.new(0.9, 0, 0.3, 0)
skipBtn.Position = UDim2.new(0.05, 0, 0.65, 0)
skipBtn.BackgroundColor3 = Color3.fromRGB(0, 170, 0)
skipBtn.Font = Enum.Font.GothamBlack
skipBtn.TextColor3 = Color3.new(1,1,1)
skipBtn.TextSize = 18
skipBtn.Text = "¡SALTAR COLA! (R$)"
Instance.new("UICorner", skipBtn).CornerRadius = UDim.new(0, 8)

skipBtn.MouseButton1Click:Connect(function()
    MarketplaceService:PromptProductPurchase(player, GameConfig.Products.SkipQueue)
end)

-- === ACTUALIZAR INTERFAZ ===

UpdateQueueEvent.OnClientEvent:Connect(function(queueTable, currentAdminId)
    -- Buscar mi posición
    local myPos = nil
    for i, id in ipairs(queueTable) do
        if id == player.UserId then
            myPos = i
            break
        end
    end
    
    -- Actualizar Texto Status
    if myPos then
        statusLabel.Text = "Tu Posición: #" .. myPos
        statusLabel.TextColor3 = Color3.new(1,1,1)
        skipBtn.Visible = true -- Solo puedes saltar si estás en la cola
    elseif currentAdminId == player.UserId then
        statusLabel.Text = "¡ERES EL ADMIN SUPREMO!"
        statusLabel.TextColor3 = Color3.fromRGB(255, 0, 0)
        skipBtn.Visible = false
    else
        statusLabel.Text = "¡Toca el pad verde para unirte!"
        statusLabel.TextColor3 = Color3.fromRGB(150, 150, 150)
        skipBtn.Visible = false
    end
    
    -- Actualizar Texto Admin
    if currentAdminId then
        local name = "Cargando..."
        pcall(function()
            name = Players:GetNameFromUserIdAsync(currentAdminId)
        end)
        currentAdminLabel.Text = "👑 Admin Actual: " .. name
    else
        currentAdminLabel.Text = "👑 Admin Actual: Nadie"
    end
end)
