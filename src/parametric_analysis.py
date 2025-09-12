"""
Análise Paramétrica Completa do Cozimento de Ovo
Estudo da influência de diferentes parâmetros no processo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
import json
import itertools
from heat_transfer_model import EggHeatTransferModel
from egg_simulation import EggCookingSimulation
from convection_analysis import ConvectionAnalysis
import warnings
warnings.filterwarnings('ignore')

class ParametricAnalysis:
    """
    Análise paramétrica completa do processo de cozimento
    """
    
    def __init__(self, base_properties_file='../data/egg_properties.json'):
        """
        Inicializa análise paramétrica
        """
        with open(base_properties_file, 'r') as f:
            self.base_props = json.load(f)
        
        self.results_database = []
        self.optimization_results = {}
    
    def define_parameter_ranges(self):
        """
        Define os ranges dos parâmetros para análise
        """
        parameters = {
            # Parâmetros geométricos
            'egg_diameter': {
                'range': np.linspace(0.045, 0.065, 5),  # 45-65 mm
                'unit': 'm',
                'description': 'Diâmetro do ovo'
            },
            'shell_thickness': {
                'range': np.linspace(0.0002, 0.0005, 4),  # 0.2-0.5 mm
                'unit': 'm',
                'description': 'Espessura da casca'
            },
            'gema_fraction': {
                'range': np.linspace(0.25, 0.45, 5),  # 25-45% volume
                'unit': 'adimensional',
                'description': 'Fração volumétrica da gema'
            },
            
            # Parâmetros térmicos
            'water_temperature': {
                'range': np.linspace(80, 120, 9),  # 80-120°C
                'unit': '°C',
                'description': 'Temperatura da água'
            },
            'initial_temperature': {
                'range': np.linspace(5, 25, 5),  # 5-25°C
                'unit': '°C',
                'description': 'Temperatura inicial do ovo'
            },
            'convection_coefficient': {
                'range': np.logspace(2, 3.5, 8),  # 100-3000 W/m²K
                'unit': 'W/m²K',
                'description': 'Coeficiente de convecção'
            },
            
            # Propriedades dos materiais
            'clara_thermal_conductivity': {
                'range': np.linspace(0.4, 0.7, 4),  # Variação ±30%
                'unit': 'W/mK',
                'description': 'Condutividade térmica da clara'
            },
            'clara_specific_heat': {
                'range': np.linspace(3200, 4400, 4),  # Variação ±15%
                'unit': 'J/kgK',
                'description': 'Calor específico da clara'
            },
            'clara_density': {
                'range': np.linspace(950, 1100, 4),  # Variação ±7%
                'unit': 'kg/m³',
                'description': 'Densidade da clara'
            }
        }
        
        return parameters
    
    def run_single_parameter_study(self, parameter_name, parameter_values, max_time=900):
        """
        Executa estudo variando um único parâmetro
        """
        print(f"Analisando parâmetro: {parameter_name}")
        
        results = []
        
        for i, value in enumerate(parameter_values):
            print(f"  Caso {i+1}/{len(parameter_values)}: {parameter_name} = {value:.4f}")
            
            # Modificar propriedades
            temp_props = self.base_props.copy()
            
            # Aplicar modificação baseada no parâmetro
            if parameter_name == 'egg_diameter':
                temp_props['physical_properties']['egg_diameter'] = value
            elif parameter_name == 'shell_thickness':
                temp_props['physical_properties']['shell_thickness'] = value
            elif parameter_name == 'gema_fraction':
                temp_props['physical_properties']['gema_fraction'] = value
            elif parameter_name == 'water_temperature':
                temp_props['physical_properties']['water_temperature'] = value
            elif parameter_name == 'initial_temperature':
                temp_props['physical_properties']['initial_temperature'] = value
            elif parameter_name == 'convection_coefficient':
                temp_props['convection_parameters']['natural_convection_h'] = value
            elif parameter_name == 'clara_thermal_conductivity':
                temp_props['thermal_properties']['clara']['thermal_conductivity'] = value
            elif parameter_name == 'clara_specific_heat':
                temp_props['thermal_properties']['clara']['specific_heat'] = value
            elif parameter_name == 'clara_density':
                temp_props['thermal_properties']['clara']['density'] = value
            
            # Salvar propriedades temporárias
            temp_file = f'../data/temp_props_{parameter_name}_{i}.json'
            with open(temp_file, 'w') as f:
                json.dump(temp_props, f)
            
            try:
                # Executar simulação
                sim = EggCookingSimulation(temp_file)
                sim_results = sim.run_complete_simulation(max_time=max_time, n_time_points=100)
                cooking_stages = sim.analyze_cooking_stages()
                
                # Extrair métricas
                metrics = {
                    'parameter_value': value,
                    'biot_number': sim.model.calculate_biot_number(),
                    'time_constant': sim_results['tau'],
                    'final_center_temp': sim_results['T_center_fd'][-1],
                    'final_surface_temp': sim_results['T_surface_fd'][-1],
                    'clara_coagulation_time': cooking_stages.get('clara_coagulation_start', None),
                    'gema_coagulation_time': cooking_stages.get('gema_coagulation_start', None),
                    'soft_boiled_time': cooking_stages.get('soft_boiled_optimal', None),
                    'medium_boiled_time': cooking_stages.get('medium_boiled_optimal', None),
                    'hard_boiled_time': cooking_stages.get('hard_boiled_optimal', None)
                }
                
                results.append(metrics)
                
            except Exception as e:
                print(f"    Erro na simulação: {e}")
                results.append({
                    'parameter_value': value,
                    'error': str(e)
                })
            
            # Limpar arquivo temporário
            import os
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return pd.DataFrame(results)
    
    def run_multi_parameter_study(self, selected_parameters, n_samples=100):
        """
        Executa estudo com múltiplos parâmetros usando amostragem
        """
        print(f"Executando análise multi-paramétrica com {n_samples} amostras...")
        
        param_ranges = self.define_parameter_ranges()
        
        # Gerar amostras usando Latin Hypercube Sampling (simplificado)
        np.random.seed(42)  # Para reprodutibilidade
        
        samples = {}
        for param in selected_parameters:
            if param in param_ranges:
                param_range = param_ranges[param]['range']
                samples[param] = np.random.choice(param_range, n_samples)
        
        results = []
        
        for i in range(n_samples):
            print(f"  Amostra {i+1}/{n_samples}")
            
            # Criar propriedades para esta amostra
            temp_props = self.base_props.copy()
            sample_values = {}
            
            for param in selected_parameters:
                value = samples[param][i]
                sample_values[param] = value
                
                # Aplicar modificações
                if param == 'egg_diameter':
                    temp_props['physical_properties']['egg_diameter'] = value
                elif param == 'water_temperature':
                    temp_props['physical_properties']['water_temperature'] = value
                elif param == 'convection_coefficient':
                    temp_props['convection_parameters']['natural_convection_h'] = value
                # ... (adicionar outros parâmetros conforme necessário)
            
            # Salvar e executar
            temp_file = f'../data/temp_multi_{i}.json'
            with open(temp_file, 'w') as f:
                json.dump(temp_props, f)
            
            try:
                sim = EggCookingSimulation(temp_file)
                sim_results = sim.run_complete_simulation(max_time=600, n_time_points=50)
                cooking_stages = sim.analyze_cooking_stages()
                
                # Compilar resultados
                result = sample_values.copy()
                result.update({
                    'clara_coagulation_time': cooking_stages.get('clara_coagulation_start', None),
                    'biot_number': sim.model.calculate_biot_number(),
                    'time_constant': sim_results['tau']
                })
                
                results.append(result)
                
            except Exception as e:
                print(f"    Erro na amostra {i+1}: {e}")
            
            # Limpar
            import os
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return pd.DataFrame(results)
    
    def sensitivity_analysis(self, parameter_name, base_value, variation_percent=20):
        """
        Análise de sensibilidade usando derivadas numéricas
        """
        variation = base_value * variation_percent / 100
        values = [base_value - variation, base_value, base_value + variation]
        
        df = self.run_single_parameter_study(parameter_name, values)
        
        if len(df) >= 3 and 'clara_coagulation_time' in df.columns:
            # Calcular sensibilidade
            times = df['clara_coagulation_time'].dropna()
            if len(times) >= 3:
                # Derivada numérica central
                dt_dp = (times.iloc[2] - times.iloc[0]) / (2 * variation)
                sensitivity = (dt_dp * base_value) / times.iloc[1]  # Sensibilidade relativa
                
                return {
                    'parameter': parameter_name,
                    'base_value': base_value,
                    'sensitivity': sensitivity,
                    'derivative': dt_dp
                }
        
        return None
    
    def optimization_study(self, target_cooking_time=300):
        """
        Otimização para atingir tempo de cozimento específico
        """
        print(f"Otimizando para tempo de cozimento: {target_cooking_time}s")
        
        def objective_function(params):
            """
            Função objetivo: minimizar diferença do tempo alvo
            """
            diameter, h_conv, water_temp = params
            
            # Criar propriedades
            temp_props = self.base_props.copy()
            temp_props['physical_properties']['egg_diameter'] = diameter
            temp_props['convection_parameters']['natural_convection_h'] = h_conv
            temp_props['physical_properties']['water_temperature'] = water_temp
            
            # Salvar temporariamente
            temp_file = '../data/temp_opt.json'
            with open(temp_file, 'w') as f:
                json.dump(temp_props, f)
            
            try:
                sim = EggCookingSimulation(temp_file)
                sim_results = sim.run_complete_simulation(max_time=900, n_time_points=50)
                cooking_stages = sim.analyze_cooking_stages()
                
                clara_time = cooking_stages.get('clara_coagulation_start', 900)
                error = abs(clara_time - target_cooking_time)
                
                # Limpar
                import os
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                return error
                
            except:
                import os
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return 1000  # Penalidade alta para falhas
        
        # Definir bounds
        bounds = [
            (0.045, 0.065),  # diâmetro
            (100, 2000),     # h_conv
            (80, 120)        # temperatura água
        ]
        
        # Valor inicial
        x0 = [0.055, 500, 100]
        
        # Otimizar
        result = minimize(objective_function, x0, bounds=bounds, method='L-BFGS-B')
        
        if result.success:
            optimal_params = {
                'egg_diameter': result.x[0],
                'convection_coefficient': result.x[1],
                'water_temperature': result.x[2],
                'final_error': result.fun,
                'target_time': target_cooking_time
            }
            
            self.optimization_results[target_cooking_time] = optimal_params
            return optimal_params
        
        return None
    
    def plot_single_parameter_results(self, df, parameter_name, parameter_info):
        """
        Plota resultados de análise de parâmetro único
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Tempo de coagulação vs parâmetro
        if 'clara_coagulation_time' in df.columns:
            valid_data = df.dropna(subset=['clara_coagulation_time'])
            if len(valid_data) > 0:
                axes[0,0].plot(valid_data['parameter_value'], 
                              valid_data['clara_coagulation_time']/60, 
                              'bo-', linewidth=2, markersize=8)
                axes[0,0].set_xlabel(f"{parameter_info['description']} ({parameter_info['unit']})")
                axes[0,0].set_ylabel('Tempo coagulação clara (min)')
                axes[0,0].set_title('Tempo de Cozimento vs Parâmetro')
                axes[0,0].grid(True, alpha=0.3)
        
        # Gráfico 2: Número de Biot vs parâmetro
        if 'biot_number' in df.columns:
            valid_data = df.dropna(subset=['biot_number'])
            if len(valid_data) > 0:
                axes[0,1].plot(valid_data['parameter_value'], 
                              valid_data['biot_number'], 
                              'ro-', linewidth=2, markersize=8)
                axes[0,1].axhline(y=0.1, color='gray', linestyle='--', alpha=0.7,
                                 label='Bi = 0.1 (limite capacidade concentrada)')
                axes[0,1].set_xlabel(f"{parameter_info['description']} ({parameter_info['unit']})")
                axes[0,1].set_ylabel('Número de Biot')
                axes[0,1].set_title('Número de Biot vs Parâmetro')
                axes[0,1].legend()
                axes[0,1].grid(True, alpha=0.3)
        
        # Gráfico 3: Constante de tempo vs parâmetro
        if 'time_constant' in df.columns:
            valid_data = df.dropna(subset=['time_constant'])
            if len(valid_data) > 0:
                axes[1,0].plot(valid_data['parameter_value'], 
                              valid_data['time_constant']/60, 
                              'go-', linewidth=2, markersize=8)
                axes[1,0].set_xlabel(f"{parameter_info['description']} ({parameter_info['unit']})")
                axes[1,0].set_ylabel('Constante de tempo (min)')
                axes[1,0].set_title('Constante de Tempo vs Parâmetro')
                axes[1,0].grid(True, alpha=0.3)
        
        # Gráfico 4: Temperaturas finais
        if 'final_center_temp' in df.columns and 'final_surface_temp' in df.columns:
            valid_data = df.dropna(subset=['final_center_temp', 'final_surface_temp'])
            if len(valid_data) > 0:
                axes[1,1].plot(valid_data['parameter_value'], 
                              valid_data['final_center_temp'], 
                              'mo-', linewidth=2, markersize=8, label='Centro')
                axes[1,1].plot(valid_data['parameter_value'], 
                              valid_data['final_surface_temp'], 
                              'co-', linewidth=2, markersize=8, label='Superfície')
                axes[1,1].set_xlabel(f"{parameter_info['description']} ({parameter_info['unit']})")
                axes[1,1].set_ylabel('Temperatura final (°C)')
                axes[1,1].set_title('Temperaturas Finais vs Parâmetro')
                axes[1,1].legend()
                axes[1,1].grid(True, alpha=0.3)
        
        plt.suptitle(f'Análise Paramétrica: {parameter_info["description"]}', fontsize=16)
        plt.tight_layout()
        
        return fig
    
    def plot_multi_parameter_results(self, df):
        """
        Plota resultados da análise multi-paramétrica
        """
        # Correlation matrix
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Selecionar colunas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        
        # Heatmap de correlação
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   ax=axes[0,0], square=True)
        axes[0,0].set_title('Matriz de Correlação')
        
        # Scatter plots para principais correlações
        if 'clara_coagulation_time' in df.columns:
            # vs diâmetro do ovo
            if 'egg_diameter' in df.columns:
                axes[0,1].scatter(df['egg_diameter'], df['clara_coagulation_time']/60, alpha=0.6)
                axes[0,1].set_xlabel('Diâmetro do ovo (m)')
                axes[0,1].set_ylabel('Tempo coagulação (min)')
                axes[0,1].set_title('Tempo vs Diâmetro')
                axes[0,1].grid(True, alpha=0.3)
            
            # vs temperatura da água
            if 'water_temperature' in df.columns:
                axes[1,0].scatter(df['water_temperature'], df['clara_coagulation_time']/60, alpha=0.6)
                axes[1,0].set_xlabel('Temperatura da água (°C)')
                axes[1,0].set_ylabel('Tempo coagulação (min)')
                axes[1,0].set_title('Tempo vs Temperatura Água')
                axes[1,0].grid(True, alpha=0.3)
            
            # vs coeficiente de convecção
            if 'convection_coefficient' in df.columns:
                axes[1,1].scatter(df['convection_coefficient'], df['clara_coagulation_time']/60, alpha=0.6)
                axes[1,1].set_xlabel('Coeficiente h (W/m²K)')
                axes[1,1].set_ylabel('Tempo coagulação (min)')
                axes[1,1].set_title('Tempo vs Coeficiente h')
                axes[1,1].set_xscale('log')
                axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def export_parametric_results(self, output_dir='../results'):
        """
        Exporta todos os resultados da análise paramétrica
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Executar análises principais
        param_ranges = self.define_parameter_ranges()
        
        # Análises de parâmetro único para parâmetros principais
        key_parameters = ['egg_diameter', 'water_temperature', 'convection_coefficient']
        
        for param in key_parameters:
            if param in param_ranges:
                print(f"Executando análise para {param}...")
                df = self.run_single_parameter_study(param, param_ranges[param]['range'])
                
                # Salvar dados
                df.to_csv(f'{output_dir}/parametric_{param}.csv', index=False)
                
                # Salvar gráfico
                fig = self.plot_single_parameter_results(df, param, param_ranges[param])
                fig.savefig(f'{output_dir}/parametric_{param}.png', dpi=300, bbox_inches='tight')
                plt.close(fig)
        
        # Análise multi-paramétrica
        print("Executando análise multi-paramétrica...")
        df_multi = self.run_multi_parameter_study(key_parameters, n_samples=50)
        df_multi.to_csv(f'{output_dir}/parametric_multi.csv', index=False)
        
        fig_multi = self.plot_multi_parameter_results(df_multi)
        fig_multi.savefig(f'{output_dir}/parametric_multi.png', dpi=300, bbox_inches='tight')
        plt.close(fig_multi)
        
        # Otimização para diferentes tempos alvo
        target_times = [180, 300, 420]  # 3, 5, 7 minutos
        optimization_results = {}
        
        for target in target_times:
            print(f"Otimizando para {target}s...")
            opt_result = self.optimization_study(target)
            if opt_result:
                optimization_results[f'target_{target}s'] = opt_result
        
        # Salvar resultados de otimização
        with open(f'{output_dir}/optimization_results.json', 'w') as f:
            json.dump(optimization_results, f, indent=2)
        
        print(f"✅ Resultados da análise paramétrica salvos em: {output_dir}")
        return optimization_results

def main():
    """
    Executa análise paramétrica completa
    """
    print("=== ANÁLISE PARAMÉTRICA COMPLETA ===")
    
    # Criar análise
    analysis = ParametricAnalysis()
    
    # Executar e exportar resultados
    optimization_results = analysis.export_parametric_results()
    
    # Mostrar resultados de otimização
    print("\n📊 RESULTADOS DE OTIMIZAÇÃO:")
    for target, result in optimization_results.items():
        print(f"\n{target}:")
        print(f"  • Diâmetro ótimo: {result['egg_diameter']*1000:.1f} mm")
        print(f"  • Coeficiente h ótimo: {result['convection_coefficient']:.0f} W/m²K")
        print(f"  • Temperatura ótima: {result['water_temperature']:.1f} °C")
        print(f"  • Erro final: {result['final_error']:.1f} s")
    
    print("\n✅ Análise paramétrica concluída!")
    return analysis

if __name__ == "__main__":
    analysis = main()