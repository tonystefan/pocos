#!/usr/bin/env python3
"""
Script de teste para verificar as modificações no sistema de projeção de poços.
"""

import sys
import os
from datetime import date, datetime

# Adicionar o diretório do projeto ao path
sys.path.append('/home/ubuntu/pocos/temp_zip')

# Importar as funções modificadas
from pocos_app.utils import gerar_datas_periodo, gerar_tabela_dados

def test_gerar_datas_periodo():
    """Testa a função gerar_datas_periodo"""
    print("=== Testando gerar_datas_periodo ===")
    
    # Teste 1: Período simples com julho selecionado
    data_inicio = date(2024, 7, 15)
    data_fim = date(2024, 8, 15)
    meses_selecionados = ["jul"]
    
    datas = gerar_datas_periodo(data_inicio, data_fim, meses_selecionados)
    
    print(f"Período: {data_inicio} a {data_fim}")
    print(f"Meses selecionados: {meses_selecionados}")
    print(f"Total de datas geradas: {len(datas)}")
    
    # Mostrar algumas datas
    for i, (data, selecionado) in enumerate(datas[:10]):
        print(f"  {data.strftime('%d/%m/%Y')} - Selecionado: {selecionado}")
    
    if len(datas) > 10:
        print("  ...")
        for i, (data, selecionado) in enumerate(datas[-5:]):
            print(f"  {data.strftime('%d/%m/%Y')} - Selecionado: {selecionado}")
    
    print()

def test_gerar_tabela_dados():
    """Testa a função gerar_tabela_dados"""
    print("=== Testando gerar_tabela_dados ===")
    
    # Parâmetros de teste
    parametros = {
        "data_inicio": date(2024, 7, 15),
        "data_fim": date(2024, 8, 15),
        "horimetro_inicial": 1000.0,
        "horimetro_final": 1100.0,
        "hidrometro_inicial": 5000.0,
        "hidrometro_final": 5500.0,
        "max_horimetro_diario": 10.0,
        "max_hidrometro_diario": 50.0,
        "meses_selecionados": ["jul", "ago"]
    }
    
    print("Parâmetros de teste:")
    for key, value in parametros.items():
        print(f"  {key}: {value}")
    
    df = gerar_tabela_dados(parametros)
    
    print(f"\nDataFrame gerado:")
    print(f"  Número de linhas: {len(df)}")
    print(f"  Colunas: {list(df.columns)}")
    
    if not df.empty:
        print("\nPrimeiras 5 linhas:")
        print(df.head().to_string())
        
        print("\nÚltimas 5 linhas:")
        print(df.tail().to_string())
        
        # Verificar valores acumulados
        print(f"\nVerificação dos valores finais:")
        print(f"  Horímetro final esperado: {parametros['horimetro_final']}")
        print(f"  Horímetro final obtido: {df['Horimetro'].iloc[-1]}")
        print(f"  Hidrômetro final esperado: {parametros['hidrometro_final']}")
        print(f"  Hidrômetro final obtido: {df['Medidor de Vazão'].iloc[-1]}")
    
    print()

if __name__ == "__main__":
    test_gerar_datas_periodo()
    test_gerar_tabela_dados()
    print("Testes concluídos!")

