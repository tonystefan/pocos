from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ParametrosForm
from .utils import gerar_tabela_dados, exportar_para_xlsx
import pandas as pd
import json # Import json for pretty printing

def index(request):
    """
    View para a página inicial com o formulário de parâmetros.
    """
    form = ParametrosForm()
    return render(request, 'pocos_app/index.html', {'form': form})

def gerar_tabela(request):
    """
    View para processar o formulário e gerar a tabela de dados.
    """
    if request.method == 'POST':
        form = ParametrosForm(request.POST)
        if form.is_valid():
            # Armazenar os dados do formulário na sessão
            # Certificar que os dados são serializáveis para JSON (necessário para sessão)
            parametros_cleaned = form.cleaned_data
            request.session['parametros'] = parametros_cleaned
            print("--- Parâmetros salvos na sessão (gerar_tabela) ---")
            # Use json.dumps for better readability if needed, but ensure data types are session-compatible
            # print(json.dumps(parametros_cleaned, indent=2, default=str)) 
            print(parametros_cleaned)
            print("--------------------------------------------------")
            
            # Gerar a tabela de dados
            df = gerar_tabela_dados(parametros_cleaned)
            
            # Armazenar a tabela na sessão (convertendo para dicionário)
            request.session['tabela'] = df.to_dict('records')
            
            # Renderizar a página de resultados
            return render(request, 'pocos_app/resultados.html', {
                'tabela': df.to_html(classes='table table-striped', index=False),
                'form': form
            })
    else:
        # Se não for POST, redirecionar para a página inicial
        return redirect('index')
    
    # Se o formulário não for válido, voltar para a página inicial com o formulário
    return render(request, 'pocos_app/index.html', {'form': form})

def exportar_xlsx(request):
    """
    View para exportar a tabela para XLSX.
    """
    print("--- Tentando exportar XLSX ---")
    # Verificar se há dados na sessão
    if 'tabela' not in request.session or 'parametros' not in request.session:
        print("Erro: 'tabela' ou 'parametros' não encontrados na sessão.")
        return redirect('index')
    
    # Recuperar a tabela e os parâmetros da sessão
    tabela_dict = request.session.get('tabela', [])
    parametros = request.session.get('parametros', {})
    
    print("--- Parâmetros recuperados da sessão (exportar_xlsx) ---")
    # print(json.dumps(parametros, indent=2, default=str))
    print(parametros)
    print("------------------------------------------------------")
    print(f"Tipo de 'parametros': {type(parametros)}")
    print(f"'parametros' é um dicionário? {isinstance(parametros, dict)}")

    if not isinstance(parametros, dict) or not parametros:
        print("Erro: 'parametros' recuperados da sessão não são um dicionário válido ou estão vazios.")
        # Talvez redirecionar ou mostrar um erro mais específico
        return redirect('index') 
        
    df = pd.DataFrame(tabela_dict)
    
    if df.empty:
        print("Erro: DataFrame criado a partir da sessão está vazio.")
        return redirect('index')

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

