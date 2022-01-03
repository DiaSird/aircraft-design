$obj = Get-NetIPConfiguration -InterfaceAlias "vEthernet (WSL)" | ForEach-Object { $_.IPv4Address }
$WSLIPAddress = $obj[0].ToString()

$composeText = @"
version: "3.2"
services:
  python-gui:
    image: ./Dockerfile
    build: .
    restart: always
    tty: true
    volumes:
      - $(Get-Location):/home/user/code
    environment:
      - DISPLAY=$WSLIPAddress
"@

$composeText > .\.devcontainer\docker-compose.yml
