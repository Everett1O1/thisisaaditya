import os

from sqlalchemy import create_engine, text

db_conn_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_conn_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_homes():
  with engine.connect() as conn:
    result = conn.execute(text("select * from homes"))
    homes = []
    for row in result.all():
      homes.append(dict(row._mapping))
    return homes


def load_home(id):
  with engine.connect() as conn:
    result = conn.execute(text("select * from homes where id = :id"),
                          {"id": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    return dict(rows[0]._mapping)


def add_apply(home_id, apply):
  with engine.connect() as conn:
    query = text(
        "INSERT INTO apply (home_id, name, phone_number, email, details, people, aadhar_link) VALUES (:home_id, :name, :phone_number, :email, :details, :people, :aadhar_link)"
    )

    conn.execute(
        query, {
            "home_id": home_id,
            "name": apply["name"],
            "phone_number": apply["phone_number"],
            "email": apply["email"],
            "details": apply["details"],
            "people": apply["people"],
            "aadhar_link": apply["aadhar_link"]
        })


def add_home(homes):
  with engine.connect() as conn:
    query = text(
        "INSERT INTO homes (house, location, rent, currency, owner_details, requirements) VALUES (:house, :location, :rent, :currency, :owner_details, :requirements)"
    )
    conn.execute(
        query, {
            "house": homes["house"],
            "location": homes["location"],
            "rent": homes["rent"],
            "currency": homes["currency"],
            "owner_details": homes["owner_details"],
            "requirements": homes["requirements"]
        })

def load_apply():
  with engine.connect() as conn:
    result = conn.execute(text("select * from apply"))
    apply = []
    for row in result.all():
      apply.append(dict(row._mapping))
    return apply