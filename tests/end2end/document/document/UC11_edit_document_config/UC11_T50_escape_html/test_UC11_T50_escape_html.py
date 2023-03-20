from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.helpers.screens.document.form_edit_config import (
    Form_EditConfig,
)
from tests.end2end.helpers.screens.document_tree.screen_document_tree import (
    Screen_DocumentTree,
)
from tests.end2end.server import SDocTestServer


class Test_UC11_T50_EscapeHTML(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            screen_document_tree = Screen_DocumentTree(self)

            screen_document_tree.assert_on_screen()
            screen_document_tree.assert_contains_document("Document 1")

            screen_document = screen_document_tree.do_click_on_first_document()

            screen_document.assert_on_screen_document()
            screen_document.assert_text("Link does not get corrupted")

            root_node = screen_document.get_root_node()
            form_config: Form_EditConfig = root_node.do_open_form_edit_config()

            form_config.assert_document_abstract_contains(
                "`Link does not get corrupted "
                "<https://github.com/strictdoc-project/"
                "sphinx-latex-reqspec-template>`_"
            )

            form_config.do_form_submit()

            root_node.assert_document_abstract_contains(
                "Link does not get corrupted\n"
                "Link does not get corrupted\n"
                "Link does not get corrupted\n"
            )

        assert test_setup.compare_sandbox_and_expected_output()