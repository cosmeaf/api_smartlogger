from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.urls import NoReverseMatch, get_resolver, get_urlconf, URLResolver, URLPattern

@api_view(['GET'])
def api_root(request, format=None):
    resolver = get_resolver(get_urlconf())
    urls = {}
    
    # Função auxiliar para processar padrões de URL
    def process_urlpatterns(urlpatterns):
        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                process_urlpatterns(pattern.url_patterns)
            elif isinstance(pattern, URLPattern):
                if pattern.name:  # Apenas adiciona rotas que têm um nome
                    try:
                        urls[pattern.name] = reverse(pattern.name, request=request, format=format)
                    except NoReverseMatch:
                        pass

    process_urlpatterns(resolver.url_patterns)
    
    return Response(urls)
