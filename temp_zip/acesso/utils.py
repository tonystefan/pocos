from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps
from .models import PermissaoModulo

def usuario_tem_acesso(user, nome_modulo):
    """
    Verifica se o usuário tem permissão para acessar o módulo.
    """
    if user.is_superuser:
        return True
    return PermissaoModulo.objects.filter(usuario=user, modulo__nome=nome_modulo).exists()

def acesso_requerido(nome_modulo, redirect_url='menu_principal'):
    """
    Decorator para views que requerem acesso a um módulo específico.
    Redireciona para a URL especificada se o usuário não tiver permissão.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Redireciona para a página de login se não estiver autenticado
                return redirect(f'{reverse("admin:login")}?next={request.path}')
            
            if usuario_tem_acesso(request.user, nome_modulo):
                return view_func(request, *args, **kwargs)
            else:
                # Redireciona para a página de menu principal ou outra página de erro
                return redirect(redirect_url)
        return _wrapped_view
    return decorator
