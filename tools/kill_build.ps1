Get-CimInstance Win32_Process |
	Where-Object { $_.CommandLine -match 'vite build' } |
	ForEach-Object {
		Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
		Write-Output ("killed " + $_.ProcessId)
	}
