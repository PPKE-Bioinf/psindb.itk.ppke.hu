from django.shortcuts import render
from psindb.util.db import DB


def create_graph_data(protein_id, connectivity, row_title=""):
    if not row_title:
        row_title = protein_id

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
        "3": "#879cac",
        "4": "#a9d1d5",
        "5": "#32a481",
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
    rowTitle: "{row_title}",
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


def interactions(request):
    id1 = request.GET.get('id1', None)
    id2 = request.GET.get('id2', None)
    print(f"id1: {id1}")
    print(f"id2: {id2}")

    if request.method == 'GET':
        if not (id1 and id2):
            # TODO FAIL
            return render(
                request,
                "home.html",
                {
                    "protein_id": None,
                },
            )

        query, db_1_results = DB.execute_sql(
            """
            SELECT DISTINCT
            Protein.GO, Protein.G2C,
            Protein.Syngo,
            Protein.Synaptomedb,
            Protein.protein_id
            FROM Protein INNER JOIN Alias ON
            Alias.protein_id=Protein.protein_id AND
            (Alias.protein_alias=%s OR
            Alias.protein_id=%s);
            """,
            (id1, id1)
        )

        id1_db = {
            "id": id1,
            "go": "no",
            "g2c": "no",
            "syngo": "no",
            "synaptomedb": "no",
        }

        try:
            id1_db = {
                "id": id1,
                "go": db_1_results[0][0],
                "g2c": db_1_results[0][1],
                "syngo": db_1_results[0][2],
                "synaptomedb": db_1_results[0][3],
            }
        except IndexError:
            pass

        query, db_2_results = DB.execute_sql(
            """
            SELECT DISTINCT
            Protein.GO, Protein.G2C,
            Protein.Syngo,
            Protein.Synaptomedb,
            Protein.protein_id
            FROM Protein INNER JOIN Alias ON
            Alias.protein_id=Protein.protein_id AND
            (Alias.protein_alias=%s OR
            Alias.protein_id=%s);
            """,
            (id2, id2)
        )

        id2_db = {
            "id": id2,
            "go": "no",
            "g2c": "no",
            "syngo": "no",
            "synaptomedb": "no",
        }

        try:
            id2_db = {
                "id": id2,
                "go": db_2_results[0][0],
                "g2c": db_2_results[0][1],
                "syngo": db_2_results[0][2],
                "synaptomedb": db_2_results[0][3],
            }
        except IndexError:
            pass

        query, query_results = DB.execute_sql(
            """
            SELECT I.protein_id1, I.protein_id2, I.reg_p1, I.reg_p2, I.inferred,
            I.orig_p1, I.orig_p2, I.tax1, P1.link, I.tax2, P2.link, I.host_id, P3.link,
            I.participant_detection1, P4.link, I.participant_detection2, P5.link,
            I.interaction_detection, P6.link, I.interaction_type, P7.link,
            I.experimental_role_region1, P8.link, I.biological_role_region1, P9.link,
            I.experimental_role_region2, P10.link, I.biological_role_region2, P11.link,
            I.source, I.crossreference, I.evidence, I.pmid
            FROM Interaction as I
                INNER JOIN PSI as P1 ON P1.term_id=I.tax1
                INNER JOIN PSI as P2 ON P2.term_id=I.tax2
                INNER JOIN PSI as P3 ON P3.term_id=I.host_id
                INNER JOIN PSI as P4 ON P4.term_id=I.participant_detection1
                INNER JOIN PSI as P5 ON P5.term_id=I.participant_detection2
                INNER JOIN PSI as P6 ON P6.term_id=I.interaction_detection
                INNER JOIN PSI as P7 ON P7.term_id=I.interaction_type
                INNER JOIN PSI as P8 ON P8.term_id=I.experimental_role_region1
                INNER JOIN PSI as P9 ON P9.term_id=I.biological_role_region1
                INNER JOIN PSI as P10 ON P10.term_id=I.experimental_role_region2
                INNER JOIN PSI as P11 ON P11.term_id=I.biological_role_region2
            WHERE (I.protein_id1=%s AND I.protein_id2=%s)
               OR (I.protein_id1=%s AND I.protein_id2=%s);
            """,
            (id1, id2, id2, id1)
        )

        if not query_results:
            return render(
                request,
                "home.html",
                {
                    "protein_id": "NOT FOUND",
                },
            )

        print(query_results)
        print("''''''''''''''''''''query_results''''''''''''''''''''")

        json_results = []

        for result in query_results:
            print(result)

            crossreference_link = ""
            source = result[29]
            crossreference = result[30]
            if source == "Intact":
                crossreference_link = f"https://www.ebi.ac.uk/intact/interaction/{crossreference}"
            elif source == "Biogrid":
                crossreference_link = f"https://thebiogrid.org/interaction/{crossreference}"
            elif source == "STRING":
                crossreference_link = f"https://string-db.org/cgi/network?identifiers=/{crossreference}"


            json_results.append({
                "id_1": result[0],
                "id_2": result[1],
                "connectivity_1": create_graph_data(result[0], result[2]),
                "connectivity_2": create_graph_data(result[1], result[3]),
                "inferred": result[4],
                "original_protein_1": result[5],
                "original_protein_2": result[6],
                "tax_1": result[7],
                "tax_link_1": result[8],
                "tax_2": result[9],
                "tax_link_2": result[10],
                "host": result[11],
                "host_ink": result[12],
                "participant_detection_method_1": result[13],
                "participant_detection_link_1": result[14],
                "participant_detection_method_2": result[15],
                "participant_detection_link_2": result[16],
                "interaction_detection_method": result[17],
                "interaction_detection_link": result[18],
                "interaction_type": result[19],
                "interaction_type_link": result[20],
                "experimental_role_region1": result[21],
                "experimental_role_region1_link": result[22],
                "biological_role_region1": result[23],
                "biological_role_region1_link": result[24],
                "experimental_role_region2": result[25],
                "experimental_role_region2_link": result[26],
                "biological_role_region2": result[27],
                "biological_role_region2_link": result[28],
                "source": result[29],
                "crossreference": crossreference_link,
                "evidence": result[31],
                "pmid": result[32],
            })

        return render(
            request,
            "interactions.html",
            {
                "results": json_results,
                "id1_db": id1_db,
                "id2_db": id2_db,
            },
        )
