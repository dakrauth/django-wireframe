from django.views import debug as debug_view


def technical_500_response(request, exc_type, exc_value, tb):
    """
    Create a technical server error response. The last three arguments are
    the values returned from sys.exc_info() and friends.
    """
    reporter = debug_view.get_exception_reporter_class(request)(request, exc_type, exc_value, tb)
    html = reporter.get_traceback_html()
    text = reporter.get_traceback_text()
    return text, html
