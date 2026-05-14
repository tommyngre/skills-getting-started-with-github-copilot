import uuid


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_succeeds_for_new_email(client):
    random_email = f"test-user-{uuid.uuid4()}@example.com"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": random_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {random_email} for Chess Club"

    activities_response = client.get("/activities")
    assert random_email in activities_response.json()["Chess Club"]["participants"]


def test_signup_fails_for_duplicate_email(client):
    duplicate_email = "emma@mergington.edu"
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": duplicate_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_succeeds(client):
    email_to_remove = "daniel@mergington.edu"
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": email_to_remove},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email_to_remove} from Chess Club"

    activities_response = client.get("/activities")
    assert email_to_remove not in activities_response.json()["Chess Club"]["participants"]


def test_remove_participant_fails_when_missing(client):
    missing_email = "not-a-participant@example.com"
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": missing_email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_remove_participant_fails_for_invalid_activity(client):
    response = client.delete(
        "/activities/Nonexistent%20Activity/participants",
        params={"email": "someone@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
