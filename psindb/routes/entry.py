from django.shortcuts import render
from psindb.util.db import DB


def generate_transmembrane_data_list(transmembrane):
    transmembrane_value_ranges = {
        "I": [],
        "O": [],
        "M": [],
        "L": [],
        "#": [],
    }

    prev_value = transmembrane[0]
    value_from = 1
    i, value = None, None

    for i, value in enumerate(transmembrane[1:]):
        if value != prev_value:
            if prev_value not in "IOML":
                transmembrane_value_ranges["#"].append({
                    "begin": value_from,
                    "end": i + 1
                })
            else:
                transmembrane_value_ranges[prev_value].append({
                    "begin": value_from,
                    "end": i + 1
                })

            value_from = i + 2

        prev_value = value

    transmembrane_value_ranges[value].append({
        "begin": value_from,
        "end": i + 2
    })

    value_colors = {
        "I": "#ff0000",
        "O": "#0000ff",
        "M": "#ffff00",
        "L": "#ffa500",
        "#": "#808080",
    }

    value_display_ids = {
        "I": "1_1",
        "O": "1_2",
        "M": "1_3",
        "L": "1_4",
        "#": "1_5",
    }

    transmembrane_data_list = []

    for value in transmembrane_value_ranges:
        if not transmembrane_value_ranges[value]:
            continue

        transmembrane_data_list.append(
            {
                "displayType": "block",
                "displayColor": value_colors[value],
                "displayId": value_display_ids[value],
                "displayData": transmembrane_value_ranges[value]
            }
        )

    return transmembrane_data_list


def get_binary_data_list(data):
    binary_value_ranges = {
        "0": [],
        "1": [],
    }

    prev_value = data[0]
    value_from = 1
    i, value = None, None

    for i, value in enumerate(data[1:]):
        if value != prev_value:
            binary_value_ranges[prev_value].append({
                "begin": value_from,
                "end": i + 1
            })

            value_from = i + 2

        prev_value = value

    binary_value_ranges[value].append({
        "begin": value_from,
        "end": i + 2
    })

    value_colors = {
        "1": "#32a481",
        "0": "#879cac",
    }

    value_display_ids = {
        "1": "1_1",
        "0": "1_2",
    }

    binary_data_list = []

    for value in binary_value_ranges:
        if not binary_value_ranges[value]:
            continue

        binary_data_list.append(
            {
                "displayType": "block",
                "displayColor": value_colors[value],
                "displayId": value_display_ids[value],
                "displayData": binary_value_ranges[value]
            }
        )

    return binary_data_list


def generate_connectivity_data_list(connectivity):
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

    return connectivity_data_list


def create_graph_data(
        protein_id,
        transmembrane=None,
        llps=None,
        elm=None,
        phosphorylation=None,
        pfam=None,
        coiled_coil=None,
        anchor=None,
        disordered=None,
        connectivity=None,
        sequence=None,
):
    transmembrane_data_list = generate_transmembrane_data_list(transmembrane)
    llps_data_list = get_binary_data_list(llps)
    elm_data_list = get_binary_data_list(elm)
    phosphorylation_data_list = get_binary_data_list(phosphorylation)
    pfam_data_list = get_binary_data_list(pfam)
    coiled_coil_data_list = get_binary_data_list(coiled_coil)
    anchor_data_list = get_binary_data_list(anchor)
    disordered_data_list = get_binary_data_list(disordered)
    connectivity_data_list = generate_connectivity_data_list(connectivity)

    js = f"""
    $(document).ready(function(){{
    const transmembrane = "{transmembrane}";

    const boardConfigData = {{
      length: transmembrane.length,
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
    rowTitle: "Transmembrane",
    displayConfig: {transmembrane_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "LLPS",
    displayConfig: {llps_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "ELM",
    displayConfig: {elm_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "Phosphorylation",
    displayConfig: {phosphorylation_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "PFAM",
    displayConfig: {pfam_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "Coiled coil",
    displayConfig: {coiled_coil_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "Anchor",
    displayConfig: {anchor_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "Disordered",
    displayConfig: {disordered_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: "Interacting regions",
    displayConfig: {connectivity_data_list}
  }},
  {{
    trackId: "sequenceTrack",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "sequence",
    nonEmptyDisplay: true,
    rowTitle: "Sequence",
    trackData: [
      {{
        begin: 1,
        value: "{sequence}"
      }}
    ]
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


def create_partner_data(uniprot_id, partners):
    partner_data_list = []
    for partner in partners:
        partner_name = partner[0]
        partner_connectivity = partner[1]

        connectivity_data_list = generate_connectivity_data_list(
            partner_connectivity
        )

        partner_row_title = f"""
        RcsbFvLink = {{
            visibleTex: "{partner_name}",
            url: "/interactions?id1={uniprot_id}&id2={partner_name}"
        }}
        """

        partner_js = f"""
            $(document).ready(function(){{
            const partner_connectivity = "{partner_connectivity}";

            const boardConfigData = {{
              length: partner_connectivity.length,
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
            rowTitle: {partner_row_title},
            displayConfig: {connectivity_data_list}
          }}
        ];

        const elementId = "pfv-{partner_name}";
        const pfv = new RcsbFv.Create({{
                    boardConfigData,
                    rowConfigData,
                    elementId
                }});
            }});
            """

        partner_data_list.append({
            "name": partner_name,
            "connectivity_js": partner_js,
        })

    return partner_data_list


def entry(request, uniprot_id,):
    query, sql2 = DB.execute_sql(
        """
        SELECT protein_id, GO, G2C, SynGO, SynaptomeDB, Functions,
        Transmembrane, HTP, LLPS, ELM, Phos, PFAM, Coiled_coil, Anchor,
        Disordered, ELM, interacting, sequence
        FROM Protein WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    query, sql3 = DB.execute_sql(
        """
        SELECT protein_id2, reg_p2, isPSD, evidence
        FROM Partners
        WHERE protein_id1=%s AND region='yes';
        """,
        (uniprot_id,)
    )

    query, all_partners_list = DB.execute_sql(
        """
        SELECT protein_id2, evidence, isPSD 
        FROM Partners
        WHERE protein_id1=%s 
        ORDER BY evidence DESC;
        """,
        (uniprot_id,)
    )

    partners_list = []

    for partner in all_partners_list:
        name = partner[0]
        highest_evidence = partner[1]
        entry_link = None
        interaction_link = f"/interactions?id1={uniprot_id}&id2={name}"
        is_psd = True if partner[2] == "PSD" else False

        if is_psd:
            entry_link = f"/entry/{name}"


        partners_list.append({
            "name": name,
            "entry_link": entry_link,
            "interaction_link": interaction_link,
            "highest_evidence": highest_evidence,
            "is_psd": is_psd,
        })

    query, sql7 = DB.execute_sql(
        """
        SELECT Alignment FROM Splice WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    try:
        isoforms = sql7[0][0].split(";")
    except IndexError:
        isoforms = None

    query, disease_sql = DB.execute_sql(
        """
        SELECT posi, original, mutation, descr, in_region
        FROM Mendeley WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    diseases = []

    for disease in disease_sql:
        diseases.append({
            "position": disease[0],
            "original": disease[1],
            "mutation": disease[2],
            "descr": disease[3],
            "in_region": disease[4],
        })

    query, phospo = DB.execute_sql(
        """
        SELECT posi, in_region FROM Phospho WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    query, linear_motifs_sql = DB.execute_sql(
        """
        SELECT instance_ref, elm_ref, elm_type, start_pos, end_pos, in_region
        FROM ELM WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

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

    query, fp_mol_func_sql = DB.execute_sql(
        """
        SELECT Fingerprint.ontology_type, Fingerprint.ontology_number,
               Fingerprint.ontology_total1, Fingerprint.ontology_total2,
               Fingerprint.term_id, Ontology.des, Fingerprint.ontology_level
        FROM Fingerprint
            INNER JOIN Ontology ON Fingerprint.protein_id=%s AND
                    Ontology.term_id=Fingerprint.term_id AND
                    NOT Fingerprint.ontology_level=0 AND
                    NOT Fingerprint.ontology_level=1 AND
                    Fingerprint.ontology_type='molecular function'
        ORDER BY Fingerprint.ontology_number DESC
        LIMIT 10;
        """,
        (uniprot_id,)
    )

    fp_mol_func = []
    for fp in fp_mol_func_sql:
        fp_mol_func.append({
            "ontology_type": fp[0],
            "ontology_number": fp[1],
            "ontology_total1": fp[2],
            "ontology_total2": fp[3],
            "term_id": fp[4],
            "des": fp[5],
            "ontology_level": fp[6]
        })

    query, fp_biol_proc_sql = DB.execute_sql(
        """
        SELECT Fingerprint.ontology_type, Fingerprint.ontology_number,
               Fingerprint.ontology_total1, Fingerprint.ontology_total2,
               Fingerprint.term_id, Ontology.des, Fingerprint.ontology_level
        FROM Fingerprint
            INNER JOIN Ontology ON Fingerprint.protein_id=%s AND
                    Ontology.term_id=Fingerprint.term_id AND
                    NOT Fingerprint.ontology_level=0 AND
                    NOT Fingerprint.ontology_level=1 AND
                    Fingerprint.ontology_type='biological process'
        ORDER BY Fingerprint.ontology_number DESC
        LIMIT 10;
        """,
        (uniprot_id,)
    )

    fp_biol_proc = []
    for fp in fp_biol_proc_sql:
        fp_biol_proc.append({
            "ontology_type": fp[0],
            "ontology_number": fp[1],
            "ontology_total1": fp[2],
            "ontology_total2": fp[3],
            "term_id": fp[4],
            "des": fp[5],
            "ontology_level": fp[6]
        })

    query, fp_disease_sql = DB.execute_sql(
        """
        SELECT Fingerprint.ontology_type, Fingerprint.ontology_number,
               Fingerprint.ontology_total1, Fingerprint.ontology_total2,
               Fingerprint. term_id, Ontology.des, Fingerprint.ontology_level
        FROM Fingerprint
            INNER JOIN Ontology ON Fingerprint.protein_id=%s AND
                                   Ontology.term_id=Fingerprint.term_id AND
                                   NOT Fingerprint.ontology_level=0 AND
                                   NOT Fingerprint.ontology_level=1 AND
                                   Fingerprint.ontology_type='disease'
        ORDER BY Fingerprint.ontology_number DESC
        LIMIT 10;
                """,
        (uniprot_id,)
    )

    fp_disease = []
    for fp in fp_disease_sql:
        fp_disease.append({
            "ontology_type": fp[0],
            "ontology_number": fp[1],
            "ontology_total1": fp[2],
            "ontology_total2": fp[3],
            "term_id": fp[4],
            "des": fp[5],
            "ontology_level": fp[6]
        })

    db_data = {
        "go": sql2[0][1],
        "g2c": sql2[0][2],
        "SynGO": sql2[0][3],
        "SynaptomeDB": sql2[0][4],
        "Functions": sql2[0][5],
    }

    features_graph_js = create_graph_data(
        uniprot_id,
        transmembrane=sql2[0][6],
        llps=sql2[0][8],
        elm=sql2[0][9],
        phosphorylation=sql2[0][10],
        pfam=sql2[0][11],
        coiled_coil=sql2[0][12],
        anchor=sql2[0][13],
        disordered=sql2[0][14],
        connectivity=sql2[0][16],
        sequence=sql2[0][17],
    )

    partner_data = create_partner_data(uniprot_id, sql3)

    return render(
        request,
        "entry.html",
        {
            "uniprot_id": uniprot_id,
            "db_data": db_data,
            "partners": partner_data,
            "partners_list": partners_list,
            "isoforms": isoforms,
            "diseases": diseases,
            "linear_motifs": linear_motifs,
            "fp_mol_func": fp_mol_func,
            "fp_biol_proc": fp_biol_proc,
            "fp_disease": fp_disease,
            "features_graph_js": features_graph_js,
        },
    )