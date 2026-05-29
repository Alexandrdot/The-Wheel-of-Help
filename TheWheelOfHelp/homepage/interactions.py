from collections import defaultdict
from dataclasses import dataclass

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q

from .models import Comment, ServiceReaction


@dataclass
class ServiceEngagement:
    likes: int = 0
    dislikes: int = 0
    user_vote: int | None = None
    comments_count: int = 0


def _service_key(service):
    ct = ContentType.objects.get_for_model(service.__class__)
    return ct.id, service.pk


def get_engagement(service, user=None):
    ct_id, pk = _service_key(service)
    stats = bulk_engagement([service], user)
    return stats.get((ct_id, pk), ServiceEngagement())


def bulk_engagement(services, user=None):
    if not services:
        return {}

    keys = []
    by_ct = defaultdict(set)
    for service in services:
        ct_id, pk = _service_key(service)
        keys.append((service, ct_id, pk))
        by_ct[ct_id].add(pk)

    query = Q()
    for ct_id, pks in by_ct.items():
        query |= Q(content_type_id=ct_id, object_id__in=pks)

    result = {(ct_id, pk): ServiceEngagement() for _, ct_id, pk in keys}

    for row in (
        ServiceReaction.objects.filter(query)
        .values('content_type_id', 'object_id', 'value')
        .annotate(total=Count('id'))
    ):
        key = (row['content_type_id'], row['object_id'])
        engagement = result[key]
        if row['value'] == ServiceReaction.LIKE:
            engagement.likes = row['total']
        else:
            engagement.dislikes = row['total']

    for row in (
        Comment.objects.filter(query)
        .values('content_type_id', 'object_id')
        .annotate(total=Count('id'))
    ):
        key = (row['content_type_id'], row['object_id'])
        result[key].comments_count = row['total']

    if user and user.is_authenticated:
        for row in ServiceReaction.objects.filter(query, user=user).values(
            'content_type_id', 'object_id', 'value'
        ):
            key = (row['content_type_id'], row['object_id'])
            result[key].user_vote = row['value']

    for service, ct_id, pk in keys:
        service.engagement = result[(ct_id, pk)]

    return result


def set_reaction(user, service, value):
    reaction, created = ServiceReaction.objects.get_or_create(
        user=user,
        content_type=ContentType.objects.get_for_model(service.__class__),
        object_id=service.pk,
        defaults={'value': value},
    )
    if not created:
        if reaction.value == value:
            reaction.delete()
        else:
            reaction.value = value
            reaction.save()


def get_comments(service):
    ct = ContentType.objects.get_for_model(service.__class__)
    return (
        Comment.objects.filter(content_type=ct, object_id=service.pk)
        .select_related('author')
        .order_by('-time_create')
    )
