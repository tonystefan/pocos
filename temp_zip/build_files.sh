#!/usr/bin/env bash
# exit on error

echo "Building the project..."
# Instalar dependências
pip install -r requirements.txt

# Coletar arquivos estáticos
# O Vercel usa o comando 'python' ou 'python3' dependendo da configuração.
# Usaremos 'python' para maior compatibilidade com o ambiente Vercel.
echo "Collect Static..."
python manage.py collectstatic --noinput --clear

# O projeto não usa banco de dados (models.py vazio), então makemigrations/migrate não são estritamente necessários,
# mas mantê-los pode evitar erros de configuração do Django.
echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
