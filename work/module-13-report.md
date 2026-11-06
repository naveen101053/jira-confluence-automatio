# Module 13 Completion Report

## MCP Configuration
```json
{ 
  "servers": { 
    "echo-windows": { 
      "command": "powershell", 
      "args": ["-ExecutionPolicy", "Bypass", "-File", "${workspaceFolder}/tools/mcp-echo.ps1"] 
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    }
  }  
}  
```
(No API keys or tokens are present in this configuration, so no redaction was needed.)

## Configured Servers
- echo-windows
- filesystem

## MCP Tool Test

### Test 1 — Custom tool (`echo-windows-calculate`)
- Tool used: `echo-windows-calculate`
- Input: `{ "operation": "divide", "a": 100, "b": 4 }`
- Raw JSON-RPC response:
```json
{"result":{"content":[{"text":"25","type":"text"}]},"id":3,"jsonrpc":"2.0"}
```

### Test 2 — Official MCP server tool (`filesystem` / `list_directory`)
This test demonstrates real MCP functionality beyond basic calculation: using the official
`@modelcontextprotocol/server-filesystem` package to list files in the `tools/` directory via the
`list_directory` tool, over the standard MCP stdio JSON-RPC protocol (`initialize` → `tools/call`).

- Tool used: `filesystem` server, `list_directory` tool
- Input: `{ "path": "C:\\workspace\\hello-genai\\work\\module03-task\\tools" }`
- Raw JSON-RPC responses (captured directly from the server's stdout):
```json
{"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":true},"resources":{"listChanged":true}},"serverInfo":{"name":"secure-filesystem-server","version":"2.2.0"}},"jsonrpc":"2.0","id":1}
{"result":{"content":[{"type":"text","text":"[FILE] Blocked-work-detection.py\n[FILE] compound_interest.py\n[FILE] mcp-echo.ps1"}],"structuredContent":{"content":"[FILE] Blocked-work-detection.py\n[FILE] compound_interest.py\n[FILE] mcp-echo.ps1"}},"jsonrpc":"2.0","id":3}
```
