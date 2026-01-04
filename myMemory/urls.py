"""
URL configuration for myMemory project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = 'Memory Slideshow Administration'
admin.site.site_title = 'Memory Admin'
admin.site.index_title = 'Welcome to Memory Slideshow Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slideshows/', include('memories.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
