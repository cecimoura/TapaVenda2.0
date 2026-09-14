import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from scripts.build import build


class LocalReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("src", "href") and value:
                self.references.append(value)


class BuildTests(unittest.TestCase):
    def test_variants_and_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            build(output)
            priced = (output / "com-valor/index.html").read_text(encoding="utf-8")
            unpriced = (output / "sem-valor/index.html").read_text(encoding="utf-8")
            self.assertIn("R$ 3.500", priced)
            self.assertIn("6x de R$ 618,33", priced)
            self.assertIn("FAZER MINHA INSCRIÇÃO PELO WHATSAPP", unpriced)
            self.assertNotRegex(unpriced, r"R\$|6x de|Valor aumenta|pagar mais caro")

            for name, html in (("com-valor", priced), ("sem-valor", unpriced)):
                self.assertNotIn("variant:priced", html)
                parser = LocalReferences()
                parser.feed(html)
                whatsapp = [urlsplit(ref) for ref in parser.references if "wa.me/" in ref]
                self.assertTrue(whatsapp, name)
                for url in whatsapp:
                    self.assertEqual(url.path, "/5545999259973")
                    self.assertEqual(
                        parse_qs(url.query).get("text"),
                        ["Tenho interesse no TAPA 2.0 e gostaria de fazer minha inscrição"],
                    )
                for reference in parser.references:
                    url = urlsplit(reference)
                    if url.scheme or url.netloc or not url.path:
                        continue
                    path = (output / name / unquote(url.path)).resolve()
                    self.assertTrue(path.is_relative_to(output / name), reference)
                    self.assertTrue(path.is_file(), f"{name}: {reference}")
                css = (output / name / "style.css").read_text(encoding="utf-8")
                for reference in re.findall(r"url\(['\"]?([^)'\"]+)", css):
                    url = urlsplit(reference)
                    if url.scheme or url.netloc or url.path.startswith("data:"):
                        continue
                    self.assertTrue((output / name / unquote(url.path)).is_file(), reference)


if __name__ == "__main__":
    unittest.main()
