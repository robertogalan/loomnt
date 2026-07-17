from loomnt import loom


def test_extract_video_id_from_share_url():
    url = "https://www.loom.com/share/0123456789abcdef0123456789abcdef"
    assert loom.extract_video_id(url) == "0123456789abcdef0123456789abcdef"


def test_extract_video_id_from_embed_url_with_query():
    url = "https://www.loom.com/embed/ABCDEF0123456789ABCDEF0123456789?t=10"
    assert loom.extract_video_id(url) == "abcdef0123456789abcdef0123456789"


def test_extract_video_id_rejects_non_loom():
    try:
        loom.extract_video_id("https://example.com/video")
    except ValueError:
        return
    raise AssertionError("expected ValueError for a non-Loom URL")


def test_parse_vtt_produces_mmss_lines():
    vtt = (
        "WEBVTT\n\n"
        "1\n"
        "00:00:03.000 --> 00:00:05.000\n"
        "make this button blue\n\n"
        "2\n"
        "00:01:12.500 --> 00:01:14.000\n"
        "fix that spacing\n"
    )
    out = loom._parse_vtt(vtt)
    assert "00:03  make this button blue" in out
    assert "01:12  fix that spacing" in out
