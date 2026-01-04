from django.shortcuts import render, get_object_or_404
from django.template import context
from django.db.models import F
from .models import MemorySlideShow, Slide
from khayyam import JalaliDate

def get_language(request):
    """Get language from request parameter, session, or default to 'en'"""
    lang = request.GET.get('lang', '')
    if lang not in ['en', 'fa']:
        lang = request.session.get('language', 'en')
    if lang not in ['en', 'fa']:
        lang = 'en'
    # Store in session for future requests
    request.session['language'] = lang
    return lang

def showProfile(request, slug):
    """Unified profile view that handles both languages"""
    user = get_object_or_404(MemorySlideShow, slug=slug)
    lang = get_language(request)

    # Increment visit count (using F() to avoid race conditions)
    MemorySlideShow.objects.filter(pk=user.pk).update(visit_count=F('visit_count') + 1)
    # Refresh the user object to get updated visit_count
    user.refresh_from_db()

    context = {
        'user': user,
        'lang': lang
    }

    # Add Jalali date formatting for Farsi
    if lang == 'fa':
        context.update({
            'date_of_birth': JalaliDate(user.date_of_birth).strftime('%Y/%m/%d'),
            'date_of_death': JalaliDate(user.date_of_death).strftime('%Y/%m/%d'),
            'born_year': JalaliDate(user.date_of_birth).strftime('%Y'),
            'death_year': JalaliDate(user.date_of_death).strftime('%Y')
        })
        template = 'core/profileFa.html'
    else:
        template = 'core/profileEn.html'

    return render(request, template, context)

def showSlide(request, slug):
    """Unified slideshow view that handles both languages"""
    user = get_object_or_404(MemorySlideShow, slug=slug)
    slides = user.ordered_slides
    lang = get_language(request)

    # Increment visit count (using F() to avoid race conditions)
    MemorySlideShow.objects.filter(pk=user.pk).update(visit_count=F('visit_count') + 1)
    # Refresh the user object to get updated visit_count
    user.refresh_from_db()

    context = {
        'user': user,
        'slides': slides,
        'music_url': user.music.url if user.music else None,
        'lang': lang
    }

    template = 'core/slideFa.html' if lang == 'fa' else 'core/slideEn.html'
    return render(request, template, context)

# Keep old views for backward compatibility (optional - can be removed)
def showProfileEn(request, slug):
    # Create a mutable copy of GET parameters
    mutable_get = request.GET._mutable
    request.GET._mutable = True
    request.GET['lang'] = 'en'
    request.GET._mutable = mutable_get
    return showProfile(request, slug)

def showProfileFa(request, slug):
    # Create a mutable copy of GET parameters
    mutable_get = request.GET._mutable
    request.GET._mutable = True
    request.GET['lang'] = 'fa'
    request.GET._mutable = mutable_get
    return showProfile(request, slug)

def showSlideEn(request, slug):
    # Create a mutable copy of GET parameters
    mutable_get = request.GET._mutable
    request.GET._mutable = True
    request.GET['lang'] = 'en'
    request.GET._mutable = mutable_get
    return showSlide(request, slug)

def showSlideFa(request, slug):
    # Create a mutable copy of GET parameters
    mutable_get = request.GET._mutable
    request.GET._mutable = True
    request.GET['lang'] = 'fa'
    request.GET._mutable = mutable_get
    return showSlide(request, slug)