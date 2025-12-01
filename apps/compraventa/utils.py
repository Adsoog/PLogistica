import os
from django.conf import settings
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    """
    Convierte URLs de HTML (/media/foto.png) a rutas absolutas del sistema (C:/.../media/foto.png)
    """
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    
    elif uri.startswith(sUrl):
        relativePath = uri.replace(sUrl, "")
        path = finders.find(relativePath)
        if not path:
            path = os.path.join(sRoot, relativePath)
            
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(f'Error generando PDF: No se encuentra el archivo: {path}')
    return path