from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('codingame/replays/', include('replays.urls')),
    path('codingame/puzzles/', include('puzzles.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
