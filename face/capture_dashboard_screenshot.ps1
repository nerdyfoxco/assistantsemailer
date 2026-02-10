Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$token = Get-Content "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\token.txt"
$frontendUrl = "http://localhost:3006/signup?token=$token"
$screenshotPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\dashboard_report.png"

Write-Host "Opening Frontend: $frontendUrl"
$wshell = New-Object -ComObject WScript.Shell
Start-Process "msedge" $frontendUrl

Write-Host "Waiting 10 seconds for page load and redirect..."
Start-Sleep -Seconds 10

# Try to bring to front
Write-Host "Focusing window..."
try {
    $wshell.AppActivate("Vite + React")
}
catch {
    Write-Host "Could not focus window, continuing..."
}
Start-Sleep -Seconds 2

Write-Host "Capturing screen..."
$bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bmp.Size)

Write-Host "Saving to: $screenshotPath"
$bmp.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bmp.Dispose()

Write-Host "Screenshot captured successfully."
