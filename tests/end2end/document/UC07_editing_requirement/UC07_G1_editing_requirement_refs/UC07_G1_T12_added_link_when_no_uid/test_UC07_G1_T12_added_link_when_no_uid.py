import os
import shutil

from selenium.webdriver.common.by import By
from seleniumbase import BaseCase

from tests.end2end.server import SDocTestServer

path_to_this_test_file_folder = os.path.dirname(os.path.abspath(__file__))


class Test_UC07_G1_T12_AddedLinkWhenNoUID(BaseCase):
    def test_01(self):
        path_to_sandbox = os.path.join(
            path_to_this_test_file_folder, ".sandbox"
        )

        test_server = SDocTestServer.create(path_to_sandbox)
        shutil.copyfile(
            os.path.join(path_to_this_test_file_folder, "document.sdoc"),
            os.path.join(path_to_sandbox, "document.sdoc"),
        )

        test_server.run()

        self.open(test_server.get_host_and_port())

        self.assert_text("Document 1")
        self.assert_text("PROJECT INDEX")

        self.click_link("DOC")

        self.assert_text("Hello world!")

        self.hover_and_click(
            hover_selector="(//sdoc-node)[2]",
            click_selector=(
                '(//sdoc-node)[2]//*[@data-testid="node-edit-action"]'
            ),
            hover_by=By.XPATH,
            click_by=By.XPATH,
        )

        self.click_xpath(
            "//a[@data-testid='requirement-add-parent-link-action']"
        )
        self.type(
            "(//*[@data-testid='requirement-parent-link-field'])[1]", "REQ-002"
        )

        self.click_xpath("//button[@type='submit' and text()='Save']")

        self.assert_text(
            "Requirement with parent links must have an UID. "
            "Either provide a parent UID, or "
            "delete the parent requirement links.",
        )