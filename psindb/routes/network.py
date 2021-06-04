from django.http import JsonResponse
import json

def network(request, accession):
    print(f"ACCESSION requested: {accession}")

    # read file
    with open('psindb/routes/test.json', 'r') as myfile:
        data = myfile.read()

    real_test_json = json.loads(data)
    return JsonResponse(real_test_json, safe=False)
