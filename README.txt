GuaranteedRate personapi project:

This project contains two small apps that allow ingesting of Person data in 3 different formats, sorting of the Person data in three different ways, and returning of the sorted and transformed Person data.

To install:
`git clone https://github.com/grantnicholas/guaranteedrate`
`pip install -r requirements.txt`
`python setup.py install`

To run unittests:
`cd personapi/test`
`pytest`

CLI sample usage:
`python personapi/cli/person_ingester.py -f personapi/test/testfiles/file-comma.txt -d ',' -t 1`
[Person(LastName='Mae', FirstName='Sally', Gender='F', FavoriteColor='Blue', DateOfBirth='06/01/1990'), Person(LastName='Nicholas', FirstName='Grant', Gender='M', FavoriteColor='Purple', DateOfBirth='07/06/1993')]

try python personapi/cli/person_ingester.py -h for help

Flask server sample usage:
start the flask app
`python personapi/api/run.py`

post some data using your favorite httpclient:
`curl -X POST -d @personapi/test/testfiles/test_json.json http://127.0.0.1:5000/records`

get some data using your favorite httpclient:
`curl -X GET http://127.0.0.1:5000/records/gender`
[{"LastName": "Nicholas", "FirstName": "Grant", "Gender": "M", "FavoriteColor": "Purple", "DateOfBirth": "07/06/1993"}]
