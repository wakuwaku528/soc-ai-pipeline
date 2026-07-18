# 1. Setup paths
$repoPath = "C:\Projects\soc-ai-pipeline"
$logDir = "$repoPath\incoming"
if (!(Test-Path -Path $logDir)) { New-Item -ItemType Directory -Path $logDir }
$logFile = "$logDir\security_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

# 2. Extract last 20 Logon Failure (4625) events
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20 | 
    Select-Object -Property TimeCreated, Id, Message | 
    Out-File -FilePath $logFile -Encoding utf8

# 3. Git Automation
Set-Location -Path $repoPath
git add $logFile
git commit -m "Automated log export: $(Get-Date)"
git push
