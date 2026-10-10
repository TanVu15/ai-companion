"""Cài chung cho mọi test."""
import pytest

from app import config


@pytest.fixture(autouse=True)
def _tat_chuc_le(monkeypatch):
    # Chạy test đúng ngày lễ (ví dụ 20/10) thì Bơ sẽ đòi chúc lễ → test khác bị lệch. Test chúc lễ tự bật lại.
    monkeypatch.setattr(config, "CHUC_LE", False)


@pytest.fixture(autouse=True)
def _sao_luu_vao_thu_muc_tam(monkeypatch, tmp_path):
    # Test gọi /api/chat sẽ tự sao lưu: ghi vào thư mục tạm, không đụng data/ thật.
    from app import main

    monkeypatch.setattr(config, "SAO_LUU_DIR", tmp_path / "sao_luu")
    monkeypatch.setattr(main, "_sao_luu_ngay", None)
