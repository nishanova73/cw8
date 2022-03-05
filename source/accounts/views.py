from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, ListView

from webapp.models import Review
from .models import Profile
from accounts.forms import SignUpForm, UserChangePasswordForm, UserUpdateForm, ProfileChangeForm



def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('webapp:main_page')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:main_page')


def register_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'register.html', context={'form': form})
    elif request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                is_active=True
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            Profile.objects.create(user=user)

            return redirect('webapp:main_page')
        else:
            return render(request, 'register.html', context={'form': form})


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        con = super().get_context_data()
        con['reviews'] = Review.objects.filter(author=self.object)
        return con


class UserChangeView(UserPassesTestMixin, UpdateView):
        model = User
        template_name = 'user_update.html'
        context_object_name = 'user_obj'
        form_class = UserUpdateForm

        def get_context_data(self, **kwargs):
            if 'profile_form' not in kwargs:
                kwargs['profile_form'] = self.get_profile_form()
            return super().get_context_data(**kwargs)

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            form = self.get_form()
            profile_form = self.get_profile_form()
            if form.is_valid() and profile_form.is_valid():
                return self.form_valid(form, profile_form)
            else:
                return self.form_invalid(form, profile_form)

        def form_valid(self, form, profile_form):
            response = super().form_valid(form)
            profile_form.save()
            return response

        def form_invalid(self, form, profile_form):
            context = self.get_context_data(form=form, profile_form=profile_form)
            return self.render_to_response(context)

        def get_profile_form(self):
            form_kwargs = {'instance': self.object.profile}
            if self.request.method == 'POST':
                form_kwargs['data'] = self.request.POST
                form_kwargs['files'] = self.request.FILES
            return ProfileChangeForm(**form_kwargs)

        def get_success_url(self):
            return reverse('accounts:detail', kwargs={'pk': self.object.pk})

        def test_func(self):
            return self.get_object() == self.request.user


class UserChangePasswordView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_change_password.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:login')


class AllUsers(ListView):
    model = User
    template_name = 'all_users.html'
    context_object_name = 'allusers'