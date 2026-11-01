import tempfile
import unittest
from pathlib import Path

from restovisuals.audit import compare_protected, inspect_environment, read_ini


class AuditTests(unittest.TestCase):
    def setUp(self):
        temp_root = Path(__file__).resolve().parents[1] / ".local/test-tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=temp_root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8-sig")
        return path

    def test_csp_ini_quotes_comments_duplicates(self):
        path = self.write("test.ini", "[FSR]\nACTIVE=0 ; default\nLABEL='part;label'\n[FSR]\nACTIVE=1\nURL=https://example.test/a=b\n")
        parsed = read_ini(path)["FSR"]
        self.assertEqual(parsed["ACTIVE"], "1")
        self.assertEqual(parsed["LABEL"], "part;label")
        self.assertEqual(parsed["URL"], "https://example.test/a=b")

    def test_missing_optional_data_stays_unknown(self):
        game, user = self.root / "game", self.root / "user"
        game.mkdir()
        user.mkdir()
        result = inspect_environment(game, user)
        self.assertIsNone(result["csp"]["manifest_version"])
        self.assertEqual(result["configured"]["upscaling_method"], "unknown")
        self.assertFalse(result["runtime_validated"])
        self.assertEqual(result["reshade"]["runtime_active"], "unknown")

    def test_observations_merge_defaults_without_writing(self):
        self.write("game/extension/config/graphics_adjustments.ini", "[FSR]\nACTIVE=0\nOLD_IMPLEMENTATION=0\n")
        self.write("user/extension/graphics_adjustments.ini", "[FSR]\nACTIVE=1\nOLD_IMPLEMENTATION=2\n")
        self.write("game/extension/weather/pure/manifest.ini", "[ABOUT]\nNAME=Pure Gamma\nVERSION=3.50\n")
        self.write("game/system/cfg/ppfilters/synthetic.ini", "[TEST]\nVALUE=1\n")
        game, user = self.root / "game", self.root / "user"
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = inspect_environment(game, user)
        self.assertEqual(result["configured"]["upscaling_method"], "nis")
        self.assertEqual(result["configured"]["upscaling_active"], "1")
        self.assertEqual(result["pure"]["gamma_manifest_version"], "3.50")
        self.assertEqual(result["pp_filters"], ["synthetic.ini"])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertNotIn(str(self.root), str(result))

    def test_guard_detects_content_change_addition_and_removal(self):
        game, user = self.root / "game", self.root / "user"
        game.mkdir()
        user.mkdir()
        self.write("user/video.ini", "[VIDEO]\nWIDTH=1920\n")
        self.write("game/system/cfg/ppfilters/synthetic.ini", "before")
        before = inspect_environment(game, user)
        self.write("user/video.ini", "[VIDEO]\nWIDTH=1280\n")
        (game / "system/cfg/ppfilters/synthetic.ini").unlink()
        self.write("game/system/cfg/ppfilters/new.ini", "new")
        changes = compare_protected(before, inspect_environment(game, user))
        self.assertEqual(len(changes), 3)
        self.assertIn("user/video.ini", changes)

    def test_invalid_roots_fail(self):
        with self.assertRaises(ValueError):
            inspect_environment(self.root / "absent", self.root)

    def test_historical_reshade_is_not_runtime_evidence(self):
        self.write("game/ReShade.log1", "Initializing ReShade version '6.5.1.2008' from 'private/path'\n")
        (self.root / "user").mkdir()
        result = inspect_environment(self.root / "game", self.root / "user")
        self.assertEqual(result["reshade"]["historical_log_version"], "6.5.1.2008")
        self.assertFalse(any(result["reshade"]["root_loader_present"].values()))
        self.assertEqual(result["reshade"]["runtime_active"], "unknown")
        self.assertNotIn("private/path", str(result))


if __name__ == "__main__":
    unittest.main()
