from django.shortcuts import render
from django.http import HttpResponse

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="daniel",
    password="password",
    database="PSDInteractome_v0_09"
)


def index(request):
    return HttpResponse("Hello, world. You're at the psindb index.")


def protein(request, protein_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM Protein WHERE protein_id = %s",
            (protein_id,)
        )

        myresult = mycursor.fetchall()

        if not myresult:

        for x in myresult:
            print(x)

        return render(
            request,
            "protein.html",
            {
                "protein_id": protein_id,
            },
        )
