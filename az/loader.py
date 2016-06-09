import pkgutil


def obj_cache(f):
    cache = {}

    def wrapper(namespace, name, **kwargs):
        key = '{}.{}'.format(namespace, name)

        if key not in cache:
            cache[key] = f(namespace, name, **kwargs)

        return cache[key]

    return wrapper


@obj_cache
def get_object(namespace, name, **kwargs):
    obj_name = '{}.{}'.format(namespace, name)
    loader = pkgutil.get_loader(obj_name)
    obj_not_found = "Unknown object: {}".format(obj_name)

    if loader is None:
        raise RuntimeError(obj_not_found)

    module = loader.load_module()

    factory = getattr(module, 'exports')

    if callable(factory):
        return factory(**kwargs)

    raise RuntimeError(obj_not_found)
