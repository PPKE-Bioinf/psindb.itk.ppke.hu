from django.shortcuts import render
from django.http import HttpResponse

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="daniel",
    password="password",
    database="PSDInteractome_v0_10"
)


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

    print(connectivity_data_list)

    # rowTitle: "Interacting regions",
    # rowTitle: RcsbFvLink = {{
    #     visibleTex: "VISIBLE TEXT",
    #     url: "google.com"
    # }},

    js = f"""
    $(document).ready(function(){{
    const connectivity = "{connectivity}";
    
    const boardConfigData = {{
      length: connectivity.length,
      trackWidth: 920,
      includeAxis: true,
      includeTooltip: false
    }};
    
    const rowConfigData = [
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    includeTooltip: false,
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
            """
            SELECT DISTINCT Protein.GO, Protein.G2C, 
                Protein.Syngo, Protein.Synaptomedb,
                Protein.protein_id, Protein.Interactions,
                Protein.interacting
            FROM Protein
            INNER JOIN Alias ON Alias.protein_id=Protein.protein_id
            WHERE (Alias.protein_alias=%s OR Alias.protein_id=%s);
            """,
            (search, search,)
        )

        query_results = mycursor.fetchall()

        if not query_results:
            return render(
                request,
                "home.html",
                {
                    "protein_id": "NOT FOUND",
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
            connectivity = query_result[6]
            insert_js = create_graph_data(protein_id, connectivity)

            results.append({
                "evidence_go": evidence_go,
                "evidence_g2c": evidence_g2c,
                "evidence_syngo": evidence_syngo,
                "evidence_synaptomedb": evidence_synaptomedb,
                "protein_id": protein_id,
                "num_interactions": num_interactions,
                "insert_js": insert_js,
            })

        return render(
            request,
            "home.html",
            {
                "results": results,
                "search_term": search,
            },
        )


def entry(request, uniprot_id):
    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT protein_id, GO, G2C, SynGO, SynaptomeDB, Functions,
        Transmembrane, HTP, LLPS, ELM, Phos, PFAM, Coiled_coil, Anchor,
        Disordered, ELM, interacting, sequence
        FROM Protein WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    sql2 = mycursor.fetchone()

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT protein_id2, reg_p2, isPSD, evidence
        FROM Partners
        WHERE protein_id1=%s AND region='yes';
        """,
        (uniprot_id,)
    )

    sql3 = mycursor.fetchall()
    # print("###################### sql3 ###########################")
    # print(sql3)
    # print("###################### sql3 end #######################")

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT protein_id2, isPSD
        FROM Partners WHERE protein_id1=%s AND evidence='LT';
        """,
        (uniprot_id,)
    )

    sql4 = mycursor.fetchall()
    # print("###################### sql4 ###########################")
    # print(sql4)
    # print("###################### sql4 end #######################")

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT protein_id2, isPSD
        FROM Partners WHERE protein_id1=%s AND evidence='HT';
        """,
        (uniprot_id,)
    )

    sql5 = mycursor.fetchall()

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT protein_id2, isPSD
        FROM Partners WHERE protein_id1=%s AND evidence='Computational';
        """,
        (uniprot_id,)
    )

    sql6 = mycursor.fetchall()

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT Alignment FROM Splice WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    sql7 = mycursor.fetchone()
    isoforms = sql7[0].split(";")
    # print("###################### sql7 ###########################")
    # for isoform in isoforms:
    #     print(isoform)
    # print("###################### sql7 end #######################")

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT posi, original, mutation, descr, in_region
        FROM Mendeley WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    diseases = []
    disease_sql = mycursor.fetchall()
    for disease in disease_sql:
        diseases.append({
            "position": disease[0],
            "original": disease[1],
            "mutation": disease[2],
            "descr": disease[3],
            "in_region": disease[4],
        })

    # print("###################### disease ###########################")
    # print(diseases)
    # print("###################### disease end #######################")

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT posi, in_region FROM Phospho WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    phospo = mycursor.fetchall()
    # print("###################### phospo ###########################")
    # print(phospo)
    # print("###################### phospo end #######################")

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT instance_ref, elm_ref, elm_type, start_pos, end_pos, in_region
        FROM ELM WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    linear_motifs_sql = mycursor.fetchall()

    print("###################### linear_motifs_sql ###########################")
    print(linear_motifs_sql)
    print("###################### linear_motifs_sql end #######################")

    linear_motifs = []
    for motif in linear_motifs_sql:
        linear_motifs.append({
            "instance_ref": motif[0],
            "elm_ref": motif[1],
            "elm_type": motif[2],
            "start_pos": motif[3],
            "end_pos": motif[4],
            "in_region": motif[5],
        })

    print("###################### linear_motifs ###########################")
    print(linear_motifs)
    print("###################### linear_motifs end #######################")

    db_data = {
        "go": sql2[1],
        "g2c": sql2[2],
        "SynGO": sql2[3],
        "SynaptomeDB": sql2[4],
        "Functions": sql2[5],
    }

    viewer_data = {
        "Transmembrane": sql2[6],
        "Transmembrane_link": sql2[7],
        "LLPS": sql2[8],
        "ELM": sql2[9],
        "Phos": sql2[10],
        "PFAM": sql2[11],
        "Coiled_coil": sql2[12],
        "Anchor": sql2[13],
        "Disordered": sql2[14],
    }

    return render(
        request,
        "entry.html",
        {
            "uniprot_id": uniprot_id,
            "db_data": db_data,
            "partners": sql3,
            "low_tp_evidence": sql4,
            "high_tp_evidence": sql5,
            "comp_evidence": sql6,
            "isoforms": isoforms,
            "diseases": diseases,
            "phospo": phospo,
            "linear_motifs": linear_motifs
        },
    )