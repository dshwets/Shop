from webapp.forms import SimpleSeachForm


def search_form(request):
    form = SimpleSeachForm(request.GET)
    return{'search_from': form}


