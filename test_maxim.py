import requests
import logging
import pytest
from models import ObjectData, SearchResult, Departments, Objects

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

logging.basicConfig(level=logging.INFO)


def log_request_response(response):
    logging.info(f"Request URL: {response.url}")
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Response: {response.text}")


def test_get_objects():
    response = requests.get(f"{BASE_URL}/objects")
    log_request_response(response)
    assert response.status_code == 200
    objects = Objects(**response.json())
    assert objects.total == len(objects.objectIDs)


@pytest.mark.parametrize("object_id", [436121, 437853])  # Примеры валидных ID
def test_get_object_by_id(object_id):
    response = requests.get(f"{BASE_URL}/objects/{object_id}")
    log_request_response(response)
    assert response.status_code == 200
    data = response.json()
    validated = ObjectData(**data)
    assert validated.objectID == object_id


def test_get_object_by_invalid_id():
    invalid_id = 999999999  # Очень большой ID
    response = requests.get(f"{BASE_URL}/objects/{invalid_id}")
    log_request_response(response)
    assert response.status_code == 404
    data = response.json()
    assert data.get("objectID", 0) == 0


def test_search_objects_by_keyword():
    query = "Sunflowers"
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    log_request_response(response)
    assert response.status_code == 200
    result = SearchResult(**response.json())
    assert result.total > 0
    assert isinstance(result.objectIDs, list)


@pytest.mark.parametrize("query", ["Rembrandt", "Van Gogh", "Picasso"])
def test_multiple_queries(query):
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    log_request_response(response)
    assert response.status_code == 200
    result = SearchResult(**response.json())
    assert result.total > 0


def test_get_all_departments():
    response = requests.get(f"{BASE_URL}/departments")
    log_request_response(response)
    assert response.status_code == 200
    departments = Departments(**response.json())

    assert len(departments.departments) > 0
    assert departments.departments[0].departmentId > 0
