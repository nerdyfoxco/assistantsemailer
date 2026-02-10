Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$token = Get-Content "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\token.txt"
$dashboardUrl = "http://localhost:3006/login?token=$token"
$reportPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\auth_report.png"
$wshell = New-Object -ComObject WScript.Shell

Write-Host "Opening Dashboard: $dashboardUrl"
Start-Process "msedge" $dashboardUrl

Write-Host "Waiting 5 seconds for page load..."
Start-Sleep -Seconds 5

Write-Host "Focusing..."
try { $wshell.AppActivate("Vite + React") } catch {}
Start-Sleep -Seconds 1

Write-Host "Capturing screen..."
$bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bmp.Size)
$bmp.Save($reportPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bmp.Dispose()
Write-Host "Saved to $reportPath"
