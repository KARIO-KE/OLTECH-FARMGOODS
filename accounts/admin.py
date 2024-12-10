from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages  # Import messages framework
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser
from farmers.models import Product


class CustomUserAdmin(UserAdmin):
    # List display for the admin page
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'is_approved', 'date_joined', 'short_message',
                    'full_message', 'image']

    # List filter for the admin page
    list_filter = ['role', 'is_staff', 'is_active', 'is_approved']

    # Search fields for the admin page
    search_fields = ['username', 'email']

    # Custom actions for the admin page
    actions = ['approve_farmer', 'approve_buyer', 'reject_farmer', 'delete_farmer', 'delete_buyer', 'customize_account',
               'add_messages_and_image']

    # Modify the fieldsets to add custom fields without duplicating existing ones
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'is_approved', 'short_message', 'full_message', 'image')}),
    )

    # Add fieldsets for creating a new user (this allows admin to add the necessary fields)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'role', 'is_approved', 'short_message', 'full_message', 'image'),
        }),
    )

    # Override the save_model method to approve new users by default
    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created (not updated)
            obj.is_approved = True  # Automatically approve new users
        obj.save()

    # Action to approve a farmer
    def approve_farmer(self, request, queryset):
        updated_count = 0
        for user in queryset:
            if user.role == 'farmer' and not user.is_approved:
                user.is_approved = True
                user.save()
                updated_count += 1
        messages.success(request, f"{updated_count} selected farmers have been approved.")
        self.message_user(request, "Selected farmers have been approved.")

    approve_farmer.short_description = "Approve selected farmers"

    # Action to approve a buyer
    def approve_buyer(self, request, queryset):
        updated_count = 0
        for user in queryset:
            if user.role == 'buyer' and not user.is_approved:
                user.is_approved = True
                user.save()
                updated_count += 1
        messages.success(request, f"{updated_count} selected buyers have been approved.")
        self.message_user(request, "Selected buyers have been approved.")

    approve_buyer.short_description = "Approve selected buyers"

    # Action to reject a farmer
    def reject_farmer(self, request, queryset):
        updated_count = 0
        for user in queryset:
            if user.role == 'farmer':
                user.is_approved = False
                user.save()
                updated_count += 1
        messages.warning(request, f"{updated_count} selected farmers have been rejected.")
        self.message_user(request, "Selected farmers have been rejected.")

    reject_farmer.short_description = "Reject selected farmers"

    # Action to delete a farmer
    def delete_farmer(self, request, queryset):
        deleted_count = queryset.delete()[0]
        messages.success(request, f"{deleted_count} selected farmers have been deleted.")
        self.message_user(request, f"{deleted_count} selected farmers have been deleted.")

    delete_farmer.short_description = "Delete selected farmers"

    # Action to delete a buyer
    def delete_buyer(self, request, queryset):
        deleted_count = queryset.delete()[0]
        messages.success(request, f"{deleted_count} selected buyers have been deleted.")
        self.message_user(request, f"{deleted_count} selected buyers have been deleted.")

    delete_buyer.short_description = "Delete selected buyers"

    # Custom action to customize a user's account (redirect to user change page)
    def customize_account(self, request, queryset):
        user = queryset.first()
        if user:
            # Redirect to the change user page in the Django admin interface
            url = reverse('admin:%s_%s_change' % (user._meta.app_label, user._meta.model_name), args=[user.pk])
            return HttpResponseRedirect(url)
        else:
            messages.error(request, "No user selected for customization.")
            self.message_user(request, "No user selected for customization.", level='error')

    customize_account.short_description = "Customize selected account"

    # New action to add short/full message and image
    def add_messages_and_image(self, request, queryset):
        updated_count = 0
        for user in queryset:
            # Add short and full messages to the user
            user.short_message = "This is a short message for the user."
            user.full_message = "This is a more detailed, full message about the user."
            user.image = "path_to_image.jpg"  # Example image path, update this as needed
            user.save()
            updated_count += 1
            # Add messages for the action
            messages.success(request, f"Message and image for {user.username} have been updated.")

        self.message_user(request, f"{updated_count} users' messages and images have been updated.")

    add_messages_and_image.short_description = "Add short/full message and image for selected users"


class ProductAdmin(admin.ModelAdmin):
    # List display for the admin page
    list_display = ['name', 'price', 'is_approved', 'created_at', 'updated_at', 'farmer']

    # List filter for the admin page
    list_filter = ['is_approved']

    # Search fields for the admin page
    search_fields = ['name', 'description']

    # Custom actions for the admin page
    actions = ['approve_products', 'delete_products', 'redirect_to_upload_list']

    # Action to approve selected products
    def approve_products(self, request, queryset):
        updated_count = 0
        for product in queryset:
            if not product.is_approved:
                product.is_approved = True
                product.save()
                updated_count += 1
        messages.success(request, f"{updated_count} selected products have been approved.")
        self.message_user(request, f"{updated_count} selected products have been approved.")

    approve_products.short_description = "Approve selected products"

    # Action to delete selected products
    def delete_products(self, request, queryset):
        deleted_count = queryset.delete()[0]
        messages.success(request, f"{deleted_count} selected products have been deleted.")
        self.message_user(request, f"{deleted_count} selected products have been deleted.")

    delete_products.short_description = "Delete selected products"

    # Custom action to redirect to the shop/upload.list.html
    def redirect_to_upload_list(self, request, queryset):
        # This would be the custom admin page for product upload
        url = reverse('shop:upload_list')  # Make sure 'upload_list' is the name of your URL pattern
        return HttpResponseRedirect(url)

    redirect_to_upload_list.short_description = "Go to upload list"


admin.site.register(Product, ProductAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
