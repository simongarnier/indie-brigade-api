not_found = ('Not Found', 404)
created = ('Created', 201)


def call_or_not_found(obj, process):
    if obj:
        return process(obj)
    else:
        return not_found
