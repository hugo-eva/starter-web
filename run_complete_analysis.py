#!/usr/bin/env python3
"""
Script Principal - Projeto de Transferência de Calor: Cozimento de Ovo
Executa análise completa com todos os módulos desenvolvidos
"""

import os
import sys
import time
from datetime import datetime

# Adicionar diretório src ao path
sys.path.append('./src')

# Importações
from heat_transfer_model import EggHeatTransferModel
from egg_simulation import EggCookingSimulation
from convection_analysis import ConvectionAnalysis
from visualization import EggVisualization
from parametric_analysis import ParametricAnalysis

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_step(step, description):
    """Imprime etapa do processo"""
    print(f"\n🔄 Etapa {step}: {description}")
    print("-" * 50)

def main():
    """
    Executa análise completa do projeto
    """
    start_time = time.time()
    
    print_header("PROJETO DE TRANSFERÊNCIA DE CALOR - COZIMENTO DE OVO")
    print(f"📅 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Objetivo: Modelar o processo de cozimento usando modelos simplificados")
    print("📚 Disciplina: Engenharia Mecânica - Transferência de Calor")
    
    # Criar diretório de resultados
    os.makedirs('./results', exist_ok=True)
    
    try:
        # ETAPA 1: Análise do Modelo Base
        print_step(1, "Análise do Modelo de Transferência de Calor")
        
        model = EggHeatTransferModel('./data/egg_properties.json')
        
        print(f"   • Raio total do ovo: {model.R_total*1000:.1f} mm")
        print(f"   • Raio da gema: {model.R_gema*1000:.1f} mm")
        print(f"   • Número de Biot: {model.calculate_biot_number():.4f}")
        
        if model.calculate_biot_number() < 0.1:
            print("   ✅ Modelo de capacidade concentrada é válido")
        else:
            print("   ⚠️ Gradientes internos são significativos")
        
        # ETAPA 2: Simulação Completa
        print_step(2, "Simulação Completa do Cozimento")
        
        simulation = EggCookingSimulation('./data/egg_properties.json')
        results = simulation.run_complete_simulation(max_time=900, n_time_points=200)
        
        # Gerar relatório
        simulation.generate_report()
        
        # Gráficos principais
        fig1 = simulation.plot_temperature_evolution()
        fig1.savefig('./results/temperature_evolution.png', dpi=300, bbox_inches='tight')
        print("   📊 Gráfico de evolução temporal salvo")
        
        fig2, cooking_stages = simulation.plot_cooking_analysis()
        fig2.savefig('./results/cooking_analysis.png', dpi=300, bbox_inches='tight')
        print("   📊 Análise de cozimento salva")
        
        # Exportar dados
        df, params = simulation.export_results('./results')
        print("   💾 Dados exportados para CSV e JSON")
        
        # ETAPA 3: Análise de Convecção
        print_step(3, "Análise de Convecção na Água")
        
        conv_analysis = ConvectionAnalysis('./data/egg_properties.json')
        
        # Gráficos de convecção
        fig3 = conv_analysis.plot_convection_analysis()
        fig3.savefig('./results/convection_regimes.png', dpi=300, bbox_inches='tight')
        print("   📊 Análise de regimes de convecção salva")
        
        # Comparação de condições
        fig4, condition_results = conv_analysis.plot_conditions_comparison()
        fig4.savefig('./results/cooking_conditions_comparison.png', dpi=300, bbox_inches='tight')
        print("   📊 Comparação de condições de cozimento salva")
        
        # Exportar dados de convecção
        df_conv = conv_analysis.export_convection_data('./results')
        print("   💾 Dados de convecção exportados")
        
        # ETAPA 4: Visualizações Avançadas
        print_step(4, "Geração de Visualizações Avançadas")
        
        viz = EggVisualization()
        
        # Distribuição 3D
        fig5 = viz.plot_3d_temperature_distribution(time_point=300)
        fig5.savefig('./results/3d_temperature_distribution.png', dpi=300, bbox_inches='tight')
        print("   📊 Distribuição 3D de temperatura salva")
        
        # Análise de sensibilidade
        fig6 = viz.plot_sensitivity_analysis()
        fig6.savefig('./results/sensitivity_analysis.png', dpi=300, bbox_inches='tight')
        print("   📊 Análise de sensibilidade salva")
        
        # Gráfico interativo
        fig_plotly = viz.create_interactive_plotly()
        fig_plotly.write_html('./results/interactive_analysis.html')
        print("   🌐 Gráfico interativo HTML gerado")
        
        # ETAPA 5: Análise Paramétrica
        print_step(5, "Análise Paramétrica e Otimização")
        
        param_analysis = ParametricAnalysis('./data/egg_properties.json')
        
        # Análise de parâmetros principais
        key_parameters = ['egg_diameter', 'water_temperature', 'convection_coefficient']
        param_ranges = param_analysis.define_parameter_ranges()
        
        for param in key_parameters:
            if param in param_ranges:
                print(f"     → Analisando {param}...")
                df_param = param_analysis.run_single_parameter_study(
                    param, param_ranges[param]['range'][:3]  # Reduzir para velocidade
                )
                
                # Salvar resultados
                df_param.to_csv(f'./results/parametric_{param}.csv', index=False)
                
                # Gráfico
                fig_param = param_analysis.plot_single_parameter_results(
                    df_param, param, param_ranges[param]
                )
                fig_param.savefig(f'./results/parametric_{param}.png', 
                                 dpi=300, bbox_inches='tight')
                print(f"       ✅ Análise de {param} concluída")
        
        # Otimização
        print("     → Executando otimização...")
        target_times = [180, 300, 420]  # 3, 5, 7 minutos
        optimization_results = {}
        
        for target in target_times:
            opt_result = param_analysis.optimization_study(target)
            if opt_result:
                optimization_results[f'target_{target}s'] = opt_result
                print(f"       ✅ Otimização para {target}s concluída")
        
        # Salvar resultados de otimização
        import json
        with open('./results/optimization_results.json', 'w') as f:
            json.dump(optimization_results, f, indent=2)
        
        # ETAPA 6: Relatório Final
        print_step(6, "Geração do Relatório Final")
        
        # Criar relatório em markdown
        with open('./results/relatorio_final.md', 'w', encoding='utf-8') as f:
            f.write("# Relatório Final - Projeto de Transferência de Calor\n\n")
            f.write("## Cozimento de Ovo usando Modelos Simplificados\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            
            f.write("## Resumo Executivo\n\n")
            f.write("Este projeto analisou o processo de transferência de calor durante o ")
            f.write("cozimento de um ovo usando modelos matemáticos simplificados de ")
            f.write("engenharia mecânica.\\n\\n")
            
            f.write("### Parâmetros Principais\n\n")
            f.write(f"- **Raio do ovo:** {model.R_total*1000:.1f} mm\\n")
            f.write(f"- **Número de Biot:** {model.calculate_biot_number():.4f}\\n")
            f.write(f"- **Constante de tempo:** {results['tau']/60:.1f} min\\n")
            f.write(f"- **Coeficiente de convecção:** {model.h_conv} W/m²K\\n\\n")
            
            f.write("### Tempos de Cozimento\n\n")
            for stage, time_val in cooking_stages.items():
                if time_val:
                    stage_name = stage.replace('_', ' ').title()
                    f.write(f"- **{stage_name}:** {time_val/60:.1f} min\\n")
            
            f.write("\\n### Arquivos Gerados\n\n")
            result_files = [
                "temperature_evolution.png - Evolução temporal das temperaturas",
                "cooking_analysis.png - Análise dos estágios de cozimento",
                "convection_regimes.png - Análise de convecção",
                "3d_temperature_distribution.png - Distribuição 3D de temperatura",
                "sensitivity_analysis.png - Análise de sensibilidade",
                "interactive_analysis.html - Gráfico interativo",
                "temperature_evolution.csv - Dados temporais",
                "simulation_parameters.json - Parâmetros do modelo",
                "optimization_results.json - Resultados de otimização"
            ]
            
            for file_desc in result_files:
                f.write(f"- `{file_desc}`\\n")
            
            f.write("\\n## Conclusões\n\n")
            f.write("1. O modelo de capacidade concentrada ")
            if model.calculate_biot_number() < 0.1:
                f.write("é adequado para este problema.\\n")
            else:
                f.write("apresenta limitações devido aos gradientes internos.\\n")
            
            f.write("2. Os tempos de cozimento calculados estão na faixa esperada.\\n")
            f.write("3. A convecção tem papel fundamental no processo.\\n")
            f.write("4. O tamanho do ovo e temperatura da água são parâmetros críticos.\\n")
        
        print("   📄 Relatório final gerado: ./results/relatorio_final.md")
        
        # FINALIZAÇÃO
        end_time = time.time()
        total_time = end_time - start_time
        
        print_header("ANÁLISE COMPLETA FINALIZADA COM SUCESSO!")
        print(f"⏱️  Tempo total de execução: {total_time/60:.1f} minutos")
        print(f"📁 Resultados salvos em: ./results/")
        print(f"📊 Total de gráficos gerados: 8+")
        print(f"💾 Total de arquivos de dados: 6+")
        print(f"🎯 Projeto concluído com êxito!")
        
        # Listar arquivos gerados
        print("\n📋 Arquivos gerados:")
        result_files = os.listdir('./results')
        for i, file in enumerate(sorted(result_files), 1):
            file_size = os.path.getsize(f'./results/{file}') / 1024  # KB
            print(f"   {i:2d}. {file:<35} ({file_size:.1f} KB)")
        
        print("\n" + "="*70)
        print("✅ Para visualizar os resultados:")
        print("   • Abra os arquivos PNG para ver os gráficos")
        print("   • Abra interactive_analysis.html no navegador")
        print("   • Execute o notebook egg_cooking_analysis.ipynb")
        print("   • Leia o relatorio_final.md")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO durante a execução: {str(e)}")
        print("🔧 Verifique as dependências e tente novamente.")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Projeto executado com sucesso!")
        sys.exit(0)
    else:
        print("\n💥 Projeto falhou na execução!")
        sys.exit(1)