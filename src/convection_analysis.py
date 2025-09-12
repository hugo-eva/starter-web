"""
Análise de Convecção na Água para Cozimento de Ovo
Correlações para transferência de calor convectiva
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from heat_transfer_model import EggHeatTransferModel
import json

class ConvectionAnalysis:
    """
    Análise detalhada da transferência de calor por convecção
    """
    
    def __init__(self, properties_file='../data/egg_properties.json'):
        """
        Inicializa análise de convecção
        """
        with open(properties_file, 'r') as f:
            self.props = json.load(f)
        
        # Propriedades da água a 100°C
        self.water_props = self.props['thermal_properties']['water']
        self.T_water = self.props['physical_properties']['water_temperature']
        self.T_initial = self.props['physical_properties']['initial_temperature']
        self.D_egg = self.props['physical_properties']['egg_diameter']
        
        # Propriedades físicas da água
        self.rho_water = self.water_props['density']  # kg/m³
        self.k_water = self.water_props['thermal_conductivity']  # W/mK
        self.nu_water = self.water_props['kinematic_viscosity']  # m²/s
        self.Pr_water = self.water_props['prandtl_number']  # adimensional
        self.beta_water = self.water_props['thermal_expansion']  # 1/K
        
        # Aceleração gravitacional
        self.g = 9.81  # m/s²
    
    def calculate_grashof_number(self, T_surface):
        """
        Calcula número de Grashof para convecção natural
        """
        delta_T = abs(self.T_water - T_surface)
        Gr = (self.g * self.beta_water * delta_T * self.D_egg**3) / self.nu_water**2
        return Gr
    
    def calculate_rayleigh_number(self, T_surface):
        """
        Calcula número de Rayleigh (Ra = Gr * Pr)
        """
        Gr = self.calculate_grashof_number(T_surface)
        Ra = Gr * self.Pr_water
        return Ra
    
    def calculate_reynolds_number(self, velocity):
        """
        Calcula número de Reynolds para convecção forçada
        """
        Re = velocity * self.D_egg / self.nu_water
        return Re
    
    def natural_convection_nusselt(self, T_surface):
        """
        Correlação de Nusselt para convecção natural em esfera
        Correlação de Churchill e Chu
        """
        Ra = self.calculate_rayleigh_number(T_surface)
        
        if Ra < 1e4:
            # Regime laminar
            Nu = 2 + 0.589 * Ra**(1/4) / (1 + (0.469/self.Pr_water)**(9/16))**(4/9)
        else:
            # Regime turbulento
            Nu = 2 + 0.589 * Ra**(1/4) / (1 + (0.469/self.Pr_water)**(9/16))**(4/9)
        
        return Nu
    
    def forced_convection_nusselt(self, velocity):
        """
        Correlação de Nusselt para convecção forçada em esfera
        Correlação de Whitaker
        """
        Re = self.calculate_reynolds_number(velocity)
        
        if Re < 1:
            # Regime de Stokes
            Nu = 2 + 0.6 * Re**(1/2) * self.Pr_water**(1/3)
        elif Re < 1000:
            # Regime intermediário
            Nu = 2 + 0.6 * Re**(1/2) * self.Pr_water**(1/3)
        else:
            # Regime turbulento
            Nu = 2 + 0.4 * Re**(1/2) * self.Pr_water**(1/3) + 0.06 * Re**(2/3) * self.Pr_water**(0.4)
        
        return Nu
    
    def calculate_heat_transfer_coefficient(self, T_surface, velocity=0):
        """
        Calcula coeficiente de transferência de calor
        """
        if velocity == 0:
            # Convecção natural
            Nu = self.natural_convection_nusselt(T_surface)
        else:
            # Convecção forçada
            Nu_natural = self.natural_convection_nusselt(T_surface)
            Nu_forced = self.forced_convection_nusselt(velocity)
            # Convecção mista (combinação)
            Nu = (Nu_natural**3 + Nu_forced**3)**(1/3)
        
        h = Nu * self.k_water / self.D_egg
        return h, Nu
    
    def analyze_convection_regimes(self):
        """
        Analisa diferentes regimes de convecção
        """
        T_range = np.linspace(20, 95, 50)  # Temperatura da superfície do ovo
        velocities = [0, 0.01, 0.05, 0.1, 0.2, 0.5]  # m/s
        
        results = {}
        
        for v in velocities:
            h_values = []
            Nu_values = []
            Ra_values = []
            Re_values = []
            
            for T in T_range:
                h, Nu = self.calculate_heat_transfer_coefficient(T, v)
                Ra = self.calculate_rayleigh_number(T)
                Re = self.calculate_reynolds_number(v) if v > 0 else 0
                
                h_values.append(h)
                Nu_values.append(Nu)
                Ra_values.append(Ra)
                Re_values.append(Re)
            
            results[f'v_{v:.2f}'] = {
                'velocity': v,
                'temperature': T_range,
                'h_coefficient': np.array(h_values),
                'nusselt': np.array(Nu_values),
                'rayleigh': np.array(Ra_values),
                'reynolds': np.array(Re_values)
            }
        
        return results
    
    def plot_convection_analysis(self):
        """
        Plota análise dos regimes de convecção
        """
        results = self.analyze_convection_regimes()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Coeficiente de transferência de calor vs temperatura
        for key, data in results.items():
            v = data['velocity']
            label = f'v = {v:.2f} m/s' if v > 0 else 'Convecção natural'
            axes[0,0].plot(data['temperature'], data['h_coefficient'], 
                          label=label, linewidth=2)
        
        axes[0,0].set_xlabel('Temperatura da superfície (°C)')
        axes[0,0].set_ylabel('Coeficiente h (W/m²K)')
        axes[0,0].set_title('Coeficiente de Transferência de Calor')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # Gráfico 2: Número de Nusselt vs temperatura
        for key, data in results.items():
            v = data['velocity']
            label = f'v = {v:.2f} m/s' if v > 0 else 'Convecção natural'
            axes[0,1].plot(data['temperature'], data['nusselt'], 
                          label=label, linewidth=2)
        
        axes[0,1].set_xlabel('Temperatura da superfície (°C)')
        axes[0,1].set_ylabel('Número de Nusselt')
        axes[0,1].set_title('Número de Nusselt vs Temperatura')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # Gráfico 3: Número de Rayleigh vs temperatura (convecção natural)
        nat_conv_data = results['v_0.00']
        axes[1,0].semilogy(nat_conv_data['temperature'], nat_conv_data['rayleigh'])
        axes[1,0].set_xlabel('Temperatura da superfície (°C)')
        axes[1,0].set_ylabel('Número de Rayleigh')
        axes[1,0].set_title('Número de Rayleigh - Convecção Natural')
        axes[1,0].grid(True, alpha=0.3)
        
        # Gráfico 4: Comparação h vs velocidade para diferentes temperaturas
        velocities = [0, 0.01, 0.05, 0.1, 0.2, 0.5]
        temperatures_plot = [30, 50, 70, 90]
        
        for T in temperatures_plot:
            h_vs_v = []
            for v in velocities:
                h, _ = self.calculate_heat_transfer_coefficient(T, v)
                h_vs_v.append(h)
            
            axes[1,1].plot(velocities, h_vs_v, 'o-', label=f'T = {T}°C', linewidth=2)
        
        axes[1,1].set_xlabel('Velocidade da água (m/s)')
        axes[1,1].set_ylabel('Coeficiente h (W/m²K)')
        axes[1,1].set_title('Efeito da Velocidade no Coeficiente h')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def simulate_different_conditions(self):
        """
        Simula cozimento sob diferentes condições de convecção
        """
        from egg_simulation import EggCookingSimulation
        
        # Condições a testar
        conditions = [
            {'name': 'Água parada', 'h': 250},
            {'name': 'Água com bolhas', 'h': 500},
            {'name': 'Água agitada', 'h': 1000},
            {'name': 'Água vigorosamente agitada', 'h': 2000}
        ]
        
        results = {}
        
        for condition in conditions:
            # Modificar propriedades temporariamente
            temp_props = self.props.copy()
            temp_props['convection_parameters']['natural_convection_h'] = condition['h']
            
            # Salvar propriedades temporárias
            with open('../data/temp_properties.json', 'w') as f:
                json.dump(temp_props, f)
            
            # Executar simulação
            sim = EggCookingSimulation('../data/temp_properties.json')
            sim_results = sim.run_complete_simulation(max_time=900, n_time_points=100)
            
            results[condition['name']] = {
                'h_coefficient': condition['h'],
                'time': sim_results['time'],
                'temperature_center': sim_results['T_center_fd'],
                'cooking_stages': sim.analyze_cooking_stages()
            }
        
        # Remover arquivo temporário
        import os
        if os.path.exists('../data/temp_properties.json'):
            os.remove('../data/temp_properties.json')
        
        return results
    
    def plot_conditions_comparison(self):
        """
        Compara diferentes condições de cozimento
        """
        results = self.simulate_different_conditions()
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico 1: Evolução da temperatura
        for condition, data in results.items():
            time_min = data['time'] / 60
            axes[0].plot(time_min, data['temperature_center'], 
                        label=f"{condition} (h={data['h_coefficient']} W/m²K)", 
                        linewidth=2)
        
        axes[0].axhline(y=62, color='orange', linestyle='--', alpha=0.7, 
                       label='Coagulação clara')
        axes[0].axhline(y=65, color='red', linestyle='--', alpha=0.7, 
                       label='Coagulação gema')
        
        axes[0].set_xlabel('Tempo (min)')
        axes[0].set_ylabel('Temperatura no centro (°C)')
        axes[0].set_title('Efeito das Condições de Convecção')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Gráfico 2: Tempos de cozimento
        h_values = []
        cooking_times = []
        
        for condition, data in results.items():
            h_values.append(data['h_coefficient'])
            stages = data['cooking_stages']
            if 'clara_coagulation_start' in stages:
                cooking_times.append(stages['clara_coagulation_start'] / 60)
            else:
                cooking_times.append(None)
        
        # Remover valores None
        valid_data = [(h, t) for h, t in zip(h_values, cooking_times) if t is not None]
        if valid_data:
            h_valid, t_valid = zip(*valid_data)
            axes[1].plot(h_valid, t_valid, 'o-', linewidth=2, markersize=8)
            
            for h, t, condition in zip(h_values, cooking_times, results.keys()):
                if t is not None:
                    axes[1].annotate(condition.split()[0], (h, t), 
                                   xytext=(5, 5), textcoords='offset points')
        
        axes[1].set_xlabel('Coeficiente de convecção h (W/m²K)')
        axes[1].set_ylabel('Tempo para coagulação da clara (min)')
        axes[1].set_title('Tempo de Cozimento vs Coeficiente h')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig, results
    
    def export_convection_data(self, output_dir='../results'):
        """
        Exporta dados da análise de convecção
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Análise de regimes
        regime_results = self.analyze_convection_regimes()
        
        # Criar DataFrame para exportação
        data_rows = []
        for key, data in regime_results.items():
            v = data['velocity']
            for i, T in enumerate(data['temperature']):
                data_rows.append({
                    'velocity_m_s': v,
                    'surface_temperature_C': T,
                    'heat_transfer_coefficient_W_m2K': data['h_coefficient'][i],
                    'nusselt_number': data['nusselt'][i],
                    'rayleigh_number': data['rayleigh'][i],
                    'reynolds_number': data['reynolds'][i]
                })
        
        df = pd.DataFrame(data_rows)
        df.to_csv(f'{output_dir}/convection_analysis.csv', index=False)
        
        print(f"Dados de convecção exportados para: {output_dir}/convection_analysis.csv")
        return df

def main():
    """
    Executa análise completa de convecção
    """
    print("=== ANÁLISE DE CONVECÇÃO ===")
    
    # Criar análise
    conv_analysis = ConvectionAnalysis()
    
    # Análise básica
    print(f"Propriedades da água a {conv_analysis.T_water}°C:")
    print(f"  • Densidade: {conv_analysis.rho_water:.0f} kg/m³")
    print(f"  • Condutividade térmica: {conv_analysis.k_water:.2f} W/mK")
    print(f"  • Viscosidade cinemática: {conv_analysis.nu_water:.2e} m²/s")
    print(f"  • Número de Prandtl: {conv_analysis.Pr_water:.2f}")
    
    # Calcular números adimensionais para T_surface = 50°C
    T_test = 50
    Gr = conv_analysis.calculate_grashof_number(T_test)
    Ra = conv_analysis.calculate_rayleigh_number(T_test)
    h_nat, Nu_nat = conv_analysis.calculate_heat_transfer_coefficient(T_test, 0)
    
    print(f"\nPara T_superfície = {T_test}°C:")
    print(f"  • Número de Grashof: {Gr:.2e}")
    print(f"  • Número de Rayleigh: {Ra:.2e}")
    print(f"  • Número de Nusselt (conv. natural): {Nu_nat:.1f}")
    print(f"  • Coeficiente h (conv. natural): {h_nat:.0f} W/m²K")
    
    # Gerar gráficos
    print("\nGerando análise gráfica...")
    fig1 = conv_analysis.plot_convection_analysis()
    fig1.savefig('../results/convection_regimes.png', dpi=300, bbox_inches='tight')
    
    # Comparar condições
    print("Simulando diferentes condições de cozimento...")
    fig2, condition_results = conv_analysis.plot_conditions_comparison()
    fig2.savefig('../results/cooking_conditions_comparison.png', dpi=300, bbox_inches='tight')
    
    # Exportar dados
    df = conv_analysis.export_convection_data()
    
    print("\n✅ Análise de convecção concluída!")
    return conv_analysis, condition_results

if __name__ == "__main__":
    analysis, results = main()