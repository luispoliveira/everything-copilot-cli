# Recommended MCP Servers

## 1. GitHub (já incluído)

Interact with GitHub resources

```bash
# Already configured
```

## 2. Filesystem

Extended file operations

```bash
copilot
> /mcp add

Name: filesystem
Command: npx
Args: -y @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

## 3. Postgres (se usar PostgreSQL)

```bash
Name: postgres
Command: npx
Args: -y @modelcontextprotocol/server-postgres postgresql://localhost/dbname
```

## 4. Brave Search

Web search capabilities

```bash
Name: brave-search
Command: npx
Args: -y @modelcontextprotocol/server-brave-search
Env: BRAVE_API_KEY=your_key
```

## 5. Slack (para notificações)

```bash
Name: slack
Command: npx
Args: -y @modelcontextprotocol/server-slack
Env: SLACK_BOT_TOKEN=your_token
```

## Configuration File

Location: `~/.copilot/mcp-config.json`

Example:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/luispoliveira"
      ]
    }
  }
}
```
