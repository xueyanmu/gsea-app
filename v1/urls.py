from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
import a1

urlpatterns = [
    path('a1/', include('a1.urls')),
    path('admin/', admin.site.urls),
    url(r'^', a1.views.list, name='list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)