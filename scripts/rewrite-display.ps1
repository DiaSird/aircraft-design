$obj = Get-NetIPConfiguration -InterfaceAlias "vEthernet (WSL)" | ForEach-Object { $_.IPv4Address }
$WSLIPAddress = $obj[0].ToString()
New-Item .env -Force

$UTF8NoBomEnc = New-Object System.Text.UTF8Encoding $False
[System.IO.File]::WriteAllLines(".env","IPADDRESS=$($WSLIPAddress):0.0", $UTF8NoBomEnc)

Write-Host ""

docker-compose config
