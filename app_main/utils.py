from .models import Project, Tag

from django.db.models import Q


def project_search(request, query):
    all_projects = Project.objects.all().order_by('-created')
    tags = Tag.objects.filter(
        Q(name__icontains=query)
    )

    all_projects = all_projects.filter(
        Q(name__icontains=query) |
        Q(tags__in=tags) |
        Q(owner__fullname__icontains=query)
    ).distinct()

    return all_projects, query
