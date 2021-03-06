from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                path('admin/', admin.site.urls),
                path('sub/', include('subdivision.urls')),
                path('', include('accounts.urls')),
                path('rep/', include('repartition.urls')),
                path('calc/', include('calculs.urls')),
                path('vac/', include('vacations.urls')),
              ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'subdivision.views.handler_404'
handler500 = 'subdivision.views.handler_500'
