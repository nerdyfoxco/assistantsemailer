Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$reportPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\infrastructure\aws\cache\cache_report.html"
$screenshotPath = "c:\Users\Admin\.gemini\Workspaces\Email Systems\infrastructure\aws\cache\cache_report.png"

Write-Host "Opening report: $reportPath"
Start-Process $reportPath

Write-Host "Waiting 5 seconds for browser load..."
Start-Sleep -Seconds 5

Write-Host "Capturing screen..."
$bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bmp.Size)

Write-Host "Saving to: $screenshotPath"
$bmp.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bmp.Dispose()

Write-Host "Screenshot captured successfully."
