import unittest
from webshell_generator import get_behinder4_jsp_shell
from webshell_generator import get_behinder4_php_shell
from webshell_generator import get_behinder4_aspx_shell
from webshell_generator import get_godzilla_jsp_shell
from webshell_generator import get_godzilla_jspx_shell
from webshell_generator import get_godzilla_php_shell
from webshell_generator import get_godzilla_aspx_shell
from webshell_generator import get_godzilla_ashx_shell
from webshell_generator import get_define_class_shell


class TestBehinderWebshell(unittest.TestCase):

    def test_get_jsp_shell(self):
        webshell = get_behinder4_jsp_shell()
        self.assertEqual(webshell.tool, "behinder4")
        self.assertEqual(webshell.type, "jsp")
        self.assertEqual(webshell._pass, "rebeyond")
        self.assertEqual(webshell._key, None)
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_php_shell(self):
        webshell = get_behinder4_php_shell()
        self.assertEqual(webshell.tool, "behinder4")
        self.assertEqual(webshell.type, "php")
        self.assertEqual(webshell._pass, "rebeyond")
        self.assertEqual(webshell._key, None)
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_aspx_shell(self):
        webshell = get_behinder4_aspx_shell()
        self.assertEqual(webshell.tool, "behinder4")
        self.assertEqual(webshell.type, "aspx")
        self.assertEqual(webshell._pass, "rebeyond")
        self.assertEqual(webshell._key, None)
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)


class TestGodzillaWebshell(unittest.TestCase):

    def test_get_jsp_shell(self):
        webshell = get_godzilla_jsp_shell()
        print(webshell.content)
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "jsp")
        self.assertEqual(webshell._pass, "pass")
        self.assertEqual(webshell._key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_jspx_shell(self):
        webshell = get_godzilla_jspx_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "jspx")
        self.assertEqual(webshell._pass, "pass")
        self.assertEqual(webshell._key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_php_shell(self):
        webshell = get_godzilla_php_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "php")
        self.assertEqual(webshell._pass, "pass")
        self.assertEqual(webshell._key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_aspx_shell(self):
        webshell = get_godzilla_aspx_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "aspx")
        self.assertEqual(webshell._pass, "pass")
        self.assertEqual(webshell._key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_ashx_shell(self):
        webshell = get_godzilla_ashx_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "ashx")
        self.assertEqual(webshell._pass, "pass")
        self.assertEqual(webshell._key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_define_class_shell(self):
        webshell = get_define_class_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "jsp")
        self.assertEqual(webshell._pass, "PaSs")
        self.assertEqual(webshell._key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)
        self.assertTrue(len(webshell.shell_class) > 0)
        self.assertTrue(len(webshell.headers) > 0)


if __name__ == "__main__":
    unittest.main()
