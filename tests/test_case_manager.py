import shutil

from app.config import settings
from app.core import case_manager


def test_ids_no_se_repiten_tras_borrar(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "CASES_PATH", tmp_path)
    monkeypatch.setattr(case_manager, "set_case", lambda p: None)

    ids = [case_manager.create_case("uno", "users").name for _ in range(3)]
    shutil.rmtree(tmp_path / ids[1])

    nuevo = case_manager.create_case("dos", "users").name
    assert nuevo not in ids


def test_target_se_normaliza(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "CASES_PATH", tmp_path)
    monkeypatch.setattr(case_manager, "set_case", lambda p: None)

    case = case_manager.create_case("@PabloG", "users")
    assert '"target": "pablog"' in (case / "info.json").read_text(encoding="utf-8")
