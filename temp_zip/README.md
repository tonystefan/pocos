# Sistema de Análise de Poços de Bombeamento de Água

Este é um sistema web desenvolvido com Django para gerar tabelas de distribuição de consumo de água e horas de trabalho de poços de bombeamento, com base em parâmetros definidos pelo usuário.

## Funcionalidades

- Formulário para entrada de parâmetros (ano início/fim, horímetro inicial/final, hidrômetro inicial/final)
- Definição de valores máximos diários para horímetro e hidrômetro
- Configuração de valores mensais de vazão, horas/dia e dias/mês
- Geração de tabela com datas aleatórias distribuídas conforme os dias/mês especificados
- Cálculo de valores de horímetro e hidrômetro que respeitam a soma total e o valor máximo diário
- Exportação dos resultados para formato XLSX

## Requisitos

- Python 3.10 ou superior
- Django 5.2
- pandas
- openpyxl

## Instalação

1. Clone ou descompacte o projeto em um diretório de sua escolha

2. Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```
     venv\Scripts\activate
     ```
   - No Linux/Mac:
     ```
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Execute as migrações do banco de dados:
   ```
   python manage.py migrate
   ```

6. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

7. Acesse a aplicação em seu navegador:
   ```
   http://127.0.0.1:8000/
   ```

## Como usar

1. Na página inicial, preencha o formulário com os parâmetros desejados:
   - Ano Início e Fim
   - Horímetro Inicial e Final
   - Hidrômetro Inicial e Final
   - Valores máximos diários para horímetro e hidrômetro
   - Para cada mês, defina:
     - Vazão m³/h
     - Horas/Dia
     - Dias (quantidade de dias no mês para gerar dados)

2. Clique no botão "Gerar Tabela"

3. Na página de resultados, você verá a tabela gerada com:
   - Datas distribuídas aleatoriamente conforme os dias/mês especificados
   - Valores de horímetro e hidrômetro que respeitam a soma total e o valor máximo diário
   - Vazão e horas/dia conforme configurado para cada mês

4. Para exportar a tabela para Excel, clique no botão "Exportar para Excel"

## Estrutura do Projeto

- `pocos_project/`: Configurações do projeto Django
- `pocos_app/`: Aplicação principal
  - `forms.py`: Formulários para coleta de parâmetros
  - `utils.py`: Funções utilitárias para geração de dados
  - `views.py`: Views para processamento de formulários e exportação
  - `templates/`: Templates HTML para interface do usuário
  - `urls.py`: Configuração de URLs
- `static/`: Arquivos estáticos (CSS)
- `requirements.txt`: Dependências do projeto

## Personalização

Você pode personalizar o sistema modificando os seguintes arquivos:

- `pocos_app/utils.py`: Para alterar a lógica de geração de dados
- `pocos_app/templates/pocos_app/`: Para modificar a interface do usuário
- `static/css/styles.css`: Para alterar o estilo da aplicação
