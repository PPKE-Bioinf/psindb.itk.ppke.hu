import psindb.routes as routes


def index(request):
    return routes.index(request)


def entry(request, uniprot_id):
    return routes.entry(request, uniprot_id)


def network(request, accession):
    return routes.network(request, accession)


def interactions(request):
    return routes.interactions(request)
