import datetime

def add_current_year(request):
    """
    Adds the current year to the context of all templates
    """
    return {'current_year': datetime.datetime.now().year}