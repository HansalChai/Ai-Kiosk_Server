from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        from allauth.account.utils import user_field
        user = super().save_user(request, user, form, commit)
        user_field(user, 'name', request.data.get('name', ''))
        user.save()
        return user