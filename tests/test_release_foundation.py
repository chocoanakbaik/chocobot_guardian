"""Release foundation checks for packaged resources and user-data location."""
from chocobot import constants as const


def test_user_data_is_separate_from_bundled_application_resources():
    assert const.DATA_DIR != const.BASE_DIR / "data"
    assert const.CONFIG_FILE.parent == const.DATA_DIR
    assert const.LOG_DIR.is_relative_to(const.DATA_DIR)
    assert const.QUARANTINE_DIR.is_relative_to(const.DATA_DIR)


def test_language_packs_remain_in_bundled_resource_directory():
    assert (const.LANGUAGE_DIR / "id.json").is_file()
    assert (const.LANGUAGE_DIR / "en.json").is_file()


def test_expected_resource_locations_are_defined():
    assert const.LOGO_PATH.parent == const.IMAGES_DIR
    assert const.LOGO_ICO_PATH.parent == const.ICONS_DIR
