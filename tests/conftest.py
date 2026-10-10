"""Cài chung cho mọi test."""
import pytest

from app import config


@pytest.fixture(autouse=True)
def _tat_chuc_le(monkeypatch):
    # Chạy test đúng ngày lễ (ví dụ 20/10) thì Bơ sẽ đòi chúc lễ → test khác bị lệch. Test chúc lễ tự bật lại.
    monkeypatch.setattr(config, "CHUC_LE", False)
