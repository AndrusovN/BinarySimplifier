def singleton(given_singleton_class):
    instances = {}

    def get_instance(*args, **kwargs):
        if given_singleton_class not in instances:
            instances[given_singleton_class] = given_singleton_class(*args, **kwargs)
        return instances[given_singleton_class]

    return get_instance
