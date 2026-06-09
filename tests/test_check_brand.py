from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_brand import check_text, load_brand_config


def test_loads_blacklist_and_nuance_words():
    blacklist, nuance_words = load_brand_config()

    assert "hype_hustle_fake_urgency" in blacklist
    assert "game-changer" in blacklist["hype_hustle_fake_urgency"]
    assert "transform" in nuance_words


def test_passes_clean_copy():
    result = check_text("AI adoption works when operators build proof before process.")

    assert result["verdict"] == "PASS"
    assert result["blacklist_violations"] == {}


def test_fails_blacklisted_copy():
    result = check_text("This game-changer will unlock your potential and 10x your work.")

    assert result["verdict"] == "FAIL"
    assert "hype_hustle_fake_urgency" in result["blacklist_violations"]
    assert "empty_pleasing_generic" in result["blacklist_violations"]


def test_flags_nuance_words_without_failing():
    result = check_text("The client felt alive after the operating rhythm changed.")

    assert result["verdict"] == "PASS"
    assert result["nuance_words"] == ["alive"]
