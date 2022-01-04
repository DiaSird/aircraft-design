New-Item .env -Force
$obj = Get-NetIPConfiguration -InterfaceAlias "vEthernet (WSL)" | ForEach-Object { $_.IPv4Address }
$WSLIPAddress = $obj[0].ToString()
$UTF8NoBomEnc = New-Object System.Text.UTF8Encoding $False
[System.IO.File]::WriteAllLines(".env", "IPADDRESS=$($WSLIPAddress):0.0", $UTF8NoBomEnc)
Write-Host "For X-server: .env is generated." -ForegroundColor Green
Write-Output "------------------------ .env ----------------------------------"
Get-Content .env
Write-Output "----------------------------------------------------------------"

Write-Host ""

Get-Content ./docker/Docker-compose-xserver.yml > docker-compose.yml
Write-Host "For X-server: Docker-compose.yml is generated." -ForegroundColor Green
Write-Output "------------------docker-compose.yml settings-------------------"
docker-compose config
Write-Output "----------------------------------------------------------------"
