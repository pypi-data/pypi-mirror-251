import desktop_entry_lib
import pytest_subtests
import subprocess
import pyfakefs
import pathlib
import pytest
import shutil
import os


DATA_DIR = pathlib.Path(__file__).parent / "data"


def _create_test_directory(path: pathlib.Path) -> None:
    first = desktop_entry_lib.DesktopEntry()
    first.Name.default_text = "First"
    first.Categories.append("Office")
    first.MimeType.append("text/plain")
    first.Hidden = True
    first.write_file(os.path.join(path, "com.example.First.desktop"))

    second = desktop_entry_lib.DesktopEntry()
    second.Name.default_text = "Second"
    second.Categories.append("Internet")
    second.NoDisplay = True
    second.write_file(os.path.join(path, "com.example.Second.desktop"))

    third = desktop_entry_lib.DesktopEntry()
    third.Name.default_text = "Third"
    third.Name.translations["de"] = "Dritte"
    third.Categories.append("Internet")
    third.write_file(os.path.join(path, "com.example.Third.desktop"))


def test_data_collection() -> None:
    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(DATA_DIR)
    for i in os.listdir(DATA_DIR):
        if not i.endswith(".desktop"):
            continue

        desktop_id = i.removesuffix(".desktop")

        assert desktop_id in collection
        assert desktop_id in collection.desktop_entries


def test_load_menu(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, tmp_path: pathlib.Path) -> None:
    collection_menu = desktop_entry_lib.DesktopEntryCollection()
    collection_data = desktop_entry_lib.DesktopEntryCollection()

    shutil.copytree(DATA_DIR, tmp_path / "applications")
    monkeypatch.setenv("XDG_DATA_DIRS", str(tmp_path))

    assert collection_data.load_directory(DATA_DIR) is True

    with subtests.test("Without error"):
        assert collection_menu.load_menu() is True

        assert collection_menu == collection_data

    with subtests.test("With error"):
        (tmp_path / "applications" / "invalid.desktop").write_bytes(b"\0xe4\0xf8")

        assert collection_menu.load_menu() is False

        assert collection_menu == collection_data


def test_load_desktop(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    with subtests.test("Exists"):
        monkeypatch.setattr(subprocess, "check_output", lambda args: str(tmp_path).encode("utf-8"))

        collection = desktop_entry_lib.DesktopEntryCollection()
        assert collection.load_desktop() is True

        assert "com.example.First" in collection
        assert "com.example.Second" in collection
        assert "com.example.Third" in collection
        assert "com.example.Fourth" not in collection

    with subtests.test("Not Exists"):
        monkeypatch.setattr(subprocess, "check_output", lambda args: str(tmp_path / "invalid").encode("utf-8"))

        collection = desktop_entry_lib.DesktopEntryCollection()
        assert collection.load_desktop() is False

        assert len(collection) == 0


def test_load_autostart(subtests: pytest_subtests.SubTests, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    fs.os = pyfakefs.fake_filesystem.OSType.LINUX
    fs.create_dir("/etc/xdg/autostart")

    _create_test_directory(pathlib.Path("/etc/xdg/autostart"))

    with subtests.test("Exists"):
        collection = desktop_entry_lib.DesktopEntryCollection()
        assert collection.load_autostart() is True
        assert len(collection) == 3

    with subtests.test("Not Exists"):
        with open("/etc/xdg/autostart/invalid.desktop", "wb") as f:
            f.write(b"\0xe4\0xf8")

        collection = desktop_entry_lib.DesktopEntryCollection()
        collection.load_autostart() is False
        assert len(collection) == 3


def test_get_entries_by_category(tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.First.desktop")) in collection.get_entries_by_category("Office")
    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.Second.desktop")) in collection.get_entries_by_category("Internet")
    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.Third.desktop")) in collection.get_entries_by_category("Internet")


def test_get_entries_by_mime_type(tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)
    entry_list = collection.get_entries_by_mime_type("text/plain")

    assert len(entry_list) == 1
    assert entry_list[0].desktop_id == "com.example.First"


def test_get_visible_entries(tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.First.desktop")) not in collection.get_visible_entries()
    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.Second.desktop")) in collection.get_visible_entries()
    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.Third.desktop")) in collection.get_visible_entries()


def test_get_menu_entries(tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.First.desktop")) not in collection.get_menu_entries()
    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.Second.desktop")) not in collection.get_menu_entries()
    assert desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.Third.desktop")) in collection.get_menu_entries()


def test_get_entry_by_name(subtests: pytest_subtests.SubTests, tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    with subtests.test("Name exists"):
        assert collection.get_entry_by_name("Second").desktop_id == "com.example.Second"

    with subtests.test("Translated Name exists"):
        assert collection.get_entry_by_name("Dritte").desktop_id == "com.example.Third"

    with subtests.test("Name not exists"):
        assert collection.get_entry_by_name("NotFound") is None

    with subtests.test("Don't search translations"):
        assert collection.get_entry_by_name("Dritte", False) is None


def test_length(tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    assert len(collection) == 3


def test_equal(subtests: pytest_subtests.SubTests, tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection_a = desktop_entry_lib.DesktopEntryCollection()
    collection_b = desktop_entry_lib.DesktopEntryCollection()
    collection_c = desktop_entry_lib.DesktopEntryCollection()

    assert collection_a.load_directory(tmp_path) is True
    assert collection_b.load_directory(tmp_path) is True

    with subtests.test("Equal"):
        assert collection_a == collection_b

    with subtests.test("Not equal"):
        assert collection_a != collection_c

    with subtests.test("Not a collection"):
        assert collection_a != "test"


def test_getitem(subtests: pytest_subtests.SubTests, tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    with subtests.test("Contains"):
        assert collection["com.example.First"].Name.default_text == "First"

    with subtests.test("Contains not"):
        with pytest.raises(KeyError):
            collection["invalid"]


def test_setitem(subtests: pytest_subtests.SubTests) -> None:
    with subtests.test("Everything working"):
        collection = desktop_entry_lib.DesktopEntryCollection()
        entry = desktop_entry_lib.DesktopEntry.from_file(DATA_DIR / "com.gitlab.JakobDev.jdTextEdit.desktop")

        collection["test"] = entry
        assert collection["test"].desktop_id == "com.gitlab.JakobDev.jdTextEdit"

    with subtests.test("Key not string"):
        collection = desktop_entry_lib.DesktopEntryCollection()
        entry = desktop_entry_lib.DesktopEntry.from_file(DATA_DIR / "com.gitlab.JakobDev.jdTextEdit.desktop")

        with pytest.raises(ValueError) as ex:
            collection[42] = entry

        assert ex.value.args[0] == "Key must be a string"

    with subtests.test("value not entry"):
        collection = desktop_entry_lib.DesktopEntryCollection()

        with pytest.raises(ValueError) as ex:
            collection["test"] = 42

        assert ex.value.args[0] == "Value must be a DesktopEntry"


def test_contains(tmp_path: pathlib.Path) -> None:
    _create_test_directory(tmp_path)

    collection = desktop_entry_lib.DesktopEntryCollection()
    collection.load_directory(tmp_path)

    assert "com.example.First" in collection
    assert "com.example.Second" in collection
    assert "com.example.Third" in collection
    assert "com.example.Fourth" not in collection
