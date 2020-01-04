"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from store.views import index as def_view
from django.conf import settings
from django.conf.urls.static import static
from tastypie.api import Api
from store.api import ReviewResource


v1_api = Api(api_name='v1')
v1_api.register(ReviewResource())

import debug_toolbar

urlpatterns = [
    path('', def_view, name='index'),
    path('store/', include('store.urls'), name='store'),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('api/', include(v1_api.urls)),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
