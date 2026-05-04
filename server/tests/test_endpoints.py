from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch
from pathlib import Path

import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_developer_logs_reads_requested_file(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line1\nline2\nline3\n", encoding="utf-8")

    resp = TEST_CLIENT.get(f"{ep.DEVELOPER_LOGS_EP}?path={log_file}&lines=2")
    assert resp.status_code == OK

    data = resp.get_json()
    assert data["path"] == str(log_file)
    assert data["lines_requested"] == 2
    assert data["lines"] == ["line2", "line3"]


def test_developer_logs_returns_candidates_when_default_logs_missing():
    with patch.object(ep, "DEFAULT_LOG_PATHS", (Path("/tmp/definitely-missing.log"),)):
        resp = TEST_CLIENT.get(ep.DEVELOPER_LOGS_EP)

    assert resp.status_code == NOT_FOUND
    data = resp.get_json()
    assert ep.MESSAGE in data
    assert "candidates" in data

def test_developer_logs_rejects_non_integer_lines(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line1\nline2\n", encoding="utf-8")

    resp = TEST_CLIENT.get(f"{ep.DEVELOPER_LOGS_EP}?path={log_file}&lines=abc")
    assert resp.status_code == BAD_REQUEST

    data = resp.get_json()
    assert ep.ERROR in data


