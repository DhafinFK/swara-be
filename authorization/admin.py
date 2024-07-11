from django.contrib import admin
from .models import *


admin.site.register(User)


@admin.register(LawExpertSignUp)
class LawExpertSignup(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_approved')
    actions = ['approve_signup']

    def approve_signup(self, request, queryset):
        for signup in queryset:
            if signup.is_approved:
                self.message_user(request, f'{signup.full_name} is already approved.')
                continue
            
            print("creating user")
            user = User.objects.create(
                email=signup.email,
                full_name=signup.full_name,
                password=signup.password,
                role='law_expert',
                law_certificate=signup.law_certificate
            )

            user.save()
            
            signup.is_approved = True
            signup.save()
            self.message_user(request, f'{signup.full_name} has been approved')

    approve_signup.short_description = 'Approve selected signups'
