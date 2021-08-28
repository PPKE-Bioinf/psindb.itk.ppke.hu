from django.shortcuts import render
from psindb.util.db import DB
import re


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


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
        "0": "#a9d1d5",
        "1": "#32a481",
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


def get_alignment_data_list(data):
    binary_value_ranges = {
        "0": [],
        "1": [],
    }

    prev_value = "0" if data[0] == "-" else "1"
    value_from = 1
    i, value = None, None

    for i, value in enumerate(data[1:]):
        if value == "-":
            value = "0"
        else:
            value = "1"

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
        "0": "#28C7FF",
        "1": "#0080FF",
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
        "-": [],
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
        # if value == "-":
        #     value = "1"
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
        "-": "#28C7FF",
        "1": "#4a2226",
        "2": "#705080",
        "3": "#32a481",
        "4": "#879cac",
        "5": "#a9d1d5",
    }

    value_display_ids = {
        "-": "1_0",
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
        htp=None,
        llps=None,
        elm=None,
        phosphorylation=None,
        pfam=None,
        coiled_coil=None,
        anchor=None,
        disordered=None,
        connectivity=None,
        phasepro=None,
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

    transmembrane_row_title = '"Transmembrane"'

    if htp != "-":
        transmembrane_row_title = f"""
            RcsbFvLink = {{
                visibleTex: "Transmembrane",
                url: "http://htp.enzim.hu/?_=/viewer/{htp}",
                isThirdParty: true
            }}
            """

    llps_row_title = '"Phase separation"'

    if phasepro != "-":
        llps_row_title = f"""
        RcsbFvLink = {{
            visibleTex: "Phase separation",
            url: "https://phasepro.elte.hu/entry/{phasepro}",
            isThirdParty: true
        }}
        """

    pfam_row_title = f"""
    RcsbFvLink = {{
        visibleTex: "PFAM",
        url: "http://pfam.xfam.org/protein/{protein_id}",
        isThirdParty: true
    }}
    """

    js = f"""
    $(document).ready(function(){{
    const transmembrane = "{transmembrane}";

    const boardConfigData = {{
      length: transmembrane.length,
      trackWidth: 920,
      includeAxis: true,
      disableMenu: true,
      hideRowGlow: true,
      hideTrackFrameGlow: true,
      highlightHoverElement: false,
      highlightHoverPosition: false,
      includeTooltip: false
    }};

    const rowConfigData = [
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: {transmembrane_row_title},
    displayConfig: {transmembrane_data_list}
  }},
  {{
    trackId: "compositeSequence",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "composite",
    rowTitle: {llps_row_title},
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
    rowTitle: {pfam_row_title},
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

const elementId = "pfv-{protein_id}-features";
const pfv = new RcsbFv.Create({{
            boardConfigData,
            rowConfigData,
            elementId
        }});
    }});
    """

    return js


def create_isoform_data(
        canonical_name, canonical_seq, connectivity, isoforms
):
    canonical_seq_connectivity = generate_connectivity_data_list(connectivity)

    isoform_tracks = ""

    for i, isoform in enumerate(isoforms):
        isoform_name = isoform[0]
        isoform_seq = isoform[1]

        isoform_seq_data_list = get_alignment_data_list(isoform_seq)

        isoform_row_title = f"""
        RcsbFvLink = {{
            visibleTex: "Isoform [{isoform_name}] sequence",
            url: "https://www.uniprot.org/uniprot/{isoform_name}",
            isThirdParty: true
        }}
        """

        isoform_tracks += f"""
        ,{{
        trackId: "compositeSequence_mini_{isoform_name}",
        trackHeight: 20,
        trackColor: "#F9F9F9",
        displayType: "composite",
        rowTitle: "Isoform [{isoform_name}] alignment",
        displayConfig: {isoform_seq_data_list}
        }},
        {{
            trackId: "sequenceTrack_{isoform_name}",
            trackHeight: 20,
            trackColor: "#F9F9F9",
            displayType: "sequence",
            nonEmptyDisplay: true,
            rowTitle: {isoform_row_title},
            trackData: [
                {{
                    begin: 1,
                    value: "{isoform_seq}"
                }}
            ]
        }}"""


    js = f"""
    $(document).ready(function(){{
    const connectivity = "{connectivity}";

    const boardConfigData = {{
      length: connectivity.length,
      trackWidth: 900,
      rowTitleWidth: 207,
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
    displayConfig: {canonical_seq_connectivity}
  }},
  {{
    trackId: "sequenceTrack",
    trackHeight: 20,
    trackColor: "#F9F9F9",
    displayType: "sequence",
    nonEmptyDisplay: true,
    rowTitle: "Canonical [{canonical_name}]",
    trackData: [
        {{
            begin: 1,
            value: "{canonical_seq}"
        }}
    ]
  }}
  {isoform_tracks}
];

const elementId = "pfv-isoform";
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
        partner_connectivity = partner[2]
        partner_connectivity2 = partner[1]

        connectivity_data_list = generate_connectivity_data_list(
            partner_connectivity
        )

        connectivity_data_list2 = generate_connectivity_data_list(
            partner_connectivity2
        )

        display_length = len(partner_connectivity)

        if len(partner_connectivity2) > len(partner_connectivity):
            display_length = len(partner_connectivity2)

        partner_row_title = f"""
        RcsbFvLink = {{
            visibleTex: "{partner_name}",
            url: "/interactions?id1={uniprot_id}&id2={partner_name}"
        }}
        """

        partner_js = f"""
            $(document).ready(function(){{

            const boardConfigData = {{
              length: {display_length},
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
            rowTitle: "{uniprot_id}",
            displayConfig: {connectivity_data_list2}
          }},
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
        topology, HTP, LLPS, ELM, phosphorylation, PFAM, coiledcoil, Anchor,
        Disordered, ELM, interacting, sequence, phasepro
        FROM Protein WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    query, sql3 = DB.execute_sql(
        """
        SELECT protein_id2, reg_p1, reg_p2 FROM Partners 
        WHERE protein_id1=%s AND ispsd='PSD' AND region='yes';
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

        if highest_evidence == "LT":
            highest_evidence = "Low throughput"
        elif highest_evidence == "HT":
            highest_evidence = "High throughput"

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
        isoforms_sql = sql7[0][0].split(";")
        canonical_name = isoforms_sql[0]
        connectivity_data = isoforms_sql[1]
        canonical_seq = isoforms_sql[2]
        isoforms = []

        for pair in chunks(isoforms_sql[3:], 2):
            isoform_name = pair[0]
            isoform_full_seq = pair[1]
            isoforms.append([isoform_name, isoform_full_seq])

        isoforms_data = {
            "connectivity": create_isoform_data(
                canonical_name,
                canonical_seq,
                connectivity_data,
                isoforms

            )
        }

    except IndexError:
        isoforms_data = None

    query, disease_sql = DB.execute_sql(
        """
        SELECT posi, original, mutation, descr, in_region, mim, partner
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
            "mim": disease[5],
            "partner": disease[6].split(";"),
        })

    query, linear_motifs_sql = DB.execute_sql(
        """
        SELECT instance_ref, elm_ref, elm_type, 
        start_pos, end_pos, in_region, partner
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
            "partner": motif[6].split(";"),
        })

    query, fp_mol_func_sql = DB.execute_sql(
        """
        SELECT Fingerprint.term_id, Ontology.descr, 
        100*Fingerprint.ontology_number/Fingerprint.ontology_total1, 
        Fingerprint.ontology_level, Fingerprint.main
        FROM Fingerprint INNER JOIN Ontology ON 
        Fingerprint.protein_id=%s AND 
        Ontology.term_id=Fingerprint.term_id AND
        NOT Fingerprint.ontology_level=0 AND 
        NOT Fingerprint.ontology_level=1 AND 
        Fingerprint.ontology_type='molecular function' AND 
        Fingerprint.ontology_level>3 AND 
        Fingerprint.ontology_number>1 
        ORDER BY cast(Fingerprint.ontology_number as SIGNED)
        DESC;
        """,
        (uniprot_id,)
    )

    fp_mol_func = []
    for fp in fp_mol_func_sql:
        fp_mol_func.append({
            "term_id": fp[0],
            "des": fp[1],
            "ontology_number": fp[2],
            "ontology_level": fp[3],
            "main": fp[4],
        })

    query, fp_biol_proc_sql = DB.execute_sql(
        """
        SELECT Fingerprint.term_id, Ontology.descr, 
        100*Fingerprint.ontology_number/Fingerprint.ontology_total1,
        Fingerprint.ontology_level, Fingerprint.main
        FROM Fingerprint INNER JOIN Ontology ON 
        Fingerprint.protein_id=%s AND 
        Ontology.term_id=Fingerprint.term_id AND 
        NOT Fingerprint.ontology_level=0 AND 
        NOT Fingerprint.ontology_level=1 AND 
        Fingerprint.ontology_type='biological process' AND 
        Fingerprint.ontology_level>3 AND 
        Fingerprint.ontology_number>1 
        ORDER BY cast(Fingerprint.ontology_number as SIGNED) 
        DESC;
        """,
        (uniprot_id,)
    )

    fp_biol_proc = []
    for fp in fp_biol_proc_sql:
        fp_biol_proc.append({
            "term_id": fp[0],
            "des": fp[1],
            "ontology_number": fp[2],
            "ontology_level": fp[3],
            "main": fp[4],
        })

    query, fp_disease_sql = DB.execute_sql(
        """
        SELECT Fingerprint.term_id, Ontology.descr,
        100*Fingerprint.ontology_number/Fingerprint.ontology_total1,
        Fingerprint.ontology_level, Fingerprint.main
        FROM Fingerprint INNER JOIN Ontology 
        ON Fingerprint.protein_id=%s AND 
        Ontology.term_id=Fingerprint.term_id AND 
        NOT Fingerprint.ontology_level=0 AND 
        NOT Fingerprint.ontology_level=1 AND 
        Fingerprint.ontology_type='disease' AND 
        Fingerprint.ontology_level>2 AND 
        Fingerprint.ontology_number>1 
        ORDER BY cast(Fingerprint.ontology_number as SIGNED)
        DESC;
                """,
        (uniprot_id,)
    )

    fp_disease = []
    for fp in fp_disease_sql:
        fp_disease.append({
            "term_id": fp[0],
            "des": fp[1],
            "ontology_number": fp[2],
            "ontology_level": fp[3],
            "main": fp[4],
        })

    functions_desc = sql2[0][5]
    functions_desc = re.sub(
        r"(PubMed):(\d*)",
        r'<a href="https://pubmed.ncbi.nlm.nih.gov/\2" target="_blank" rel="noopener noreferrer">\1</a>',
        functions_desc
    )

    functions_desc += f' <a href="https://www.uniprot.org/uniprot/{uniprot_id}" target="_blank" rel="noopener noreferrer">[View more on UniProt]</a>'

    db_data = {
        "go": sql2[0][1],
        "g2c": sql2[0][2],
        "SynGO": sql2[0][3],
        "SynaptomeDB": sql2[0][4],
        "Functions": functions_desc,
    }

    features_graph_js = create_graph_data(
        uniprot_id,
        transmembrane=sql2[0][6],
        htp=sql2[0][7],
        llps=sql2[0][8],
        elm=sql2[0][9],
        phosphorylation=sql2[0][10],
        pfam=sql2[0][11],
        coiled_coil=sql2[0][12],
        anchor=sql2[0][13],
        disordered=sql2[0][14],
        connectivity=sql2[0][16],
        sequence=sql2[0][17],
        phasepro=sql2[0][18],
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
            "isoforms": isoforms_data,
            "diseases": diseases,
            "linear_motifs": linear_motifs,
            "fp_mol_func": fp_mol_func,
            "fp_biol_proc": fp_biol_proc,
            "fp_disease": fp_disease,
            "features_graph_js": features_graph_js,
        },
    )