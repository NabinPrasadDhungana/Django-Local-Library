from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        try:
            form.save(
                use_https=self.request.is_secure(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                request=self.request,
            )
            return super().form_valid(form)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}')

class SignUpView(UserPassesTestMixin, CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add user to the "librarians" group
        group = Group.objects.get(name='library members')
        self.object.groups.add(group)
        return response
    
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('index')