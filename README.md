# Projeto de Transmissão de Calor: Cozimento de Ovo

## Descrição do Projeto

Este projeto simula o processo de transmissão de calor durante o cozimento de um ovo usando modelos simplificados de engenharia mecânica. O projeto aborda os três mecanismos de transferência de calor:

1. **Condução**: Transferência de calor através da casca e interior do ovo
2. **Convecção**: Transferência de calor entre a água quente e a superfície do ovo
3. **Radiação**: Efeitos secundários (desprezíveis neste caso)

## Objetivos

- Modelar matematicamente o processo de aquecimento do ovo
- Simular a distribuição de temperatura no tempo
- Analisar o tempo necessário para diferentes níveis de cozimento
- Validar resultados com dados experimentais conhecidos

## Estrutura do Projeto

```
/workspace/
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências Python
├── src/
│   ├── heat_transfer_model.py   # Modelo matemático principal
│   ├── egg_simulation.py        # Simulação do cozimento
│   ├── visualization.py         # Gráficos e visualizações
│   └── parametric_analysis.py   # Análise paramétrica
├── data/
│   └── egg_properties.json      # Propriedades físicas do ovo
├── results/
│   └── (arquivos gerados)       # Resultados das simulações
└── docs/
    ├── teoria.md               # Fundamentação teórica
    └── resultados.md           # Análise dos resultados
```

## Modelos Físicos Utilizados

### 1. Modelo de Condução Esférica
- Equação de difusão de calor em coordenadas esféricas
- Condições de contorno convectivas
- Propriedades termofísicas variáveis

### 2. Modelo de Convecção
- Correlações para transferência de calor em esferas
- Número de Nusselt em função do Reynolds e Prandtl
- Coeficiente de transferência de calor convectivo

### 3. Simplificações Adotadas
- Geometria esférica simplificada
- Propriedades homogêneas por região (clara/gema)
- Estado quasi-estacionário para a convecção

## Como Executar

### Opção 1: Execução Completa (Recomendada)
```bash
# Instalar dependências (se necessário)
pip install --break-system-packages numpy scipy matplotlib pandas seaborn

# Executar análise completa
python3 run_complete_analysis.py
```

### Opção 2: Execução Modular
```bash
# Modelo básico
python3 -c "
import sys; sys.path.append('./src')
from heat_transfer_model import EggHeatTransferModel
model = EggHeatTransferModel('./data/egg_properties.json')
print(f'Biot = {model.calculate_biot_number():.3f}')
"

# Simulação completa
python3 -c "
import sys; sys.path.append('./src')
import matplotlib; matplotlib.use('Agg')
from egg_simulation import EggCookingSimulation
sim = EggCookingSimulation('./data/egg_properties.json')
results = sim.run_complete_simulation(max_time=600)
sim.generate_report()
"

# Análise de convecção
python3 -c "
import sys; sys.path.append('./src')
from convection_analysis import ConvectionAnalysis
conv = ConvectionAnalysis('./data/egg_properties.json')
print('Análise de convecção executada!')
"
```

### Opção 3: Notebook Jupyter
```bash
# Instalar jupyter (se necessário)
pip install --break-system-packages jupyter

# Executar notebook
jupyter notebook egg_cooking_analysis.ipynb
```

## Resultados Esperados

- Perfis de temperatura vs tempo
- Distribuição espacial de temperatura
- Tempo de cozimento para diferentes condições
- Análise de sensibilidade dos parâmetros

## Autor

Projeto desenvolvido para demonstrar aplicações de transferência de calor em engenharia mecânica.