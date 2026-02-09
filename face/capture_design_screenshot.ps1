Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$url = "http://localhost:3001"
$screenshotPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\design_report.png"

Write-Host "Opening Frontend: $url"
$wshell = New-Object -ComObject WScript.Shell
Start-Process "msedge" $url

Write-Host "Waiting 8 seconds for page load..."
Start-Sleep -Seconds 8

# Try to bring to front
Write-Host "Focusing window..."
#-1 for current window? Or attempt title match "Vite + React"
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
