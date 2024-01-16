from humane.humanid import human_id, short_human_id


def test_humanid_and_short_common() -> None:
    assert human_id("test") == "12-wide-firefoxes-jumped-gleefully"

    assert short_human_id("test") in human_id("test")
