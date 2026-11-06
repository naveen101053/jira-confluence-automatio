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
