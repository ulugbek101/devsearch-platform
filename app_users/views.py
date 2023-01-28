from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.db.models import Q

from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, DeleteView

from .forms import SkillForm, UserRegistrationForm, UserAccountForm
from .models import Skill, Profile


def developers(request):
    # profiles = Profile.objects.all()
    profiles = Profile.objects.exclude(
        Q(short_intro="") |
        Q(bio="") |
        Q(fullname="")
    ).order_by("created")
    context = {
        "profiles": profiles,
    }
    return render(request, 'app_users/developers.html', context)


class UserAccountView(TemplateView):
    template_name = 'app_users/account.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(UserAccountView, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.profile

        return context


class ProfileView(TemplateView):
    template_name = 'app_users/profile.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['dev_skills'] = self.request.user.profile.skill_set.exclude(description="")
        context['other_skills'] = self.request.user.profile.skill_set.filter(description="")
        return context


def user_account_update(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = UserAccountForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been successfully updated')
            return redirect('account')
        else:
            messages.success(request, 'Form filled incorrectly')
            return redirect('update_account')

    form = UserAccountForm(instance=profile)
    context = {
        'btn_text': 'Update account',
        'form': form,
    }
    return render(request, 'form_template.html', context)


def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'Logout first to log in again')
        return redirect('developers')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, f'Welcome, {user.username}')
            return redirect('account')
        else:
            messages.error(request, 'Incorrect credentials, check and try again')
            return redirect('login')

    return render(request, 'app_users/login.html')


def user_registration(request):
    if request.user.is_authenticated:
        messages.info(request, 'Log out first')
        return redirect('developers')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been successfully created')
            return redirect('login')
        else:
            messages.error(request, 'Check and fill the form correctly')
            return redirect('registration')

    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'app_users/registration.html', context)


def user_logout(request):
    auth.logout(request)
    return redirect('login')


class SkillCreateView(CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'form_template.html'
    extra_context = {
        'btn_text': 'Create skill'
    }

    def get_success_url(self):
        return reverse('account')

    def form_valid(self, form):
        form = form.save(commit=False)
        form.owner = self.request.user.profile
        messages.success(self.request, 'Skill has been successfully added')
        return super(SkillCreateView, self).form_valid(form)


class SkillUpdateView(UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'form_template.html'
    extra_context = {
        'btn_text': 'Update skill'
    }

    def get(self, request, **kwargs):
        try:
            skill = self.request.user.profile.skill_set.get(id=kwargs['pk'])
        except:
            skill = None
        if not skill:
            messages.error(request, 'You cannot update other\'s skill')
            return redirect('account')
        return super(SkillUpdateView, self).get(request, **kwargs)

    def get_success_url(self):
        return reverse('account')

    def form_valid(self, form):
        messages.success(self.request, 'Skill has been successfully updated')
        return super(SkillUpdateView, self).form_valid(form)


def skill_delete(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(pk=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill successfully deleted')
        return redirect('account')

    context = {
        'obj_name': skill.name,
        'obj_type': 'skill'
    }
    return render(request, 'delete_form.html', context)

# class SkillDeleteView(DeleteView):
#     model = Skill
#     template_name = 'delete_form.html'
#
#     def get_success_url(self):
#         return reverse('account')
#
#     def post(self, request, *args, **kwargs):
#         messages.success(self.request, 'Skill successfully deleted')
#         return super(SkillDeleteView, self).post(request, *args, **kwargs)
#
#     # TODO The problem here is that I cannot identify wether a user deleting his own skill or not
#
#     def get_context_data(self, **kwargs):
#         context = super(SkillDeleteView, self).get_context_data(**kwargs)
#         context['obj_name'] = Skill.objects.get(id=kwargs['id']).name
#         context['obj_type'] = 'skill'
#         return context
