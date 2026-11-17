def test_root_redirects_to_static_index(client):
    # Arrange
    expected_page_title = "Mergington High School"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert expected_page_title in response.text


def test_get_activities_returns_activity_and_participants(client):
    # Arrange
    expected_participant = "existing@mergington.edu"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["Chess Club"]["participants"] == [expected_participant]
    assert response.json()["Chess Club"]["max_participants"] == 12


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "existing@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity = "Unknown Club"
    email = "new@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "existing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_rejects_participant_not_signed_up(client):
    # Arrange
    activity = "Chess Club"
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity = "Unknown Club"
    email = "existing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
