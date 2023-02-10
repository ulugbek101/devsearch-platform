from django.db.models import Q
from app_users.models import Skill, Profile
from app_main.models import Project

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def developers_search(request):
    query = request.GET.get("query") if request.GET.get("query") else ""
    all_profiles = Profile.objects.exclude(
        Q(fullname=None) |
        Q(fullname="") |
        Q(short_intro=None) |
        Q(short_intro="") |
        Q(bio=None) |
        Q(bio="") |
        Q(location=None) |
        Q(location="")
    ).order_by("created")

    skills = Skill.objects.filter(name__icontains=query)

    all_profiles = all_profiles.filter(
        Q(fullname__icontains=query) |
        Q(short_intro__icontains=query) |
        Q(skill__in=skills)
    ).distinct()
    print(all_profiles, query)
    return all_profiles, query


def generate_pages(request, queryset: Profile | Project):
    page = 1
    if request.GET.get(f'page'):
        page = request.GET.get(f'page')

    paginator = Paginator(queryset, 6)

    try:
        queryset = paginator.page(page)
    except EmptyPage:
        queryset = paginator.page(1)
    except PageNotAnInteger:
        queryset = paginator.page(paginator.num_pages)

    left_index = queryset.number - 2
    right_index = queryset.number + 2

    if left_index < 1:
        left_index = 1
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return queryset, custom_range
