import uuid
from typing import List, Optional

from strictdoc.backend.sdoc.document_reference import DocumentReference
from strictdoc.backend.sdoc.models.free_text import FreeText
from strictdoc.backend.sdoc.models.node import Node
from strictdoc.helpers.auto_described import auto_described


@auto_described
class SectionContext:
    def __init__(self):
        self.title_number_string = None


@auto_described
class Section(Node):  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent,
        uid,
        custom_level: Optional[str],
        title,
        free_texts: List[FreeText],
        section_contents: List[Node],
    ):
        self.parent = parent
        # TODO: Remove .uid, keep reserved_uid only.
        self.uid = uid
        self.reserved_uid = uid
        self.title = title

        self.free_texts: List[FreeText] = free_texts
        self.section_contents = section_contents

        # HEF4
        self.custom_level: Optional[str] = custom_level
        self.ng_resolved_custom_level: Optional[str] = custom_level

        self.ng_level: Optional[int] = None
        self.ng_has_requirements = False
        self.ng_document_reference: Optional[DocumentReference] = None
        self.context = SectionContext()
        self.node_id = uuid.uuid4().hex

    @property
    def document(self):
        return self.ng_document_reference.get_document()

    @property
    def is_requirement(self):
        return False

    @property
    def is_composite_requirement(self):
        return False

    @property
    def is_section(self):
        return True
