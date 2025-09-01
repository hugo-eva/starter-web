# Amos Resource System

Sistema de gerenciamento de recursos para o Lumy TV, desenvolvido para gerenciar funcionalidades e configurações do sistema.

## Estrutura de Arquivos

```
resources/
├── amosbresource.js    # Sistema principal de recursos
├── amosbresource.css   # Estilos do sistema
└── README.md          # Esta documentação
```

## Funcionalidades

### Gerenciamento de Recursos
- **Adicionar recursos**: `amosResource.addResource(name, data)`
- **Obter recursos**: `amosResource.getResource(name)`
- **Atualizar recursos**: `amosResource.updateResource(name, data)`
- **Remover recursos**: `amosResource.removeResource(name)`
- **Listar recursos**: `amosResource.listResources()`

### Recursos Padrão
- **Theme**: Configurações de tema (light, dark, auto)
- **Language**: Configurações de idioma (en, pt)
- **Features**: Funcionalidades do sistema

### Estatísticas
- **getStats()**: Retorna estatísticas do sistema
- **hasResource(name)**: Verifica se um recurso existe

## Uso

### Inicialização
O sistema é inicializado automaticamente quando o DOM estiver pronto:

```javascript
// O sistema já está disponível globalmente
console.log(window.amosResource.getStats());
```

### Adicionando Recursos Personalizados
```javascript
// Adicionar um recurso personalizado
amosResource.addResource('customFeature', {
    enabled: true,
    version: '1.0.0',
    config: { /* configurações */ }
});

// Obter o recurso
const feature = amosResource.getResource('customFeature');
```

### Atualizando Recursos
```javascript
// Atualizar um recurso existente
amosResource.updateResource('theme', { current: 'dark' });

// Verificar se foi atualizado
const theme = amosResource.getResource('theme');
console.log(theme.current); // 'dark'
```

## Integração com HTML

Para usar o sistema no HTML, inclua os arquivos:

```html
<link rel="stylesheet" href="resources/amosbresource.css">
<script src="resources/amosbresource.js"></script>
```

## Exemplo de Uso no HTML

```html
<div class="amos-resource">
    <div class="resource-panel">
        <div class="resource-header">
            <h3 class="resource-title">Sistema de Recursos</h3>
            <span class="resource-status active">Ativo</span>
        </div>
        <div class="resource-content">
            <div class="resource-item">
                <span class="resource-label">Tema Atual:</span>
                <span class="resource-value" id="current-theme">light</span>
            </div>
            <div class="resource-item">
                <span class="resource-label">Idioma:</span>
                <span class="resource-value" id="current-language">en</span>
            </div>
        </div>
        <div class="resource-actions">
            <button class="resource-btn" onclick="toggleTheme()">Alternar Tema</button>
            <button class="resource-btn primary" onclick="refreshResources()">Atualizar</button>
        </div>
    </div>
</div>

<script>
function toggleTheme() {
    const currentTheme = amosResource.getResource('theme');
    const newTheme = currentTheme.current === 'light' ? 'dark' : 'light';
    amosResource.updateResource('theme', { current: newTheme });
    document.getElementById('current-theme').textContent = newTheme;
}

function refreshResources() {
    const stats = amosResource.getStats();
    console.log('Estatísticas do sistema:', stats);
}
</script>
```

## Compatibilidade

- **Navegadores**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **ES6+**: Suporte completo a classes e módulos ES6
- **Node.js**: Suporte para uso em servidor (CommonJS)

## Desenvolvimento

Para contribuir com o desenvolvimento:

1. Mantenha a compatibilidade com navegadores antigos
2. Use ES6+ features quando apropriado
3. Documente novas funcionalidades
4. Teste em diferentes navegadores

## Licença

Este sistema é parte do projeto Lumy TV e segue as mesmas diretrizes de licenciamento.