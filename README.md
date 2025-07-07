# Sistema de Comunicação - Interface Gráfica

Este projeto implementa uma interface gráfica para simular um sistema de comunicação com 4 camadas principais, utilizando GTK4 e Matplotlib.

## Funcionalidades Implementadas

### 1. Segmento de Configurações
- **Entradas numéricas:**
  - Taxa de Bits (bps)
  - Frequência da Portadora (Hz)
- **Seletores:**
  - Tipo de Modulação (NRZ, Manchester, Bipolar)
  - Codificação (Contagem de Caracteres, Byte Flag, Bits Flag)
  - Detecção de Erro (Paridade, CRC)
- **Botão "Aplicar Configurações"** para salvar as configurações

### 2. Segmento de Aplicação
- **Entrada:**
  - Campo de texto para entrada de dados
  - Display automático dos dados em formato de bits
- **Saída:**
  - Campo de texto para saída processada
  - Display dos dados de saída em formato de bits
- **Botão "Processar →"** para executar o processamento

### 3. Segmento de Enlace
- **4 saídas de texto em formato de bits:**
  - Dados com Codificação
  - Dados com Detecção de Erro
  - Dados com Controle de Fluxo
  - Dados Finais do Enlace

### 4. Segmento Físico
- **4 gráficos usando GraphFrame:**
  - Sinal Original
  - Sinal Modulado
  - Espectro de Frequência
  - Sinal Demodulado
- **Botão "Atualizar Gráficos"** para gerar novos dados

## Como Executar

### Pré-requisitos
```bash
# Instalar dependências do sistema
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-4.0
sudo apt-get install python3-matplotlib python3-numpy

# Ou usando pip
pip3 install PyGObject matplotlib numpy
```

### Execução
```bash
# Executar a aplicação principal
python3 src/teste.py

# Executar testes de funcionalidade
python3 src/test_demo.py
```

## Estrutura do Projeto

```
src/
├── teste.py              # Aplicação principal com interface
├── test_demo.py          # Script de testes
├── gui/
│   └── graph_frame.py    # Componente de gráfico
├── data_link_layer/      # Implementações da camada de enlace
├── physical_layer/       # Implementações da camada física
└── communication.py      # Módulo de comunicação
```

## Características Técnicas

- **Interface:** GTK4 com Python
- **Gráficos:** Matplotlib integrado com GTK4
- **Layout:** Notebook com 4 abas organizadas
- **Responsividade:** Interface redimensionável
- **Modularidade:** Componentes reutilizáveis

## Funcionalidades de Demonstração

### Conversão Texto-Bits
- Converte automaticamente texto ASCII para representação binária
- Exemplo: "Hello" → "01001000 01100101 01101100 01101100 01101111"

### Geração de Gráficos
- Sinais senoidais e modulados
- Espectros de frequência usando FFT
- Dados com ruído simulado

### Configurações Dinâmicas
- Todas as configurações são aplicáveis em tempo real
- Interface intuitiva com comboboxes e campos numéricos

## Próximos Passos

1. Integração com os módulos de comunicação existentes
2. Implementação de algoritmos reais de codificação/detecção de erro
3. Simulação de transmissão em tempo real
4. Adição de mais tipos de modulação
5. Implementação de controle de fluxo real

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste com `python3 src/test_demo.py`
5. Envie um pull request 