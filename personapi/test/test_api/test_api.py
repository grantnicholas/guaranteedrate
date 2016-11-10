from personapi.models.models import Person
import datetime
from simplejson import dumps, loads
from personapi.api.run import jdumps


def test_jdumps_datetime_correctly():
    obj = {
        "adate": datetime.datetime(year=1900, month=2, day=1, hour=0, minute=0)
    }

    output = jdumps(obj)

    assert '{"adate": "02/01/1900"}' == output


def test_post_good(test_client, db_client):
    assert db_client.get_records() == []
    posted_data = dumps({
        "line": "Nicholas,Grant,M,Purple,07-06-1993",
        "delimiter": ","
    })
    rv = test_client.post('/records', data=posted_data)

    assert rv.data == ""
    assert rv.status_code == 200
    assert db_client.get_records() == [
    Person(FirstName="Grant", LastName="Nicholas", Gender="M",
           FavoriteColor="Purple", DateOfBirth=datetime.datetime(year=1993, month=7, day=6, hour=0, minute=0))
    ]


def test_post_bad(test_client, db_client):
    assert db_client.get_records() == []
    posted_data = dumps({
        "line": "Nicholas,Grant,Purple,07-06-1993",
        "delimiter": ","
    })
    rv = test_client.post('/records', data=posted_data)

    assert rv.data == "Error: unprocessible entity"
    assert rv.status_code == 422
    assert db_client.get_records() == []


def test_get_records_gender_norecords(test_client, db_client):
    assert db_client.get_records() == []
    rv = test_client.get('/records/gender')

    assert loads(rv.data) == []
    assert rv.status_code == 200


def test_get_records_gender_onerecord(test_client, db_client):
    assert db_client.get_records() == []
    posted_data = dumps({
        "line": "Nicholas,Grant,M,Purple,07-06-1993",
        "delimiter": ","
    })
    response = test_client.post('/records', data=posted_data)
    assert response.status_code == 200

    rv = test_client.get('/records/gender')

    assert loads(rv.data) == [{
        "LastName": "Nicholas",
        "FirstName": "Grant",
        "Gender": "M",
        "FavoriteColor": "Purple",
        "DateOfBirth": "07/06/1993"
    }]
    assert rv.status_code == 200


def test_get_records_gender_tworecords(test_client, db_client):
    assert db_client.get_records() == []
    posted_data = dumps({
        "line": "Nicholas,Grant,M,Purple,07-06-1993",
        "delimiter": ","
    })
    response = test_client.post('/records', data=posted_data)
    assert response.status_code == 200

    posted_data = dumps({
        "line": "Mae|Sally|F|Blue|06-01-1990",
        "delimiter": "|"
    })
    response = test_client.post('/records', data=posted_data)
    assert response.status_code == 200

    response = test_client.get('/records/gender')

    assert loads(response.data) == [
        {
            "LastName": "Mae",
            "FirstName": "Sally",
            "Gender": "F",
            "FavoriteColor": "Blue",
            "DateOfBirth": "06/01/1990"
        },
        {
            "LastName": "Nicholas",
            "FirstName": "Grant",
            "Gender": "M",
            "FavoriteColor": "Purple",
            "DateOfBirth": "07/06/1993"
        }
    ]
    assert response.status_code == 200

