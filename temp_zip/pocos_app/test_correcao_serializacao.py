#!/usr/bin/env python3
"""
Script de teste para verificar a correção do erro de serialização JSON.
"""

import sys
import os
from datetime import date, datetime
import json

# Adicionar o diretório do projeto ao path
sys.path.append('/home/ubuntu/pocos/temp_zip')

def test_serialization():
    """Testa a serialização e deserialização de datas"""
    print("=== Testando Serialização de Datas ===")
    
    # Simular dados do formulário
    parametros_originais = {
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
    
    print("Parâmetros originais:")
    for key, value in parametros_originais.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    # Simular conversão para serialização (como na view gerar_tabela)
    parametros_serializaveis = parametros_originais.copy()
    
    # Converter objetos date para strings
    if 'data_inicio' in parametros_serializaveis and parametros_serializaveis['data_inicio']:
        parametros_serializaveis['data_inicio'] = parametros_serializaveis['data_inicio'].isoformat()
    if 'data_fim' in parametros_serializaveis and parametros_serializaveis['data_fim']:
        parametros_serializaveis['data_fim'] = parametros_serializaveis['data_fim'].isoformat()
    
    print("\nParâmetros serializáveis:")
    for key, value in parametros_serializaveis.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    # Testar serialização JSON
    try:
        json_string = json.dumps(parametros_serializaveis, indent=2)
        print("\n✓ Serialização JSON bem-sucedida!")
        print("JSON gerado:")
        print(json_string)
    except Exception as e:
        print(f"\n✗ Erro na serialização JSON: {e}")
        return False
    
    # Simular recuperação da sessão e deserialização (como na view exportar_xlsx)
    parametros_recuperados = json.loads(json_string)
    
    # Converter strings de data de volta para objetos date
    if 'data_inicio' in parametros_recuperados and isinstance(parametros_recuperados['data_inicio'], str):
        parametros_recuperados['data_inicio'] = datetime.fromisoformat(parametros_recuperados['data_inicio']).date()
    if 'data_fim' in parametros_recuperados and isinstance(parametros_recuperados['data_fim'], str):
        parametros_recuperados['data_fim'] = datetime.fromisoformat(parametros_recuperados['data_fim']).date()
    
    print("\nParâmetros após deserialização:")
    for key, value in parametros_recuperados.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    # Verificar se os dados são equivalentes
    print("\n=== Verificação de Equivalência ===")
    for key in parametros_originais:
        original = parametros_originais[key]
        recuperado = parametros_recuperados[key]
        if original == recuperado:
            print(f"✓ {key}: {original} == {recuperado}")
        else:
            print(f"✗ {key}: {original} != {recuperado}")
            return False
    
    print("\n✓ Todos os dados foram serializados e deserializados corretamente!")
    return True

if __name__ == "__main__":
    success = test_serialization()
    if success:
        print("\n🎉 Teste de correção da serialização passou!")
    else:
        print("\n❌ Teste de correção da serialização falhou!")
        sys.exit(1)

