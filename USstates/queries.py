# USstates/queries.py

MIN_CODE_LEN = 2
CODE = "code"
NAME = "name"

state_cache = {}

SAMPLE_STATE = {
    CODE: "CA",
    NAME: "California",
}

def is_valid_code(code: str) -> bool:
    """Return True if code is a valid 2-letter abbreviation."""
    return isinstance(code, str) and len(code) == 2 and code.isalpha()

def num_states() -> int:
    """Return the number of states currently stored."""
    return len(state_cache)

def create(flds: dict) -> str:
    """Add a new state record and return its code."""
    if not isinstance(flds, dict):
        raise ValueError(f"Expected dict, got {type(flds).__name__}")
    if not flds.get(NAME) or not flds.get(CODE):
        raise ValueError("State name and code are required")
    if not is_valid_code(flds[CODE]):
        raise ValueError(f"Invalid state code: {flds[CODE]}")
    state_cache[flds[CODE]] = flds
    return flds[CODE]
