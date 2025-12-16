--[[
    MonetizationHandler.server.lua
    Maneja las compras de DevProducts y Gamepasses.
]]

local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GameConfig = require(ReplicatedStorage.Shared.GameConfig)

-- Procesar compras de productos consumibles (DevProducts)
local function processReceipt(receiptInfo)
    local player = Players:GetPlayerByUserId(receiptInfo.PlayerId)
    
    if not player then
        -- El jugador se fue antes de procesar la compra
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end
    
    if receiptInfo.ProductId == GameConfig.Products.SkipQueue then
        print("💰 " .. player.Name .. " compró SALTAR COLA")
        
        if _G.QueueSystem then
            _G.QueueSystem.SkipToFront(player)
            return Enum.ProductPurchaseDecision.PurchaseGranted
        else
            warn("Sistema de Cola no cargado aún")
            return Enum.ProductPurchaseDecision.NotProcessedYet
        end
        
    elseif receiptInfo.ProductId == GameConfig.Products.InstantAdmin then
        print("💰 " .. player.Name .. " compró ADMIN INSTANTANEO")
        -- Lógica: Echar al admin actual (o esperar) y ponerse él
        if _G.QueueSystem then
             _G.QueueSystem.SkipToFront(player)
             _G.QueueSystem.ForceTurnEnd() -- Fuerza el cambio de turno inmediato
            return Enum.ProductPurchaseDecision.PurchaseGranted
        end
    end
    
    return Enum.ProductPurchaseDecision.NotProcessedYet
end

MarketplaceService.ProcessReceipt = processReceipt

-- Chequear Gamepasses al entrar
Players.PlayerAdded:Connect(function(player)
    local success, hasPass = pcall(function()
        return MarketplaceService:UserOwnsGamePassAsync(player.UserId, GameConfig.Gamepasses.VIP)
    end)
    
    if success and hasPass then
        print("🌟 VIP Conectado: " .. player.Name)
        -- Aquí podrías darle un chat tag o algo visual
    end
end)
