from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from django.db import models
from .models import MemorySlideShow, Slide
from accounts.models import User


class SlideInline(admin.TabularInline):
    """Inline admin for Slide model."""
    model = Slide
    extra = 1
    fields = ('media_type', 'media_file', 'caption', 'caption_fa', 'order')
    ordering = ('order',)
    verbose_name = 'Slide'
    verbose_name_plural = 'Slides'


@admin.register(MemorySlideShow)
class MemorySlideShowAdmin(admin.ModelAdmin):
    """Enhanced admin for MemorySlideShow model."""
    list_display = (
        'title',
        'title_fa',
        'owner_link',
        'preview_image',
        'slide_count',
        'date_range',
        'is_public',
        'visit_count',
        'created_at',
    )
    list_filter = (
        'is_public',
        'owner',
        'created_at',
        'date_of_birth',
        'profile_theme',
        'slide_theme',
    )
    search_fields = (
        'title',
        'title_fa',
        'slug',
        'owner__username',
        'owner__email',
        'description',
        'description_fa',
    )
    readonly_fields = (
        'slug',
        'created_at',
        'visit_count',
        'preview_image_display',
        'preview_music_display',
    )
    inlines = [SlideInline]
    date_hierarchy = 'created_at'
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'title_fa', 'slug', 'owner')
        }),
        ('Date Information', {
            'fields': ('date_of_birth', 'date_of_death')
        }),
        ('Content', {
            'fields': ('description', 'description_fa')
        }),
        ('Media', {
            'fields': ('mainImage', 'preview_image_display', 'music', 'preview_music_display')
        }),
        ('Themes', {
            'fields': ('profile_theme', 'slide_theme')
        }),
        ('Settings', {
            'fields': ('is_public', 'visit_count', 'created_at')
        }),
    )
    
    actions = ['make_public', 'make_private', 'duplicate_slideshow']
    
    def owner_link(self, obj):
        """Link to owner's admin page."""
        if obj.owner:
            url = reverse('admin:accounts_user_change', args=[obj.owner.pk])
            return format_html('<a href="{}">{}</a>', url, obj.owner.username)
        return '-'
    owner_link.short_description = 'Owner'
    owner_link.admin_order_field = 'owner__username'
    
    def preview_image(self, obj):
        """Preview main image in list view."""
        if obj.mainImage:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />',
                obj.mainImage.url
            )
        return '-'
    preview_image.short_description = 'Image'
    
    def preview_image_display(self, obj):
        """Preview main image in detail view."""
        if obj.mainImage:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px; object-fit: cover;" />',
                obj.mainImage.url
            )
        return 'No image uploaded'
    preview_image_display.short_description = 'Preview Image'
    
    def preview_music_display(self, obj):
        """Display music file info."""
        if obj.music:
            return format_html(
                '<audio controls><source src="{}" type="audio/mpeg">Your browser does not support the audio tag.</audio><br><small>{}</small>',
                obj.music.url,
                obj.music.name
            )
        return 'No music file uploaded'
    preview_music_display.short_description = 'Preview Music'
    
    def slide_count(self, obj):
        """Display slide count with link."""
        count = obj.slides.count()
        if count > 0:
            url = reverse('admin:memories_slide_changelist') + f'?slideshow__id__exact={obj.pk}'
            return format_html('<a href="{}">{}</a>', url, count)
        return count
    slide_count.short_description = 'Slides'
    slide_count.admin_order_field = 'slides__count'
    
    def date_range(self, obj):
        """Display date range."""
        if obj.date_of_birth and obj.date_of_death:
            return f"{obj.date_of_birth} - {obj.date_of_death}"
        elif obj.date_of_birth:
            return f"Born: {obj.date_of_birth}"
        elif obj.date_of_death:
            return f"Died: {obj.date_of_death}"
        return '-'
    date_range.short_description = 'Date Range'
    
    def make_public(self, request, queryset):
        """Action to make slideshows public."""
        updated = queryset.update(is_public=True)
        self.message_user(
            request,
            f'{updated} slideshow(s) marked as public.',
            messages.SUCCESS
        )
    make_public.short_description = 'Mark selected slideshows as public'
    
    def make_private(self, request, queryset):
        """Action to make slideshows private."""
        updated = queryset.update(is_public=False)
        self.message_user(
            request,
            f'{updated} slideshow(s) marked as private.',
            messages.SUCCESS
        )
    make_private.short_description = 'Mark selected slideshows as private'
    
    def duplicate_slideshow(self, request, queryset):
        """Action to duplicate slideshows."""
        count = 0
        for slideshow in queryset:
            # Create new slideshow
            new_slideshow = MemorySlideShow.objects.create(
                owner=slideshow.owner,
                title=f"{slideshow.title} (Copy)",
                title_fa=slideshow.title_fa,
                date_of_birth=slideshow.date_of_birth,
                date_of_death=slideshow.date_of_death,
                description=slideshow.description,
                description_fa=slideshow.description_fa,
                mainImage=slideshow.mainImage,
                music=slideshow.music,
                profile_theme=slideshow.profile_theme,
                slide_theme=slideshow.slide_theme,
                is_public=False,
            )
            # Copy slides
            for slide in slideshow.slides.all():
                Slide.objects.create(
                    slideshow=new_slideshow,
                    media_type=slide.media_type,
                    media_file=slide.media_file,
                    caption=slide.caption,
                    caption_fa=slide.caption_fa,
                    order=slide.order,
                )
            count += 1
        self.message_user(
            request,
            f'{count} slideshow(s) duplicated successfully.',
            messages.SUCCESS
        )
    duplicate_slideshow.short_description = 'Duplicate selected slideshows'


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    """Enhanced admin for Slide model."""
    list_display = (
        'order',
        'caption_preview',
        'slideshow_link',
        'owner_link',
        'media_type',
        'preview_media',
        'created_info',
    )
    list_filter = (
        'media_type',
        'slideshow__owner',
        'slideshow',
        'slideshow__is_public',
    )
    search_fields = (
        'caption',
        'caption_fa',
        'slideshow__title',
        'slideshow__title_fa',
        'slideshow__owner__username',
        'slideshow__slug',
    )
    list_per_page = 50
    ordering = ('slideshow', 'order')
    date_hierarchy = 'slideshow__created_at'
    
    fieldsets = (
        ('Slide Information', {
            'fields': ('slideshow', 'order', 'media_type', 'caption', 'caption_fa')
        }),
        ('Media File', {
            'fields': ('media_file', 'preview_media_display')
        }),
    )
    
    readonly_fields = ('preview_media_display',)
    change_list_template = 'core/change_list.html'
    
    actions = ['move_up', 'move_down', 'change_media_type_to_image']
    
    def caption_preview(self, obj):
        """Display caption preview."""
        caption = obj.caption or obj.caption_fa or '-'
        if len(caption) > 50:
            return f"{caption[:50]}..."
        return caption
    caption_preview.short_description = 'Caption'
    caption_preview.admin_order_field = 'caption'
    
    def slideshow_link(self, obj):
        """Link to slideshow admin page."""
        if obj.slideshow:
            url = reverse('admin:memories_memoryslideshow_change', args=[obj.slideshow.pk])
            return format_html('<a href="{}">{}</a>', url, obj.slideshow.title)
        return '-'
    slideshow_link.short_description = 'Slideshow'
    slideshow_link.admin_order_field = 'slideshow__title'
    
    def owner_link(self, obj):
        """Link to owner's admin page."""
        if obj.slideshow and obj.slideshow.owner:
            url = reverse('admin:accounts_user_change', args=[obj.slideshow.owner.pk])
            return format_html('<a href="{}">{}</a>', url, obj.slideshow.owner.username)
        return '-'
    owner_link.short_description = 'Owner'
    owner_link.admin_order_field = 'slideshow__owner__username'
    
    def preview_media(self, obj):
        """Preview media in list view."""
        if obj.media_file:
            if obj.media_type == 'image':
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />',
                    obj.media_file.url
                )
            elif obj.media_type == 'video':
                return format_html('<span style="color: red;">▶ VIDEO</span>')
            elif obj.media_type == 'gif':
                return format_html('<span style="color: green;">🎬 GIF</span>')
            elif obj.media_type == 'audio':
                return format_html('<span style="color: blue;">🎵 AUDIO</span>')
        return '-'
    preview_media.short_description = 'Preview'
    
    def preview_media_display(self, obj):
        """Preview media in detail view."""
        if obj.media_file:
            if obj.media_type == 'image':
                return format_html(
                    '<img src="{}" style="max-height: 300px; max-width: 300px; object-fit: contain;" />',
                    obj.media_file.url
                )
            elif obj.media_type == 'video':
                return format_html(
                    '<video controls style="max-width: 400px;"><source src="{}" type="video/mp4">Your browser does not support the video tag.</video>',
                    obj.media_file.url
                )
            elif obj.media_type == 'gif':
                return format_html(
                    '<img src="{}" style="max-height: 300px; max-width: 300px; object-fit: contain;" />',
                    obj.media_file.url
                )
            elif obj.media_type == 'audio':
                return format_html(
                    '<audio controls><source src="{}" type="audio/mpeg">Your browser does not support the audio tag.</audio>',
                    obj.media_file.url
                )
        return 'No media file uploaded'
    preview_media_display.short_description = 'Preview Media'
    
    def created_info(self, obj):
        """Display creation date from slideshow."""
        if obj.slideshow:
            return obj.slideshow.created_at.strftime('%Y-%m-%d %H:%M')
        return '-'
    created_info.short_description = 'Created'
    created_info.admin_order_field = 'slideshow__created_at'
    
    def move_up(self, request, queryset):
        """Action to move slides up (decrease order)."""
        for slide in queryset:
            if slide.order > 1:
                # Swap with previous slide
                prev_slide = Slide.objects.filter(
                    slideshow=slide.slideshow,
                    order=slide.order - 1
                ).first()
                if prev_slide:
                    prev_slide.order, slide.order = slide.order, prev_slide.order
                    prev_slide.save()
                    slide.save()
        self.message_user(request, 'Selected slides moved up.', messages.SUCCESS)
    move_up.short_description = 'Move selected slides up'
    
    def move_down(self, request, queryset):
        """Action to move slides down (increase order)."""
        for slide in queryset.order_by('-order'):
            max_order = Slide.objects.filter(slideshow=slide.slideshow).aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0
            if slide.order < max_order:
                # Swap with next slide
                next_slide = Slide.objects.filter(
                    slideshow=slide.slideshow,
                    order=slide.order + 1
                ).first()
                if next_slide:
                    next_slide.order, slide.order = slide.order, next_slide.order
                    next_slide.save()
                    slide.save()
        self.message_user(request, 'Selected slides moved down.', messages.SUCCESS)
    move_down.short_description = 'Move selected slides down'
    
    def change_media_type_to_image(self, request, queryset):
        """Action to change media type to image."""
        updated = queryset.update(media_type='image')
        self.message_user(
            request,
            f'{updated} slide(s) changed to image type.',
            messages.SUCCESS
        )
    change_media_type_to_image.short_description = 'Change selected slides to image type'
    
    def changelist_view(self, request, extra_context=None):
        """Custom changelist view with grouped slideshows."""
        # Only show grouped view if no specific filter/search is applied
        if not any(key in request.GET for key in ['slideshow__owner__id__exact', 'slideshow__id__exact', 'q', 'media_type']):
            extra_context = extra_context or {}
            slideshows = MemorySlideShow.objects.select_related('owner').prefetch_related('slides').all()
            
            slideshow_groups = []
            for slideshow in slideshows:
                slides = slideshow.slides.all()
                if slides.exists():
                    slideshow_groups.append({
                        'id': slideshow.id,
                        'title': slideshow.title,
                        'user': slideshow.owner,
                        'slug': slideshow.slug,
                        'slides': slides,
                        'count': slides.count(),
                    })
            
            extra_context['slideshow_groups'] = slideshow_groups
        
        return super().changelist_view(request, extra_context=extra_context)