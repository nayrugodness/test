from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import User, Order
from django import forms


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = ["name", "first_name", "last_name", "image", "phone"]


class UserChangePassword(admin_forms.PasswordChangeForm):
    class Meta(admin_forms.PasswordChangeForm):
        model = User
        fields = '__all__'


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = '__all__'
        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserPersonalCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ["username", "name", "first_name", "last_name", "nit", "phone", "contact", "email"]


class UserEnterpriseCreationForm(admin_forms.UserCreationForm):
    # role = forms.CharField(widget=forms.CharField(attrs={"value":"Empresa"}))

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ["username", "name", "nit", "phone", "contact", "email", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({"value": "Empresa", "class": "invisible", "type": "hidden"})
        self.fields['role'] = forms.CharField(widget=forms.HiddenInput())


class OrderCreationForm(forms.ModelForm):
    class Meta(forms.Form):
        model = Order
        fields = ["id", "nft", "bonuses", "buyer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["nft"].widget.attrs.update({"class": "invisible", "type": "hidden"})
        # self.fields["nft"] = forms.IntegerField(widget=forms.HiddenInput())
        # self.fields["buyer"].widget.attrs.update({"class": "invisible", "type": "hidden"})
        # self.fields["buyer"] = forms.IntegerField(widget=forms.HiddenInput())
        # self.fields["buyer"].widget.attrs.update({"value" : request.user , "class" : "invisible", "type" : "hidden "})


class OrderUpdateForm(forms.ModelForm):
    class Meta(forms.Form):
        model = Order
        fields = ["nft", "purchase", "bonuses", "buyer", "voucher"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["nft"].widget.attrs.update({'readonly': 'readonly'})
