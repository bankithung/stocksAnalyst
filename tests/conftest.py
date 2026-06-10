import os, sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("STOCK_RESEARCH_DATA", str(tmp_path))
    monkeypatch.setenv("STOCK_RESEARCH_DB", str(tmp_path / "market.db"))
    import importlib, common
    importlib.reload(common)
    return common
