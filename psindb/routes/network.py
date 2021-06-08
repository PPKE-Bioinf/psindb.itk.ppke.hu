from django.http import JsonResponse
import json

def network(request, accession):
    with open(
            f'psindb/routes/network_json/{accession}.json', 'r'
    ) as myfile:
        data = myfile.read()

    return JsonResponse(json.loads(data), safe=False)
