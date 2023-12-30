from django.contrib import admin
from django.urls import path, include
from .views import landing_page, home_page
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home_page, name='home_page'),
    path('books/', include('main.urls')),
    path('readers/', include('readers.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
