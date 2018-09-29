"""auction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/

    https://docs.djangoproject.com/en/2.1/topics/http/urls/

    https://docs.djangoproject.com/en/2.1/topics/http/urls/
>>>>>>> a4af1d00283fb766ff8537be5ed1082455fb0442
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    #path('ajax_search/',include('ajax_search.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




