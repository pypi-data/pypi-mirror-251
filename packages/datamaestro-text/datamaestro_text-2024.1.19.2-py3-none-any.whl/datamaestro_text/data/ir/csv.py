from pathlib import Path
from typing import Iterator, Tuple

from experimaestro import Param, Option, Constant, Meta
from datamaestro.definitions import argument
import datamaestro_text.data.ir as ir
from datamaestro_text.data.ir.base import GenericTopic
from datamaestro_text.interfaces.plaintext import read_tsv


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
class AdhocRunWithText(ir.AdhocRun):
    "(qid, doc.id, query, passage)"
    pass


@argument("path", type=Path)
@argument("separator", type=str, default="\t", ignored=True)
class Topics(ir.Topics):
    "Pairs of query id - query using a separator"

    def iter(self):
        return (GenericTopic(qid, title) for qid, title in read_tsv(self.path))


class Documents(ir.Documents):
    "One line per document, format pid<SEP>text"

    path: Param[Path]
    separator: Meta[str] = "\t"

    pass


class TrainingTripletsID(ir.TrainingTripletsLines):
    """Training triplets (query/document IDs only)

    Attributes:
        separator: Field separator
        documents: The documents
        topics: The topics
        ids: Whether documents are IDs or full text
    """

    separator: Option[str] = "\t"
    documents: Param[ir.Documents]
    topics: Param[ir.Topics]
    ids: Constant[bool] = True

    def iter(self) -> Iterator[Tuple[str, str, str]]:
        queries = {}
        for query in self.topics.iter():
            queries[query.get_id()] = query.get_text()

        for qid, pos, neg in read_tsv(self.path):
            yield queries[qid], pos, neg


class TrainingTriplets(ir.TrainingTriplets):
    "Training triplets (full text)"
    path: Param[Path]
    separator: Meta[str] = "\t"
    ids: Constant[bool] = True

    def iter(self) -> Iterator[Tuple[str, str, str]]:
        yield from read_tsv(self.path)
