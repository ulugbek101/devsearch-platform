from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_main.models import Tag, Project
from . import serializers


@api_view(['POST'])
def add_tag(request):
    project_id, new_tag = request.data.get('project'), request.data.get('tag')
    project = Project.objects.get(id=project_id)

    tag, created = Tag.objects.get_or_create(name=new_tag.lower().replace(',', '').strip())

    try:
        project_tag = project.tags.get(name=tag)
        project_tag_created = 'false'
    except:
        project_tag = None
        project_tag_created = 'true'
    if not project_tag:
        project.tags.add(tag)
        project.save()
    tag = serializers.TagSerializer(tag, many=False).data

    return Response({
        'tag': tag,
        'project_id': project_id,
        'created': project_tag_created,
    })


@api_view(['POST'])
def remove_tag(request):
    project_id, tag_id = request.data.get('projectId'), request.data.get('tagId')
    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    try:
        project.tags.remove(tag)
        deleted = 'true'
    except:
        deleted = 'false'    
        
    return Response({
        'deleted': 'true' if deleted else 'false',
    })
