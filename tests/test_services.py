from app.services import maigret_service, sherlock_service

SALIDA = """[*] Checking username objetivo on:

[+] GitHub: https://github.com/objetivo
[+] Reddit: https://reddit.com/u/objetivo

[*] Checking username otro on:

[+] GitHub: https://github.com/otro
[+] VK: https://vk.com/otro
[+] Steam: https://steamcommunity.com/otro
"""


def test_sherlock_cuenta(tmp_path):
    folder = tmp_path / "sherlock"
    folder.mkdir()
    (folder / "stdout.txt").write_text(
        "[+] TikTok: https://tiktok.com/@x\n[-] Twitter: no\n", encoding="utf-8"
    )
    assert sherlock_service._count(folder) == 1


def test_sherlock_fallback_total(tmp_path):
    folder = tmp_path / "sherlock"
    folder.mkdir()
    (folder / "stdout.txt").write_text("[*] Search completed with 12 results\n", encoding="utf-8")
    assert sherlock_service._count(folder) == 12


def test_maigret_separa_variantes(tmp_path):
    folder = tmp_path / "maigret"
    folder.mkdir()
    (folder / "stdout.txt").write_text(SALIDA, encoding="utf-8")
    counts = maigret_service._blocks(folder)
    assert counts["objetivo"] == 2
    assert counts["otro"] == 3
