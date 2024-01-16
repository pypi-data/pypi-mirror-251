import desktop_entry_lib
import pytest_subtests
import subprocess
import pyfakefs
import pathlib
import pytest
import os


def _generate_test_entry() -> desktop_entry_lib.DesktopEntry:
    entry = desktop_entry_lib.DesktopEntry()
    entry.Type = "Application"
    entry.Version = "1.5"
    entry.Name.default_text = "Test"
    entry.Comment.default_text = "Hello"
    entry.Comment.translations["de"] = "Hallo"
    return entry


def test_should_show(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("XDG_CURRENT_DESKTOP", False)

    entry = desktop_entry_lib.DesktopEntry()

    assert entry.should_show() is True

    entry.Hidden = True
    assert entry.should_show() is False

    entry.Hidden = False
    assert entry.should_show() is True

    entry.NotShowIn.append("TestDesktop")
    assert entry.should_show() is True

    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "TestDesktop")
    assert entry.should_show() is False

    entry.NotShowIn.clear()

    entry.OnlyShowIn.append("HelloWorld")
    assert entry.should_show() is False

    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "HelloWorld")
    assert entry.should_show() is True

    entry.OnlyShowIn.clear()

    assert entry.should_show() is True

    entry.Hidden = True
    assert entry.should_show() is False


def test_should_show_in_menu() -> None:
    entry = desktop_entry_lib.DesktopEntry()

    assert entry.should_show_in_menu() is True

    entry.NoDisplay = True
    assert entry.should_show_in_menu() is False

    entry.NoDisplay = False
    assert entry.should_show_in_menu() is True


def test_get_icon_path(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    fs.os = pyfakefs.fake_filesystem.OSType.LINUX
    fs.create_file("/usr/share/pixmaps/test.png")

    monkeypatch.delenv("XDG_DATA_DIRS", False)

    with subtests.test("Icon exists"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Icon = "test"

        assert entry.get_icon_path() == "/usr/share/pixmaps/test.png"

    with subtests.test("Icon not exists"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Icon = "invalid"

        assert entry.get_icon_path() is None

    with subtests.test("No Icon"):
        assert desktop_entry_lib.DesktopEntry().get_icon_path() is None


def test_is_empty() -> None:
    entry = desktop_entry_lib.DesktopEntry()
    assert entry.is_empty() is True
    entry.Name.default_text = "Test"
    assert entry.is_empty() is False


def test_from_string() -> None:
    entry = desktop_entry_lib.DesktopEntry.from_string("[Desktop Entry]\nType=Application\nName=Test\nExec=prog")
    assert entry.Name.default_text == "Test"
    assert entry.Exec == "prog"


def test_invalid_desktop_entry_exception() -> None:
    with pytest.raises(desktop_entry_lib.InvalidDesktopEntry):
        desktop_entry_lib.DesktopEntry.from_string("Hello")


def test_from_file(tmp_path: pathlib.Path) -> None:
    entry = _generate_test_entry()
    entry.write_file(os.path.join(tmp_path, "com.example.App.desktop"))
    assert entry == desktop_entry_lib.DesktopEntry.from_file(os.path.join(tmp_path, "com.example.App.desktop"))


def test_from_id(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, tmp_path: pathlib.Path) -> None:
    monkeypatch.setenv("XDG_DATA_DIRS", str(tmp_path))

    entry = _generate_test_entry()
    entry.write_file(os.path.join(tmp_path, "applications", "com.example.App.desktop"))

    with subtests.test("Exists"):
        assert desktop_entry_lib.DesktopEntry.from_id("com.example.App") == entry

    with subtests.test("Not exists"):
        assert desktop_entry_lib.DesktopEntry.from_id("invalid") is None


def test_repr() -> None:
    entry = desktop_entry_lib.DesktopEntry()
    entry.Name.default_text = "Test123"

    assert entry.__repr__() == "<DesktopEntry Name='Test123'>"


def test_equals() -> None:
    entry = _generate_test_entry()
    assert entry == entry
    assert not entry == desktop_entry_lib.DesktopEntry()
    assert not entry == 42


def test_get_keywords() -> None:
    entry = _generate_test_entry()
    assert isinstance(entry.get_keywords(), list)
    assert isinstance(desktop_entry_lib.DesktopEntry.get_keywords(), list)


def test_get_working_directory(subtests: pytest_subtests.SubTests) -> None:
    with subtests.test("Path key set"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Path = "/test"
        assert entry.get_working_directory() == "/test"

    with subtests.test("Path key not set"):
        assert desktop_entry_lib.DesktopEntry().get_working_directory() == os.path.expanduser("~")


def test_get_command(subtests: pytest_subtests.SubTests, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    fs.os = pyfakefs.fake_filesystem.OSType.LINUX

    with subtests.test("Exec key not set"):
        assert desktop_entry_lib.DesktopEntry().get_command([], []) == []

    with subtests.test("Single file path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%f"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["/hello.txt"]

    with subtests.test("Single file url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%f"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["/hello.txt"]

    with subtests.test("Multiple files path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%F"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["/hello.txt", "/world.txt"]

    with subtests.test("Multiple files url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%F"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["/hello.txt", "/world.txt"]

    with subtests.test("Single url path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%u"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["file:///hello.txt"]

    with subtests.test("Single url url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%u"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["https://example.com"]

    with subtests.test("Multiple urls path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%U"
        assert entry.get_command(["/hello.txt", "/world.txt"], []) == ["file:///hello.txt", "file:///world.txt"]

    with subtests.test("Multiple urls url"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%U"
        assert entry.get_command([], ["https://example.com", "file:///hello.txt", "file:///world.txt"]) == ["https://example.com", "file:///hello.txt", "file:///world.txt"]

    with subtests.test("With icon"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Icon = "Testicon"
        entry.Exec = "%i"
        assert entry.get_command([], []) == ["--icon", "Testicon"]

    with subtests.test("Without icon"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%i"
        assert entry.get_command([], []) == []

    with subtests.test("Name"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Name.default_text = "Testname"
        entry.Exec = "%c"
        assert entry.get_command([], []) == ["Testname"]

    with subtests.test("With path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.file_path = "Testpath"
        entry.Exec = "%k"
        assert entry.get_command([], []) == ["Testpath"]

    with subtests.test("Without path"):
        entry = desktop_entry_lib.DesktopEntry()
        entry.Exec = "%k"
        assert entry.get_command([], []) == [""]


def test_full_read_write(tmp_path: pathlib.Path) -> None:
    write_entry = desktop_entry_lib.DesktopEntry()

    write_entry.leading_comment = "Leading"
    write_entry.Type = "Application"
    write_entry.Version = "1.5"
    write_entry.Name.default_text = "Name"
    write_entry.GenericName.default_text = "GenericName"
    write_entry.NoDisplay = True
    write_entry.Comment.default_text = "Comment"
    write_entry.Icon = "Icon"
    write_entry.Hidden = True
    write_entry.OnlyShowIn.append("OnlyShowIn")
    write_entry.NotShowIn.append("NotShowIn")
    write_entry.DBusActivatable = False
    write_entry.TryExec = "TryExec"
    write_entry.Exec = "Exec"
    write_entry.Path = "Path"
    write_entry.Terminal = True
    write_entry.MimeType.append("MimeType")
    write_entry.Categories.append("Categories")
    write_entry.Implements.append("Implements")
    write_entry.Keywords.default_list.append("Keywords")
    write_entry.StartupNotify = True
    write_entry.StartupWMClass = "StartupWMClass"
    write_entry.URL = "URL"
    write_entry.PrefersNonDefaultGPU = True
    write_entry.SingleMainWindow = True
    write_entry.CustomKeys["X-Test"] = "Custom"

    action = desktop_entry_lib.DesktopAction()
    action.Name.default_text = "ActionName"
    action.Icon = "ActionIcon"
    action.Exec = "ActionExec"

    write_entry.Actions["TestAction"] = action

    assert write_entry.get_text().startswith("# Leading")
    write_entry.write_file(tmp_path / "test.desktop")

    read_entry = desktop_entry_lib.DesktopEntry.from_file(tmp_path / "test.desktop")

    assert read_entry.Type == "Application"
    assert read_entry.Version == "1.5"
    assert read_entry.Name.default_text == "Name"
    assert read_entry.GenericName.default_text == "GenericName"
    assert read_entry.NoDisplay is True
    assert read_entry.Comment.default_text == "Comment"
    assert read_entry.Icon == "Icon"
    assert read_entry.Hidden is True
    assert read_entry.OnlyShowIn == ["OnlyShowIn"]
    assert read_entry.NotShowIn == ["NotShowIn"]
    assert read_entry.DBusActivatable is False
    assert read_entry.TryExec == "TryExec"
    assert read_entry.Exec == "Exec"
    assert read_entry.Path == "Path"
    assert read_entry.Terminal is True
    assert read_entry.MimeType == ["MimeType"]
    assert read_entry.Categories == ["Categories"]
    assert read_entry.Implements == ["Implements"]
    assert read_entry.Keywords.default_list == ["Keywords"]
    assert read_entry.StartupNotify is True
    assert read_entry.StartupWMClass == "StartupWMClass"
    assert read_entry.URL == "URL"
    assert read_entry.PrefersNonDefaultGPU is True
    assert read_entry.SingleMainWindow is True
    assert read_entry.CustomKeys == {"X-Test": "Custom"}

    assert len(read_entry.Actions) == 1
    assert read_entry.Actions["TestAction"].Name.default_text == "ActionName"
    assert read_entry.Actions["TestAction"].Icon == "ActionIcon"
    assert read_entry.Actions["TestAction"].Exec == "ActionExec"

    assert write_entry == read_entry


def test_is_valid(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests) -> None:
    with subtests.test("Valid"):
        monkeypatch.setattr(subprocess, "run", lambda args, capture_output: subprocess.CompletedProcess([], 0))

        assert desktop_entry_lib.DesktopEntry().is_valid() is True

    with subtests.test("Invalid"):
        monkeypatch.setattr(subprocess, "run", lambda args, capture_output: subprocess.CompletedProcess([], 1))

        assert desktop_entry_lib.DesktopEntry().is_valid() is False


def test_get_validation_messages(monkeypatch: pytest.MonkeyPatch) -> None:
    output = "test.desktop: error: TestError\n"
    output += "test.desktop: error: (will be fatal in the future): TestFutureError\n"
    output += "test.desktop: warning: TestWarning\n"
    output += "test.desktop: hint: TestHint\n"

    result = subprocess.CompletedProcess([], 0)
    result.stdout = output.encode("utf-8")

    monkeypatch.setattr(subprocess, "run", lambda args, capture_output: result)

    messages = desktop_entry_lib.DesktopEntry().get_validation_messages()

    assert len(messages) == 4
    assert messages["Error"] == ["TestError"]
    assert messages["FutureError"] == ["TestFutureError"]
    assert messages["Warning"] == ["TestWarning"]
    assert messages["Hint"] == ["TestHint"]
