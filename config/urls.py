from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Мой учебный портал курсов'
admin.site.index_title = 'Разделы админки портала курсов'
admin.site.site_title = 'Админка портала курсов'

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
