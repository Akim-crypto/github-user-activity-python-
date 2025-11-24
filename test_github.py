import pytest
from unittest.mock import patch , Mock
from user_actitivy import fetch_github_activity , format_event


def test_format_event_push():
    event = {
        "type":"PushEvent",
        "repo": {"name": "user/repo"},
        "payload":{"commits": [{} ,{}]}
    }
    assert format_event(event) == "Pushed 2 commits to user/repo"

def test_format_event_unknown():
    event = {"type":"SomeEvent","repo": {"name":"repo/name"}}
    assert format_event(event) == "SomeEvent in repo/name"

@patch('user_actitivy.requests.get')
def test_fetch_github_activity_user_not_found(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = fetch_github_activity("nonexistentuser")
    assert result == "Ошибка: пользователь не найден"


@patch('user_actitivy.requests.get')
def test_fetch_github_activity_no_events(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    result = fetch_github_activity("user")
    assert result == "Нет недавней активности"

@patch('user_actitivy.requests.get')
def test_fetch_github_activity_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"type": "PushEvent", "repo": {"name": "repo"}, "payload": {"commits": [{}]}},
        {"type": "WatchEvent", "repo": {"name": "repo2"}}
    ]
    mock_get.return_value = mock_response

    result = fetch_github_activity("user")
    assert result == [
        "Pushed 1 commits to repo",
        "Starred repo2"
    ]