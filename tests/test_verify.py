"""Exercise actual drift/boundary refusals without touching a live config."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("berry_verify", ROOT / "tools/verify.py")
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class VerifyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "candidate"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def test_clean_check_writes_nothing(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        self.assertEqual(verifier.verify(self.root), ([], 14))
        self.assertEqual(snapshot(), before)

    def test_modified_config_refused(self):
        path = self.root / "config/kitty/kitty.conf"
        path.write_text(path.read_text() + "font_size 42\n")
        self.assertTrue(any("source drift" in x for x in verifier.verify(self.root)[0]))

    def test_symlink_boundary_refused(self):
        path = self.root / "config/kitty/kitty.conf"
        external = Path(self.temp.name) / "unowned"
        external.write_text("must not be imported")
        path.unlink()
        path.symlink_to(external)
        self.assertTrue(any("symlink boundary" in x for x in verifier.verify(self.root)[0]))
        self.assertEqual(external.read_text(), "must not be imported")

    def test_unreviewed_file_refused(self):
        (self.root / "config/unreviewed").write_text("extra")
        self.assertIn("configuration inventory differs from allowlist", verifier.verify(self.root)[0])

    def test_waybar_symlink_refused_without_reading_target(self):
        path = self.root / "config/waybar/config.json"
        external = Path(self.temp.name) / "external-waybar"
        external.write_text("private external content is not JSON")
        path.unlink()
        path.symlink_to(external)
        original_open = Path.open

        def guarded_open(candidate, *args, **kwargs):
            if candidate == path or candidate == external:
                raise AssertionError("refused Waybar symlink target was opened")
            return original_open(candidate, *args, **kwargs)

        with patch.object(Path, "open", guarded_open):
            findings, _ = verifier.verify(self.root)
        self.assertIn("symlink boundary: config/waybar/config.json", findings)
        self.assertEqual(external.read_text(), "private external content is not JSON")


if __name__ == "__main__":
    unittest.main()
