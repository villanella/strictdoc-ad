import os

from seleniumbase import BaseCase

from tests.end2end.server import SDocTestServer

path_to_this_test_file_folder = os.path.dirname(os.path.abspath(__file__))


class Test_02_CreatingDocumentWithEmptyPath(BaseCase):
    def test_01(self):
        path_to_sandbox = os.path.join(
            path_to_this_test_file_folder, ".sandbox"
        )

        test_server = SDocTestServer.create(path_to_sandbox)
        test_server.run()

        self.open("http://localhost:8001")
        self.save_screenshot_to_logs()

        self.assert_text("Project index")

        self.assert_text("The document tree has no documents yet.")

        self.click_link("Add document")

        self.type("#document_title", "Document 1")  # Empty document
        self.type("#document_path", "")

        self.click_xpath("//button[@type='submit' and text()='Save']")

        self.assert_text("Document path must not be empty.")