from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, CustomerProfile


class CustomerProfileInline(admin.StackedInline):
    """Inline admin for CustomerProfile."""
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fk_name = 'user'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with customer profile inline."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_customer', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_customer', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    inlines = (CustomerProfileInline,)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_customer',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('is_customer',)}),
    )
    
    def get_inline_instances(self, request, obj=None):
        """Only show inline if editing existing user."""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Admin for CustomerProfile."""
    list_display = ('user_link', 'user_email', 'user_date_joined')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user__date_joined', 'user__is_active')
    readonly_fields = ('user',)
    
    def user_link(self, obj):
        """Link to user admin page."""
        if obj.user:
            url = admin.site._registry[User].get_url('change', obj.user.pk)
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__username'
    
    def user_email(self, obj):
        """Display user email."""
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def user_date_joined(self, obj):
        """Display user date joined."""
        return obj.user.date_joined if obj.user else '-'
    user_date_joined.short_description = 'Date Joined'
    user_date_joined.admin_order_field = 'user__date_joined'
    
    def has_add_permission(self, request):
        """Prevent adding profiles directly - use user admin."""
        return False
