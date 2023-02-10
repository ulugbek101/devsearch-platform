from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, DeleteView

from .forms import SkillForm, UserRegistrationForm, UserAccountForm, MessageForm
from .models import Skill, Profile, Message

from .utils import developers_search, generate_pages


def developers(request):
    # profiles = Profile.objects.all()
    all_profiles, query = developers_search(request)
    all_profiles, custom_range = generate_pages(request, all_profiles)

    context = {
        "all_profiles": all_profiles,
        "query": query,
        "custom_range": custom_range,
    }
    return render(request, 'app_users/developers.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    context = {
        'unread_messages': profile.messages.filter(is_read=False).count(),
        'recieved_messages': profile.messages.all(),
    }
    return render(request, 'app_users/inbox.html', context)


def send_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    if request.user.is_authenticated:
        is_authenticated = True
        profile = request.user.profile
    else:
        is_authenticated = False
        profile = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = profile if is_authenticated else None
            message.recipient = recipient
            message.fullname = profile.fullname if is_authenticated else request.POST.get('fullname')
            message.email = profile.fullname if is_authenticated else request.POST.get('email')
            message.save()
            messages.success(request, 'Message sent')
            return redirect('profile', pk=pk)
        else:
            messages.error(request, 'Form filled incorrectly')
            return redirect('send_message', pk=pk)

    form = MessageForm()
    context = {
        'form': form,
    }
    return render(request, 'app_users/send_message.html', context)


def message_detail(request, pk):
    message = Message.objects.get(id=pk)
    message.is_read = True
    message.save()
    context = {
        'message': Message.objects.get(id=pk),
    }
    return render(request, 'app_users/message_detail.html', context)


def account(request):
    user_account = request.user.profile

    if user_account.fullname == "" or user_account.fullname is None or \
            user_account.short_intro == "" or user_account.short_intro is None or \
            user_account.bio == "" or user_account.bio is None or \
            user_account.location == "" or user_account.location is None:
        messages.warning(request, 'Provide your fullname, occupation, location and bio, otherwise you will not be'
                                  ' shown on search results or anywhere else')

    context = {
        'profile': user_account
    }
    return render(request, 'app_users/account.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {
        'profile': profile,
        'dev_skills': profile.skill_set.exclude(description=""),
        'other_skills': profile.skill_set.filter(description=""),

    }
    return render(request, 'app_users/profile_detail.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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
