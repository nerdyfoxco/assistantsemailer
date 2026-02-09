Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$reportPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\infrastructure\aws\quality\quality_report.html"
$screenshotPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\infrastructure\aws\quality\quality_report.png"

Write-Host "Opening report: $reportPath"
$wshell = New-Object -ComObject WScript.Shell
$proc = Start-Process $reportPath -PassThru

Write-Host "Waiting 5 seconds for browser launch..."
Start-Sleep -Seconds 5

# Try to bring to front
Write-Host "Focusing window..."
$wshell.AppActivate($proc.Id)
Start-Sleep -Seconds 1

Write-Host "Capturing screen..."
$bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bmp.Size)

Write-Host "Saving to: $screenshotPath"
$bmp.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bmp.Dispose()

Write-Host "Screenshot captured successfully."
