from typing import Dict, List

from strictdoc.backend.sdoc.models.document import Document
from strictdoc.backend.sdoc.models.requirement import Requirement
from strictdoc.backend.sdoc.models.section import Section
from strictdoc.core.analyzers.document_stats import (
    DocumentStats,
    DocumentTreeStats,
    SinglePrefixRequirements,
)
from strictdoc.core.document_iterator import DocumentCachingIterator
from strictdoc.core.traceability_index import TraceabilityIndex
from strictdoc.helpers.string import (
    extract_last_numeric_part,
    extract_numeric_uid_prefix_part,
)


class DocumentUIDAnalyzer:
    @staticmethod
    def analyze_document_tree(traceability_index: TraceabilityIndex):
        global_requirements_per_prefix: Dict[str, SinglePrefixRequirements] = {}
        document_tree_stats: List[DocumentStats] = []

        for document in traceability_index.document_tree.document_list:
            document_stats: DocumentStats = (
                DocumentUIDAnalyzer.analyze_document(document)
            )
            for (
                requirement_prefix_,
                prefix_requirements_,
            ) in document_stats.requirements_per_prefix.items():
                global_prefix_requirements = (
                    global_requirements_per_prefix.setdefault(
                        requirement_prefix_, SinglePrefixRequirements()
                    )
                )
                global_prefix_requirements.requirements_no_uid.extend(
                    prefix_requirements_.requirements_no_uid
                )
                global_prefix_requirements.requirements_uid_numbers.extend(
                    prefix_requirements_.requirements_uid_numbers
                )
            document_tree_stats.append(document_stats)

        return DocumentTreeStats(
            single_document_stats=document_tree_stats,
            requirements_per_prefix=global_requirements_per_prefix,
        )

    @staticmethod
    def analyze_document(
        document: Document,
    ) -> DocumentStats:
        this_document_stats = DocumentStats(document)
        document_iterator = DocumentCachingIterator(document)
        for node in document_iterator.all_content():
            if isinstance(node, Section):
                if node.reserved_uid is None:
                    this_document_stats.sections_without_uid.append(node)
                continue
            if not isinstance(node, Requirement):
                continue
            requirement: Requirement = node
            requirement_parent_prefix: str = (
                requirement.get_requirement_prefix()
            )

            if (
                requirement_parent_prefix
                not in this_document_stats.requirements_per_prefix
            ):
                this_document_stats.requirements_per_prefix[
                    requirement_parent_prefix
                ] = SinglePrefixRequirements()

            prefix_requirements: SinglePrefixRequirements = (
                this_document_stats.requirements_per_prefix[
                    requirement_parent_prefix
                ]
            )
            if requirement.reserved_uid is None:
                prefix_requirements.requirements_no_uid.append(requirement)
            else:
                requirement_prefix = extract_numeric_uid_prefix_part(
                    requirement.reserved_uid
                )

                # If the requirement has a prefix which is different to that of
                # the parent section/document's prefix, we ignore this node as
                # incredible for contributing to the next UID calculation.
                if requirement_prefix != requirement_parent_prefix:
                    continue

                requirement_uid_numeric_part = extract_last_numeric_part(
                    requirement.reserved_uid
                )
                assert len(requirement_uid_numeric_part) > 0
                requirement_uid_number = int(requirement_uid_numeric_part)

                prefix_requirements.requirements_uid_numbers.append(
                    requirement_uid_number
                )

        return this_document_stats
