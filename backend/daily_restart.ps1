$port = 8000
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        if ($conn.State -eq 'Listen') {
            Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
}
Start-Process -FilePath "C:\Users\PC\.gemini\antigravity\worldnews\backend\start.bat" -WindowStyle Minimized
