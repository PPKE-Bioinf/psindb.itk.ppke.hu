from django.shortcuts import render
from psindb.util.db import DB


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

    # print("###################### sql3 ###########################")
    # print(sql3)
    # print("###################### sql3 end #######################")

    query, sql4 = DB.execute_sql(
        """
        SELECT protein_id2, isPSD
        FROM Partners WHERE protein_id1=%s AND evidence='LT';
        """,
        (uniprot_id,)
    )

    query, sql5 = DB.execute_sql(
        """
        SELECT protein_id2, isPSD
        FROM Partners WHERE protein_id1=%s AND evidence='HT';
        """,
        (uniprot_id,)
    )


    query, sql6 = DB.execute_sql(
        """
        SELECT protein_id2, isPSD
        FROM Partners WHERE protein_id1=%s AND evidence='Computational';
        """,
        (uniprot_id,)
    )

    query, sql7 = DB.execute_sql(
        """
        SELECT Alignment FROM Splice WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    # print("###################### sql7 ###########################")
    # print(sql7[0][0])
    # print("###################### sql7 end #######################")

    isoforms = sql7[0][0].split(";")
    # print("###################### sql7 ###########################")
    # for isoform in isoforms:
    #     print(isoform)
    # print("###################### sql7 end #######################")

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

    # print("###################### disease ###########################")
    # print(diseases)
    # print("###################### disease end #######################")

    query, phospo = DB.execute_sql(
        """
        SELECT posi, in_region FROM Phospho WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    # print("###################### phospo ###########################")
    # print(phospo)
    # print("###################### phospo end #######################")

    query, linear_motifs_sql = DB.execute_sql(
        """
        SELECT instance_ref, elm_ref, elm_type, start_pos, end_pos, in_region
        FROM ELM WHERE protein_id=%s;
        """,
        (uniprot_id,)
    )

    # print("###################### linear_motifs_sql ###########################")
    # print(linear_motifs_sql)
    # print("###################### linear_motifs_sql end #######################")

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

    # print("###################### linear_motifs ###########################")
    # print(linear_motifs)
    # print("###################### linear_motifs end #######################")

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

    print(
        "###################### fp_mol_func ###########################")
    print(fp_mol_func)
    print(
        "###################### fp_mol_func end #######################")

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

    # print(
    #     "###################### fp_mol_func ###########################")
    # print(fp_biol_proc)
    # print(
    #     "###################### fp_mol_func end #######################")

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

    print("###################### sql2 ###########################")
    print(sql2)
    print("###################### sql2 end #######################")


    db_data = {
        "go": sql2[0][1],
        "g2c": sql2[0][2],
        "SynGO": sql2[0][3],
        "SynaptomeDB": sql2[0][4],
        "Functions": sql2[0][5],
    }

    viewer_data = {
        "Transmembrane": sql2[0][6],
        "Transmembrane_link": sql2[0][7],
        "LLPS": sql2[0][8],
        "ELM": sql2[0][9],
        "Phos": sql2[0][10],
        "PFAM": sql2[0][11],
        "Coiled_coil": sql2[0][12],
        "Anchor": sql2[0][13],
        "Disordered": sql2[0][14],
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
            "linear_motifs": linear_motifs,
            "fp_mol_func": fp_mol_func,
            "fp_biol_proc": fp_biol_proc,
            "fp_disease": fp_disease,
        },
    )