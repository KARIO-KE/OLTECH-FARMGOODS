from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # List display for the admin page
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'is_approved', 'date_joined']

    # List filter for the admin page
    list_filter = ['role', 'is_staff', 'is_active', 'is_approved']

    # Search fields for the admin page
    search_fields = ['username', 'email']

    # Custom actions for the admin page
    actions = ['approve_farmer', 'approve_buyer', 'reject_farmer', 'delete_farmer', 'delete_buyer', 'customize_account']

    # Modify the fieldsets to add custom fields without duplicating existing ones
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'is_approved')}),
    )

    # Add fieldsets for creating a new user (this allows admin to add the necessary fields)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_approved'),
        }),
    )

    # Override the save_model method to approve new users by default
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created (not updated)
            obj.is_approved = True  # Automatically approve new users
        obj.save()

    # Action to approve a farmer
    def approve_farmer(self, request, queryset):
        for user in queryset:
            if user.role == 'farmer' and not user.is_approved:
                user.is_approved = True
                user.save()
        self.message_user(request, "Selected farmers have been approved.")

    approve_farmer.short_description = "Approve selected farmers"

    # Action to approve a buyer
    def approve_buyer(self, request, queryset):
        for user in queryset:
            if user.role == 'buyer' and not user.is_approved:
                user.is_approved = True
                user.save()
        self.message_user(request, "Selected buyers have been approved.")

    approve_buyer.short_description = "Approve selected buyers"

    # Action to reject a farmer
    def reject_farmer(self, request, queryset):
        for user in queryset:
            if user.role == 'farmer':
                user.is_approved = False
                user.save()
        self.message_user(request, "Selected farmers have been rejected.")

    reject_farmer.short_description = "Reject selected farmers"

    # Action to delete a farmer
    def delete_farmer(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected farmers have been deleted.")

    delete_farmer.short_description = "Delete selected farmers"

    # Action to delete a buyer
    def delete_buyer(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected buyers have been deleted.")

    delete_buyer.short_description = "Delete selected buyers"

    # Custom action to customize a user's account (redirect to user change page)
    def customize_account(self, request, queryset):
        # If more than one user is selected, redirect to the first selected user's change page
        user = queryset.first()
        if user:
            # Redirect to the change user page in the Django admin interface
            url = reverse('admin:%s_%s_change' % (user._meta.app_label, user._meta.model_name), args=[user.pk])
            return HttpResponseRedirect(url)
        else:
            self.message_user(request, "No user selected for customization.", level='error')

    customize_account.short_description = "Customize selected account"

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
