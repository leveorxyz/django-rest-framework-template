"""Django_rest_framework_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.conf.urls import handler500, url
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

from .views import Custom404


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("docs/", include_docs_urls(title="Template API")),
    path("__debug__/", include(debug_toolbar.urls)),
    url(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = Custom404.as_view()
handler500 = "Django_rest_framework_template.views.custom_500_handler"
