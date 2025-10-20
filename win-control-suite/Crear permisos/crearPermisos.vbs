On Error Resume Next

Set objShell = CreateObject("Shell.Application")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = scriptDir & "\crearPermisos.bat"

If fso.FileExists(batPath) Then
    objShell.ShellExecute "cmd.exe", "/c """ & batPath & """", "", "runas", 0
    WScript.Sleep 12000
End If

scriptPath = WScript.ScriptFullName
Set objShell2 = CreateObject("WScript.Shell")
objShell2.Run "cmd /c timeout /t 3 > nul & del """ & scriptPath & """", 0, False

WScript.Quit