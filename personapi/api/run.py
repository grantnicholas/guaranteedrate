from flask import Flask, request
from personapi.lib.person_transformer import TransformOptions, transform_persons
from personapi.lib.file_ingester import ingest_string, df_to_persons
from personapi.db.data_repository import DataFetcher
from personapi.models.models import Person
from simplejson import dumps
import datetime


app = Flask(__name__)
app.db_client = DataFetcher()

def jdumps(data):
    enco = lambda obj: (
        obj.strftime("%m/%d/%Y")
        if isinstance(obj, datetime.datetime)
           or isinstance(obj, datetime.date)
        else None
    )
    return dumps(data, default=enco)


@app.route("/records", methods=["POST"])
def post_records():
    try:
        jobj = request.get_json(force=True)
        line = jobj["line"]
        delimiter = jobj["delimiter"]
        df = ingest_string(line, delimiter,header=False)
        persons = df_to_persons(df, header=False)
        app.db_client.insert_records(persons)
    except:
        return "Error: unprocessible entity", 422

    return "", 200


@app.route("/records/gender")
def records_gender():
    data = transform_persons(app.db_client.get_records(), TransformOptions.GenderThenLastNameAsc)
    return jdumps(data), 200


@app.route("/records/birthdate")
def records_birthdate():
    data = transform_persons(app.db_client.get_records(), TransformOptions.BirthDateAsc)
    return jdumps(data), 200


@app.route("/records/name")
def records_name():
    data = transform_persons(app.db_client.get_records(), TransformOptions.LastNameDesc)
    return jdumps(data), 200


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
