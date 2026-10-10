"""Test từ đánh thức "Bơ ơi" (web/danh_thuc.js). Cần Node.js; máy không có Node thì bỏ qua."""
import json
import shutil
import subprocess

import pytest

from app import config

CASES = {
    "Bơ ơi hôm nay trời đẹp quá": "hôm nay trời đẹp quá",
    "bơ ơi": "",
    "Bơ ơi.": "",
    "ê Bơ, kể chuyện đi": "kể chuyện đi",
    "bờ ới mấy giờ rồi": "mấy giờ rồi",
    "mình ăn quả bơ": None,
    "bơ ngon lắm": None,
    "hôm nay vui": None,
}


@pytest.mark.skipif(shutil.which("node") is None, reason="cần Node.js")
def test_wake_word():
    js = config.ROOT / "web" / "danh_thuc.js"
    code = (
        f"const {{ boDanhThuc }} = require({json.dumps(str(js))});"
        f"console.log(JSON.stringify({json.dumps(list(CASES))}.map(boDanhThuc)));"
    )
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, encoding="utf-8", check=True)
    assert dict(zip(CASES, json.loads(out.stdout))) == CASES


def test_wake_script_served(tmp_path):
    from tests.test_api import make_client

    c = make_client(tmp_path, [])
    r = c.get("/web/danh_thuc.js")
    assert r.status_code == 200 and "boDanhThuc" in r.text
    assert 'id="handsBtn"' in c.get("/").text
