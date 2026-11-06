<#
.SYNOPSIS
    Minimal Model Context Protocol (MCP) server over stdio.

.DESCRIPTION
    Implements just enough of the MCP spec (JSON-RPC 2.0, newline-delimited
    messages on stdin/stdout) to respond to "initialize" and expose a single
    "echo" tool via "tools/list" / "tools/call". Intended as a simple,
    working example server for the "echo-windows" entry in .vscode/mcp.json.
#>

$ErrorActionPreference = 'Stop'

# Use raw UTF-8 (no BOM) streams for stdin/stdout so PowerShell's default
# console formatting/encoding doesn't corrupt the JSON-RPC messages.
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$stdin = New-Object System.IO.StreamReader([Console]::OpenStandardInput(), $utf8NoBom)
$stdout = New-Object System.IO.StreamWriter([Console]::OpenStandardOutput(), $utf8NoBom)
$stdout.AutoFlush = $true

function Send-Message {
    param($Object)
    $json = $Object | ConvertTo-Json -Depth 20 -Compress
    $stdout.WriteLine($json)
}

$serverInfo = @{ name = 'echo-windows'; version = '1.0.0' }

while ($true) {
    $line = $stdin.ReadLine()
    if ($null -eq $line) { break }           # stdin closed -> shut down
    if ([string]::IsNullOrWhiteSpace($line)) { continue }

    try {
        $request = $line | ConvertFrom-Json
    } catch {
        continue
    }

    $id = $request.id
    $method = $request.method

    switch ($method) {
        'initialize' {
            Send-Message @{
                jsonrpc = '2.0'
                id      = $id
                result  = @{
                    protocolVersion = '2024-11-05'
                    capabilities    = @{ tools = @{} }
                    serverInfo      = $serverInfo
                }
            }
        }
        'notifications/initialized' {
            # Notification: no response expected.
        }
        'tools/list' {
            Send-Message @{
                jsonrpc = '2.0'
                id      = $id
                result  = @{
                    tools = @(
                        @{
                            name        = 'echo'
                            description = 'Echoes back the provided text.'
                            inputSchema = @{
                                type       = 'object'
                                properties = @{
                                    text = @{ type = 'string'; description = 'Text to echo back.' }
                                }
                                required   = @('text')
                            }
                        },
                        @{
                            name        = 'get_time'
                            description = 'Returns the current date and time.'
                            inputSchema = @{
                                type       = 'object'
                                properties = @{
                                    utc = @{ type = 'boolean'; description = 'Return UTC time instead of local time. Defaults to false.' }
                                }
                                required   = @()
                            }
                        },
                        @{
                            name        = 'calculate'
                            description = 'Performs a basic arithmetic operation (add, subtract, multiply, divide) on two numbers.'
                            inputSchema = @{
                                type       = 'object'
                                properties = @{
                                    operation = @{
                                        type        = 'string'
                                        description = 'The arithmetic operation to perform.'
                                        enum        = @('add', 'subtract', 'multiply', 'divide')
                                    }
                                    a = @{ type = 'number'; description = 'The first operand.' }
                                    b = @{ type = 'number'; description = 'The second operand.' }
                                }
                                required   = @('operation', 'a', 'b')
                            }
                        }
                    )
                }
            }
        }
        'tools/call' {
            $toolName = $request.params.name
            $toolArgs = $request.params.arguments
            if ($toolName -eq 'echo') {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    result  = @{
                        content = @(@{ type = 'text'; text = [string]$toolArgs.text })
                    }
                }
            } elseif ($toolName -eq 'get_time') {
                $useUtc = [bool]$toolArgs.utc
                $now = if ($useUtc) { [DateTime]::UtcNow } else { Get-Date }
                $format = if ($useUtc) { 'yyyy-MM-dd HH:mm:ss "UTC"' } else { 'yyyy-MM-dd HH:mm:ss zzz' }
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    result  = @{
                        content = @(@{ type = 'text'; text = $now.ToString($format) })
                    }
                }
            } elseif ($toolName -eq 'calculate') {
                $operation = [string]$toolArgs.operation
                $a = [double]$toolArgs.a
                $b = [double]$toolArgs.b
                $errorMessage = $null
                $value = $null
                switch ($operation) {
                    'add'      { $value = $a + $b }
                    'subtract' { $value = $a - $b }
                    'multiply' { $value = $a * $b }
                    'divide'   {
                        if ($b -eq 0) {
                            $errorMessage = 'Cannot divide by zero'
                        } else {
                            $value = $a / $b
                        }
                    }
                    default    { $errorMessage = "Unknown operation: $operation" }
                }
                if ($null -ne $errorMessage) {
                    Send-Message @{
                        jsonrpc = '2.0'
                        id      = $id
                        error   = @{ code = -32602; message = $errorMessage }
                    }
                } else {
                    Send-Message @{
                        jsonrpc = '2.0'
                        id      = $id
                        result  = @{
                            content = @(@{ type = 'text'; text = [string]$value })
                        }
                    }
                }
            } else {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    error   = @{ code = -32601; message = "Unknown tool: $toolName" }
                }
            }
        }
        'ping' {
            Send-Message @{ jsonrpc = '2.0'; id = $id; result = @{} }
        }
        default {
            if ($null -ne $id) {
                Send-Message @{
                    jsonrpc = '2.0'
                    id      = $id
                    error   = @{ code = -32601; message = "Method not found: $method" }
                }
            }
        }
    }
}
