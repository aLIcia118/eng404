from functools import wraps

# import data.db_connect as dbc

"""
Our record format to meet our requirements (see security.md) will be:

{
    feature_name1: {
        create: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        read: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        update: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        delete: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
    },
    feature_name2: # etc.
}
"""

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'

# Features:
PEOPLE = 'people'

security_recs = None
# These will come from the DB soon:
temp_recs = {
    PEOPLE: {
        CREATE: {
            USER_LIST: ['ejc369@nyu.edu', 'admin@eng404.com'],
            CHECKS: {
                LOGIN: True,
            },
        },
        READ: {
            USER_LIST: ['ejc369@nyu.edu', 'admin@eng404.com'],
            CHECKS: {
                LOGIN: True,
            },
        },
    },
}


def read() -> dict:
    global security_recs
    # dbc.read()
    security_recs = temp_recs
    return security_recs


def needs_recs(fn):
    """
    Should be used to decorate any function that directly accesses sec recs.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if not security_recs:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    if feature_name in security_recs:
        return security_recs[feature_name]
    else:
        return None

@needs_recs
def is_allowed(feature_name: str, action: str, user_email: str, logged_in: bool) -> bool:
    feature = read_feature(feature_name)

    if not feature:
        return False

    if action not in feature:
        return False

    action_rules = feature[action]

    if user_email not in action_rules.get(USER_LIST, []):
        return False

    checks = action_rules.get(CHECKS, {})

    if checks.get(LOGIN) and not logged_in:
        return False

    return True