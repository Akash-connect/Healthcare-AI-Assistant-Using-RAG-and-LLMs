from datetime import datetime


def check_available_slots(department: str = "general medicine", date: str = "Monday"):
    """
    Mock appointment availability tool.
    This does not connect to any real hospital system.
    """

    mock_slots = {
        "cardiology": ["10:00 AM", "12:30 PM", "04:00 PM"],
        "dermatology": ["11:00 AM", "03:00 PM"],
        "general medicine": ["09:30 AM", "01:00 PM", "05:00 PM"],
        "pediatrics": ["10:30 AM", "02:00 PM"],
        "orthopedics": ["12:00 PM", "04:30 PM"],
        "neurology": ["11:30 AM", "03:30 PM"],
    }

    department = department.lower().strip()

    slots = mock_slots.get(department, mock_slots["general medicine"])

    return {
        "tool": "check_available_slots",
        "department": department,
        "date": date,
        "available_slots": slots,
        "message": f"Mock appointment slots for {department} on {date}: {', '.join(slots)}"
    }


def extract_department(question: str) -> str:
    departments = [
        "cardiology",
        "dermatology",
        "general medicine",
        "pediatrics",
        "orthopedics",
        "neurology"
    ]

    question_lower = question.lower()

    for department in departments:
        if department in question_lower:
            return department

    return "general medicine"


def extract_date(question: str) -> str:
    days = [
        "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"
    ]

    question_lower = question.lower()

    for day in days:
        if day in question_lower:
            return day.capitalize()

    return "requested date"