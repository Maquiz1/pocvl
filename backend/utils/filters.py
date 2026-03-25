from django.db.models import Q


# def apply_search(queryset, search, fields):

#     if not search:
#         return queryset

#     query = Q()

#     for field in fields:
#         query |= Q(**{f"{field}__icontains": search})

#     return queryset.filter(query)


def apply_search(queryset, search, fields):

    if not search:
        return queryset

    valid_fields = [f.name for f in queryset.model._meta.get_fields()]

    query = Q()

    for field in fields:
        if field in valid_fields:
            query |= Q(**{f"{field}__icontains": search})

    return queryset.filter(query)


def apply_filters(queryset, request, fields):

    """
    Apply simple GET filters automatically.

    Example:
    ?site=2&sex=male
    """

    for field in fields:

        value = request.GET.get(field)

        if value:
            queryset = queryset.filter(**{field: value})

    return queryset
