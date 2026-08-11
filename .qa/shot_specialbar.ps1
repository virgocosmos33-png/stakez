$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$out = "c:\Users\Emex33\Documents\tombstone reborn\.qa"
$stories = @(
	@{ name = "empty"; id = "mode-base-book--dead-spin" },
	@{ name = "hit"; id = "mode-base-book--special-bar-hit" },
	@{ name = "gang"; id = "mode-base-book--split-gang" }
)
foreach ($s in $stories) {
	$profile = Join-Path $out ("profile_" + $s.name)
	$shot = Join-Path $out ("specialbar_" + $s.name + ".png")
	if (Test-Path $profile) { Remove-Item -Recurse -Force $profile }
	if (Test-Path $shot) { Remove-Item -Force $shot }
	$url = "http://localhost:6009/iframe.html?id=$($s.id)&viewMode=story&v=fix6"
	# Paths contain a space ("tombstone reborn") — must be quoted for Chrome.
	$argList = @(
		"--headless=new",
		"--disable-gpu",
		"--no-sandbox",
		"--hide-scrollbars",
		"--window-size=1280,800",
		"--virtual-time-budget=60000",
		"--screenshot=`"$shot`"",
		"--user-data-dir=`"$profile`"",
		"`"$url`""
	)
	Write-Output ("RUN " + $s.name)
	$p = Start-Process -FilePath $chrome -ArgumentList $argList -PassThru -Wait -NoNewWindow
	$len = if (Test-Path $shot) { (Get-Item $shot).Length } else { 0 }
	Write-Output "$($s.name) exit=$($p.ExitCode) bytes=$len"
}
