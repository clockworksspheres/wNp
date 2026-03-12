# tests/fixtures/noaa_observations.py

VALID_OBSERVATION = {
    "timestamp": "2024-01-01T10:30:00+00:00",
    "temperature": {"value": 50, "unitCode": "unit:F"},
    "dewpoint": {"value": 40, "unitCode": "unit:F"},
    "relativeHumidity": {"value": 55},
    "barometricPressure": {"value": 100000}
}

MISSING_VALUES_OBSERVATION = {
    "timestamp": "2024-01-01T11:00:00+00:00",
    "temperature": {"value": None, "unitCode": "unit:F"},
    "dewpoint": {"value": None, "unitCode": "unit:F"},
    "relativeHumidity": {"value": None},
    "barometricPressure": {"value": None}
}

CELSIUS_OBSERVATION = {
    "timestamp": "2024-01-01T12:00:00+00:00",
    "temperature": {"value": 10, "unitCode": "unit:C"},
    "dewpoint": {"value": 5, "unitCode": "unit:C"},
    "relativeHumidity": {"value": 60},
    "barometricPressure": {"value": 101000}
}

MULTI_OBSERVATION_LIST = [
    VALID_OBSERVATION,
    CELSIUS_OBSERVATION,
    MISSING_VALUES_OBSERVATION
]

