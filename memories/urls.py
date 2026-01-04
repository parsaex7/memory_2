from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from memories import views

urlpatterns = [
    # Unified URLs (primary)
    path('<slug:slug>/', views.showProfile, name='memoir-profile'),
    path('<slug:slug>/show/', views.showSlide, name='play-slide'),
    
    # Backward compatibility URLs (optional - can be removed later)
    path('<slug:slug>/fa/', views.showProfileFa, name='memoir-profile-fa'),
    path('<slug:slug>/en/', views.showProfileEn, name='memoir-profile-en'),
    path('<slug:slug>/show/en/', views.showSlideEn, name='play-slide-en'),
    path('<slug:slug>/show/fa/', views.showSlideFa, name='play-slide-fa')
]

