"""Test phần giọng nói trên web: từ đánh thức "Bơ ơi", dọn chữ trước khi đọc. Cần Node.js; máy không có Node thì bỏ qua."""
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


SPEECH_CASES = {
    "Hôm nay vui quá 😄🎉!!!": "Hôm nay vui quá!",
    "**Cố lên** nha :)": "Cố lên nha",
    "Tập chân 💪🏽 xong chưa??": "Tập chân xong chưa?",
    "Xem https://abc.com nè": "Xem nè",
    "Giá 3.5 triệu, ok.": "Giá 3.5 triệu, ok.",
}


@pytest.mark.skipif(shutil.which("node") is None, reason="cần Node.js")
def test_speech_text_cleaned():
    js = config.ROOT / "web" / "doc_to.js"
    code = (
        f"const {{ boChuDeDoc }} = require({json.dumps(str(js))});"
        f"console.log(JSON.stringify({json.dumps(list(SPEECH_CASES))}.map(boChuDeDoc)));"
    )
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, encoding="utf-8", check=True)
    assert dict(zip(SPEECH_CASES, json.loads(out.stdout))) == SPEECH_CASES


SPLIT_CASES = {
    "Chào nha!": ["Chào nha!"],
    "Ừa. Hôm nay Bơ thấy vui lắm luôn đó. Còn bạn thì sao, đi tập chưa? Kể Bơ nghe với nha!":
        ["Ừa. Hôm nay Bơ thấy vui lắm luôn đó.", "Còn bạn thì sao, đi tập chưa?", "Kể Bơ nghe với nha!"],
    "Giá vàng hôm qua khoảng 3.5 triệu một chỉ đó. Nhưng Bơ không chắc giá hôm nay đâu nha.":
        ["Giá vàng hôm qua khoảng 3.5 triệu một chỉ đó.", "Nhưng Bơ không chắc giá hôm nay đâu nha."],
    "Một. Hai đây là câu thứ hai. Ba đây là câu thứ ba. Bốn đây là câu thứ tư. Năm nè.":
        ["Một. Hai đây là câu thứ hai.", "Ba đây là câu thứ ba.", "Bốn đây là câu thứ tư. Năm nè."],
}


@pytest.mark.skipif(shutil.which("node") is None, reason="cần Node.js")
def test_split_reply_into_bubbles():
    js = config.ROOT / "web" / "doc_to.js"
    code = (
        f"const {{ boTachTin }} = require({json.dumps(str(js))});"
        f"console.log(JSON.stringify({json.dumps(list(SPLIT_CASES))}.map(x => boTachTin(x))));"
    )
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, encoding="utf-8", check=True)
    assert dict(zip(SPLIT_CASES, json.loads(out.stdout))) == SPLIT_CASES


def test_wake_script_served(tmp_path):
    from tests.test_api import make_client

    c = make_client(tmp_path, [])
    r = c.get("/web/danh_thuc.js")
    assert r.status_code == 200 and "boDanhThuc" in r.text
    assert 'id="handsBtn"' in c.get("/").text
    assert "boChuDeDoc" in c.get("/web/doc_to.js").text


@pytest.mark.skipif(shutil.which("node") is None, reason="cần Node.js")
def test_chon_giong_doc():
    code = """
    const { boChonGiong, boGiongKe, boGiongViet } = require('./web/doc_to.js');
    const vs = [{name: 'Anna', lang: 'en-US'}, {name: 'An', lang: 'vi-VN'}, {name: 'HoaiMy', lang: 'vi_VN'}];
    console.log(JSON.stringify([
      boGiongViet(vs).length, boChonGiong(vs, '').name, boChonGiong(vs, 'HoaiMy').name,
      boChonGiong(vs, 'Mất rồi').name, boGiongKe(vs, 'An').name, boGiongKe(vs, 'HoaiMy').name,
      boChonGiong([], 'x'), boGiongKe([{name: 'A', lang: 'en'}], 'A')]));
    """
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, encoding="utf-8", check=True)
    assert json.loads(out.stdout) == [2, "An", "HoaiMy", "An", "HoaiMy", "An", None, None]


@pytest.mark.skipif(shutil.which("node") is None, reason="cần Node.js")
def test_gio_yen_lang():
    code = """
    const { boGioYenLang: q } = require('./web/doc_to.js');
    console.log(JSON.stringify([q(23,'23-6'), q(2,'23-6'), q(6,'23-6'), q(12,'23-6'), q(13,'13-14'), q(14,'13-14'),
      q(2,''), q(2,'abc'), q(5,'5-5'), q(0,'22-24'), q(23,'22-24')]));
    """
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, encoding="utf-8", check=True)
    assert json.loads(out.stdout) == [True, True, False, False, True, False, False, False, False, False, True]
