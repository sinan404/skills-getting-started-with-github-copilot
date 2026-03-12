import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_all_activities(self, client):
        """Should return all activities"""
        # Arrange
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_activities_contain_required_fields(self, client):
        """Each activity should have all required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in {activity_name}"
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup"""
    
    def test_signup_new_participant_success(self, client):
        """Should successfully sign up a new participant"""
        # Arrange
        activity_name = "Chess%20Club"
        new_email = "newemail@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert new_email in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate_participant_fails(self, client):
        """Should reject signup for already registered participant"""
        # Arrange
        activity_name = "Chess%20Club"
        duplicate_email = "michael@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_fails(self, client):
        """Should return 404 when activity doesn't exist"""
        # Arrange
        fake_activity = "Nonexistent%20Club"
        test_email = "test@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{fake_activity}/signup?email={test_email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_multiple_different_participants(self, client):
        """Should allow multiple different participants to sign up"""
        # Arrange
        activity_name = "Art%20Studio"
        emails = ["test1@mergington.edu", "test2@mergington.edu", "test3@mergington.edu"]
        
        # Act
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        # Assert
        activities_response = client.get("/activities")
        activities = activities_response.json()
        for email in emails:
            assert email in activities["Art Studio"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup"""
    
    def test_unregister_existing_participant_success(self, client):
        """Should successfully unregister an existing participant"""
        # Arrange
        activity_name = "Chess%20Club"
        email_to_remove = "michael@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email_to_remove}")
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities["Chess Club"]["participants"]
    
    def test_unregister_non_registered_participant_fails(self, client):
        """Should reject unregistering a participant who isn't signed up"""
        # Arrange
        activity_name = "Chess%20Club"
        not_registered_email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={not_registered_email}")
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client):
        """Should return 404 when activity doesn't exist"""
        # Arrange
        fake_activity = "Nonexistent%20Club"
        test_email = "test@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{fake_activity}/signup?email={test_email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_decreases_participant_count(self, client):
        """Unregistering should decrease participant count"""
        # Arrange
        activity_name = "Tennis%20Team"
        email_to_remove = "alex@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()["Tennis Team"]["participants"][:]
        initial_count = len(initial_participants)
        
        # Act
        client.delete(f"/activities/{activity_name}/signup?email={email_to_remove}")
        
        # Assert
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()["Tennis Team"]["participants"]
        assert len(updated_participants) == initial_count - 1


class TestSignupUnregisterIntegration:
    """Integration tests for signup and unregister workflows"""
    
    def test_complete_signup_and_unregister_cycle(self, client):
        """Should handle complete signup and unregister cycle"""
        # Arrange
        test_email = "integration@mergington.edu"
        activity_name = "Basketball%20Club"
        
        # Act - Sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        assert signup_response.status_code == 200
        
        # Assert - Verify signed up
        activities_after_signup = client.get("/activities").json()
        assert test_email in activities_after_signup["Basketball Club"]["participants"]
        
        # Act - Unregister
        unregister_response = client.delete(f"/activities/{activity_name}/signup?email={test_email}")
        assert unregister_response.status_code == 200
        
        # Assert - Verify unregistered
        activities_after_unregister = client.get("/activities").json()
        assert test_email not in activities_after_unregister["Basketball Club"]["participants"]
    
    def test_each_test_starts_with_fresh_state(self, client):
        """Each test should start with the original participant state"""
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
