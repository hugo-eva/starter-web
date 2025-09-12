"""
Simulação Completa do Cozimento de Ovo
Integra modelos de transferência de calor e análise de resultados
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from heat_transfer_model import EggHeatTransferModel
import json
import os

class EggCookingSimulation:
    """
    Simulação completa do processo de cozimento do ovo
    """
    
    def __init__(self, properties_file='../data/egg_properties.json'):
        """
        Inicializa a simulação
        """
        self.model = EggHeatTransferModel(properties_file)
        self.results = {}
        
        # Configurar estilo dos gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def run_complete_simulation(self, max_time=900, n_time_points=200):
        """
        Executa simulação completa com diferentes modelos
        """
        print("=== INICIANDO SIMULAÇÃO COMPLETA ===")
        
        time_array = np.linspace(0, max_time, n_time_points)
        
        # 1. Modelo de Capacidade Concentrada
        print("Executando modelo de capacidade concentrada...")
        T_lumped, tau = self.model.lumped_capacity_model(time_array)
        
        # 2. Modelo de Diferenças Finitas
        print("Executando modelo de diferenças finitas...")
        time_span = (0, max_time)
        sol, r = self.model.finite_difference_model(time_span, n_radial=30)
        
        # Extrair temperaturas em pontos específicos
        T_center = []
        T_surface = []
        T_gema_surface = []
        
        for t in time_array:
            T_profile = sol.sol(t)
            T_center.append(T_profile[0])  # Centro
            T_surface.append(T_profile[-1])  # Superfície
            
            # Temperatura na superfície da gema
            r_gema_idx = np.argmin(np.abs(r - self.model.R_gema))
            T_gema_surface.append(T_profile[r_gema_idx])
        
        T_center = np.array(T_center)
        T_surface = np.array(T_surface)
        T_gema_surface = np.array(T_gema_surface)
        
        # 3. Solução Analítica por Séries
        print("Executando solução analítica...")
        T_analytical, lambdas = self.model.analytical_series_solution(time_array)
        
        # Armazenar resultados
        self.results = {
            'time': time_array,
            'T_lumped': T_lumped,
            'T_center_fd': T_center,
            'T_surface_fd': T_surface,
            'T_gema_surface_fd': T_gema_surface,
            'T_analytical': T_analytical,
            'tau': tau,
            'lambdas': lambdas,
            'radial_grid': r,
            'finite_diff_solution': sol
        }
        
        print("Simulação concluída!")
        return self.results
    
    def analyze_cooking_stages(self):
        """
        Analisa os diferentes estágios de cozimento
        """
        if not self.results:
            print("Execute a simulação primeiro!")
            return
        
        time = self.results['time']
        T_center = self.results['T_center_fd']
        T_gema = self.results['T_gema_surface_fd']
        
        # Temperaturas críticas
        T_clara_coag = self.model.props['cooking_criteria']['clara_coagulation_temp']
        T_gema_coag = self.model.props['cooking_criteria']['gema_coagulation_temp']
        
        # Encontrar tempos críticos
        cooking_stages = {}
        
        # Clara começa a coagular
        idx_clara = np.where(T_center >= T_clara_coag)[0]
        if len(idx_clara) > 0:
            cooking_stages['clara_coagulation_start'] = time[idx_clara[0]]
        
        # Gema começa a coagular
        idx_gema = np.where(T_gema >= T_gema_coag)[0]
        if len(idx_gema) > 0:
            cooking_stages['gema_coagulation_start'] = time[idx_gema[0]]
        
        # Ovo mole (clara coagulada, gema líquida)
        soft_idx = np.where((T_center >= T_clara_coag) & (T_gema < T_gema_coag))[0]
        if len(soft_idx) > 0:
            cooking_stages['soft_boiled_optimal'] = time[soft_idx[-1]]
        
        # Ovo médio (gema parcialmente coagulada)
        medium_idx = np.where((T_gema >= T_gema_coag) & (T_gema < T_gema_coag + 5))[0]
        if len(medium_idx) > 0:
            cooking_stages['medium_boiled_optimal'] = time[medium_idx[-1]]
        
        # Ovo duro (totalmente coagulado)
        hard_idx = np.where(T_gema >= T_gema_coag + 10)[0]
        if len(hard_idx) > 0:
            cooking_stages['hard_boiled_optimal'] = time[hard_idx[0]]
        
        return cooking_stages
    
    def plot_temperature_evolution(self):
        """
        Plota evolução temporal das temperaturas
        """
        if not self.results:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        time_min = self.results['time'] / 60  # Converter para minutos
        
        # Gráfico 1: Comparação de modelos (centro)
        axes[0,0].plot(time_min, self.results['T_lumped'], 'b-', 
                      label='Capacidade Concentrada', linewidth=2)
        axes[0,0].plot(time_min, self.results['T_center_fd'], 'r--', 
                      label='Diferenças Finitas (centro)', linewidth=2)
        axes[0,0].plot(time_min, self.results['T_analytical'], 'g:', 
                      label='Solução Analítica', linewidth=2)
        
        axes[0,0].axhline(y=62, color='orange', linestyle='--', alpha=0.7, 
                         label='Coagulação clara')
        axes[0,0].axhline(y=65, color='red', linestyle='--', alpha=0.7, 
                         label='Coagulação gema')
        
        axes[0,0].set_xlabel('Tempo (min)')
        axes[0,0].set_ylabel('Temperatura (°C)')
        axes[0,0].set_title('Comparação de Modelos - Centro do Ovo')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # Gráfico 2: Perfil radial em diferentes tempos
        times_plot = [3, 6, 10, 15]  # minutos
        r_mm = self.results['radial_grid'] * 1000
        
        for t_min in times_plot:
            t_sec = t_min * 60
            T_profile = self.results['finite_diff_solution'].sol(t_sec)
            axes[0,1].plot(r_mm, T_profile, label=f'{t_min} min')
        
        axes[0,1].axhline(y=62, color='orange', linestyle='--', alpha=0.7)
        axes[0,1].axhline(y=65, color='red', linestyle='--', alpha=0.7)
        axes[0,1].axvline(x=self.model.R_gema*1000, color='brown', 
                         linestyle=':', alpha=0.7, label='Interface gema')
        
        axes[0,1].set_xlabel('Raio (mm)')
        axes[0,1].set_ylabel('Temperatura (°C)')
        axes[0,1].set_title('Perfil de Temperatura Radial')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # Gráfico 3: Evolução em diferentes pontos
        axes[1,0].plot(time_min, self.results['T_center_fd'], 'b-', 
                      label='Centro', linewidth=2)
        axes[1,0].plot(time_min, self.results['T_gema_surface_fd'], 'orange', 
                      label='Superfície da gema', linewidth=2)
        axes[1,0].plot(time_min, self.results['T_surface_fd'], 'r-', 
                      label='Superfície do ovo', linewidth=2)
        
        axes[1,0].axhline(y=62, color='orange', linestyle='--', alpha=0.7)
        axes[1,0].axhline(y=65, color='red', linestyle='--', alpha=0.7)
        
        axes[1,0].set_xlabel('Tempo (min)')
        axes[1,0].set_ylabel('Temperatura (°C)')
        axes[1,0].set_title('Evolução Temporal em Diferentes Pontos')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # Gráfico 4: Mapa de calor 2D
        time_2d = np.linspace(0, 15, 50)  # 15 minutos
        r_2d = self.results['radial_grid']
        T_2d = np.zeros((len(r_2d), len(time_2d)))
        
        for i, t in enumerate(time_2d * 60):  # Converter para segundos
            T_2d[:, i] = self.results['finite_diff_solution'].sol(t)
        
        im = axes[1,1].imshow(T_2d, aspect='auto', origin='lower', 
                             extent=[0, 15, 0, self.model.R_total*1000],
                             cmap='hot', vmin=20, vmax=100)
        
        # Adicionar contornos de temperatura
        contours = axes[1,1].contour(np.linspace(0, 15, 50), 
                                    r_mm, T_2d, 
                                    levels=[62, 65, 80], 
                                    colors=['orange', 'red', 'white'],
                                    linewidths=2)
        axes[1,1].clabel(contours, inline=True, fontsize=10)
        
        axes[1,1].set_xlabel('Tempo (min)')
        axes[1,1].set_ylabel('Raio (mm)')
        axes[1,1].set_title('Mapa de Calor - Distribuição de Temperatura')
        
        # Colorbar
        cbar = plt.colorbar(im, ax=axes[1,1])
        cbar.set_label('Temperatura (°C)')
        
        plt.tight_layout()
        return fig
    
    def plot_cooking_analysis(self):
        """
        Plota análise dos estágios de cozimento
        """
        cooking_stages = self.analyze_cooking_stages()
        
        if not cooking_stages:
            print("Não foi possível determinar os estágios de cozimento")
            return
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        time_min = self.results['time'] / 60
        
        # Plotar temperaturas
        ax.plot(time_min, self.results['T_center_fd'], 'b-', 
               label='Centro (clara)', linewidth=3)
        ax.plot(time_min, self.results['T_gema_surface_fd'], 'orange', 
               label='Superfície da gema', linewidth=3)
        
        # Linhas de referência
        ax.axhline(y=62, color='orange', linestyle='--', alpha=0.7, 
                  label='Coagulação clara (62°C)')
        ax.axhline(y=65, color='red', linestyle='--', alpha=0.7, 
                  label='Coagulação gema (65°C)')
        
        # Marcar estágios de cozimento
        colors = ['green', 'yellow', 'red']
        labels = ['Ovo mole', 'Ovo médio', 'Ovo duro']
        
        for i, (stage, color, label) in enumerate(zip(cooking_stages.values(), colors, labels)):
            if stage:
                ax.axvline(x=stage/60, color=color, linestyle='-', alpha=0.8, 
                          linewidth=2, label=f'{label} ({stage/60:.1f} min)')
        
        ax.set_xlabel('Tempo (min)')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Análise dos Estágios de Cozimento do Ovo')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig, cooking_stages
    
    def export_results(self, output_dir='../results'):
        """
        Exporta resultados para arquivos
        """
        if not self.results:
            print("Execute a simulação primeiro!")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Dados numéricos em CSV
        df = pd.DataFrame({
            'tempo_s': self.results['time'],
            'tempo_min': self.results['time'] / 60,
            'T_capacidade_concentrada': self.results['T_lumped'],
            'T_centro_diferenças_finitas': self.results['T_center_fd'],
            'T_superficie_ovo': self.results['T_surface_fd'],
            'T_superficie_gema': self.results['T_gema_surface_fd'],
            'T_analitica': self.results['T_analytical']
        })
        
        df.to_csv(f'{output_dir}/temperature_evolution.csv', index=False)
        
        # 2. Parâmetros do modelo em JSON
        model_params = {
            'geometric_properties': {
                'total_radius_mm': self.model.R_total * 1000,
                'yolk_radius_mm': self.model.R_gema * 1000,
                'shell_thickness_mm': self.model.t_shell * 1000
            },
            'thermal_properties': {
                'biot_number': self.model.calculate_biot_number(),
                'time_constant_s': self.results['tau'],
                'fourier_number_at_600s': self.model.calculate_fourier_number(600)
            },
            'cooking_stages': self.analyze_cooking_stages()
        }
        
        with open(f'{output_dir}/simulation_parameters.json', 'w') as f:
            json.dump(model_params, f, indent=2)
        
        print(f"Resultados exportados para: {output_dir}")
        
        return df, model_params
    
    def generate_report(self):
        """
        Gera relatório completo da simulação
        """
        if not self.results:
            print("Execute a simulação primeiro!")
            return
        
        print("\n" + "="*60)
        print("         RELATÓRIO DE SIMULAÇÃO - COZIMENTO DE OVO")
        print("="*60)
        
        # Parâmetros do modelo
        print(f"\n📏 PARÂMETROS GEOMÉTRICOS:")
        print(f"   • Raio total do ovo: {self.model.R_total*1000:.1f} mm")
        print(f"   • Raio da gema: {self.model.R_gema*1000:.1f} mm")
        print(f"   • Espessura da casca: {self.model.t_shell*1000:.2f} mm")
        
        print(f"\n🔥 PARÂMETROS TÉRMICOS:")
        print(f"   • Número de Biot: {self.model.calculate_biot_number():.3f}")
        print(f"   • Constante de tempo: {self.results['tau']:.1f} s ({self.results['tau']/60:.1f} min)")
        print(f"   • Coeficiente de convecção: {self.model.h_conv:.0f} W/m²K")
        
        # Análise de cozimento
        cooking_stages = self.analyze_cooking_stages()
        print(f"\n🥚 ESTÁGIOS DE COZIMENTO:")
        
        stage_names = {
            'clara_coagulation_start': 'Início coagulação clara',
            'gema_coagulation_start': 'Início coagulação gema',
            'soft_boiled_optimal': 'Ovo mole ótimo',
            'medium_boiled_optimal': 'Ovo médio ótimo',
            'hard_boiled_optimal': 'Ovo duro ótimo'
        }
        
        for stage, time_val in cooking_stages.items():
            if time_val:
                name = stage_names.get(stage, stage)
                print(f"   • {name}: {time_val:.0f} s ({time_val/60:.1f} min)")
        
        # Comparação de modelos
        print(f"\n📊 COMPARAÇÃO DE MODELOS (t=600s):")
        idx_600 = np.argmin(np.abs(self.results['time'] - 600))
        
        print(f"   • Capacidade concentrada: {self.results['T_lumped'][idx_600]:.1f} °C")
        print(f"   • Diferenças finitas (centro): {self.results['T_center_fd'][idx_600]:.1f} °C")
        print(f"   • Solução analítica: {self.results['T_analytical'][idx_600]:.1f} °C")
        
        # Validação do modelo
        Bi = self.model.calculate_biot_number()
        print(f"\n✅ VALIDAÇÃO DO MODELO:")
        if Bi < 0.1:
            print(f"   • Modelo de capacidade concentrada: VÁLIDO (Bi = {Bi:.3f} < 0.1)")
        else:
            print(f"   • Modelo de capacidade concentrada: QUESTIONÁVEL (Bi = {Bi:.3f} > 0.1)")
            print(f"   • Recomenda-se usar modelo de diferenças finitas")
        
        print("\n" + "="*60)

def main():
    """
    Executa simulação completa
    """
    # Criar simulação
    sim = EggCookingSimulation()
    
    # Executar simulação
    results = sim.run_complete_simulation(max_time=900, n_time_points=200)
    
    # Gerar relatório
    sim.generate_report()
    
    # Criar gráficos
    print("\nGerando visualizações...")
    
    # Gráfico principal
    fig1 = sim.plot_temperature_evolution()
    fig1.savefig('../results/temperature_evolution.png', dpi=300, bbox_inches='tight')
    
    # Análise de cozimento
    fig2, cooking_stages = sim.plot_cooking_analysis()
    fig2.savefig('../results/cooking_analysis.png', dpi=300, bbox_inches='tight')
    
    # Exportar resultados
    df, params = sim.export_results()
    
    print("\n✅ Simulação concluída com sucesso!")
    print("📁 Arquivos gerados em ../results/")
    
    return sim, results

if __name__ == "__main__":
    simulation, results = main()