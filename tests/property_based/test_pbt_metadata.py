import pytest

import string

from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st

from hangar import Repository

# ----------------------- Fixture Setup -----------------------------


@pytest.fixture()
def w_metadata_co(managed_tmpdir) -> Repository:
    repo_obj = Repository(path=managed_tmpdir, exists=False)
    repo_obj.init(user_name='tester', user_email='foo@test.bar', remove_old=True)
    co = repo_obj.checkout(write=True)
    yield co
    co.close()
    repo_obj._env._close_environments()


# ----------------------- Test Generation --------------------------


st_valid_names = st.text(min_size=1, alphabet=string.ascii_letters + string.digits + '_-.', max_size=16)
st_valid_ints = st.integers(min_value=0, max_value=999)
st_valid_keys = st.one_of(st_valid_ints, st_valid_names)

st_valid_values = st.text(min_size=1, alphabet=string.printable + string.whitespace, max_size=16)


@settings(max_examples=200, deadline=None)
@given(key=st_valid_keys, val=st_valid_values)
def test_metadata_key_values(key, val, w_metadata_co):
    w_metadata_co.metadata[key] = val
    assert w_metadata_co.metadata[key] == val
