'#!cscript /NoLogo
'This script converts a Visio (.vsd or .vsdx) into a SVG image
Option Explicit

' constants required for opening files in Visio
Const visOpenRO = 2
Const visOpenMinimized = 16
Const visOpenHidden = 64
Const visOpenMacrosDisabled = 128
Const visOpenNoWorkspace = 256
Const visRasterFitToCustomSize = 3
Const visRasterPixel = 0

Sub export(filePath, fileName, widthInPixels, heightInPixels)
    Dim visioApplication : Set visioApplication = CreateObject("Visio.InvisibleApp")
    visioApplication.Settings.SetRasterExportSize visRasterFitToCustomSize, widthInPixels, heightInPixels, visRasterPixel
    visioApplication.Documents.OpenEx filePath, visOpenRO + visOpenMinimized + visOpenHidden + visOpenMacrosDisabled + visOpenNoWorkspace
    visioApplication.ActiveDocument.Pages.Item(1).Export fileName
    visioApplication.Quit
End Sub

Dim currentDirectory : currentDirectory = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")

if WScript.Arguments.Count = 0 then
    WScript.Echo "Missing parameters"
end if

Dim filePath : filePath = currentDirectory & "\" & WScript.Arguments(0)
Dim objRegEx
Set objRegEx = CreateObject("VBScript.RegExp")
objRegEx.Global = True
objRegEx.IgnoreCase = True
objRegEx.Pattern = "\.vsdx?"

export filePath, objRegEx.Replace(filePath, ".svg"), 3557, 4114
