/**
 * GEARS. — Open Source Environmental Engineering (Congonhas, MG)
 * Architecture: Vanilla ES6 Modular Controllers (Zero External Dependencies)
 * Components: Navigation, Modular Visualizer, Impact Calculator,
 * Dynamic Telemetry Simulator, Donation/PIX Subsystem, Technical Accordion FAQ.
 */

'use strict';

const GEARS = {
  /**
   * --------------------------------------------------------------------------
   * 1. Navigation & Scroll Controller
   * --------------------------------------------------------------------------
   */
  Navigation: {
    init() {
      const mobileToggle = document.querySelector('.mobile-nav-toggle') || document.getElementById('mobile-menu-toggle');
      const navMenu = document.getElementById('nav-menu');
      const navLinks = document.querySelectorAll('.nav-links .nav-link, .nav-menu .nav-link');
      const progressBar = document.getElementById('scroll-progress-bar');
      const sections = document.querySelectorAll('section[id]');

      // Mobile Menu Toggle
      if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
          const isExpanded = mobileToggle.getAttribute('aria-expanded') === 'true';
          mobileToggle.setAttribute('aria-expanded', String(!isExpanded));
          navMenu.classList.toggle('open');
        });

        // Close on link click
        navLinks.forEach((link) => {
          link.addEventListener('click', () => {
            navMenu.classList.remove('open');
            if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'false');
          });
        });
      }

      // Scroll Spy & Scroll Progress Indicator
      window.addEventListener('scroll', () => {
        // Progress Bar
        if (progressBar) {
          const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
          const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
          const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
          progressBar.style.width = `${scrolled}%`;
        }

        // Section Highlight
        const scrollPos = window.scrollY + 140;
        sections.forEach((sec) => {
          const top = sec.offsetTop;
          const height = sec.offsetHeight;
          const id = sec.getAttribute('id');
          if (scrollPos >= top && scrollPos < top + height) {
            navLinks.forEach((link) => {
              link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
            });
          }
        });
      }, { passive: true });

      // Technical Tab Switching (T.U.L.I.P.A. section)
      const tabBtns = document.querySelectorAll('[data-tech-tab]');
      const tabPanels = document.querySelectorAll('[data-tech-panel]');
      tabBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          const target = btn.getAttribute('data-tech-tab');
          tabBtns.forEach((b) => {
            b.classList.remove('active');
            b.setAttribute('aria-selected', 'false');
          });
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');

          tabPanels.forEach((p) => {
            p.classList.toggle('active', p.getAttribute('data-tech-panel') === target);
          });
        });
      });
    }
  },

  /**
   * --------------------------------------------------------------------------
   * 2. Modular Exploded Visualizer Controller
   * --------------------------------------------------------------------------
   */
  Visualizer: {
    modulesData: {
      'mod-petal': {
        code: 'MOD-TUL-01 // COLETOR BIOMIMÉTICO',
        name: 'Pétalas Biomiméticas & Estação Pluvial',
        cat: 'Meio Ambiente & Aerodinâmica Urbana',
        specs: [
          ['Cota de Fixação:', '3,0 metros do solo'],
          ['Material Estrutural:', 'PETG Técnico com proteção anti-UV50+'],
          ['Função Primária:', 'Captação pluvial e difusão aerodinâmica do ar a 45°'],
          ['Troca / Manutenção:', 'Sistema Be-Clean Hot-Swap (sem ferramentas, 45s)'],
          ['Sensores Integrados:', 'Sondas de pH, Condutividade (TDS) e Turbidez Óptica']
        ]
      },
      'mod-casing': {
        code: 'MOD-TUL-02 // ISOLAMENTO & COIFA',
        name: 'Módulo de Tampas (Interna & Externa)',
        cat: 'Fluidodinâmica & Blindagem',
        specs: [
          ['Vedação:', 'Guarnições de silicone alimentar anti-bypass'],
          ['Resistência:', 'Radiação solar contínua, névoa ácida e poeira'],
          ['Fixadores:', 'Aço Inoxidável 316 naval com travamento mecânico'],
          ['FEARS.™ Upgrade:', 'Fibra de Carbono Pre-Preg autoclave (-35% arrasto)']
        ]
      },
      'mod-filter': {
        code: 'MOD-TUL-03 // FILTRAGEM MECÂNICA',
        name: 'Cassete de Filtragem Multiestágio (HEPA H13)',
        cat: 'Saúde Pública & Retenção de Aerossóis',
        specs: [
          ['Estágio 1:', 'Pré-filtro lavável (fuligem e poeira mineral grossa)'],
          ['Estágio 2:', 'Manta de carvão ativado com absorção de gases ácidos'],
          ['Estágio 3:', 'Filtro HEPA Classe H13 (99,97% para PM2.5 / PM10)'],
          ['Estágio 4:', 'Atenuador acústico de poliuretano expandido (< 42 dBA)'],
          ['Troca Rápida:', 'Gaveta deslizante frontal com engate rápido']
        ]
      },
      'mod-motherboard': {
        code: 'MOD-TUL-04 // CÉREBRO ELETRÔNICO',
        name: 'Placa-Mãe Industrial & MCU ESP32-S3',
        cat: 'Eletrônica Embarcada & Controle Closed-Loop',
        specs: [
          ['Processador:', 'ESP32-S3 Dual-Core Xtensa LX7 @ 240MHz'],
          ['Proteção:', 'Verniz conformal IPC-CC-830 anti-umidade e poeira'],
          ['Segurança:', 'Criptochip de hardware ATECC608A para autenticidade'],
          ['Conectividade:', 'Wi-Fi 802.11 b/g/n + Rádio LoRa Mesh 915MHz']
        ]
      },
      'mod-battery': {
        code: 'MOD-TUL-05 // ENERGIA & BMS',
        name: 'Módulo de Bateria LiFePO4 & Gestão Ativa',
        cat: 'Armazenamento Energético & Resiliência',
        specs: [
          ['Química:', 'Fosfato de Ferro-Lítio (LiFePO4) 12.8V 6Ah (76.8Wh)'],
          ['BMS:', 'Balanceamento ativo de células e proteção térmica'],
          ['Operação:', 'Contínua durante desligamento diurno da iluminação'],
          ['Ciclos de Vida:', '> 3.000 ciclos até 80% capacidade']
        ]
      },
      'mod-io': {
        code: 'MOD-TUL-06 // BARRAMENTO I/O',
        name: 'Módulo de Entradas & Barramento M12',
        cat: 'Conectividade de Campo & Diagnóstico',
        specs: [
          ['Conectores:', 'M12 Baioneta industrial com certificação IP68'],
          ['Interface Local:', 'USB-C magnética com proteção contra surtos ESD (±15kV)'],
          ['Alimentação:', 'Entrada universal 12V/5V chaveada blindada']
        ]
      },
      'mod-telemetry': {
        code: 'MOD-TUL-07 // ANÁLISE PLUVIAL',
        name: 'Câmara Físico-Química Pluvial & Microclima',
        cat: 'Monitoramento Ambiental em Tempo Real',
        specs: [
          ['Sensor Pluvial:', 'Eletrodo selado de pH e sensor condutimétrico TDS'],
          ['Turbidímetro:', 'Célula óptica de espalhamento nephelométrico'],
          ['Estação Climática:', 'BME280 (Pressão, Umidade e Temperatura)'],
          ['Auditória PM:', 'Sensor laser duplo Plantower PMS7003']
        ]
      },
      'mod-fears-turbo': {
        code: 'FEARS-PWR-01 // DIVISION TUNING',
        name: 'Turbina Hiperbárica de Alta Vazão (FEARS.™)',
        cat: 'Ultra-Performance & Operação em Severidade Máxima',
        specs: [
          ['Vazão:', '836 m³/h (+120% sobre a unidade padrão GEARS.)'],
          ['Mancais:', 'Cerâmica de Nitreto de Silício com levitação magnética'],
          ['Construção:', 'Rotor em Alumínio 6061 usinado CNC em 5 eixos'],
          ['Finalidade:', 'Frentes de lavra poeirentas e mineradoras subterrâneas']
        ]
      }
    },

    init() {
      const container = document.getElementById('modular-visualizer');
      if (!container) return;

      const stage = document.getElementById('visualizer-stage');
      const btnExploded = document.getElementById('btn-toggle-exploded');
      const btnFearsBoost = document.getElementById('fears-boost-toggle');
      const btnReset = document.getElementById('btn-reset-view');
      const ecoBtns = container.querySelectorAll('.eco-btn');
      const moduleBtns = container.querySelectorAll('.module-btn[data-module]');
      const modGroups = container.querySelectorAll('.mod-group');

      // Exploded View Toggle
      if (btnExploded && stage) {
        btnExploded.addEventListener('click', () => {
          const isExploded = stage.classList.toggle('exploded-view');
          btnExploded.setAttribute('aria-pressed', String(isExploded));
          btnExploded.classList.toggle('active', isExploded);
        });
      }

      // FEARS Boost Toggle
      if (btnFearsBoost && stage) {
        btnFearsBoost.addEventListener('click', () => {
          const isActive = stage.classList.toggle('fears-mode-active');
          btnFearsBoost.setAttribute('aria-pressed', String(isActive));
          btnFearsBoost.classList.toggle('active', isActive);
          if (isActive) {
            this.selectModule('mod-fears-turbo');
            GEARS.Toasts.show('FEARS.™ Boost Ativado: Turbina Hiperbárica +120% vazão');
          }
        });
      }

      // Ecosystem Selector
      ecoBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          ecoBtns.forEach((b) => {
            b.classList.remove('active');
            b.setAttribute('aria-checked', 'false');
          });
          btn.classList.add('active');
          btn.setAttribute('aria-checked', 'true');

          const eco = btn.getAttribute('data-eco');
          if (eco === 'fears') {
            stage.classList.add('fears-mode-active');
            if (btnFearsBoost) btnFearsBoost.classList.add('active');
            this.selectModule('mod-fears-turbo');
          } else {
            stage.classList.remove('fears-mode-active');
            if (btnFearsBoost) btnFearsBoost.classList.remove('active');
            this.selectModule('mod-petal');
          }
        });
      });

      // Reset View
      if (btnReset && stage) {
        btnReset.addEventListener('click', () => {
          stage.classList.remove('exploded-view', 'fears-mode-active');
          if (btnExploded) {
            btnExploded.classList.remove('active');
            btnExploded.setAttribute('aria-pressed', 'false');
          }
          if (btnFearsBoost) {
            btnFearsBoost.classList.remove('active');
            btnFearsBoost.setAttribute('aria-pressed', 'false');
          }
          ecoBtns.forEach((b, idx) => {
            b.classList.toggle('active', idx === 0);
            b.setAttribute('aria-checked', String(idx === 0));
          });
          this.selectModule('mod-petal');
        });
      }

      // Select Module on Button Click
      moduleBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          const modId = btn.getAttribute('data-module');
          this.selectModule(modId);
        });
      });

      // Select Module on SVG click
      modGroups.forEach((grp) => {
        grp.addEventListener('click', () => {
          const modId = grp.getAttribute('data-module');
          this.selectModule(modId);
        });
      });
    },

    selectModule(modId) {
      const data = this.modulesData[modId];
      if (!data) return;

      // Update Inspector Panel
      const codeEl = document.getElementById('inspector-code');
      const nameEl = document.getElementById('inspector-name');
      const catEl = document.getElementById('inspector-cat');
      const specsTable = document.getElementById('inspector-specs');

      if (codeEl) codeEl.textContent = data.code;
      if (nameEl) nameEl.textContent = data.name;
      if (catEl) catEl.textContent = data.cat;

      if (specsTable) {
        specsTable.innerHTML = data.specs
          .map(([lbl, val]) => `<tr><td>${lbl}</td><td>${val}</td></tr>`)
          .join('');
      }

      // Highlight active module button
      const moduleBtns = document.querySelectorAll('.module-btn[data-module]');
      moduleBtns.forEach((b) => {
        b.classList.toggle('active', b.getAttribute('data-module') === modId);
      });

      // Highlight active SVG group & dim others
      const modGroups = document.querySelectorAll('.mod-group');
      modGroups.forEach((grp) => {
        const isCurrent = grp.getAttribute('data-module') === modId;
        grp.classList.toggle('active', isCurrent);
        grp.classList.toggle('dimmed', !isCurrent);
      });
    }
  },

  /**
   * --------------------------------------------------------------------------
   * 3. Particulate Impact Calculator Controller
   * --------------------------------------------------------------------------
   */
  Calculator: {
    presets: {
      'julia-kubitschek': { nodes: 15, pm: 65, hours: 24, label: 'Av. Júlia Kubitschek' },
      'bom-jesus': { nodes: 8, pm: 40, hours: 18, label: 'Rua Bom Jesus & Centro' },
      'cinturao-mina': { nodes: 25, pm: 95, hours: 24, label: 'Cinturão de Mineração' }
    },

    init() {
      const rangeFlow = document.getElementById('calc-range-flow');
      const rangePm = document.getElementById('calc-range-pm');
      const rangeHours = document.getElementById('calc-range-hours');
      const fearsBoost = document.getElementById('fears-boost-calc-toggle');
      const exportBtn = document.getElementById('btn-export-calc');
      const presetBtns = document.querySelectorAll('.preset-btn[data-preset]');

      if (!rangeFlow || !rangePm || !rangeHours) return;

      const runUpdate = () => this.update();

      rangeFlow.addEventListener('input', runUpdate);
      rangePm.addEventListener('input', runUpdate);
      rangeHours.addEventListener('input', runUpdate);
      if (fearsBoost) fearsBoost.addEventListener('change', runUpdate);

      // Presets
      presetBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          presetBtns.forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');

          const key = btn.getAttribute('data-preset');
          const p = this.presets[key];
          if (p) {
            rangeFlow.value = p.nodes;
            rangePm.value = p.pm;
            rangeHours.value = p.hours;
            this.update();
            GEARS.Toasts.show(`Preset aplicado: ${p.label}`);
          }
        });
      });

      // Export report button
      if (exportBtn) {
        exportBtn.addEventListener('click', () => {
          const report = this.generateReportText();
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(report).then(() => {
              GEARS.Toasts.show('Relatório da simulação copiado com sucesso!');
            }).catch(() => {
              this.fallbackCopy(report);
            });
          } else {
            this.fallbackCopy(report);
          }
        });
      }

      this.update();
    },

    update() {
      const rangeFlow = document.getElementById('calc-range-flow');
      const rangePm = document.getElementById('calc-range-pm');
      const rangeHours = document.getElementById('calc-range-hours');
      const fearsBoost = document.getElementById('fears-boost-calc-toggle');

      const nodes = parseInt(rangeFlow.value, 10);
      const pm = parseInt(rangePm.value, 10);
      const hours = parseInt(rangeHours.value, 10);
      const isFears = fearsBoost ? fearsBoost.checked : false;

      // Update slider value labels
      const valNodes = document.getElementById('val-nodes');
      const valPm = document.getElementById('val-pm');
      const valHours = document.getElementById('val-hours');

      if (valNodes) valNodes.textContent = `${nodes} postes`;
      if (valPm) valPm.textContent = `${pm} µg/m³`;
      if (valHours) valHours.textContent = `${hours} horas (${hours === 24 ? 'Contínuo' : 'Diário'})`;

      // Mathematical formulas:
      // Flow per node: 380 m³/h (or 836 m³/h with FEARS turbo)
      const flowPerUnit = isFears ? 836 : 380;
      const dailyVolume = nodes * flowPerUnit * hours;
      const annualVolume = dailyVolume * 365;

      // Particulate Mass Filtered:
      // Volume (m³/ano) * Concentration (µg/m³) * HEPA Efficiency (0.9997) * 10^-9 (kg/µg)
      const annualMassKg = annualVolume * pm * 0.9997 * 1e-9;

      // Respiratory consultations prevented: WHO epidemiologic ratio
      const consultations = Math.max(1, Math.round(annualMassKg * 0.207));

      // Display in UI
      const cleanAirEl = document.getElementById('calc-clean-air');
      const massPmEl = document.getElementById('calc-mass-pm');
      const healthEl = document.getElementById('calc-health-savings');

      if (cleanAirEl) {
        cleanAirEl.textContent = `${annualVolume.toLocaleString('pt-BR')} m³/ano`;
      }
      if (massPmEl) {
        cleanAirEl.textContent = `${annualVolume.toLocaleString('pt-BR')} m³/ano`;
        massPmEl.textContent = `${annualMassKg.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} kg/ano`;
      }
      if (healthEl) {
        healthEl.textContent = `~${consultations.toLocaleString('pt-BR')} atendimentos`;
      }
    },

    generateReportText() {
      const nodes = document.getElementById('calc-range-flow')?.value || 10;
      const pm = document.getElementById('calc-range-pm')?.value || 45;
      const hours = document.getElementById('calc-range-hours')?.value || 24;
      const isFears = document.getElementById('fears-boost-calc-toggle')?.checked ? 'SIM (Twin-Turbine 836 m³/h)' : 'NÃO (GEARS Standard 380 m³/h)';
      const air = document.getElementById('calc-clean-air')?.textContent || '';
      const mass = document.getElementById('calc-mass-pm')?.textContent || '';
      const health = document.getElementById('calc-health-savings')?.textContent || '';

      return `RELATÓRIO TÉCNICO DE SIMULAÇÃO // T.U.L.I.P.A.™ - GEARS. CORPORATION
Localidade: Congonhas (MG) — Quadrilátero Ferrífero
Parâmetros de Entrada:
- Unidades / Postes Instalados: ${nodes} nós
- Concentração de Particulado Ambiente (PM2.5 / PM10): ${pm} µg/m³
- Regime de Operação Diária: ${hours} horas/dia
- Pacote FEARS.™ High-Performance: ${isFears}

Resultados Anuais Projetados:
- Volume de Ar Descontaminado: ${air}
- Massa de Pó de Minério (Hematita/Sílica) Retida: ${mass}
- Redução Estimada de Atendimentos Respiratórios: ${health}
Metodologia: Equações de Balanço de Massa Atmosférica & Eficiência HEPA H13 (99.97%).
Auditável em: https://github.com/gearsbr/gearsbr`;
    },

    fallbackCopy(text) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
        GEARS.Toasts.show('Relatório copiado com sucesso!');
      } catch (err) {
        console.error('Falha ao copiar:', err);
      }
      document.body.removeChild(ta);
    }
  },

  /**
   * --------------------------------------------------------------------------
   * 4. Dynamic Telemetry Simulator Controller
   * --------------------------------------------------------------------------
   */
  Telemetry: {
    timer: null,
    basePM25: 18.4,
    basePM10: 34.2,
    baseFilter: 84.3,

    init() {
      const bar = document.getElementById('telemetry-bar');
      if (!bar) return;

      const pm25El = document.getElementById('telemetry-pm25-val');
      const pm10El = document.getElementById('telemetry-pm10-val');
      const filterEl = document.getElementById('telemetry-filter-gauge');

      const tick = () => {
        // Micro-jitter: +/- 0.8% organic variation
        const jitter25 = (Math.random() - 0.5) * 0.6;
        const jitter10 = (Math.random() - 0.5) * 1.0;

        const cur25 = Math.max(12.0, this.basePM25 + jitter25);
        const cur10 = Math.max(20.0, this.basePM10 + jitter10);

        if (pm25El) pm25El.textContent = `${cur25.toFixed(1)} µg/m³`;
        if (pm10El) pm10El.textContent = `${cur10.toFixed(1)} µg/m³`;
      };

      this.timer = setInterval(tick, 2800);

      // Pause when page is backgrounded for battery & CPU conservation
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          if (this.timer) clearInterval(this.timer);
        } else {
          this.timer = setInterval(tick, 2800);
        }
      });
    }
  },

  /**
   * --------------------------------------------------------------------------
   * 5. Donation & Accessible PIX Modal Controller
   * --------------------------------------------------------------------------
   */
  Donation: {
    pixKeys: {
      email: 'gabrielrossipe@gmail.com',
      cnpj: '58.214.932/0001-44'
    },

    init() {
      const modal = document.getElementById('pix-modal');
      const openBtns = document.querySelectorAll('[data-open-modal="pix-modal"]');
      const closeBtn = document.getElementById('close-pix-modal');
      const copyBtn = document.getElementById('copy-pix-btn');
      const copyTextSpan = document.getElementById('copy-pix-btn-text');
      const statusSpan = document.getElementById('pix-copy-status');
      const keyInput = document.getElementById('pix-key-input');
      const presetBtns = document.querySelectorAll('.pix-preset-btn');

      if (!modal) return;

      // Open Modal Handlers
      openBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          if (typeof modal.showModal === 'function') {
            modal.showModal();
          } else {
            modal.setAttribute('open', '');
          }

          // If button specified tier amount, select that preset
          const tierAmount = btn.getAttribute('data-tier-amount');
          if (tierAmount && presetBtns.length) {
            presetBtns.forEach((pBtn) => {
              pBtn.classList.toggle('active', pBtn.getAttribute('data-amount') === tierAmount);
            });
          }
        });
      });

      // Close Modal Handler
      const closeModal = () => {
        if (typeof modal.close === 'function') {
          modal.close();
        } else {
          modal.removeAttribute('open');
        }
      };

      if (closeBtn) closeBtn.addEventListener('click', closeModal);

      // Close on backdrop click
      modal.addEventListener('click', (evt) => {
        const rect = modal.getBoundingClientRect();
        const isInDialog = (
          rect.top <= evt.clientY &&
          evt.clientY <= rect.top + rect.height &&
          rect.left <= evt.clientX &&
          evt.clientX <= rect.left + rect.width
        );
        if (!isInDialog) {
          closeModal();
        }
      });

      // Close on Escape key
      modal.addEventListener('keydown', (evt) => {
        if (evt.key === 'Escape') {
          closeModal();
        }
      });

      // Preset Amount Buttons
      presetBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          presetBtns.forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');
          const amount = btn.getAttribute('data-amount');
          GEARS.Toasts.show(`Valor selecionado: R$ ${amount},00`);
        });
      });

      // 1-Click PIX Clipboard Copy
      if (copyBtn && keyInput) {
        copyBtn.addEventListener('click', () => {
          const keyToCopy = keyInput.value.trim();

          const setSuccessState = () => {
            copyBtn.classList.add('copied');
            if (copyTextSpan) copyTextSpan.textContent = '✓ CHAVE COPIADA COM SUCESSO!';
            if (statusSpan) statusSpan.textContent = 'Chave copiada para a área de transferência.';
            GEARS.Toasts.show('✓ Chave PIX copiada com sucesso!');

            setTimeout(() => {
              copyBtn.classList.remove('copied');
              if (copyTextSpan) copyTextSpan.textContent = 'Copiar Chave PIX';
              if (statusSpan) statusSpan.textContent = '';
            }, 2500);
          };

          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(keyToCopy).then(setSuccessState).catch(() => {
              this.fallbackCopy(keyInput, setSuccessState);
            });
          } else {
            this.fallbackCopy(keyInput, setSuccessState);
          }
        });
      }
    },

    fallbackCopy(inputEl, onSuccess) {
      inputEl.focus();
      inputEl.select();
      try {
        const ok = document.execCommand('copy');
        if (ok && onSuccess) onSuccess();
      } catch (err) {
        console.error('Fallback copy falhou:', err);
      }
    }
  },

  /**
   * --------------------------------------------------------------------------
   * 6. Technical Accordion FAQ Controller
   * --------------------------------------------------------------------------
   */
  FAQ: {
    init() {
      const triggers = document.querySelectorAll('.accordion-trigger[aria-controls]');
      const categoryBtns = document.querySelectorAll('.faq-category-btn[data-category]');
      const faqItems = document.querySelectorAll('.accordion-item[data-category]');

      // Accordion Toggle
      triggers.forEach((btn) => {
        btn.addEventListener('click', () => {
          const isExpanded = btn.getAttribute('aria-expanded') === 'true';
          const panelId = btn.getAttribute('aria-controls');
          const panel = document.getElementById(panelId);

          btn.setAttribute('aria-expanded', String(!isExpanded));
          if (panel) {
            panel.classList.toggle('open', !isExpanded);
          }
        });
      });

      // Category Filtering
      categoryBtns.forEach((catBtn) => {
        catBtn.addEventListener('click', () => {
          categoryBtns.forEach((b) => b.classList.remove('active'));
          catBtn.classList.add('active');

          const category = catBtn.getAttribute('data-category');
          faqItems.forEach((item) => {
            if (category === 'all' || item.getAttribute('data-category') === category) {
              item.style.display = 'block';
            } else {
              item.style.display = 'none';
            }
          });
        });
      });
    }
  },

  /**
   * --------------------------------------------------------------------------
   * 7. Lightweight Toast Notification Utility
   * --------------------------------------------------------------------------
   */
  Toasts: {
    show(message, duration = 3000) {
      const container = document.getElementById('toast-container');
      if (!container) return;

      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.setAttribute('role', 'status');
      toast.textContent = message;

      container.appendChild(toast);

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 250ms ease';
        setTimeout(() => {
          if (container.contains(toast)) container.removeChild(toast);
        }, 250);
      }, duration);
    }
  },

  /**
   * --------------------------------------------------------------------------
   * Global Initialization
   * --------------------------------------------------------------------------
   */
  init() {
    this.Navigation.init();
    this.Visualizer.init();
    this.Calculator.init();
    this.Telemetry.init();
    this.Donation.init();
    this.FAQ.init();
  }
};

// Auto-run on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => GEARS.init());
} else {
  GEARS.init();
}

// Expose globally for testing suites and automated assertions
window.GEARS = GEARS;
