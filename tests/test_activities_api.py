from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity_name in data
    assert "description" in data[expected_activity_name]
    assert "schedule" in data[expected_activity_name]
    assert "max_participants" in data[expected_activity_name]
    assert "participants" in data[expected_activity_name]


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{unknown_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_participant_success(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_email} from {activity_name}"
    }
    assert existing_email not in activities[activity_name]["participants"]


def test_unregister_email_not_signed_up_returns_404(client):
    # Arrange
    activity_name = "Programming Class"
    email_not_signed_up = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email_not_signed_up}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{unknown_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_then_unregister_transitions_state(client):
    # Arrange
    activity_name = "Debate Society"
    email = "transition.case@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json() == {"message": f"Signed up {email} for {activity_name}"}

    assert unregister_response.status_code == 200
    assert unregister_response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }

    assert email not in activities[activity_name]["participants"]
