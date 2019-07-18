from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger)


def paginate(queryset, pages, request, context, queryset_name):
    """Paginate objects provided by view.

        This function :
            * objects - Queryset in elements;
            * pages - Number of objects per page;
            * request - Request object to get page param in url;
            * context - Context to set new variables into;
            * queryset_name - variable name for list of objects.
        Return:
            * context
    """
    paginator = Paginator(queryset, pages)
    page = request.GET.get('page', '1')

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if isinstance(queryset_name, str):
        context[queryset_name] = queryset
    else:
        raise TypeError('Varialable queryset_name must be a string')
    context['is_paginated'] = queryset.has_other_pages()
    context['page_obj'] = queryset
    context['paginator'] = paginator

    return context

def slice_queryset(queryset, context, size, queryset_name):

    if isinstance(queryset_name, str):

        if len(queryset) > size:
            context[queryset_name] = queryset[:size]
            context['has_other'] = True
        else:
            context[queryset_name] = queryset
            context['has_other'] = False

        return context
    else:
        raise TypeError('Varialable queryset_name must be a string')
