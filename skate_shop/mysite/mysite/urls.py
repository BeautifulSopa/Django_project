from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loja/', include('loja.urls')),  # This will include all loja/urls.py paths
    path('', RedirectView.as_view(url='/loja/', permanent=False)),  # Redirect root to loja/
]
