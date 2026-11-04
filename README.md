# GEARS. — Apple Open Source & Engenharia de Precisão

Portal institucional oficial da **GEARS. Corporation**, holding de tecnologia ambiental e engenharia de hardware aberta sediada em **Congonhas (Minas Gerais)**. Desenvolvedora do purificador urbano biomimético **T.U.L.I.P.A.™** (*Treatment Unit & Localized Isolation of Polluted Air*) e da divisão de alto rendimento e customização modular **FEARS.™** (*High-Performance Tuning*).

---

## 1. Filosofia de Engenharia: "Apple Open Source com Modularidade Controlada"

A **GEARS. Corporation** supera a falsa dicotomia entre:
- **O Modelo Creality (Open Source Caótico)**: Acesso livre com tolerâncias imprecisas, gambiarras e ausência de repetibilidade física.
- **O Modelo Bambu Lab (Jardim Murado)**: Alta engenharia com fechamento proprietário, componentes criptografados e repressão ao reparo independente.

**Nossa Solução ("Controlled High-Standard Modularity")**:
Operamos como a *Bambu Lab da infraestrutura ambiental e saúde pública*, onde todas as expansões, engates rápidos (*Hot-Swap*) e módulos oficiais são fabricados sob rigor laboratorial e tolerâncias micrométricas autoritárias. Simultaneamente, 100% dos esquemáticos, pinouts de barramento, firmwares e telemetria atmosférica são abertos, públicos e matematicamente auditáveis.

---

## 2. Estrutura Corporativa: GEARS. & FEARS.™

- **Divisão GEARS.**: Foco em infraestrutura cívica, saúde pública respiratória, análise pluvial em tempo real e educação maker em escolas públicas (IFMG).
- **Divisão FEARS.™**: O análogo direto à Mercedes-AMG e Maybach para a GEARS. Corporation — fornece customização sob medida, componentes em fibra de carbono autoclave, turbinas hiperbáricas de alta vazão (+120%) e ionização bipolar a plasma para regimes operacionais severos (frentes de lavra, plantas químicas e mineração subterrânea).

---

## 3. Arquitetura de Hardware: Os 7 Módulos de Precisão

1. **Módulo de Câmera & Inspeção Óptica**: Sensor CMOS 1080p selado IP67 com câmara óptica estanque (Upgrade FEARS: Espectro Duplo RGB+NIR com Edge-AI).
2. **Módulo de Tampas (Interna & Externa)**: Coifa em formato de tulipa em PETG UV50+ e isolamento anti-bypass (Upgrade FEARS: Fibra de Carbono Pre-Preg e parafusos em Titânio Grau 5).
3. **Módulo de Filtragem Multiestágio**: 4 estágios com Pré-filtro lavável, Manta de carvão ativado, Filtro HEPA H13 (99.97% @ 0.3µm) e atenuador acústico (&lt; 42 dBA) com engate rápido *Be-Clean Hot-Swap*.
4. **Módulo da Placa-Mãe & MCU**: PCB 4 camadas com verniz conformal, ESP32-S3 Dual-Core e criptochip de hardware ATECC608A (Upgrade FEARS: Dual-MCU redundante com CAN-FD).
5. **Módulo de Bateria & BMS**: Pack LiFePO4 12.8V 76.8Wh com balanceamento ativo de células (Upgrade FEARS: 230Wh com MPPT solar integrado).
6. **Módulo de Entradas & Barramento I/O**: Conectores industriais M12 baioneta IP68 e porta USB-C magnética com proteção ESD &plusmn;15kV.
7. **Módulo Pluvial & Microclima**: Funil central com eletrodo de pH, condutividade TDS, turbidímetro e sensores laser diferenciais de PM2.5/PM10 na cota humana de 1 metro.

---

## 4. Design System & Identidade Visual

- **Canvas Principal**: Off-White acetinado de alto padrão (`--bg-canvas: #FBFBFD;`, `--bg-surface-elevated: #F8F9FA;`) inspirado na estética Apple e Bambu Lab, eliminando ofuscamento ocular.
- **Paleta Canônica GEARS.**:
  - Azul-Marinho Profundo (`--gears-navy: #0A192F;`) — Contraste 17.03:1 (WCAG 2.1 AAA certificado)
  - Azul-Petróleo Técnico (`--gears-petrol: #0F3A4D;`) — Contraste 11.73:1
- **Paleta FEARS.™ Performance**:
  - Carbon Black (`--fears-carbon: #060D17;`)
  - Cyan Petronas / Alto Rendimento (`--fears-cyan: #00D2BE;`)
- **Eixos de Impacto**:
  - Meio Ambiente: Esmeralda (`--impact-emerald: #047857;`)
  - Saúde Humana: Rich Mahogany (`--impact-mahogany: #5C1620;`)
- **Logotipo Vetorial Canônico**: Engrenagem sólida de 8 dentes simétricos retos chanfrados, orifício central transparente via `fill-rule="evenodd"`, alinhada na linha de base Y=49 com ponto terminal retangular.

---

## 5. Componentes Interativos de Frontend (Vanilla ES6+)

1. **Visualizador Modular Explodido (`GEARS.Visualizer`)**:
   - Transições de expansão mecânica sequencial via CSS `translate(x, y)` 60fps.
   - Alternância entre ecossistema cívico GEARS. e módulo turbo FEARS.™.
   - Painel de inspeção dinâmica de especificações com foco tátil e marcação CAD.
2. **Calculadora de Impacto de Particulados (`GEARS.Calculator`)**:
   - Sliders táteis para simulação de postes, concentração de particulado (PM2.5/PM10) e horas de operação.
   - Presets geográficos de Congonhas (Av. Júlia Kubitschek, Rua Bom Jesus, Cinturão de Lavra).
   - Exportação em 1 clique de relatório formal para propostas municipais.
3. **Simulador de Telemetria Dinâmica (`GEARS.Telemetry`)**:
   - Barra de status com oscilação orgânica realista (&plusmn;0.8%) para PM2.5 e PM10.
   - Pulso LED de integridade de sinal e vida útil do filtro HEPA.
   - Suspensão automática via `visibilitychange` quando a aba fica em segundo plano.
4. **Subsistema de Doação & Modal PIX Acessível (`GEARS.Donation`)**:
   - Modal nativo `<dialog id="pix-modal">` com retenção de foco (focus trap) e descarte via tecla Escape.
   - QR Code vetorial SVG com engrenagem GEARS. centralizada.
   - Cópia da chave em 1 clique via Clipboard API com feedback visual instantâneo (*"✓ Chave Copiada com Sucesso!"*) e fallback automático.
   - Dados bancários oficiais (Banco Inter / Cora SCD, Agência 0001, Conta 2849102-4, CNPJ 58.214.932/0001-44).
5. **FAQ Técnico em Acordeão (`GEARS.FAQ`)**:
   - Expansão suave via CSS Grid `grid-template-rows: 0fr -> 1fr` sem hacks de `max-height`.
   - Filtros por categoria e acessibilidade total para leitores de tela (`aria-expanded`, `aria-controls`).

---

## 6. Estrutura do Repositório

```text
GEARS./
├── index.html            # Estrutura semântica completa com todas as seções e modal nativo
├── css/
│   └── styles.css        # Design System Off-White, tokens FEARS, bento grid, glassmorphism
├── js/
│   └── main.js           # Suíte de controladores modularizados (window.GEARS)
├── assets/
│   ├── logo-gears.svg    # Logotipo horizontal oficial (engrenagem canônica 8 dentes + texto)
│   ├── favicon.svg       # Ícone 1:1 quadrado (viewBox 0 0 100 100) para abas de navegadores
│   └── logo-fears.svg    # Insígnia oficial da divisão FEARS.™ High-Performance
└── README.md             # Documentação técnica e guia de engenharia
```

---

## 7. Como Executar e Validar Localmente

O projeto possui **zero dependências externas de compilação ou empacotamento**. Para testar localmente:

```bash
# Iniciar servidor HTTP local (Python 3)
python3 -m http.server 8000

# Abrir no navegador:
# http://localhost:8000
```

---

## 8. Governança e Liderança

- **Fundador & Arquiteto-Chefe de Hardware**: Gabriel Rossi Pereira
- **Representante Legal & Gestão Institucional**: Paula Rossi de Oliveira
- **Origem**: Congonhas, Minas Gerais — Brasil
- **Contato**: `gabrielrossipe@gmail.com` | WhatsApp: `(31) 98456-6074`
- **Código-Fonte Aberto**: `https://github.com/gearsbr/gearsbr`
