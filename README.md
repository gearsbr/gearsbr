# GEARS. — Engenharia e Tecnologia Ambiental (Open Source)

Site institucional oficial da **GEARS.**, startup de engenharia e tecnologia ambiental sediada em **Congonhas (MG)**, responsável pelo desenvolvimento do sistema modular de purificação de ar urbano **T.U.L.I.P.A.** (Filtragem Mecânica + Telemetria IoT Aberta).

---

## Estrutura do Projeto

```text
GEARS./
├── index.html            # Página principal com estrutura semântica completa
├── css/
│   └── styles.css        # Design System (Fundo Branco Puro, Azul-Marinho/Petróleo, Esmeralda, Rich Mahogany)
├── js/
│   └── main.js           # Navegação responsiva, abas técnicas e destaque de rolagem
├── assets/
│   └── logo-gears.svg    # Logotipo GEARS. em proporção Fibonacci com ponto alinhado à base
└── README.md             # Guia de manutenção e deploy no GitHub Pages
```

---

## Diretrizes Visuais e Sistema de Cores

- **Fundo Principal (`--bg-pure-white`)**: `#FFFFFF` (Branco limpo de alto contraste, sem off-white).
- **Cores Principais da Marca (`GEARS.`)**:
  - Azul-Marinho (`--gears-navy`: `#0A192F`)
  - Azul-Petróleo (`--gears-petrol`: `#0F3A4D`)
- **Cores Secundárias por Categoria de Impacto**:
  - **Meio Ambiente**: Esmeralda (`--impact-emerald`: `#047857` / `#10B981`)
  - **Saúde**: Rich Mahogany / Mogno Avermelhado Escuro (`--impact-mahogany`: `#5C1620`)
- **Logotipo**: Engrenagem construída sob proporções de Fibonacci (`3, 5, 8, 13, 21`) com o ponto final `.` alinhado exatamente à base inferior do símbolo (`Y = 49`).

---

## Como Atualizar com os Textos Finais, Imagens e Telemetria

Todos os pontos que aguardam seus arquivos ou textos finais estão sinalizados no arquivo `index.html` com comentários `<!-- [PLACEHOLDER: ...] -->`:

1. **Logotipo Oficial e Renders do T.U.L.I.P.A.**:
   - Coloque os arquivos finais na pasta `assets/`.
   - No `index.html`, substitua o `<div class="blueprint-canvas">` na seção Hero pelo seu arquivo de render oficial do protótipo.
2. **Ficha Técnica do Protótipo**:
   - Na aba `02. Ficha Técnica do Protótipo` dentro da seção `#solucao-tulipa`, preencha os valores reais de vazão, estágios de filtragem, alimentação e sensores.
3. **Módulo de Telemetria IoT em Tempo Real (Fase Posterior)**:
   - O container `.telemetry-architecture-box` já está preparado na seção do T.U.L.I.P.A. para receber o dashboard/widget conectado à API quando for implementado.
4. **Links de Contato Direto**:
   - Na seção `#parcerias`, atualize os links `mailto:`, `https://wa.me/...`, LinkedIn e GitHub para os endereços definitivos da **GEARS.**.

---

## Como Publicar no GitHub Pages

1. Inicialize o repositório Git (caso ainda não tenha feito) e suba para o GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: site institucional GEARS. e projeto T.U.L.I.P.A."
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
   git push -u origin main
   ```
2. No GitHub, acesse **Settings > Pages**.
3. Em **Build and deployment > Source**, selecione **Deploy from a branch**.
4. Escolha a branch `main` e a pasta `/ (root)`, e clique em **Save**.
5. Seu site estará publicado em poucos segundos!
