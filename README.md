# Lumy TV – Website Completo

Um website moderno e responsivo para a Lumy TV, uma plataforma de ecrãs digitais inteligentes.

## 🚀 Características

- **Design Moderno**: Layout clean e responsivo com animações suaves
- **Paleta de Cores**: Verde-menta (#A6E3D0), amarelo (#FDDC5C), branco (#FFFFFF), cinza claro (#F1FAEE)
- **Tipografia**: Inter (Google Fonts)
- **SEO Otimizado**: Meta tags, Open Graph, estrutura semântica
- **Performance**: Lazy loading, imagens otimizadas, CSS/JS minificado
- **Acessibilidade**: Navegação por teclado, alt text, contraste adequado

## 📁 Estrutura do Projeto

```
/
├── index.html              # Página inicial
├── use-cases.html          # Casos de uso
├── pricing.html            # Preços e planos
├── partners.html           # Parceiros
├── css/
│   └── style.css          # Estilos principais
├── js/
│   └── main.js            # JavaScript interativo
├── images/
│   ├── lumy-logo.svg      # Logo principal
│   ├── lumy-logo-white.svg # Logo branco (footer)
│   └── [outras imagens]   # Imagens do site
├── favicon.ico            # Favicon
└── README.md              # Este arquivo
```

## 🎨 Páginas Implementadas

### 1. Home Page (`index.html`)
- **Hero Section**: Título principal e descrição
- **Features**: 6 funcionalidades principais com ícones
- **CTA**: Call-to-action para demo

### 2. Casos de Uso (`use-cases.html`)
- **Grid de Casos**: 6 setores diferentes
- **Benefícios**: Lista de vantagens por setor
- **Links**: Para páginas individuais de cada caso de uso

### 3. Preços (`pricing.html`)
- **3 Planos**: Free, Growth, Enterprise
- **Toggle**: Mensal/Anual com desconto
- **Calculadora**: Preços dinâmicos
- **FAQ**: Perguntas frequentes

### 4. Parceiros (`partners.html`)
- **Grid de Logos**: Parceiros estratégicos
- **Benefícios**: Vantagens de ser parceiro
- **CTA**: Contacto para parcerias

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura semântica
- **CSS3**: Flexbox, Grid, animações, variáveis CSS
- **JavaScript**: Interatividade, navegação mobile, lazy loading
- **Google Fonts**: Inter (tipografia)
- **SVG**: Ícones e logos vetoriais

## 🎯 Funcionalidades JavaScript

- **Navegação Mobile**: Menu hambúrguer responsivo
- **Smooth Scrolling**: Rolagem suave entre seções
- **Intersection Observer**: Animações no scroll
- **Lazy Loading**: Carregamento otimizado de imagens
- **Pricing Calculator**: Calculadora de preços dinâmica
- **Form Validation**: Validação de formulários
- **Back to Top**: Botão de voltar ao topo

## 📱 Responsividade

- **Desktop**: Layout completo com grid de 3-4 colunas
- **Tablet**: Layout adaptado com 2 colunas
- **Mobile**: Layout single-column com menu hambúrguer

## 🔧 Como Usar

1. **Clone o repositório**:
   ```bash
   git clone [url-do-repositorio]
   cd lumy-tv-website
   ```

2. **Abra no navegador**:
   - Abra `index.html` no seu navegador
   - Ou use um servidor local:
   ```bash
   python -m http.server 8000
   # ou
   npx serve .
   ```

3. **Desenvolvimento**:
   - Edite os arquivos HTML, CSS e JS
   - As mudanças são aplicadas automaticamente

## 🖼️ Imagens Necessárias

Para completar o website, você precisará adicionar as seguintes imagens na pasta `images/`:

### Logos e Ícones
- ✅ `lumy-logo.svg` - Logo principal
- ✅ `lumy-logo-white.svg` - Logo branco

### Imagens de Conteúdo
- `hero-mockup.webp` - Mockup do produto na home
- `use-cases-hero.webp` - Hero dos casos de uso
- `retail-use-case.webp` - Caso de uso retail
- `restaurant-use-case.webp` - Caso de uso restaurantes
- `education-use-case.webp` - Caso de uso educação
- `transport-use-case.webp` - Caso de uso transportes
- `corporate-use-case.webp` - Caso de uso corporate
- `events-use-case.webp` - Caso de uso eventos

### Logos de Parceiros
- `partner-1.svg` até `partner-8.svg` - Logos dos parceiros

## 🎨 Personalização

### Cores
As cores estão definidas como variáveis CSS em `css/style.css`:
```css
:root {
    --primary-green: #A6E3D0;
    --primary-yellow: #FDDC5C;
    --white: #FFFFFF;
    --light-gray: #F1FAEE;
    --dark-gray: #2D3748;
    --text-gray: #4A5568;
    --border-gray: #E2E8F0;
}
```

### Tipografia
A fonte Inter está carregada via Google Fonts. Para alterar:
1. Mude o link no `<head>` dos arquivos HTML
2. Atualize `--font-family` no CSS

## 📈 SEO

O website está otimizado para SEO com:
- Meta tags completas
- Open Graph tags
- Estrutura semântica (H1, H2, H3)
- Alt text em imagens
- URLs descritivas
- Sitemap (a ser implementado)

## 🚀 Deploy

Para fazer deploy do website:

1. **Netlify**:
   - Conecte o repositório
   - Build command: vazio
   - Publish directory: `.`

2. **Vercel**:
   - Importe o repositório
   - Framework preset: Other
   - Build command: vazio

3. **GitHub Pages**:
   - Vá para Settings > Pages
   - Source: Deploy from a branch
   - Branch: main

## 📞 Suporte

Para dúvidas ou sugestões:
- Email: [seu-email@exemplo.com]
- Website: [url-do-website]

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Lumy TV** - Transformando a comunicação digital com ecrãs inteligentes