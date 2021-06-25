from django.shortcuts import render
from psindb.util.db import DB


def create_graph_data(protein_id, connectivity):
    value_ranges = {
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
    }

    prev_value = connectivity[0]
    value_from = 1
    i, value = None, None

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
        "1": "#4a2226",
        "2": "#705080",
        "3": "#32a481",
        "4": "#879cac",
        "5": "#a9d1d5",
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

    js = f"""
    $(document).ready(function(){{
    const connectivity = "{connectivity}";

    const boardConfigData = {{
      length: connectivity.length,
      trackWidth: 920,
      includeAxis: true,
      disableMenu: true
    }};

    const rowConfigData = [
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "Interacting regions",
    displayConfig: {connectivity_data_list}
  }}
];

const elementId = "pfv-{protein_id}";
const pfv = new RcsbFv.Create({{
            boardConfigData,
            rowConfigData,
            elementId
        }});
    }});
    """

    return js


def index(request):
    search = request.GET.get('search', None)
    browse = request.GET.get('browse', None)
    interaction = request.GET.get('interaction', None)
    print(f"SEARCH: {search}")
    print(f"BROWSE: {browse}")

    if not (search or browse or interaction):
        return render(
            request,
            "home.html",
            {
                "show_browse_list": True,
            },
        )

    if search:
        query, query_results = DB.execute_sql(
            """
            SELECT DISTINCT Protein.protein_id, Protein.go, 
            Protein.synaptomedb, Protein.syngo, Protein.g2c,
            Protein.interactions
            FROM Protein INNER JOIN Alias ON 
            Alias.protein_id = Protein.protein_id AND 
            (Alias.protein_alias LIKE %s OR Alias.protein_id LIKE %s)
            ORDER BY Protein.interactions;
            """,
            ("%" + search + "%", "%" + search + "%",)
        )

        if not query_results:
            return render(
                request,
                "home.html",
                {
                    "error": f'"{search}" NOT FOUND',
                },
            )

        results = []

        for query_result in query_results:
            protein_id = query_result[0]
            evidence_go = query_result[1]
            evidence_synaptomedb = query_result[2]
            evidence_syngo = query_result[3]
            evidence_g2c = query_result[4]
            num_interactions = query_result[5]
            # connectivity = query_result[6]
            # insert_js = create_graph_data(protein_id, connectivity)

            results.append({
                "evidence_go": evidence_go,
                "evidence_g2c": evidence_g2c,
                "evidence_syngo": evidence_syngo,
                "evidence_synaptomedb": evidence_synaptomedb,
                "protein_id": protein_id,
                "num_interactions": num_interactions,
                # "insert_js": insert_js,
            })

        return render(
            request,
            "home.html",
            {
                "results": results,
                "search_term": search,
            },
        )

    if browse:
        print("BROWSE parameter: {browse}")

        if browse == "all":
            query, query_results = DB.execute_sql(
                """
                SELECT Protein.go, Protein.g2c, Protein.syngo,
                Protein.synaptomedb, Protein.protein_id,
                Protein.interactions 
                FROM Protein ORDER BY Protein.interactions 
                DESC;
                """
            )
        else:
            query, query_results = DB.execute_sql(
                """
                SELECT Protein.go, Protein.g2c, Protein.syngo,
                Protein.synaptomedb, Protein.protein_id,
                Protein.interactions 
                FROM Protein INNER JOIN Sets 
                ON Sets.protein_id=Protein.protein_id AND 
                Sets.set_name=%s 
                ORDER BY Protein.interactions
                DESC;
                """,
                (browse,)
            )

        if not query_results:
            return render(
                request,
                "home.html",
                {
                    "error": "NOT FOUND",
                },
            )

        results = []

        for query_result in query_results:
            evidence_go = query_result[0]
            evidence_g2c = query_result[1]
            evidence_syngo = query_result[2]
            evidence_synaptomedb = query_result[3]
            protein_id = query_result[4]
            num_interactions = query_result[5]
            # connectivity = query_result[6]
            # insert_js = create_graph_data(protein_id, connectivity)

            results.append({
                "evidence_go": evidence_go,
                "evidence_g2c": evidence_g2c,
                "evidence_syngo": evidence_syngo,
                "evidence_synaptomedb": evidence_synaptomedb,
                "protein_id": protein_id,
                "num_interactions": num_interactions,
                # "insert_js": insert_js,
            })

        return render(
            request,
            "home.html",
            {
                "results": results,
                "browse_term": browse,
            },
        )

    if interaction:
        query, query_results = DB.execute_sql(
            """
            SELECT Partners.protein_id1, Partners.protein_id2, Protein.go, 
            Protein.g2c, Protein.syngo, Protein.synaptomedb
            FROM Protein INNER JOIN Partners
            WHERE (Partners.protein_id1 LIKE %s) AND
                  (Partners.ispsd='PSD') AND
                  (Partners.protein_id2=Protein.protein_id);
            """,
            ("%" + interaction + "%",)
        )

        if not query_results:
            return render(
                request,
                "home.html",
                {
                    "error": f'"INTERACTIONS FOR {interaction}" NOT FOUND',
                },
            )

        results = []

        for query_result in query_results:
            protein_id1 = query_result[0]
            protein_id = query_result[1]
            evidence_go = query_result[2]
            evidence_g2c = query_result[3]
            evidence_syngo = query_result[4]
            evidence_synaptomedb = query_result[5]

            results.append({
                "evidence_go": evidence_go,
                "evidence_g2c": evidence_g2c,
                "evidence_syngo": evidence_syngo,
                "evidence_synaptomedb": evidence_synaptomedb,
                "protein_id1": protein_id1,
                "protein_id": protein_id,
            })

        return render(
            request,
            "home.html",
            {
                "results": results,
                "interaction_term": interaction,
            },
        )
