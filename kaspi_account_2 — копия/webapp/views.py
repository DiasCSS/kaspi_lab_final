import json
from decimal import Decimal
from typing import Any
from uuid import uuid4
import pandas as pd

from django.http import HttpResponse, HttpRequest
import os

from django.shortcuts import render

from account.account import Account
from database.database import ObjectNotFound
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM
from webapp.forms import PostForm

'''dbname: str = os.environ.get("pg_dbname", "")
if dbname == "":
    database = AccountDatabaseRAM()
    print("Using RAM")
else:
    port: int = 5432
    user: str = os.environ.get("postgres")
    password: str = os.environ.get("Passw0rd")
    host: str = "localhost"
    connection_str = f"dbname={dbname} port={port} user={user} password={password} host={host}"
    database = AccountDatabasePostgres(connection=connection_str)'''

connection_str = "dbname=postgres port=5432 user=postgres password=Passw0rd host=localhost"
database = AccountDatabasePostgres(connection=connection_str)



def accounts_list(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    return render(request, "index.html", context={"accounts": accounts})


def myaccs(request: HttpRequest) -> HttpResponse:
    df = pd.read_csv(r"C:\Users\dias8\PycharmProjects\kaspi_account_2\accountbase.csv")
    print(df)
    #df = df.to_html()
    #df.sort_values(by='balance').style.apply(format_color_groups, axis=None)
    return render(request, "index1.html", context={"df": df})


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="""
    <html>
        <head>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <title>Главная</title>
        </head>
        <body>
           <h1>Привет мир!</h1> 
           <h3>Чтобы посмотреть Аккаунты нажмите аккаунты <a href="/accounts/"><button type="button" class="btn btn-primary"><span class="glyphicon glyphicon-pencil" aria-hidden="true"
                                                                ></span> Аккаунты</button></a></h3>
        </body>
    </html>
    """)


def accounts(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    if request.method == "GET":
        json_obj = [account.to_json() for account in accounts]
        return HttpResponse(content=json.dumps(json_obj))

    if request.method == "POST":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            account.id_ = uuid4()
            try:
                database.get_object(account.id_)
                return HttpResponse(content=f"Error: object already exists, use PUT to update", status=400)
            except ObjectNotFound:
                database.save(account)
                return HttpResponse(content=account.to_json_str(), status=201)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)

    if request.method == "PUT":
        try:
            account = Account.from_json_str(request.body.decode("utf8"))
            database.get_object(account.id_)
            database.save(account)
            return HttpResponse(content="OK", status=200)
        except Exception as e:
            return HttpResponse(content=f"Error: {e}", status=400)


def saveacc(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    return render(request, "saveacc.html", context={"accounts": accounts})


def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        print(form.data['currency'])
        account = Account(
            id_=uuid4(),
            currency=f'{form.data["currency"]}',
            balance=Decimal(0),
        )
        print(account)
        database.save(account)
        print(database.get_objects())
    else:
        form = PostForm()
    return render(request, "saveacc.html",{"form": form})


def addbalance(request: HttpRequest,slug) -> HttpResponse:
    print(slug)
    temp = database.get_object_transaction(slug)
    print(temp)
    print(type(temp))
    return render(request, "transaction.html", {"temp": temp})