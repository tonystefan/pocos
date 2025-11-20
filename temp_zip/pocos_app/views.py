from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ParametrosForm
from .forms_teste import TesteBombeamentoForm, TesteRecuperacaoForm
from .utils import gerar_tabela_dados, exportar_para_xlsx
from .utils_teste import gerar_teste_bombeamento, gerar_teste_recuperacao, gerar_teste_xlsx_file
from datetime import date, time
import pandas as pd
import json # Import json for pretty printing

def menu_principal(request):
    return render(request, 'pocos_app/menu.html')

def teste_bombeamento_view(request):
    """
    View para a página inicial do Teste de Bombeamento com os formulários.
    """
    form_bombeamento = TesteBombeamentoForm()
    form_recuperacao = TesteRecuperacaoForm()
    return render(request, 'pocos_app/teste_bombeamento.html', {
                'form_bombeamento': form_bombeamento,
                'form_recuperacao': form_recuperacao
            })

def teste_bombeamento_process(request):
    """
    View para processar os formulários e gerar o relatório de teste.
    """
    if request.method == 'POST':
        form_bombeamento = TesteBombeamentoForm(request.POST)
        form_recuperacao = TesteRecuperacaoForm(request.POST)
        
        if form_bombeamento.is_valid() and form_recuperacao.is_valid():
            params_bombeamento = form_bombeamento.cleaned_data
            params_recuperacao = form_recuperacao.cleaned_data
            
            # 1. Gerar Teste de Bombeamento
            df_bombeamento = gerar_teste_bombeamento(params_bombeamento)
            
            # A coluna 'Data/Hora' já deve estar formatada como string em utils_teste.py.
            # Se não estiver, a conversão para string será feita implicitamente pelo to_dict('records').
            # O erro de .dt.strftime() ocorre porque a coluna já é string.
            # Removendo a conversão explícita aqui.
            
            # 2. Determinar Níveis para o Teste de Recuperação
            # Nível Inicial da Recuperação = Nível Final do Bombeamento
            nivel_inicial_rec = params_bombeamento['nivel_final']
            # Nível Final da Recuperação = Nível Inicial do Bombeamento
            nivel_final_rec = params_bombeamento['nivel_inicial']
            
            # 3. Gerar Teste de Recuperação
            df_recuperacao = gerar_teste_recuperacao(params_recuperacao, nivel_inicial_rec, nivel_final_rec)
            
            # A coluna 'Data/Hora' já deve estar formatada como string em utils_teste.py.
            # Se não estiver, a conversão para string será feita implicitamente pelo to_dict('records').
            # O erro de .dt.strftime() ocorre porque a coluna já é string.
            # Removendo a conversão explícita aqui.
            
            # Armazenar dados na sessão para exportação
            request.session['teste_bombeamento'] = df_bombeamento.to_dict('records')
            request.session['teste_recuperacao'] = df_recuperacao.to_dict('records')
            # Converter objetos date/time nos parâmetros para string antes de salvar na sessão
            for key, value in params_bombeamento.items():
                if isinstance(value, (date, time)):
                    params_bombeamento[key] = str(value)
            
            for key, value in params_recuperacao.items():
                if isinstance(value, (date, time)):
                    params_recuperacao[key] = str(value)
            
            request.session['params_bombeamento'] = params_bombeamento
            request.session['params_recuperacao'] = params_recuperacao
            request.session['nivel_inicial_rec'] = nivel_inicial_rec
            request.session['nivel_final_rec'] = nivel_final_rec
            
            # Preparar contexto para a página de resultados
            context = {
                'df_bombeamento_html': df_bombeamento.to_html(classes='table table-striped table-hover text-center', index=False),
                'df_recuperacao_html': df_recuperacao.to_html(classes='table table-striped table-hover text-center', index=False),
            }
            
            # Redirecionar para a página de resultados
            return render(request, 'pocos_app/teste_bombeamento_resultados.html', context)
        
        else:
            # Se o formulário não for válido, voltar para a página inicial com os erros
            return render(request, 'pocos_app/teste_bombeamento.html', {
                'form_bombeamento': form_bombeamento,
                'form_recuperacao': form_recuperacao
            })
    
    return redirect('teste_bombeamento')

def exportar_teste_xlsx(request):
    """
    View para exportar os testes de Bombeamento e Recuperação para XLSX.
    """
    if 'teste_bombeamento' not in request.session or 'teste_recuperacao' not in request.session:
        return redirect('teste_bombeamento')
        
    df_bombeamento = pd.DataFrame(request.session.get('teste_bombeamento', []))
    df_recuperacao = pd.DataFrame(request.session.get('teste_recuperacao', []))
    
    params_bombeamento = request.session.get('params_bombeamento', {})
    params_recuperacao = request.session.get('params_recuperacao', {})
    nivel_inicial_rec = request.session.get('nivel_inicial_rec')
    nivel_final_rec = request.session.get('nivel_final_rec')
    
    # Converter strings de data/hora de volta para objetos
    from datetime import datetime, time, date
    
    def convert_to_datetime_object(params):
        for key in ['data_inicio']:
            if key in params and isinstance(params[key], str):
                params[key] = datetime.strptime(params[key], '%Y-%m-%d').date()
        for key in ['hora_inicial', 'hora_final']:
            if key in params and isinstance(params[key], str):
                # Assumindo que o timefield retorna string no formato HH:MM:SS
                try:
                    params[key] = datetime.strptime(params[key], '%H:%M:%S').time()
                except ValueError:
                    params[key] = datetime.strptime(params[key], '%H:%M').time()
        return params

    params_bombeamento = convert_to_datetime_object(params_bombeamento)
    params_recuperacao = convert_to_datetime_object(params_recuperacao)
    
    xlsx_data = gerar_teste_xlsx_file(df_bombeamento, df_recuperacao, params_bombeamento, params_recuperacao, nivel_inicial_rec, nivel_final_rec)
    
    response = HttpResponse(
        xlsx_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=teste_bombeamento_recuperacao.xlsx'
    return response
    return render(request, 'pocos_app/menu.html')

def gerar_tabela_consumo_view(request):
    """
    View para a página inicial com o formulário de parâmetros.
    """
    form = ParametrosForm()
    return render(request, 'pocos_app/index.html', {'form': form})

def gerar_tabela_consumo_process(request):
    """
    View para processar o formulário e gerar a tabela de dados.
    """
    if request.method == 'POST':
        form = ParametrosForm(request.POST)
        if form.is_valid():
            # Armazenar os dados do formulário na sessão
            # Certificar que os dados são serializáveis para JSON (necessário para sessão)
            parametros_cleaned = form.cleaned_data.copy()
            
            # Converter objetos date para strings para serialização JSON
            if 'data_inicio' in parametros_cleaned and parametros_cleaned['data_inicio']:
                parametros_cleaned['data_inicio'] = parametros_cleaned['data_inicio'].isoformat()
            if 'data_fim' in parametros_cleaned and parametros_cleaned['data_fim']:
                parametros_cleaned['data_fim'] = parametros_cleaned['data_fim'].isoformat()
            
            request.session['parametros'] = parametros_cleaned
            print("--- Parâmetros salvos na sessão (gerar_tabela) ---")
            # Use json.dumps for better readability if needed, but ensure data types are session-compatible
            # print(json.dumps(parametros_cleaned, indent=2, default=str)) 
            print(parametros_cleaned)
            print("--------------------------------------------------")
            
            # Gerar a tabela de dados (usando os dados originais com objetos date)
            df = gerar_tabela_dados(form.cleaned_data)
            
            # Armazenar a tabela na sessão (convertendo para dicionário)
            request.session['tabela'] = df.to_dict('records')
            
            # Renderizar a página de resultados
            return render(request, 'pocos_app/resultados.html', {
                'tabela': df.to_html(classes='table table-striped', index=False),
                'form': form
            })
    else:
        # Se não for POST, redirecionar para a página inicial
        return redirect('gerar_tabela_consumo')
    
    # Se o formulário não for válido, voltar para a página inicial com o formulário
    return render(request, 'pocos_app/index.html', {'form': form})

def exportar_xlsx(request):
    """
    View para exportar a tabela de Consumo para XLSX.
    """
    """
    View para exportar a tabela para XLSX.
    """
    print("--- Tentando exportar XLSX ---")
    # Verificar se há dados na sessão
    if 'tabela' not in request.session or 'parametros' not in request.session:
        print("Erro: 'tabela' ou 'parametros' não encontrados na sessão.")
        return redirect('gerar_tabela_consumo')
    
    # Recuperar a tabela e os parâmetros da sessão
    tabela_dict = request.session.get('tabela', [])
    parametros = request.session.get('parametros', {}).copy()
    
    # Converter strings de data de volta para objetos date
    from datetime import datetime
    if 'data_inicio' in parametros and isinstance(parametros['data_inicio'], str):
        parametros['data_inicio'] = datetime.fromisoformat(parametros['data_inicio']).date()
    if 'data_fim' in parametros and isinstance(parametros['data_fim'], str):
        parametros['data_fim'] = datetime.fromisoformat(parametros['data_fim']).date()
    
    print("--- Parâmetros recuperados da sessão (exportar_xlsx) ---")
    # print(json.dumps(parametros, indent=2, default=str))
    print(parametros)
    print("------------------------------------------------------")
    print(f"Tipo de 'parametros': {type(parametros)}")
    print(f"'parametros' é um dicionário? {isinstance(parametros, dict)}")

    if not isinstance(parametros, dict) or not parametros:
        print("Erro: 'parametros' recuperados da sessão não são um dicionário válido ou estão vazios.")
        # Talvez redirecionar ou mostrar um erro mais específico
        return redirect('gerar_tabela_consumo') 
        
    df = pd.DataFrame(tabela_dict)
    
    if df.empty:
        print("Erro: DataFrame criado a partir da sessão está vazio.")
        return redirect('gerar_tabela_consumo')

    try:
        print("Chamando exportar_para_xlsx(df, parametros)...")
        # Exportar para XLSX, passando os parâmetros
        xlsx_data = exportar_para_xlsx(df, parametros)
        print("exportar_para_xlsx executado com sucesso.")
    except Exception as e:
        print(f"Erro ao chamar exportar_para_xlsx: {e}")
        import traceback
        traceback.print_exc() # Imprime o traceback completo no console do servidor
        # Retornar uma resposta de erro para o usuário seria ideal aqui
        return HttpResponse(f"Erro ao gerar o arquivo Excel: {e}", status=500)

    
    # Criar a resposta HTTP com o arquivo XLSX
    response = HttpResponse(
        xlsx_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=dados_poco.xlsx'
    print("Enviando resposta com o arquivo XLSX.")
    return response

