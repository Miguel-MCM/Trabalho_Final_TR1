# Sistema de Comunicação - Interface Gráfica

Este projeto implementa uma interface gráfica completa para simular um sistema de comunicação digital com múltiplas camadas, utilizando GTK4, NumPy e Matplotlib. O sistema simula a transmissão de dados através de diferentes técnicas de codificação, detecção/correção de erros e modulação.

## Funcionalidades Implementadas

### 1. Segmento de Configurações
- **Configurações de Enquadramento:**
  - Tamanho máximo do frame (1-100 caracteres)
  - Tipo de codificação: Nenhum, Contagem de Caracteres, Byte Flag, Bits Flag
- **Configurações de Detecção de Erro:**
  - Paridade (par/ímpar)
  - CRC (Cyclic Redundancy Check)
- **Configurações de Correção de Erro:**
  - Código de Hamming
- **Configurações de Modulação Digital:**
  - NRZ (Non-Return to Zero)
  - Bipolar
  - Manchester
  - Taxa de bits (bps)
  - Taxa de amostragem (Hz)
- **Configurações de Modulação Analógica:**
  - ASK (Amplitude Shift Keying)
  - FSK (Frequency Shift Keying)
  - PSK (Phase Shift Keying)
  - 8-QAM (Quadrature Amplitude Modulation)
  - Frequência da portadora (Hz)
  - Taxa de amostragem analógica (Hz)
- **Configurações de Canal:**
  - SNR (Signal-to-Noise Ratio) para simulação de ruído

### 2. Segmento de Aplicação
- **Entrada:**
  - Campo de texto para entrada de dados
  - Conversão automática texto → bits ASCII
  - Limitação por tamanho de frame configurável
- **Saída:**
  - Campo de texto para dados processados
  - Conversão automática bits → texto ASCII
  - Tratamento de erros de transmissão
- **Botão "Processar →"** para executar a simulação completa

### 3. Segmento de Enlace
- **Visualização em tempo real dos dados:**
  - Dados de entrada (bits originais)
  - Dados com correção de erro (Hamming)
  - Dados com detecção de erro (Paridade/CRC)
  - Dados enquadrados (com flags/contadores)
  - Bits enviados (após modulação)
  - Bits recebidos (após demodulação)
  - Dados desenquadrados
  - Dados finais (após correção/detecção de erro)

### 4. Segmento Físico
- **Gráficos em tempo real:**
  - Sinal modulado (encoder)
  - Sinal demodulado (decoder)
  - Visualização dos efeitos do ruído no canal
- **Suporte a múltiplos tipos de modulação:**
  - Modulação digital de banda base
  - Modulação analógica de portadora

## Como Executar

### Pré-requisitos
```bash
# Instalar dependências do sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-4.0
sudo apt-get install python3-matplotlib python3-numpy

# Ou usando pip
pip3 install PyGObject matplotlib numpy
```

### Execução
```bash
# Executar a aplicação principal
python3 src/main.py

# Executar testes de funcionalidade
python3 src/test.py
```

## Estrutura do Projeto

```
src/
├── main.py                    # Aplicação principal com interface GTK4
├── base_window.py            # Classe base com configurações e lógica
├── test.py                   # Script de testes e demonstração
├── main.css                  # Estilos CSS para tema escuro
├── communication.py          # Módulo de simulação de canal
├── gui/                      # Componentes da interface gráfica
│   ├── config_page.py       # Página de configurações
│   ├── aplication_frame.py  # Frame de entrada/saída
│   ├── link_page.py         # Página de visualização do enlace
│   ├── physical_page.py     # Página de visualização física
│   └── graph_frame.py       # Componente de gráfico
├── data_link_layer/          # Implementações da camada de enlace
│   ├── framer.py            # Classe base para enquadramento
│   ├── char_counting_framer.py
│   ├── byte_flag_framer.py
│   ├── bits_flag_framer.py
│   ├── error_detector.py    # Classe base para detecção de erro
│   ├── parity_error_detector.py
│   ├── crc_error_detector.py
│   └── humming_error_corrector.py
└── physical_layer/           # Implementações da camada física
    ├── digital_modulator.py  # Classe base para modulação digital
    ├── nrz_modulator.py
    ├── bipolar_modulator.py
    ├── manchester_modulator.py
    ├── carrier_modulator.py  # Classe base para modulação analógica
    ├── ask_carrier_modulator.py
    ├── fsk_carrier_modulator.py
    ├── psk_carrier_modulator.py
    └── qam_carrier_modulator.py
```

## Características Técnicas

### Interface
- **Framework:** GTK4 com Python
- **Tema:** Modo escuro personalizado com CSS
- **Layout:** Notebook com 4 abas organizadas
- **Responsividade:** Interface redimensionável
- **Modularidade:** Componentes reutilizáveis

### Processamento de Dados
- **Codificação:** Conversão automática texto ↔ bits ASCII
- **Enquadramento:** Múltiplas técnicas (contagem, flags)
- **Detecção de Erro:** Paridade e CRC
- **Correção de Erro:** Código de Hamming
- **Modulação:** Digital (NRZ, Bipolar, Manchester) e Analógica (ASK, FSK, PSK, QAM)
- **Canal:** Simulação de ruído com SNR configurável

### Visualização
- **Gráficos:** Matplotlib integrado com GTK4
- **Tempo Real:** Atualização automática dos dados
- **Múltiplas Camadas:** Visualização separada por camada
- **Debugging:** Exibição de dados intermediários

## Funcionalidades de Demonstração

### Fluxo Completo de Transmissão
1. **Entrada:** Texto convertido para bits ASCII
2. **Correção:** Aplicação de código de Hamming (opcional)
3. **Detecção:** Adição de bits de paridade ou CRC
4. **Enquadramento:** Adição de flags ou contadores
5. **Modulação:** Conversão para sinal analógico
6. **Transmissão:** Simulação de canal com ruído
7. **Demodulação:** Conversão de volta para bits
8. **Processamento:** Desenquadramento e correção de erros
9. **Saída:** Conversão de bits para texto

### Exemplos de Configuração
- **Configuração Básica:** NRZ + Contagem de Caracteres + Paridade
- **Configuração Avançada:** Manchester + Byte Flag + CRC + Hamming
- **Configuração Analógica:** 8-QAM + Bits Flag + CRC

## Licença

Este projeto é parte do trabalho final de Telecomunicações e Redes 1. 