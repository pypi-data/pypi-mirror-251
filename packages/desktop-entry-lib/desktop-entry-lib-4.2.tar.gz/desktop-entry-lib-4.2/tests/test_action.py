import desktop_entry_lib
import pytest_subtests
import pyfakefs
import pytest


def test_get_icon_path(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    fs.os = pyfakefs.fake_filesystem.OSType.LINUX
    fs.create_file("/usr/share/pixmaps/test.png")

    monkeypatch.delenv("XDG_DATA_DIRS", False)

    with subtests.test("Icon exists"):
        action = desktop_entry_lib.DesktopAction()
        action.Icon = "test"

        assert action.get_icon_path() == "/usr/share/pixmaps/test.png"

    with subtests.test("Icon not exists"):
        action = desktop_entry_lib.DesktopAction()
        action.Icon = "invalid"

        assert action.get_icon_path() is None

    with subtests.test("No Icon"):
        assert desktop_entry_lib.DesktopAction().get_icon_path() is None


def test_get_command() -> None:
    action = desktop_entry_lib.DesktopAction()
    action.Exec = "echo Test"
    assert action.get_command() == ["echo", "Test"]


def test_equal(subtests: pytest_subtests.SubTests) -> None:
    action_a = desktop_entry_lib.DesktopAction()
    action_b = desktop_entry_lib.DesktopAction()
    action_c = desktop_entry_lib.DesktopAction()

    action_a.Name.default_text = "Name"
    action_b.Name.default_text = "Name"

    with subtests.test("Equal"):
        assert action_a == action_b

    with subtests.test("Not equal"):
        assert action_a != action_c

    with subtests.test("Not a action"):
        assert action_a != "test"
