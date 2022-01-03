$Dir = "$(Get-Location)".Trim() + ":/home/user/code"
$CMD = "docker run -d -it -u user  --name aircraft-design -v $Dir aircraftdesign:latest /bin/bash"

Invoke-Expression $CMD

Write-Host $CMD
