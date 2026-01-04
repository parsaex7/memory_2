from django.db import models
from django.dispatch import receiver
from accounts.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save

def slide_media_upload_path(instance, filename: str) -> str:
    slideshow_id = instance.slug
    return f'slideshows/{slideshow_id}/{filename}'

def slide_media_upload_path_not_profile(instance, filename):
    slideshow_id = instance.slideshow.slug
    return f'slideshows/{slideshow_id}/{filename}'

class MemorySlideShow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slideshows')
    title = models.CharField(max_length=200)
    title_fa = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    description_fa = models.TextField(blank=True)
    mainImage = models.ImageField(upload_to= slide_media_upload_path, null=True, blank=True)
    music = models.FileField(upload_to= slide_media_upload_path, null=True, blank=True) #type: ignore
    THEME_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('elegant', 'Classic & Elegant'),
        ('serene', 'Nature-Inspired & Serene'),
    ]
    
    profile_theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='modern',
        help_text='Select the theme for the profile page'
    )
    slide_theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default='modern',
        help_text='Select the theme for the slideshow page'
    )

    slug = models.SlugField(max_length=30, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True) #type: ignore
    visit_count = models.PositiveIntegerField(default=0, help_text='Total number of visits to this slideshow')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.date_of_birth} - {self.date_of_death})"

    @property
    def ordered_slides(self):
        return self.slides.order_by('order') #type: ignore

@receiver(pre_save, sender=MemorySlideShow)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        instance.slug = base_slug
        counter = 1
        # Ensure slug is unique
        while sender.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{base_slug}-{counter}"
            counter += 1

class Slide(models.Model):
    slideshow = models.ForeignKey(MemorySlideShow, on_delete=models.CASCADE, related_name='slides')
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('gif', 'GIF'),
        ('audio', 'Audio'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    media_file = models.FileField(upload_to=slide_media_upload_path_not_profile, blank=True) #type: ignore
    caption = models.TextField(blank=True)
    caption_fa = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Slide {self.order}"

