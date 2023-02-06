from django.db.models import Q
from app_users.models import Skill, Profile


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
