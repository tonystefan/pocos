# Solução de Controle de Acesso Baseado em Módulos para Plataforma Django

## Introdução

Esta documentação detalha a implementação de um sistema de **Controle de Acesso Baseado em Módulos (MABAC - Module-Based Access Control)** na sua plataforma Django. O objetivo é permitir que você gerencie quais usuários têm permissão para acessar funcionalidades (módulos) específicas da aplicação, além dos dois módulos já existentes: "Gerar Tabela de Consumo" e "Teste de Bombeamento".

## 1. Estrutura da Solução

A solução foi implementada através da criação de um novo aplicativo Django chamado `acesso`, que contém a lógica central para o gerenciamento de permissões.

### 1.1. Modelos de Dados (`acesso/models.py`)

Foram criados dois modelos principais para gerenciar o acesso:

| Modelo | Descrição | Campos Chave |
| :--- | :--- | :--- |
| **`Modulo`** | Representa uma funcionalidade ou seção da aplicação que requer controle de acesso. | `nome` (CharField, único), `descricao` (TextField) |
| **`PermissaoModulo`** | Associa um usuário (do modelo `User` padrão do Django) a um `Modulo`, concedendo a permissão de acesso. | `usuario` (ForeignKey para `User`), `modulo` (ForeignKey para `Modulo`) |

A relação `unique_together = ('usuario', 'modulo')` em `PermissaoModulo` garante que um usuário não possa ter a mesma permissão duplicada.

### 1.2. Lógica de Controle de Acesso (`acesso/utils.py`)

A lógica de verificação de permissão é centralizada em duas funções:

1.  **`usuario_tem_acesso(user, nome_modulo)`**:
    *   Verifica se o usuário é um **Superusuário** (que sempre tem acesso).
    *   Caso contrário, consulta o banco de dados para verificar se existe um registro em `PermissaoModulo` que ligue o `user` ao `Modulo` com o `nome_modulo` especificado.

2.  **`@acesso_requerido(nome_modulo, redirect_url='menu_principal')`**:
    *   Este é um **decorator** de view que encapsula a lógica de controle de acesso.
    *   Ele é aplicado diretamente às funções de view (`pocos_app/views.py`).
    *   Se o usuário não estiver autenticado, ele é redirecionado para a página de login do Admin.
    *   Se o usuário estiver autenticado, mas não tiver a permissão necessária, ele é redirecionado para a URL definida em `redirect_url` (por padrão, o menu principal).

### 1.3. Integração com Views (`pocos_app/views.py`)

O decorator `@acesso_requerido` foi aplicado a todas as views que representam os módulos:

| View | Módulo Requerido |
| :--- | :--- |
| `menu_principal` | `'Menu Principal'` |
| `gerar_tabela_consumo_view` | `'Gerar Tabela de Consumo'` |
| `gerar_tabela_consumo_process` | `'Gerar Tabela de Consumo'` |
| `exportar_xlsx` | `'Gerar Tabela de Consumo'` |
| `teste_bombeamento_view` | `'Teste de Bombeamento'` |
| `teste_bombeamento_process` | `'Teste de Bombeamento'` |
| `exportar_teste_xlsx` | `'Teste de Bombeamento'` |

### 1.4. Integração com Templates (`pocos_app/templates/pocos_app/menu.html`)

Para garantir que os links de navegação sejam exibidos apenas para usuários com permissão, foi criado um **Template Tag** personalizado (`acesso/templatetags/acesso_tags.py`):

*   **`{% load acesso_tags %}`**: Carrega as tags personalizadas.
*   **`{% has_access 'Nome do Módulo' as pode_acessar %}`**: Verifica a permissão do usuário logado e armazena o resultado booleano na variável `pode_acessar`.
*   O link só é renderizado se a condição `{% if pode_acessar %}` for verdadeira.

Além disso, foi adicionado um link de **Login/Logout** no menu principal para facilitar a autenticação e teste do sistema.

## 2. Como Gerenciar Permissões

O gerenciamento de módulos e permissões é feito através do **Painel Administrativo do Django**.

### 2.1. Cadastro de Módulos

1.  Acesse o Painel Admin (ex: `/admin/`).
2.  Na seção **Controle de Acesso**, clique em **Módulos**.
3.  Os módulos existentes (`Gerar Tabela de Consumo`, `Teste de Bombeamento` e `Menu Principal`) já foram cadastrados via script.
4.  **Para adicionar um novo módulo**, basta clicar em **Adicionar Módulo** e preencher o `Nome` (que deve ser o mesmo nome usado no decorator `@acesso_requerido` da nova view) e a `Descrição`.

### 2.2. Atribuição de Permissões

1.  Acesse o Painel Admin.
2.  Na seção **Controle de Acesso**, clique em **Permissões de Módulos**.
3.  Clique em **Adicionar Permissão de Módulo**.
4.  Selecione o **Usuário** e o **Módulo** ao qual você deseja conceder acesso.
5.  Salve.

> **Observação Importante:** Para que um usuário comum (não Superusuário) consiga acessar qualquer parte da aplicação, ele **deve** ter a permissão para o módulo **'Menu Principal'**.

## 3. Próximos Passos (Adicionando Novos Módulos)

Para adicionar um novo módulo à sua plataforma, siga estes passos:

1.  **Crie o novo app/funcionalidade** (ex: `novo_modulo`).
2.  **Defina as Views** para a nova funcionalidade.
3.  **Aplique o decorator** `@acesso_requerido` à(s) view(s), usando o nome do novo módulo como argumento:
    ```python
    from acesso.utils import acesso_requerido

    @acesso_requerido(nome_modulo='Nome do Novo Módulo')
    def nova_funcionalidade_view(request):
        # ... sua lógica ...
    ```
4.  **Cadastre o novo módulo** no Painel Admin (seção **Módulos**) com o mesmo nome exato (`'Nome do Novo Módulo'`).
5.  **Adicione o link** no seu `menu.html` (ou onde for apropriado), utilizando o template tag `{% has_access 'Nome do Novo Módulo' as pode_acessar %}` para controlar a visibilidade.
6.  **Atribua a permissão** aos usuários desejados no Painel Admin (seção **Permissões de Módulos**).

## 4. Arquivos Modificados/Adicionados

| Arquivo | Status | Descrição |
| :--- | :--- | :--- |
| `acesso/` | **Novo App** | Contém a lógica de controle de acesso. |
| `acesso/models.py` | Novo | Definição dos modelos `Modulo` e `PermissaoModulo`. |
| `acesso/admin.py` | Novo | Registro dos modelos no Painel Admin. |
| `acesso/utils.py` | Novo | Funções `usuario_tem_acesso` e decorator `@acesso_requerido`. |
| `acesso/templatetags/acesso_tags.py` | Novo | Template tag `{% has_access %}` para controle de visibilidade no menu. |
| `pocos_project/settings.py` | Modificado | Adição de `'acesso'` em `INSTALLED_APPS`. |
| `pocos_app/views.py` | Modificado | Aplicação do decorator `@acesso_requerido` em todas as views de módulo. |
| `pocos_app/templates/pocos_app/menu.html` | Modificado | Implementação da lógica de visibilidade de links usando `{% has_access %}` e adição de link de Login/Logout. |
| `populate_modules_menu.py` | Novo | Script para garantir o cadastro inicial dos módulos. |

O arquivo ZIP final com todas as modificações e o novo app `acesso` está anexado.
