from django.shortcuts import render
from django.http import HttpResponse

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="daniel",
    password="password",
    database="PSDInteractome_v0_09"
)


def create_graph_data(sequence, connectivity):
    value_ranges = {
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
    }

    prev_value = connectivity[0]
    value_from = 1

    for i, value in enumerate(connectivity[1:]):
        if value != prev_value:
            value_ranges[prev_value].append({
                "begin": value_from,
                "end": i + 1
            })

            value_from = i + 2

        prev_value = value

    value_ranges[value].append({
        "begin": value_from,
        "end": i + 2
    })

    value_colors = {
        "1": "#76B295",
        "2": "#4A9470",
        "3": "#277650",
        "4": "#0F5935",
        "5": "#001A13",
    }

    value_display_ids = {
        "1": "1_1",
        "2": "1_2",
        "3": "1_3",
        "4": "1_4",
        "5": "1_5",
    }

    connectivity_data_list = []

    for value in value_ranges:
        if not value_ranges[value]:
            continue

        connectivity_data_list.append(
            {
                "displayType": "block",
                "displayColor": value_colors[value],
                "displayId": value_display_ids[value],
                "displayData": value_ranges[value]
            }
        )

    print(connectivity_data_list)

    js = f"""
    $(document).ready(function(){{
    const sequence = "{sequence}";
    
    const boardConfigData = {{
      length: sequence.length,
      trackWidth: 940,
      includeAxis: true
    }};
    
    const rowConfigData = [
  {{
    trackId: "sequenceTrack",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "sequence",
    nonEmptyDisplay: true,
    rowTitle: "SEQUENCE",
    trackData: [
      {{
        begin: 1,
        value: sequence
      }}
    ]
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "ZOOM ME",
    displayConfig: {connectivity_data_list}
    
  }}
];

const elementId = "pfv";
const pfv = new RcsbFv.Create({{
            boardConfigData,
            rowConfigData,
            elementId
        }});
    }});
    """

    print(js)
    return js
    # return ""


def index(request):
    search = request.GET.get('search', None)
    print(f"SEARCH IS: {search}")
    if request.method == 'GET':
        if not search:
            return render(
                request,
                "home.html",
                {
                    "protein_id": None,
                },
            )

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM Protein WHERE protein_id = %s",
            (search,)
        )

        myresult = mycursor.fetchall()

        if not myresult:
            return render(
                request,
                "home.html",
                {
                    "protein_id": "NOT FOUND",
                },
            )

        for x in myresult:
            print(x[2])

        my_sequence = x[1]
        my_interact = x[2]

        insert_js = create_graph_data(my_sequence, my_interact)

        search_results = [
            {
                "my_sequence": my_sequence,
                "my_interact": my_interact
            }
        ]

        return render(
            request,
            "home.html",
            {
                "protein_id": search,
                "insert_js": insert_js,
            },
        )
