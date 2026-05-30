from src.playwright_creator import PlaywrightDraftCreator


def test_init_stores_profile_path():
    creator = PlaywrightDraftCreator(profile_path="C:/fake/profile")
    assert creator.profile_path == "C:/fake/profile"


def test_init_sets_internals_to_none():
    creator = PlaywrightDraftCreator(profile_path="C:/fake/profile")
    assert creator._pw is None
    assert creator._context is None
    assert creator._page is None
