# Everything Copilot CLI

Configuração completa e organizada para GitHub Copilot CLI com agentes customizados, instruções específicas e skills.

## 🚀 Quick Start

1. Clone este repositório
2. cd para ~/.copilot
3. ln -s everything-copilot-cli/.github/instructions/ instructions
4. ln -s everything-copilot-cli/.github/agents/ agents
5. ln -s everything-copilot-cli/.github/skills/ skills

## 📁 Estrutura

- `.github/copilot-instructions.md` - Instruções globais
- `.github/instructions/` - Instruções por contexto
- `.github/agents/` - Agentes customizados
- `.github/skills/` - Skills especializadas
- `mcp-servers/` - Configurações de MCP servers
- `examples/` - Exemplos de uso

## 🤖 Agentes Disponíveis

- **code-reviewer** - Revisão de código focada em qualidade
- **security-auditor** - Auditoria de segurança
- **test-generator** - Geração de testes
- **doc-writer** - Documentação automática

## 🛠️ Skills Disponíveis

- **git-workflow** - Workflows git automatizados

## 📖 Uso

### Usar agente específico

```bash
copilot --agent=code-reviewer --prompt "Review my changes"
```

### Usar com arquivos

```bash
copilot
> Fix bugs in @src/app.js using @security-auditor
```

### Delegar tarefas

```bash
copilot
> /delegate implement user authentication with JWT
```

## 🔧 Customização

Edite os arquivos em `.github/` para personalizar:

- Instruções globais e específicas
- Comportamento dos agentes
- Skills disponíveis

## 📚 Documentação

- [GitHub Copilot CLI Docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [Custom Agents Guide](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## 🤝 Contribuindo

Sugestões de novos agentes ou melhorias são bem-vindas!
