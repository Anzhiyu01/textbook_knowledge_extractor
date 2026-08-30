import json, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'skill' / 'textbook-knowledge-extractor' / 'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from output_naming import slugify, package_name, next_available
from check_math_rendering import check_markdown
from experiments import validate_config
from import_results import import_result

class V24Tests(unittest.TestCase):
    def test_naming_and_collision(self):
        self.assertEqual(slugify('Linear Algebra Done Right: Clear.md'), 'linear_algebra_done_right_clear_md')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/'extraction_x_chapter_1'; p.mkdir(); (p/'x').write_text('x')
            self.assertTrue(next_available(root,p.name).name.endswith('_run_2'))
    def test_math(self):
        self.assertFalse(check_markdown('Price $10 and $20\n'))
        self.assertTrue(check_markdown('\\mathbf R'))
        self.assertFalse(check_markdown('inline $x$\n'))
        self.assertTrue(check_markdown('$$x$$\n'))
        self.assertTrue(check_markdown('a_b\n'))
    def test_config(self):
        self.assertFalse(validate_config({'model':'x','reasoning_effort':'not_configurable','trials':3}))

if __name__ == '__main__': unittest.main()
