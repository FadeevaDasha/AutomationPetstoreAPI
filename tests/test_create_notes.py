from http.client import responses
from urllib.error import HTTPError

import allure
import pytest
import requests


@allure.feature('Test Create Notes')
@allure.story('Positive: create notes with custom data')
def test_create_booking_with_custom_data(api_client):
    notes_data = {
        "title": "Practice WebApp UI 1.0",
        "description": "Finish the development of the UI Automation Practice WebApp 1.0",
        "category": "Work"
    }

    response = api_client.create_notes(notes_data)
