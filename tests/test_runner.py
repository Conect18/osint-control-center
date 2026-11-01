import sys

from app.core.runner import Status, run_tool


def test_binario_inexistente(tmp_path):
    r = run_tool("Nope", ["binario-que-no-existe"], tmp_path, tmp_path)
    assert r.status is Status.MISSING
    assert r.ok is False


def test_exito_con_salida(tmp_path):
    r = run_tool("Echo", [sys.executable, "-c", "print('hola')"], tmp_path, tmp_path)
    assert r.status is Status.OK
    assert (tmp_path / "echo" / "stdout.txt").read_text().strip() == "hola"


def test_exito_sin_salida_es_empty(tmp_path):
    r = run_tool("True", [sys.executable, "-c", "pass"], tmp_path, tmp_path)
    assert r.status is Status.EMPTY


def test_dos_herramientas_no_colisionan(tmp_path):
    run_tool("A", [sys.executable, "-c", "print('a')"], tmp_path, tmp_path)
    run_tool("B", [sys.executable, "-c", "print('b')"], tmp_path, tmp_path)
    assert (tmp_path / "a" / "stdout.txt").read_text().strip() == "a"
    assert (tmp_path / "b" / "stdout.txt").read_text().strip() == "b"


def test_timeout_mata_el_proceso(tmp_path):
    r = run_tool(
        "Sleep", [sys.executable, "-c", "import time; time.sleep(30)"],
        tmp_path, tmp_path, timeout=1,
    )
    assert r.status is Status.TIMEOUT


def test_salida_no_utf8_no_rompe(tmp_path):
    code = "import sys; sys.stdout.buffer.write(b'\\xff\\xfe ok')"
    r = run_tool("Bytes", [sys.executable, "-c", code], tmp_path, tmp_path)
    assert r.returncode == 0
