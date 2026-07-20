from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import maya_lens_server


class PublicReleaseContractTests(unittest.TestCase):
    def test_public_metadata_and_runtime_files_exist(self):
        required = [
            "README.md", "LICENSE.txt", "SECURITY.md", "SAFETY_BOUNDARY.md",
            "maya_lens_server.py", "web/index.html", "web/styles.css", "web/app.js",
            "src/maya_lens/scanner.py", "src/maya_lens/public_safety.py",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_readme_commands_are_standalone_and_reference_shipped_files(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("tools/maya-lens", readme)
        self.assertNotIn("repo_brief_p1_reproduction", readme)
        self.assertIn("python tests/test_maya_lens_scanner.py", readme)
        self.assertIn("python tests/test_maya_lens_server.py", readme)

    def test_server_declares_complete_browser_hardening_set(self):
        source = (ROOT / "maya_lens_server.py").read_text(encoding="utf-8")
        for header in (
            "Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options",
            "Referrer-Policy", "Permissions-Policy", "Cross-Origin-Opener-Policy",
            "Cross-Origin-Resource-Policy",
        ):
            self.assertIn(header, source)

    def test_release_manifest_has_no_private_source_paths(self):
        manifest = json.loads((ROOT / "PUBLIC_RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
        rendered = json.dumps(manifest)
        for marker in ("C:/Users/", "E:/MAYA_BULK", "MAYA Founder Files", "2ndnatureai-maya-beta"):
            self.assertNotIn(marker, rendered)


if __name__ == "__main__":
    unittest.main()
