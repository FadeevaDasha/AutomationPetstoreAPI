from http.client import responses
from urllib.error import HTTPError
from schemas.notes_schemas import NOTES_SCHEMA

import allure
import pytest
import requests
import jsonschema


@allure.feature('Test Create Notes')
@allure.story('Positive: create notes with custom data')
def test_create_notes_with_custom_data(api_client):
    notes_data = {
        "title": "Practice WebApp UI 1.0",
        "description": "Finish the development of the UI Automation Practice WebApp 1.0",
        "category": "Work"
    }

    response = api_client.create_notes(notes_data)
    jsonschema.validate(response, NOTES_SCHEMA)
    note_data = response['data']

    assert note_data['id'] != ""
    assert response['success'] == True
    assert response['status'] == 200
    assert response['message'] == "Note successfully created"
    assert note_data['completed'] == False
    assert note_data['title'] == notes_data['title']
    assert note_data['description'] == notes_data['description']
    assert note_data['category'] == notes_data['category']