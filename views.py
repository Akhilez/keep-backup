from keep.lib.handlers import keep_view


def home(request):
    return keep_view.get_view(request)
