import security.security as sec


def test_read():
    recs = sec.read()
    assert isinstance(recs, dict)
    for feature in recs:
        assert isinstance(feature, str)
        assert len(feature) > 0


def test_read_feature_returns_people_rules():
    feature = sec.read_feature(sec.PEOPLE)
    assert feature is not None
    assert sec.CREATE in feature
    assert feature[sec.CREATE][sec.CHECKS][sec.LOGIN] is True


def test_read_feature_returns_none_for_unknown_feature():
    assert sec.read_feature("unknown_feature") is None


def test_is_allowed_allows_user_to_create_people_when_logged_in():
    assert sec.is_allowed(sec.PEOPLE, sec.CREATE, "ejc369@nyu.edu", True) is True


def test_is_allowed_allows_user_to_read_people_when_logged_in():
    assert sec.is_allowed(sec.PEOPLE, sec.READ, "ejc369@nyu.edu", True) is True


def test_is_allowed_denies_allowed_user_when_not_logged_in():
    assert sec.is_allowed(sec.PEOPLE, sec.READ, "ejc369@nyu.edu", False) is False


def test_is_allowed_denies_unknown_user():
    assert sec.is_allowed(sec.PEOPLE, sec.READ, "unknown@nyu.edu", True) is False


def test_is_allowed_denies_unknown_feature():
    assert sec.is_allowed("unknown_feature", sec.READ, "ejc369@nyu.edu", True) is False


def test_is_allowed_denies_unknown_action():
    assert sec.is_allowed(sec.PEOPLE, "unknown_action", "ejc369@nyu.edu", True) is False


def test_is_allowed_email_matching_ignores_case_and_spaces():
    assert sec.is_allowed(sec.PEOPLE, sec.READ, "  EJC369@NYU.EDU  ", True) is True


def test_is_allowed_denies_none_or_empty_email():
    assert sec.is_allowed(sec.PEOPLE, sec.READ, None, True) is False
    assert sec.is_allowed(sec.PEOPLE, sec.READ, "", True) is False
    assert sec.is_allowed(sec.PEOPLE, sec.READ, "   ", True) is False
