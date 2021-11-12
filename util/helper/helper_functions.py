"""Utility Function"""


def clean_arguments(request_args):
    """Parse Values from Restful module arguments"""
    body = {}
    for key, value in request_args.parse_args().items():
        if value is not None:
            body[key] = value
    return body


def clean_product_queries(request):
    """Parse queries from GET ALL product endpoint"""
    query = {}
    valid_queries = (
        "price__lte",
        "price__gte",
        "quantity__gte",
        "quantity__lte",
        "date__lte",
        "date__gte",
        "title_icontains",
    )
    for key, value in request.args.items():
        if key in valid_queries:
            query[key] = value
    return query
