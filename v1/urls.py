from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
import a1

urlpatterns = [
                  path('admin/', admin.site.urls),

                    #take care of the base stuff
                  path('', include('a1.urls', namespace='base')),
                  url(r'^', a1.views.upload_file, name='base'),
                    #this is where the upload_file is
                  url(r'^saved/$', a1.views.upload_file, name='saved'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
