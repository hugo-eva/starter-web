"""
Módulo de Visualizações Avançadas para Análise de Transferência de Calor
Gráficos interativos e animações
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import seaborn as sns
from heat_transfer_model import EggHeatTransferModel
from egg_simulation import EggCookingSimulation
from convection_analysis import ConvectionAnalysis

class EggVisualization:
    """
    Classe para visualizações avançadas do cozimento do ovo
    """
    
    def __init__(self):
        """
        Inicializa visualizador
        """
        self.model = EggHeatTransferModel()
        self.simulation = EggCookingSimulation()
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("viridis")
    
    def create_3d_egg_model(self):
        """
        Cria modelo 3D do ovo para visualização
        """
        # Criar malha esférica
        phi = np.linspace(0, np.pi, 30)
        theta = np.linspace(0, 2*np.pi, 60)
        phi_grid, theta_grid = np.meshgrid(phi, theta)
        
        # Coordenadas das diferentes camadas
        # Gema
        R_gema = self.model.R_gema
        x_gema = R_gema * np.sin(phi_grid) * np.cos(theta_grid)
        y_gema = R_gema * np.sin(phi_grid) * np.sin(theta_grid)
        z_gema = R_gema * np.cos(phi_grid)
        
        # Clara
        R_clara = self.model.R_shell
        x_clara = R_clara * np.sin(phi_grid) * np.cos(theta_grid)
        y_clara = R_clara * np.sin(phi_grid) * np.sin(theta_grid)
        z_clara = R_clara * np.cos(phi_grid)
        
        # Casca
        R_casca = self.model.R_total
        x_casca = R_casca * np.sin(phi_grid) * np.cos(theta_grid)
        y_casca = R_casca * np.sin(phi_grid) * np.sin(theta_grid)
        z_casca = R_casca * np.cos(phi_grid)
        
        return {
            'gema': (x_gema, y_gema, z_gema),
            'clara': (x_clara, y_clara, z_clara),
            'casca': (x_casca, y_casca, z_casca),
            'phi': phi_grid,
            'theta': theta_grid
        }
    
    def plot_3d_temperature_distribution(self, time_point=300):
        """
        Plota distribuição de temperatura 3D em um tempo específico
        """
        # Executar simulação
        results = self.simulation.run_complete_simulation(max_time=time_point+60)
        
        # Obter perfil de temperatura
        T_profile = results['finite_diff_solution'].sol(time_point)
        r_grid = results['radial_grid']
        
        # Criar modelo 3D
        egg_3d = self.create_3d_egg_model()
        
        fig = plt.figure(figsize=(15, 12))
        
        # Subplot 1: Modelo 3D com cores por temperatura
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Interpolar temperatura para malha 3D
        phi_flat = egg_3d['phi'].flatten()
        theta_flat = egg_3d['theta'].flatten()
        
        # Para cada ponto na superfície, calcular raio e temperatura
        for layer_name, (x, y, z) in [('gema', egg_3d['gema']), 
                                      ('clara', egg_3d['clara']), 
                                      ('casca', egg_3d['casca'])]:
            # Calcular raio para cada ponto
            r_surface = np.sqrt(x**2 + y**2 + z**2)
            
            # Interpolar temperatura
            T_surface = np.interp(r_surface, r_grid, T_profile)
            
            # Plotar com cores baseadas na temperatura
            surf = ax1.plot_surface(x, y, z, facecolors=plt.cm.hot(T_surface/100), 
                                   alpha=0.7, linewidth=0)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title(f'Distribuição 3D de Temperatura (t={time_point}s)')
        
        # Subplot 2: Corte transversal
        ax2 = fig.add_subplot(222)
        
        # Criar malha 2D para corte
        r_2d = np.linspace(0, self.model.R_total, 100)
        z_2d = np.linspace(-self.model.R_total, self.model.R_total, 100)
        R_2d, Z_2d = np.meshgrid(r_2d, z_2d)
        
        # Calcular temperatura para cada ponto
        T_2d = np.zeros_like(R_2d)
        for i in range(len(z_2d)):
            for j in range(len(r_2d)):
                r_point = np.sqrt(R_2d[i,j]**2 + Z_2d[i,j]**2)
                if r_point <= self.model.R_total:
                    T_2d[i,j] = np.interp(r_point, r_grid, T_profile)
                else:
                    T_2d[i,j] = self.model.T_water
        
        contour = ax2.contourf(R_2d*1000, Z_2d*1000, T_2d, levels=20, cmap='hot')
        ax2.contour(R_2d*1000, Z_2d*1000, T_2d, levels=[62, 65], colors=['orange', 'red'], 
                   linewidths=2)
        
        # Adicionar círculos das interfaces
        circle_gema = plt.Circle((0, 0), self.model.R_gema*1000, fill=False, 
                                color='brown', linestyle='--', alpha=0.7)
        circle_clara = plt.Circle((0, 0), self.model.R_shell*1000, fill=False, 
                                 color='white', linestyle='--', alpha=0.7)
        ax2.add_patch(circle_gema)
        ax2.add_patch(circle_clara)
        
        ax2.set_xlabel('Raio (mm)')
        ax2.set_ylabel('Altura (mm)')
        ax2.set_title('Corte Transversal - Isotermas')
        ax2.set_aspect('equal')
        
        # Colorbar
        cbar = plt.colorbar(contour, ax=ax2)
        cbar.set_label('Temperatura (°C)')
        
        # Subplot 3: Perfil radial
        ax3 = fig.add_subplot(223)
        ax3.plot(r_grid*1000, T_profile, 'b-', linewidth=3, label='Perfil de temperatura')
        ax3.axhline(y=62, color='orange', linestyle='--', alpha=0.7, label='Coagulação clara')
        ax3.axhline(y=65, color='red', linestyle='--', alpha=0.7, label='Coagulação gema')
        ax3.axvline(x=self.model.R_gema*1000, color='brown', linestyle=':', alpha=0.7, 
                   label='Interface gema')
        ax3.axvline(x=self.model.R_shell*1000, color='gray', linestyle=':', alpha=0.7, 
                   label='Interface casca')
        
        ax3.set_xlabel('Raio (mm)')
        ax3.set_ylabel('Temperatura (°C)')
        ax3.set_title(f'Perfil Radial de Temperatura (t={time_point}s)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Subplot 4: Gradiente de temperatura
        ax4 = fig.add_subplot(224)
        dT_dr = np.gradient(T_profile, r_grid)
        ax4.plot(r_grid*1000, -dT_dr, 'r-', linewidth=2, label='|dT/dr|')
        ax4.axvline(x=self.model.R_gema*1000, color='brown', linestyle=':', alpha=0.7)
        ax4.axvline(x=self.model.R_shell*1000, color='gray', linestyle=':', alpha=0.7)
        
        ax4.set_xlabel('Raio (mm)')
        ax4.set_ylabel('Gradiente de temperatura (°C/m)')
        ax4.set_title('Gradiente Radial de Temperatura')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_animation(self, max_time=600, fps=10):
        """
        Cria animação da evolução temporal da temperatura
        """
        # Executar simulação
        results = self.simulation.run_complete_simulation(max_time=max_time)
        
        # Configurar animação
        n_frames = int(max_time / (max_time / 60))  # 60 frames
        time_points = np.linspace(0, max_time, n_frames)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Configurar eixos
        r_mm = results['radial_grid'] * 1000
        
        ax1.set_xlim(0, max(r_mm))
        ax1.set_ylim(20, 100)
        ax1.set_xlabel('Raio (mm)')
        ax1.set_ylabel('Temperatura (°C)')
        ax1.set_title('Evolução do Perfil de Temperatura')
        ax1.grid(True, alpha=0.3)
        
        # Linhas de referência
        ax1.axhline(y=62, color='orange', linestyle='--', alpha=0.7, label='Coagulação clara')
        ax1.axhline(y=65, color='red', linestyle='--', alpha=0.7, label='Coagulação gema')
        ax1.axvline(x=self.model.R_gema*1000, color='brown', linestyle=':', alpha=0.7, 
                   label='Interface gema')
        ax1.legend()
        
        ax2.set_xlim(0, max_time/60)
        ax2.set_ylim(20, 100)
        ax2.set_xlabel('Tempo (min)')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.set_title('Evolução Temporal em Pontos Específicos')
        ax2.grid(True, alpha=0.3)
        
        # Linhas para animação
        line1, = ax1.plot([], [], 'b-', linewidth=3, label='Perfil atual')
        line2, = ax2.plot([], [], 'b-', linewidth=2, label='Centro')
        line3, = ax2.plot([], [], 'orange', linewidth=2, label='Superfície gema')
        line4, = ax2.plot([], [], 'r-', linewidth=2, label='Superfície')
        
        ax2.legend()
        
        # Texto para tempo
        time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=14,
                            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        def animate(frame):
            """Função de animação"""
            t = time_points[frame]
            
            # Perfil de temperatura atual
            T_profile = results['finite_diff_solution'].sol(t)
            line1.set_data(r_mm, T_profile)
            
            # Evolução temporal
            time_slice = results['time'][:frame*10] / 60  # Ajustar índice
            if len(time_slice) > 0:
                T_center_slice = results['T_center_fd'][:frame*10]
                T_gema_slice = results['T_gema_surface_fd'][:frame*10]
                T_surface_slice = results['T_surface_fd'][:frame*10]
                
                line2.set_data(time_slice, T_center_slice)
                line3.set_data(time_slice, T_gema_slice)
                line4.set_data(time_slice, T_surface_slice)
            
            time_text.set_text(f'Tempo: {t:.0f} s ({t/60:.1f} min)')
            
            return line1, line2, line3, line4, time_text
        
        # Criar animação
        anim = animation.FuncAnimation(fig, animate, frames=n_frames, 
                                     interval=1000/fps, blit=True, repeat=True)
        
        return anim, fig
    
    def create_interactive_plotly(self):
        """
        Cria visualização interativa com Plotly
        """
        # Executar simulação
        results = self.simulation.run_complete_simulation()
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Evolução Temporal', 'Perfil Radial', 
                           'Mapa de Calor 2D', 'Análise de Cozimento'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        time_min = results['time'] / 60
        
        # Gráfico 1: Evolução temporal
        fig.add_trace(
            go.Scatter(x=time_min, y=results['T_center_fd'], 
                      name='Centro', line=dict(width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_min, y=results['T_gema_surface_fd'], 
                      name='Superfície gema', line=dict(width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_min, y=results['T_surface_fd'], 
                      name='Superfície', line=dict(width=3)),
            row=1, col=1
        )
        
        # Linhas de referência
        fig.add_hline(y=62, line_dash="dash", line_color="orange", 
                     annotation_text="Coagulação clara", row=1, col=1)
        fig.add_hline(y=65, line_dash="dash", line_color="red", 
                     annotation_text="Coagulação gema", row=1, col=1)
        
        # Gráfico 2: Perfil radial (tempo específico)
        t_specific = 300  # 5 minutos
        T_profile = results['finite_diff_solution'].sol(t_specific)
        r_mm = results['radial_grid'] * 1000
        
        fig.add_trace(
            go.Scatter(x=r_mm, y=T_profile, name=f'Perfil t={t_specific}s',
                      line=dict(width=3, color='blue')),
            row=1, col=2
        )
        
        # Gráfico 3: Mapa de calor 2D
        time_2d = np.linspace(0, 15, 30)  # 15 minutos
        r_2d = results['radial_grid'] * 1000
        T_2d = np.zeros((len(r_2d), len(time_2d)))
        
        for i, t in enumerate(time_2d * 60):
            T_2d[:, i] = results['finite_diff_solution'].sol(t)
        
        fig.add_trace(
            go.Heatmap(z=T_2d, x=time_2d, y=r_2d, 
                      colorscale='Hot', showscale=True),
            row=2, col=1
        )
        
        # Gráfico 4: Análise de cozimento
        cooking_stages = self.simulation.analyze_cooking_stages()
        
        fig.add_trace(
            go.Scatter(x=time_min, y=results['T_center_fd'], 
                      name='Centro', line=dict(width=3, color='blue')),
            row=2, col=2
        )
        
        # Marcar estágios
        colors = ['green', 'yellow', 'red']
        stages = ['Mole', 'Médio', 'Duro']
        
        for i, (stage_time, color, stage_name) in enumerate(zip(cooking_stages.values(), colors, stages)):
            if stage_time:
                fig.add_vline(x=stage_time/60, line_dash="solid", 
                             line_color=color, annotation_text=stage_name,
                             row=2, col=2)
        
        # Configurar layout
        fig.update_layout(
            title_text="Análise Interativa de Cozimento de Ovo",
            showlegend=True,
            height=800
        )
        
        fig.update_xaxes(title_text="Tempo (min)", row=1, col=1)
        fig.update_xaxes(title_text="Raio (mm)", row=1, col=2)
        fig.update_xaxes(title_text="Tempo (min)", row=2, col=1)
        fig.update_xaxes(title_text="Tempo (min)", row=2, col=2)
        
        fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=2)
        fig.update_yaxes(title_text="Raio (mm)", row=2, col=1)
        fig.update_yaxes(title_text="Temperatura (°C)", row=2, col=2)
        
        return fig
    
    def plot_sensitivity_analysis(self):
        """
        Análise de sensibilidade dos parâmetros
        """
        # Parâmetros para variar
        parameters = {
            'h_convection': [100, 250, 500, 1000, 2000],
            'egg_diameter': [0.045, 0.050, 0.055, 0.060, 0.065],
            'water_temperature': [80, 90, 100, 110, 120]
        }
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        # Análise para cada parâmetro
        for idx, (param_name, param_values) in enumerate(parameters.items()):
            if idx >= 3:  # Apenas 3 parâmetros
                break
                
            cooking_times = []
            
            for value in param_values:
                # Modificar propriedades temporariamente
                temp_props = self.model.props.copy()
                
                if param_name == 'h_convection':
                    temp_props['convection_parameters']['natural_convection_h'] = value
                elif param_name == 'egg_diameter':
                    temp_props['physical_properties']['egg_diameter'] = value
                elif param_name == 'water_temperature':
                    temp_props['physical_properties']['water_temperature'] = value
                
                # Salvar e executar simulação
                with open('../data/temp_properties.json', 'w') as f:
                    import json
                    json.dump(temp_props, f)
                
                temp_sim = EggCookingSimulation('../data/temp_properties.json')
                temp_results = temp_sim.run_complete_simulation(max_time=900)
                temp_stages = temp_sim.analyze_cooking_stages()
                
                if 'clara_coagulation_start' in temp_stages:
                    cooking_times.append(temp_stages['clara_coagulation_start'] / 60)
                else:
                    cooking_times.append(None)
            
            # Plotar resultados
            valid_data = [(v, t) for v, t in zip(param_values, cooking_times) if t is not None]
            if valid_data:
                values, times = zip(*valid_data)
                axes[idx].plot(values, times, 'o-', linewidth=2, markersize=8)
                
                # Labels
                if param_name == 'h_convection':
                    axes[idx].set_xlabel('Coeficiente h (W/m²K)')
                    axes[idx].set_title('Efeito do Coeficiente de Convecção')
                elif param_name == 'egg_diameter':
                    axes[idx].set_xlabel('Diâmetro do ovo (m)')
                    axes[idx].set_title('Efeito do Tamanho do Ovo')
                elif param_name == 'water_temperature':
                    axes[idx].set_xlabel('Temperatura da água (°C)')
                    axes[idx].set_title('Efeito da Temperatura da Água')
                
                axes[idx].set_ylabel('Tempo para coagulação (min)')
                axes[idx].grid(True, alpha=0.3)
        
        # Remover subplot extra
        if len(parameters) < 4:
            axes[3].remove()
        
        # Limpar arquivo temporário
        import os
        if os.path.exists('../data/temp_properties.json'):
            os.remove('../data/temp_properties.json')
        
        plt.tight_layout()
        return fig
    
    def save_all_visualizations(self, output_dir='../results'):
        """
        Gera e salva todas as visualizações
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("Gerando visualizações...")
        
        # 1. Distribuição 3D
        print("  • Distribuição 3D de temperatura...")
        fig1 = self.plot_3d_temperature_distribution(time_point=300)
        fig1.savefig(f'{output_dir}/3d_temperature_distribution.png', 
                    dpi=300, bbox_inches='tight')
        plt.close(fig1)
        
        # 2. Análise de sensibilidade
        print("  • Análise de sensibilidade...")
        fig2 = self.plot_sensitivity_analysis()
        fig2.savefig(f'{output_dir}/sensitivity_analysis.png', 
                    dpi=300, bbox_inches='tight')
        plt.close(fig2)
        
        # 3. Gráfico interativo (HTML)
        print("  • Gráfico interativo...")
        fig_plotly = self.create_interactive_plotly()
        fig_plotly.write_html(f'{output_dir}/interactive_analysis.html')
        
        # 4. Animação (GIF)
        print("  • Animação temporal...")
        anim, fig_anim = self.create_animation(max_time=600, fps=5)
        anim.save(f'{output_dir}/temperature_evolution.gif', writer='pillow', fps=5)
        plt.close(fig_anim)
        
        print(f"✅ Visualizações salvas em: {output_dir}")

def main():
    """
    Executa todas as visualizações
    """
    print("=== GERAÇÃO DE VISUALIZAÇÕES ===")
    
    # Criar visualizador
    viz = EggVisualization()
    
    # Gerar todas as visualizações
    viz.save_all_visualizations()
    
    print("\n✅ Todas as visualizações foram geradas!")

if __name__ == "__main__":
    main()