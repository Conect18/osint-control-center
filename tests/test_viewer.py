import pytest

from app.utils.files import case_files, is_binary, read_text_safe, resolve_in_case


@pytest.fixture()
def case(tmp_path):
    (tmp_path / "reports").mkdir()
    (tmp_path / "users").mkdir()
    (tmp_path / "info.json").write_text("{}", encoding="utf-8")
    (tmp_path / "reports" / "report.md").write_text("# hola", encoding="utf-8")
    (tmp_path / "users" / "stdout.txt").write_text("x", encoding="utf-8")
    return tmp_path


def test_los_reportes_van_primero(case):
    assert case_files(case)[0].name == "report.md"


def test_resolve_rechaza_traversal(case):
    (case.parent / "ajeno.txt").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        resolve_in_case(case, "../ajeno.txt")


def test_resolve_inexistente(case):
    with pytest.raises(FileNotFoundError):
        resolve_in_case(case, "nada.txt")


def test_deteccion_binaria():
    assert is_binary(b"\x00\x01\x02")


def test_lectura_latin1(case):
    path = case / "users" / "latin.txt"
    path.write_bytes("ñandú".encode("latin-1"))
    text, encoding = read_text_safe(path)
    assert text == "ñandú"
    assert encoding == "latin-1"


def test_view_inexistente(case):
    from app.ui import viewer

    assert viewer.view(case, case / "no.txt") is False
