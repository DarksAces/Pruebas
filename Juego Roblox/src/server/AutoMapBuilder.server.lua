--[[
    AutoMapBuilder.server.lua
    Crea las plataformas físicas de la cola automáticamente para que no tengas que hacerlo a mano.
]]

local Workspace = game:GetService("Workspace")

local QUEUE_LENGTH = 20 -- Cantidad de plataformas
local STUD_GAP = 6 -- Separación entre plataformas

local folder = Workspace:FindFirstChild("QueueSystem") or Instance.new("Folder")
folder.Name = "QueueSystem"
folder.Parent = Workspace

-- Materiales
local queueColor = BrickColor.new("Medium stone grey")
local throneColor = BrickColor.new("Bright yellow")

local function createPart(name, pos, size, color, parent)
    if parent:FindFirstChild(name) then return parent[name] end
    
    local p = Instance.new("Part")
    p.Name = name
    p.Size = size
    p.Position = pos
    p.Anchored = true
    p.BrickColor = color
    p.TopSurface = Enum.SurfaceType.Smooth -- Estética
    p.Parent = parent
    return p
end

-- 1. Crear el Trono (Donde está el Admin/Shrek)
local throne = createPart("AdminThrone", Vector3.new(0, 5, -10), Vector3.new(8, 1, 8), throneColor, folder)

-- Texto del Trono
if not throne:FindFirstChild("Gui") then
    local gui = Instance.new("SurfaceGui", throne)
    gui.Face = Enum.NormalId.Front
    local txt = Instance.new("TextLabel", gui)
    txt.Size = UDim2.new(1,0,1,0)
    txt.Text = "👑 ADMIN ACTUAL 👑"
    txt.TextScaled = true
    txt.BackgroundTransparency = 1
end

-- 2. Salida
createPart("ExitSpawn", Vector3.new(20, 5, 0), Vector3.new(8, 1, 8), BrickColor.new("Really red"), folder)

-- 3. Crear las Plataformas de la Cola
-- Empieza cerca del trono y va hacia atrás
local startZ = 0

for i = 1, QUEUE_LENGTH do
    local pos = Vector3.new(0, 2, startZ + (i * STUD_GAP))
    local plat = createPart("QueuePt_" .. i, pos, Vector3.new(4, 1, 4), queueColor, folder)
    
    -- Número en la plataforma
    if not plat:FindFirstChild("NumberGui") then
        local gui = Instance.new("SurfaceGui", plat)
        gui.Face = Enum.NormalId.Top
        local txt = Instance.new("TextLabel", gui)
        txt.Size = UDim2.new(1,0,1,0)
        txt.Text = tostring(i)
        txt.TextScaled = true
        txt.BackgroundTransparency = 1
        txt.TextColor3 = Color3.new(1,1,1)
    end
end

-- 4. PAD DE ENTRADA (Al final de la cola o al lado)
local joinPos = Vector3.new(8, 2, startZ + (STUD_GAP)) -- Al lado del primero
local joinPad = createPart("JoinQueuePad", joinPos, Vector3.new(6, 1, 6), BrickColor.new("Lime green"), Workspace)

if not joinPad:FindFirstChild("Gui") then
    local gui = Instance.new("SurfaceGui", joinPad)
    gui.Face = Enum.NormalId.Top
    local txt = Instance.new("TextLabel", gui)
    txt.Size = UDim2.new(1,0,1,0)
    txt.Text = "¡UNIRSE A LA COLA!"
    txt.TextScaled = true
    txt.BackgroundTransparency = 1
end

print("✅ Mapa de Cola generado correctamente.")
