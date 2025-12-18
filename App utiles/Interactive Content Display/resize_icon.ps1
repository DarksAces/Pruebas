Add-Type -AssemblyName System.Drawing

$sourcePath = "c:\Users\Daniel\Documents\GitHub\Scripts-Prueba\Interactive-Text-Editor-main\node\Funcionales\Funcional 3\media_content\imagenes\icon\logo.png"
$destPath = "c:\Users\Daniel\Documents\GitHub\Scripts-Prueba\Interactive-Text-Editor-main\node\Funcionales\Funcional 3\media_content\imagenes\icon\logo_256.png"

$img = [System.Drawing.Image]::FromFile($sourcePath)
$resized = new-object System.Drawing.Bitmap(256, 256)
$graph = [System.Drawing.Graphics]::FromImage($resized)
$graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic

$graph.DrawImage($img, 0, 0, 256, 256)
$resized.Save($destPath, [System.Drawing.Imaging.ImageFormat]::Png)

$img.Dispose()
$resized.Dispose()
$graph.Dispose()

Write-Host "Resized image saved to $destPath"
