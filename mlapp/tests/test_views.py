import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
class TestPredictionAPI:

    def test_predict_keras_model(self, client):
        url = reverse('model-prediction', args=['1'])
        data = {
            "user_id": 1,
            "input": {"text": "Regulus Black yelled 'Accio!' as he reached for the elusive horcrux."}
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert "prediction" in response.data

    def test_predict_xgboost_model(self, client):
        url = reverse('model-prediction', args=['2'])
        data = {
            "user_id": 1,
            "input": {
                "CLIENT_ID": 1,
                "SEX": 1,
                "CHILD_FLAG": 0,
                "REALTY_FLAG": 1,
                "ACCOUNTS_FLAG": 0,
                "E_MAIL_FLAG": 1,
                "DCI": 14370.2002,
                "PROFIT_FAMILY": 14370.2002,
                "UCI": 0.0000,
                "FOREIGN_PASSPORT_FLAG": 0,
                "STANDING_IN_MONTHS_LAST": 26,
                "EDUCATION": 3,
                "TRANSPORT_AMOUNT": 1
            }
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert "prediction" in response.data

@pytest.mark.django_db
class TestTrainAPI:

    def test_train_keras_model(self, client):
        url = reverse('model-train', args=['1'])
        data = {
            "texts": ["Regulus Black yelled 'Accio!' as he reached for the elusive horcrux."],
            "labels": ["CRUCIO"]
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Model trained successfully'

    def test_train_xgboost_model(self, client):
        url = reverse('model-train', args=['2'])
        data = {
            "texts": [{
                "CLIENT_ID": 1,
                "SEX": 1,
                "CHILD_FLAG": 0,
                "REALTY_FLAG": 1,
                "ACCOUNTS_FLAG": 0,
                "E_MAIL_FLAG": 1,
                "DCI": 14370.2002,
                "PROFIT_FAMILY": 14370.2002,
                "UCI": 0.0000,
                "FOREIGN_PASSPORT_FLAG": 0,
                "STANDING_IN_MONTHS_LAST": 26,
                "EDUCATION": 3,
                "TRANSPORT_AMOUNT": 1
            }],
            "labels": [0]
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Model trained successfully'

@pytest.mark.django_db
def test_list_models(client):
    url = reverse('model-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0