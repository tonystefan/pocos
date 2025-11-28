from django import template
from acesso.models import PermissaoModulo, Modulo

register = template.Library()

@register.simple_tag(takes_context=True)
def has_access(context, nome_modulo):
    """
    Verifica se o usuário logado tem permissão para acessar o módulo.
    Uso: {% has_access 'Nome do Módulo' as pode_acessar %}
    """
    request = context['request']
    user = request.user
    
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
        
    try:
        modulo = Modulo.objects.get(nome=nome_modulo)
        return PermissaoModulo.objects.filter(usuario=user, modulo=modulo).exists()
    except Modulo.DoesNotExist:
        # Se o módulo não estiver cadastrado, por padrão, nega o acesso.
        return False
