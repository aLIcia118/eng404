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
