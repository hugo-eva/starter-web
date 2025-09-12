"""
Modelo de Transferência de Calor para Cozimento de Ovo
Implementação das equações de condução e convecção
"""

import numpy as np
import json
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt

class EggHeatTransferModel:
    """
    Modelo de transferência de calor para um ovo esférico simplificado
    """
    
    def __init__(self, properties_file='../data/egg_properties.json'):
        """
        Inicializa o modelo com propriedades físicas do ovo
        """
        with open(properties_file, 'r') as f:
            self.props = json.load(f)
        
        # Propriedades geométricas
        self.R_total = self.props['physical_properties']['egg_diameter'] / 2
        self.t_shell = self.props['physical_properties']['shell_thickness']
        self.R_shell = self.R_total - self.t_shell
        
        # Frações volumétricas (simplificação: gema no centro)
        self.R_gema = self.R_shell * (self.props['physical_properties']['gema_fraction'] ** (1/3))
        
        # Temperaturas
        self.T_initial = self.props['physical_properties']['initial_temperature']
        self.T_water = self.props['physical_properties']['water_temperature']
        
        # Propriedades térmicas
        self.k_shell = self.props['thermal_properties']['shell']['thermal_conductivity']
        self.k_clara = self.props['thermal_properties']['clara']['thermal_conductivity']
        self.k_gema = self.props['thermal_properties']['gema']['thermal_conductivity']
        
        self.rho_shell = self.props['thermal_properties']['shell']['density']
        self.rho_clara = self.props['thermal_properties']['clara']['density']
        self.rho_gema = self.props['thermal_properties']['gema']['density']
        
        self.cp_shell = self.props['thermal_properties']['shell']['specific_heat']
        self.cp_clara = self.props['thermal_properties']['clara']['specific_heat']
        self.cp_gema = self.props['thermal_properties']['gema']['specific_heat']
        
        # Difusividades térmicas
        self.alpha_shell = self.k_shell / (self.rho_shell * self.cp_shell)
        self.alpha_clara = self.k_clara / (self.rho_clara * self.cp_clara)
        self.alpha_gema = self.k_gema / (self.rho_gema * self.cp_gema)
        
        # Coeficiente de convecção
        self.h_conv = self.props['convection_parameters']['natural_convection_h']
    
    def calculate_biot_number(self):
        """
        Calcula o número de Biot para análise de validade do modelo
        """
        Bi = self.h_conv * self.R_total / self.k_shell
        return Bi
    
    def calculate_fourier_number(self, time):
        """
        Calcula o número de Fourier para análise temporal
        """
        Fo = self.alpha_clara * time / (self.R_total ** 2)
        return Fo
    
    def lumped_capacity_model(self, time_array):
        """
        Modelo de capacidade concentrada (válido para Bi < 0.1)
        """
        Bi = self.calculate_biot_number()
        
        if Bi > 0.1:
            print(f"Atenção: Bi = {Bi:.3f} > 0.1. Modelo de capacidade concentrada pode não ser adequado.")
        
        # Propriedades médias ponderadas
        V_gema = (4/3) * np.pi * self.R_gema**3
        V_clara = (4/3) * np.pi * (self.R_shell**3 - self.R_gema**3)
        V_shell = (4/3) * np.pi * (self.R_total**3 - self.R_shell**3)
        V_total = V_gema + V_clara + V_shell
        
        rho_avg = (self.rho_gema * V_gema + self.rho_clara * V_clara + 
                  self.rho_shell * V_shell) / V_total
        cp_avg = (self.cp_gema * V_gema + self.cp_clara * V_clara + 
                 self.cp_shell * V_shell) / V_total
        
        # Constante de tempo
        tau = (rho_avg * cp_avg * V_total) / (self.h_conv * 4 * np.pi * self.R_total**2)
        
        # Solução analítica
        T = self.T_water + (self.T_initial - self.T_water) * np.exp(-time_array / tau)
        
        return T, tau
    
    def finite_difference_model(self, time_span, n_radial=50):
        """
        Modelo de diferenças finitas para condução radial
        """
        # Malha radial
        r = np.linspace(0, self.R_total, n_radial)
        dr = r[1] - r[0]
        
        # Condições iniciais
        T0 = np.full(n_radial, self.T_initial)
        
        def heat_equation(t, T):
            """
            Sistema de EDOs para a equação de difusão de calor esférica
            """
            dTdt = np.zeros_like(T)
            
            for i in range(1, n_radial-1):
                # Determinar propriedades locais
                if r[i] <= self.R_gema:
                    alpha = self.alpha_gema
                elif r[i] <= self.R_shell:
                    alpha = self.alpha_clara
                else:
                    alpha = self.alpha_shell
                
                # Diferenças finitas para coordenadas esféricas
                d2T_dr2 = (T[i+1] - 2*T[i] + T[i-1]) / dr**2
                dT_dr = (T[i+1] - T[i-1]) / (2*dr)
                
                dTdt[i] = alpha * (d2T_dr2 + (2/r[i]) * dT_dr)
            
            # Condições de contorno
            # Centro (r=0): simetria
            dTdt[0] = 6 * self.alpha_gema * (T[1] - T[0]) / dr**2
            
            # Superfície (r=R): convecção
            dTdt[-1] = (2 * self.alpha_shell / dr**2) * (T[-2] - T[-1] + 
                       (self.h_conv * dr / self.k_shell) * (self.T_water - T[-1]))
            
            return dTdt
        
        # Resolver sistema de EDOs
        sol = solve_ivp(heat_equation, time_span, T0, dense_output=True, 
                       method='RK45', rtol=1e-6)
        
        return sol, r
    
    def analytical_series_solution(self, time_array, n_terms=20):
        """
        Solução analítica por séries para esfera com convecção
        (simplificação: propriedades uniformes)
        """
        # Usar propriedades médias
        alpha_avg = (self.alpha_gema + self.alpha_clara + self.alpha_shell) / 3
        
        Bi = self.calculate_biot_number()
        
        # Encontrar raízes da equação transcendental
        # tan(λn) = λn / (1 - Bi)
        lambdas = []
        for n in range(1, n_terms + 1):
            # Estimativa inicial
            if Bi < 1:
                lambda_n = n * np.pi - np.pi/2 + Bi/(n*np.pi)
            else:
                lambda_n = n * np.pi
            
            # Refinamento por Newton-Raphson
            for _ in range(10):
                f = np.tan(lambda_n) - lambda_n / (1 - Bi)
                df = 1/np.cos(lambda_n)**2 - 1/(1 - Bi)
                lambda_n = lambda_n - f/df
                if abs(f) < 1e-10:
                    break
            
            lambdas.append(lambda_n)
        
        lambdas = np.array(lambdas)
        
        # Coeficientes da série
        An = 4 * (np.sin(lambdas) - lambdas * np.cos(lambdas)) / \
             (2 * lambdas - np.sin(2 * lambdas))
        
        # Solução no centro (r=0)
        T_center = np.zeros_like(time_array)
        for i, t in enumerate(time_array):
            Fo = alpha_avg * t / self.R_total**2
            T_center[i] = self.T_water + (self.T_initial - self.T_water) * \
                         np.sum(An * np.exp(-lambdas**2 * Fo))
        
        return T_center, lambdas
    
    def calculate_cooking_times(self):
        """
        Calcula tempos de cozimento baseados nas temperaturas de coagulação
        """
        cooking_temps = self.props['cooking_criteria']
        
        # Usar modelo de capacidade concentrada para estimativa rápida
        time_max = 1200  # 20 minutos
        time_array = np.linspace(0, time_max, 1000)
        T, tau = self.lumped_capacity_model(time_array)
        
        cooking_times = {}
        
        for level, target_temp in [
            ('clara_coagulacao', cooking_temps['clara_coagulation_temp']),
            ('gema_coagulacao', cooking_temps['gema_coagulation_temp'])
        ]:
            # Encontrar tempo quando temperatura atinge valor alvo
            idx = np.where(T >= target_temp)[0]
            if len(idx) > 0:
                cooking_times[level] = time_array[idx[0]]
            else:
                cooking_times[level] = None
        
        return cooking_times
    
    def plot_temperature_profile(self, time_points=[60, 180, 360, 600]):
        """
        Plota perfis de temperatura em diferentes tempos
        """
        time_span = (0, max(time_points))
        sol, r = self.finite_difference_model(time_span)
        
        plt.figure(figsize=(12, 8))
        
        for t in time_points:
            T_profile = sol.sol(t)
            plt.plot(r * 1000, T_profile, label=f't = {t}s')
        
        plt.axhline(y=self.props['cooking_criteria']['clara_coagulation_temp'], 
                   color='orange', linestyle='--', alpha=0.7, 
                   label='Coagulação clara (62°C)')
        plt.axhline(y=self.props['cooking_criteria']['gema_coagulation_temp'], 
                   color='red', linestyle='--', alpha=0.7, 
                   label='Coagulação gema (65°C)')
        
        plt.xlabel('Raio (mm)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Perfil de Temperatura no Ovo vs Tempo')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt.gcf()

if __name__ == "__main__":
    # Teste do modelo
    model = EggHeatTransferModel()
    
    print("=== ANÁLISE DO MODELO DE TRANSFERÊNCIA DE CALOR ===")
    print(f"Raio total do ovo: {model.R_total*1000:.1f} mm")
    print(f"Raio da gema: {model.R_gema*1000:.1f} mm")
    print(f"Espessura da casca: {model.t_shell*1000:.1f} mm")
    print(f"Número de Biot: {model.calculate_biot_number():.3f}")
    
    # Modelo de capacidade concentrada
    time_array = np.linspace(0, 600, 100)
    T_lumped, tau = model.lumped_capacity_model(time_array)
    print(f"Constante de tempo (τ): {tau:.1f} s")
    
    # Tempos de cozimento
    cooking_times = model.calculate_cooking_times()
    print("\n=== TEMPOS DE COZIMENTO ESTIMADOS ===")
    for level, time_val in cooking_times.items():
        if time_val:
            print(f"{level}: {time_val:.0f} s ({time_val/60:.1f} min)")
        else:
            print(f"{level}: Não atingido em 20 min")
    
    # Plotar resultados
    model.plot_temperature_profile()
    plt.savefig('../results/temperature_profiles.png', dpi=300, bbox_inches='tight')
    plt.show()