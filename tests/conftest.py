import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Tennis Team": {
            "description": "Competitive tennis training and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Basketball practice and intramural games",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["james@mergington.edu", "rachel@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["jessica@mergington.edu"]
        },
        "Music Band": {
            "description": "Instrumental music performance and composition",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["marcus@mergington.edu", "luna@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on science experiments and research projects",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 24,
            "participants": ["david@mergington.edu"]
        },
        "Debate Team": {
            "description": "Prepare for and compete in academic debate tournaments",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["sophia@mergington.edu", "noah@mergington.edu"]
        }
    }
    
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    activities.clear()
    activities.update(original_activities)
