Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\Users\Robert\Documents\Scripts\WotD\WotD.bat" & Chr(34), 0
Set WinScriptHost = Nothing