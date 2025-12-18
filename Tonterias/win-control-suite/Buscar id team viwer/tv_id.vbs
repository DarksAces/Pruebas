Option Explicit
Dim fso, shell, scriptDir, ps1File, vbsFile
Dim configPath, userParameterLine, file, content, alreadyExists

' Obtener directorio del script
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Archivos a eliminar
ps1File = scriptDir & "\tv_id.ps1"
vbsFile = WScript.ScriptFullName

' Configuración - CORREGIDO: Sin espacio en UserParameter
configPath = "C:\windows\idenPC.cfg"
userParameterLine = "UserParameter=dosi.tw,reg query ""HKEY_LOCAL_MACHINE\SOFTWARE\TeamViewer"" /v ClientID"
alreadyExists = False

' Función para buscar TeamViewer dinámicamente
Function FindTeamViewerPath()
    Dim basePaths(1), basePath, teamViewerPath, cmd, result
    basePaths(0) = "HKEY_LOCAL_MACHINE\SOFTWARE\TeamViewer"
    basePaths(1) = "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\TeamViewer"
    
    For Each basePath In basePaths
        On Error Resume Next
        ' Probar si existe ClientID en esta ruta
        cmd = "reg query """ & basePath & """ /v ClientID"
        result = shell.Run(cmd, 0, True)
        If result = 0 Then
            FindTeamViewerPath = basePath
            Exit Function
        End If
        On Error GoTo 0
    Next
    
    ' Si no encuentra nada, usar ruta por defecto
    FindTeamViewerPath = "HKEY_LOCAL_MACHINE\SOFTWARE\TeamViewer"
End Function

' Obtener ruta válida de TeamViewer
Dim validPath
validPath = FindTeamViewerPath()
userParameterLine = "UserParameter=dosi.tw,reg query """ & validPath & """ /v ClientID"

' Verificar y modificar archivo de configuración
On Error Resume Next
If fso.FileExists(configPath) Then
    Set file = fso.OpenTextFile(configPath, 1) ' ForReading
    If Err.Number = 0 Then
        content = file.ReadAll
        file.Close
        If InStr(content, userParameterLine) > 0 Then
            alreadyExists = True
        End If
    End If
    Err.Clear
End If

' Añadir la línea si no existe
If Not alreadyExists Then
    If fso.FileExists(configPath) Then
        Set file = fso.OpenTextFile(configPath, 8) ' ForAppending
        If Err.Number = 0 Then
            file.WriteLine "" ' Línea en blanco para asegurar separación
            file.WriteLine userParameterLine
            file.Close
        End If
    Else
        Set file = fso.CreateTextFile(configPath, True)
        If Err.Number = 0 Then
            file.WriteLine userParameterLine
            file.Close
        End If
    End If
End If

' Limpiar archivos - crear script de autodestrucción mejorado
WScript.Sleep 1000  ' Esperar un poco antes de la limpieza

Dim cleanupVbs
cleanupVbs = "WScript.Sleep 2000" & vbCrLf & _
             "Set fso = CreateObject(""Scripting.FileSystemObject"")" & vbCrLf & _
             "On Error Resume Next" & vbCrLf

If fso.FileExists(ps1File) Then
    cleanupVbs = cleanupVbs & "fso.DeleteFile """ & ps1File & """, True" & vbCrLf
End If

cleanupVbs = cleanupVbs & "fso.DeleteFile """ & vbsFile & """, True" & vbCrLf & _
                         "fso.DeleteFile WScript.ScriptFullName, True" & vbCrLf & _
                         "On Error GoTo 0"

' Crear archivo temporal para autodestrucción
Dim tempVbs
tempVbs = fso.GetSpecialFolder(2) & "\" & fso.GetTempName & ".vbs"  ' Carpeta temporal
Set file = fso.CreateTextFile(tempVbs, True)
file.Write cleanupVbs
file.Close

' Ejecutar script de limpieza
shell.Run "cscript.exe //nologo """ & tempVbs & """", 0, False

On Error GoTo 0