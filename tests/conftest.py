import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


def pytest_runtest_logreport(report):
    if report.when != "call":
        return

    status = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"
    print(f"[{status}] {report.nodeid}")
    print()
