def allure_decorate(story):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args, **kwargs):
            case_info = kwargs.get('case_info', {})

            from allure import dynamic
            dynamic.story(story)
            dynamic.title(case_info.get('case_name', ''))
            dynamic.description(case_info.get('case_name', ''))
            return func(*args, **kwargs)

        return wrapper

    return decorator
