"""rashel_agencies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import  TemplateView
from core.views import ReactAppView

import debug_toolbar

admin.site.site_header = 'RASHEL AGENCIES'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
   
    # path('', include("django_nextjs.urls")),
    path('', TemplateView.as_view(template_name='index.html')),
    # path('', ReactAppView.as_view(), name='react-app'),
    path('login/', ReactAppView.as_view(), name='react-app-login'),
    path('home/', ReactAppView.as_view(), name='react-app-home'),
    path('loans/', ReactAppView.as_view(), name='react-app-loans'),
    path('discount/', ReactAppView.as_view(), name='react-app-discount'),
    path('wallet/', ReactAppView.as_view(), name='react-app-wallet'),
    path('spin/', ReactAppView.as_view(), name='react-app-spin'),
    path('register/', ReactAppView.as_view(), name='react-app-register'),
    path('request/', ReactAppView.as_view(), name='react-app-request'),
    #  path('login/', TemplateView.as_view(template_name='login.html')),
    path('api/', include('core.urls')),
     path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),
]


# from django.conf import settings
# from django.conf.urls.static import static

# # ...

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)