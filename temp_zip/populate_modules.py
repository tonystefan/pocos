import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocos_project.settings')
django.setup()

from acesso.models import Modulo

modulos_existentes = [
    {'nome': 'Gerar Tabela de Consumo', 'descricao': 'Funcionalidade para gerar e exportar a tabela de consumo.'},
    {'nome': 'Teste de Bombeamento', 'descricao': 'Funcionalidade para realizar e exportar o teste de bombeamento e recuperação.'},
]

def populate_modules():
    print("Iniciando a população de módulos...")
    for modulo_data in modulos_existentes:
        modulo, created = Modulo.objects.get_or_create(
            nome=modulo_data['nome'],
            defaults={'descricao': modulo_data['descricao']}
        )
        if created:
            print(f"Módulo criado: {modulo.nome}")
        else:
            print(f"Módulo já existe: {modulo.nome}")
    print("População de módulos concluída.")

if __name__ == '__main__':
    populate_modules()
