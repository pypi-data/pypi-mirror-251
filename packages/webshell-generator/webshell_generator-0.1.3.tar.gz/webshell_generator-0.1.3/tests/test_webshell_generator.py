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
from webshell_generator import get_shell_result


class TestBehinderWebshell(unittest.TestCase):

    def test_get_jsp_shell(self):
        webshell = get_behinder4_jsp_shell()
        self.assertEqual(webshell.tool, "behinder4")
        self.assertEqual(webshell.type, "jsp")
        self.assertEqual(webshell.pas, "rebeyond")
        self.assertEqual(webshell.key, None)
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_php_shell(self):
        webshell = get_behinder4_php_shell()
        self.assertEqual(webshell.tool, "behinder4")
        self.assertEqual(webshell.type, "php")
        self.assertEqual(webshell.pas, "rebeyond")
        self.assertEqual(webshell.key, None)
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_aspx_shell(self):
        webshell = get_behinder4_aspx_shell()
        self.assertEqual(webshell.tool, "behinder4")
        self.assertEqual(webshell.type, "aspx")
        self.assertEqual(webshell.pas, "rebeyond")
        self.assertEqual(webshell.key, None)
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)


class TestGodzillaWebshell(unittest.TestCase):

    def test_get_jsp_shell(self):
        webshell = get_godzilla_jsp_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "jsp")
        self.assertEqual(webshell.pas, "pass")
        self.assertEqual(webshell.key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_jspx_shell(self):
        webshell = get_godzilla_jspx_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "jspx")
        self.assertEqual(webshell.pas, "pass")
        self.assertEqual(webshell.key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_php_shell(self):
        webshell = get_godzilla_php_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "php")
        self.assertEqual(webshell.pas, "pass")
        self.assertEqual(webshell.key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_aspx_shell(self):
        webshell = get_godzilla_aspx_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "aspx")
        self.assertEqual(webshell.pas, "pass")
        self.assertEqual(webshell.key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_get_ashx_shell(self):
        webshell = get_godzilla_ashx_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "ashx")
        self.assertEqual(webshell.pas, "pass")
        self.assertEqual(webshell.key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)

    def test_define_class_shell(self):
        webshell = get_define_class_shell()
        self.assertEqual(webshell.tool, "godzilla")
        self.assertEqual(webshell.type, "jsp")
        self.assertEqual(webshell.pas, "PaSs")
        self.assertEqual(webshell.key, "key")
        self.assertTrue(len(webshell.content) > 0)
        self.assertTrue(len(webshell.raw_content) > 0)
        self.assertTrue(len(webshell.shell_class) > 0)
        self.assertTrue(len(webshell.headers) > 0)


class TestWebshellResult(unittest.TestCase):

    def test_get_godzilla_jsp_shell_result(self):
        webshell = get_godzilla_jsp_shell()
        result = get_shell_result(webshell)
        print(result)
        self.assertEqual(result["tool"], "godzilla")
        self.assertEqual(result["mode"], "java_aes_base64")
        self.assertEqual(result["type"], "jsp")
        self.assertEqual(result["pas"], "pass")
        self.assertEqual(result["key"], "key")


if __name__ == "__main__":
    unittest.main()
