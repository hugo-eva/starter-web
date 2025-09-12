# Fundamentação Teórica - Transferência de Calor no Cozimento de Ovo

## 1. Introdução

O cozimento de um ovo é um excelente exemplo prático de transferência de calor que envolve os três mecanismos fundamentais:

- **Condução**: Transferência de calor através da casca e interior do ovo
- **Convecção**: Transferência entre a água quente e a superfície do ovo
- **Radiação**: Desprezível neste caso devido às temperaturas relativamente baixas

## 2. Modelo Físico

### 2.1 Geometria Simplificada

O ovo é modelado como uma esfera composta por três regiões concêntricas:

1. **Gema** (centro): Raio 0 ≤ r ≤ R_gema
2. **Clara**: Raio R_gema < r ≤ R_shell  
3. **Casca**: Raio R_shell < r ≤ R_total

### 2.2 Propriedades Físicas

#### Gema
- Condutividade térmica: k_gema = 0.35 W/mK
- Densidade: ρ_gema = 1025 kg/m³
- Calor específico: c_p,gema = 2850 J/kgK
- Difusividade térmica: α_gema = k/(ρc_p) = 1.2×10⁻⁷ m²/s

#### Clara
- Condutividade térmica: k_clara = 0.54 W/mK
- Densidade: ρ_clara = 1030 kg/m³
- Calor específico: c_p,clara = 3800 J/kgK
- Difusividade térmica: α_clara = 1.38×10⁻⁷ m²/s

#### Casca
- Condutividade térmica: k_casca = 1.4 W/mK
- Densidade: ρ_casca = 2300 kg/m³
- Calor específico: c_p,casca = 800 J/kgK
- Difusividade térmica: α_casca = 7.6×10⁻⁷ m²/s

## 3. Equações Governantes

### 3.1 Equação de Condução de Calor

Para coordenadas esféricas com simetria radial:

```
∂T/∂t = α(1/r²)(∂/∂r)(r² ∂T/∂r)
```

Onde:
- T(r,t) = temperatura em função do raio e tempo
- α = difusividade térmica
- r = coordenada radial

### 3.2 Condições Iniciais

```
T(r,0) = T_inicial = 20°C  (para todo r)
```

### 3.3 Condições de Contorno

#### Centro (r = 0):
Simetria esférica:
```
∂T/∂r|_{r=0} = 0
```

#### Superfície (r = R_total):
Convecção com a água:
```
-k ∂T/∂r|_{r=R} = h(T_superfície - T_água)
```

#### Interfaces internas:
Continuidade de temperatura e fluxo de calor:
```
T₁|_interface = T₂|_interface
k₁ ∂T₁/∂r|_interface = k₂ ∂T₂/∂r|_interface
```

## 4. Números Adimensionais

### 4.1 Número de Biot (Bi)

```
Bi = hL_c/k
```

Onde L_c = R_total (comprimento característico)

- **Bi < 0.1**: Modelo de capacidade concentrada válido
- **Bi > 0.1**: Gradientes internos significativos

### 4.2 Número de Fourier (Fo)

```
Fo = αt/L_c²
```

Representa o tempo adimensional.

### 4.3 Número de Nusselt (Nu)

Para convecção em esfera:

**Convecção Natural:**
```
Nu = 2 + 0.589Ra^(1/4) / [1 + (0.469/Pr)^(9/16)]^(4/9)
```

**Convecção Forçada:**
```
Nu = 2 + 0.4Re^(1/2)Pr^(1/3) + 0.06Re^(2/3)Pr^0.4
```

### 4.4 Número de Rayleigh (Ra)

```
Ra = GrPr = (gβΔTL³)/(να)
```

### 4.5 Número de Reynolds (Re)

```
Re = VL/ν
```

## 5. Métodos de Solução

### 5.1 Modelo de Capacidade Concentrada

Para Bi < 0.1, a temperatura é uniforme:

```
T(t) = T_∞ + (T_0 - T_∞)exp(-t/τ)
```

Onde τ = (ρVc_p)/(hA) é a constante de tempo.

### 5.2 Solução Analítica por Séries

Para esfera com convecção:

```
T(r,t) = T_∞ + (T_0 - T_∞) Σ A_n exp(-λ_n² Fo) sin(λ_n r/R)/(λ_n r/R)
```

Onde λ_n são raízes de: tan(λ_n) = λ_n/(1 - Bi)

### 5.3 Método de Diferenças Finitas

Discretização da equação de difusão:

```
T_i^(n+1) = T_i^n + (αΔt/Δr²)[T_(i+1)^n - 2T_i^n + T_(i-1)^n] + (2αΔt)/(iΔr²)[T_(i+1)^n - T_(i-1)^n]
```

## 6. Critérios de Cozimento

### 6.1 Temperaturas de Coagulação

- **Clara**: Inicia coagulação a 62°C, completa a 65°C
- **Gema**: Inicia coagulação a 65°C, completa a 70°C

### 6.2 Classificação do Cozimento

1. **Ovo mole**: Clara coagulada (T_centro ≥ 62°C), gema líquida (T_gema < 65°C)
2. **Ovo médio**: Gema parcialmente coagulada (65°C ≤ T_gema < 70°C)
3. **Ovo duro**: Totalmente coagulado (T_gema ≥ 70°C)

## 7. Correlações para Convecção

### 7.1 Água em Ebulição (Convecção Natural)

```
h ≈ 250-500 W/m²K  (água parada)
```

### 7.2 Água Agitada (Convecção Forçada)

```
h ≈ 500-2000 W/m²K  (dependendo da agitação)
```

### 7.3 Correlação de Churchill-Chu (Convecção Natural)

```
Nu_D = 2 + [0.589Ra_D^(1/4)] / [1 + (0.469/Pr)^(9/16)]^(4/9)
```

Válida para: 10⁻¹ < Ra_D < 10¹²

## 8. Validação do Modelo

### 8.1 Verificação Dimensional

Todas as equações devem ser dimensionalmente consistentes.

### 8.2 Casos Limite

- **t → 0**: T = T_inicial
- **t → ∞**: T = T_água (equilíbrio térmico)
- **Bi → 0**: Reduz ao modelo de capacidade concentrada
- **h → ∞**: Temperatura superficial = T_água

### 8.3 Conservação de Energia

O calor transferido para o ovo deve ser igual ao aumento de energia interna.

## 9. Limitações do Modelo

1. **Geometria**: Ovo não é perfeitamente esférico
2. **Propriedades**: Variam com temperatura (modelo assume constantes)
3. **Mudança de fase**: Coagulação não é modelada como transição de fase
4. **Estrutura interna**: Membranas e câmara de ar são desprezadas
5. **Convecção interna**: Movimentação da clara líquida não é considerada

## 10. Aplicações Práticas

### 10.1 Controle de Cozimento

- Determinar tempo ótimo para diferentes níveis de cozimento
- Otimizar temperatura da água
- Efeito do tamanho do ovo

### 10.2 Análise de Sensibilidade

- Identificar parâmetros mais influentes
- Tolerâncias no processo
- Robustez do método

### 10.3 Escalamento

- Aplicação para diferentes tamanhos de ovos
- Cozimento em lote
- Processos industriais

## Referências

1. Incropera, F.P., DeWitt, D.P. "Fundamentals of Heat and Mass Transfer"
2. Holman, J.P. "Heat Transfer"
3. Özilgen, M. "Food Process Modeling and Control"
4. Singh, R.P., Heldman, D.R. "Introduction to Food Engineering"