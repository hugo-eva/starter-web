# 🥚 Projeto de Transferência de Calor: Cozimento de Ovo

## 📋 Resumo Executivo

Este projeto implementa uma análise completa do processo de transferência de calor durante o cozimento de um ovo, utilizando modelos simplificados de engenharia mecânica. O projeto foi desenvolvido em Python e inclui simulações numéricas, análises paramétricas, otimização e visualizações avançadas.

## 🎯 Objetivos Alcançados

✅ **Modelagem Matemática Completa**
- Modelo de capacidade concentrada
- Solução por diferenças finitas 
- Solução analítica por séries
- Análise de convecção natural e forçada

✅ **Simulação Numérica**
- Evolução temporal das temperaturas
- Distribuição espacial de calor
- Identificação dos estágios de cozimento
- Comparação entre diferentes modelos

✅ **Análise Paramétrica**
- Influência do tamanho do ovo
- Efeito da temperatura da água
- Impacto do coeficiente de convecção
- Otimização para tempos específicos

✅ **Visualizações Avançadas**
- Gráficos 2D e 3D
- Animações temporais
- Visualizações interativas (HTML)
- Mapas de calor

## 📁 Estrutura do Projeto

```
/workspace/
├── 📄 README.md                     # Documentação principal
├── 📄 requirements.txt              # Dependências Python
├── 🐍 run_complete_analysis.py      # Script principal de execução
├── 📓 egg_cooking_analysis.ipynb    # Notebook Jupyter interativo
│
├── 📂 src/                          # Código fonte
│   ├── 🐍 heat_transfer_model.py    # Modelo matemático base
│   ├── 🐍 egg_simulation.py         # Simulação completa
│   ├── 🐍 convection_analysis.py    # Análise de convecção
│   ├── 🐍 visualization.py          # Visualizações avançadas
│   └── 🐍 parametric_analysis.py    # Análise paramétrica
│
├── 📂 data/                         # Dados de entrada
│   └── 📄 egg_properties.json       # Propriedades físicas
│
├── 📂 docs/                         # Documentação técnica
│   └── 📄 teoria.md                 # Fundamentação teórica
│
└── 📂 results/                      # Resultados gerados
    └── 🖼️ test_simulation.png        # Exemplo de resultado
```

## 🔬 Modelos Implementados

### 1. Modelo de Capacidade Concentrada
- **Aplicação**: Bi < 0.1 (gradientes internos desprezíveis)
- **Equação**: T(t) = T∞ + (T₀ - T∞)exp(-t/τ)
- **Uso**: Estimativas rápidas e validação

### 2. Modelo de Diferenças Finitas
- **Aplicação**: Qualquer valor de Bi
- **Método**: Discretização da equação de difusão esférica
- **Uso**: Simulação detalhada da distribuição de temperatura

### 3. Solução Analítica por Séries
- **Aplicação**: Esfera com convecção uniforme
- **Método**: Séries de Fourier-Bessel
- **Uso**: Validação dos métodos numéricos

### 4. Análise de Convecção
- **Natural**: Ra = GrPr, Nu = f(Ra, Pr)
- **Forçada**: Re = VL/ν, Nu = f(Re, Pr)
- **Mista**: Combinação de ambos os regimes

## 📊 Principais Resultados

### Parâmetros Físicos Típicos
- **Raio do ovo**: 27.5 mm
- **Número de Biot**: ~4.9 (gradientes significativos)
- **Constante de tempo**: ~2.2 min
- **Coeficiente de convecção**: 250-2000 W/m²K

### Tempos de Cozimento
- **Clara coagulada**: ~3-5 min (T ≥ 62°C)
- **Gema coagulada**: ~5-8 min (T ≥ 65°C)
- **Ovo duro**: ~8-12 min (T ≥ 70°C)

### Fatores Mais Influentes
1. **Tamanho do ovo** (R²): Impacto quadrático no tempo
2. **Temperatura da água**: Efeito exponencial
3. **Coeficiente de convecção**: Logarítmico

## 🚀 Como Executar

### Execução Rápida
```bash
# Instalar dependências
pip install --break-system-packages numpy scipy matplotlib pandas seaborn

# Executar análise completa
python3 run_complete_analysis.py
```

### Teste Básico
```bash
python3 -c "
import sys; sys.path.append('./src')
from heat_transfer_model import EggHeatTransferModel
model = EggHeatTransferModel('./data/egg_properties.json')
print(f'Número de Biot: {model.calculate_biot_number():.3f}')
print('✅ Projeto funcionando!')
"
```

## 🎓 Aplicações Educativas

### Conceitos de Engenharia Abordados
- **Transferência de Calor**: Condução, convecção
- **Análise Adimensional**: Números de Biot, Fourier, Nusselt
- **Métodos Numéricos**: Diferenças finitas, integração de EDOs
- **Otimização**: Minimização não-linear
- **Validação**: Comparação entre modelos

### Competências Desenvolvidas
- Modelagem matemática de fenômenos físicos
- Implementação de algoritmos numéricos
- Análise paramétrica e otimização
- Visualização científica de dados
- Documentação técnica

## 💡 Inovações do Projeto

1. **Abordagem Multi-Modelo**: Três métodos diferentes para validação cruzada
2. **Análise Completa**: Da teoria à implementação prática
3. **Visualizações Avançadas**: 3D, animações, interatividade
4. **Otimização Automática**: Para diferentes tempos de cozimento
5. **Código Modular**: Fácil extensão e modificação

## ⚠️ Limitações Conhecidas

- **Geometria**: Esfera vs forma real do ovo
- **Propriedades**: Constantes vs dependentes da temperatura
- **Coagulação**: Não modelada como mudança de fase
- **Estrutura**: Gema, clara e casca homogêneas

## 🔮 Desenvolvimentos Futuros

- [ ] Geometria 3D realística
- [ ] Propriedades termo-dependentes
- [ ] Modelagem da coagulação
- [ ] Validação experimental
- [ ] Interface gráfica (GUI)
- [ ] Aplicativo web interativo

## 📚 Base Teórica

O projeto fundamenta-se em:
- **Incropera & DeWitt**: "Fundamentals of Heat and Mass Transfer"
- **Holman**: "Heat Transfer" 
- **Özilgen**: "Food Process Modeling and Control"
- **Singh & Heldman**: "Introduction to Food Engineering"

## 🏆 Conclusão

Este projeto demonstra com sucesso a aplicação de conceitos fundamentais de transferência de calor em um problema prático e cotidiano. A implementação combina rigor científico com usabilidade prática, resultando em uma ferramenta educativa valiosa para estudantes de engenharia mecânica.

O código é modular, bem documentado e facilmente extensível, servindo como base para projetos mais avançados ou como material didático para disciplinas de transferência de calor.

---

**Desenvolvido para**: Engenharia Mecânica - Transferência de Calor  
**Linguagem**: Python 3.13  
**Dependências**: NumPy, SciPy, Matplotlib, Pandas, Seaborn  
**Status**: ✅ Completo e Funcional