import falcon
from falcon import testing
import pytest
import json
from hivery.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_list_company(client):
    result = {
                "employees": [
                    "Mabel Steele",
                    "Beatriz Holder",
                    "Mcleod Mcbride",
                    "Knapp Moss",
                    "Bass Hansen",
                    "Janine Hill",
                    "Alisha Blackburn"
                ]
            }       

    response = client.simulate_get('/v1/company/TECHTRIX')
    result_doc =json.loads(response.content)

    assert result_doc == result
    assert response.status == falcon.HTTP_OK

def test_company_fail(client):
    #result = { "error": "Sorry.It looks like there are no employees listed for the particular company"
    #            }
    response = client.simulate_get('/v1/company/ABC')
    #result_doc = json.loads(response.content)

    #assert result_doc == result
    assert response.status == falcon.HTTP_404

def test_people_detail(client):
    result = {
            "age": "26",
            "fruits": [
                "strawberry"
            ],
            "username": "Cote Booth",
            "vegetables": [
                "beetroot",
                "carrot",
                "cucumber"
            ]
        }
    response = client.simulate_get('/v1/people/Cote%20Booth')
    result_doc = json.loads(response.content)
    assert result_doc == result
    assert response.status == falcon.HTTP_OK

def test_people_detail_fail(client):
    response = client.simulate_get('/v1/people/abc')
    assert response.status == falcon.HTTP_404

def test_people_friends(client):
    result = {"details": [
        {
            "address": "394 Loring Avenue, Salvo, Maryland, 9396",
            "age": "26",
            "name": "Cote Booth",
            "phone": "+1 (842) 598-3525"
        },
        {
            "address": "872 Nassau Street, Harviell, Utah, 9532",
            "age": "22",
            "name": "Rena Vincent",
            "phone": "+1 (978) 575-2298"
        }
    ],
    "mutual_friends": [
        "Decker Mckenzie"
    ]
    }
    response = client.simulate_get('/v1/people/Cote%20Booth,Rena%20Vincent')
    result_doc = json.loads(response.content)
    assert result_doc == result
    assert response.status == falcon.HTTP_OK

def test_people_friends_fail(client):
    response = client.simulate_get('/v1/people/abc,bcd')
    assert response.status == falcon.HTTP_404
