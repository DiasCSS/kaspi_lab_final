import sys
from decimal import Decimal
from uuid import uuid4

from account.account import Account
from database.database import AccountDatabase
from database.implementations.postgres_db import AccountDatabasePostgres
import os

from database.implementations.ram import AccountDatabaseRAM


def create_account(database: AccountDatabase, currency: str, balance: Decimal) -> None:
    account = Account(
        id_=uuid4(),
        currency=currency,
        balance=balance,
    )
    database.save(account)


if __name__ == "__main__":
    dbname:str = os.environ.get("pg_dbname", "")
    if dbname == "":
        database = AccountDatabaseRAM()
        print("Using RAM")
    else:
        port:int = 5432
        user:str = os.environ.get("postgress")
        password:str = os.environ.get("Passw0rd")
        host:str = "localhost"
        connection_str = f"dbname={dbname} port={port} user={user} password={password} host={host}"
        database = AccountDatabasePostgres(connection=connection_str)
        print("Connected!")
    currency = input("Enter Currency: ")
    balance = Decimal(input("Enter balance: "))
    create_account(database=database, balance=balance, currency=currency)
    sys.exit(0)
