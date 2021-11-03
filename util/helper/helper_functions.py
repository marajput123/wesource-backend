"""Utility Function"""

def clean_arguments(request_args):
    """Parse Values from Restful module arguments"""
    body = {}
    for key,value in request_args.parse_args().items():
        if value is not None:
            body[key] = value
    return body
