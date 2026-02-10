Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$token = Get-Content "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\token.txt"
$signupUrl = "http://localhost:3006/signup"
$dashboardUrl = "http://localhost:3006/login?token=$token"
$signupPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\signup_page.png"
$dashboardPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\face\dashboard_page.png"
$wshell = New-Object -ComObject WScript.Shell

function Capture-Screen($path) {
    $bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bmp)
    $graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bmp.Size)
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bmp.Dispose()
    Write-Host "Saved screenshot to $path"
}

# 1. Capture Signup Page
Write-Host "Navigating to Signup Page: $signupUrl"
Start-Process "msedge" $signupUrl
Start-Sleep -Seconds 8
Write-Host "Focusing..."
try { $wshell.AppActivate("Vite + React") } catch {}
Start-Sleep -Seconds 2
Capture-Screen $signupPath

# 2. Capture Dashboard (via Login Token)
Write-Host "Navigating to Dashboard (via Login): $dashboardUrl"
Start-Process "msedge" $dashboardUrl
Start-Sleep -Seconds 10
Write-Host "Focusing..."
try { $wshell.AppActivate("Vite + React") } catch {}
Start-Sleep -Seconds 2
Capture-Screen $dashboardPath

Write-Host "Visual Sequence Complete."
