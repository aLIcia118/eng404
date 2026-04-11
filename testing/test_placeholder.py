"""Smoke tests for the in-repo security defaults."""

import security.security as sec


def test_security_defaults_require_login_for_people_create():
    """The sample PEOPLE/create policy should always require login."""
    recs = sec.read()

    assert sec.PEOPLE in recs
    assert sec.CREATE in recs[sec.PEOPLE]

    create_rules = recs[sec.PEOPLE][sec.CREATE]
    assert create_rules[sec.CHECKS][sec.LOGIN] is True
    assert "ejc369@nyu.edu" in create_rules[sec.USER_LIST]
