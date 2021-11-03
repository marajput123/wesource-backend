def cleanArguments(request_args):
    body = {}
    for key,value in request_args.parse_args().items():
        if value != None:
            body[key] = value
    return body

