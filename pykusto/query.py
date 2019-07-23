from abc import abstractmethod
from enum import Enum
from itertools import chain
from typing import Tuple, List, Union, Optional

from azure.kusto.data.helpers import dataframe_from_result_table

from pykusto.assignments import AssigmentBase, AssignmentToSingleColumn, AssignmentFromAggregationToColumn, \
    AssignmentFromGroupExpressionToColumn
from pykusto.column import Column
from pykusto.expressions import BooleanType, ExpressionType, AggregationExpression, GroupExpression
from pykusto.tables import Table
from pykusto.utils import KQL, logger


class Order(Enum):
    ASC = "asc"
    DESC = "desc"


class Nulls(Enum):
    FIRST = "first"
    LAST = "last"


class JoinKind(Enum):
    INNERUNIQUE = "innerunique"
    INNER = "inner"
    LEFTOUTER = "leftouter"
    RIGHTOUTER = "rightouter"
    FULLOUTER = "fullouter"
    LEFTANTI = "leftanti"
    ANTI = "anti"
    LEFTANTISEMI = "leftantisemi"
    RIGHTANTI = "rightanti"
    RIGHTANTISEMI = "rightantisemi"
    LEFTSEMI = "leftsemi"
    RIGHTSEMI = "rightsemi"


class Query:
    _head: Optional['Query']
    _table: Optional[Table]

    def __init__(self, head=None) -> None:
        self._head = head if isinstance(head, Query) else None
        self._table = head if isinstance(head, Table) else None

    def where(self, predicate: BooleanType) -> 'WhereQuery':
        return WhereQuery(self, predicate)

    def take(self, num_rows: int) -> 'TakeQuery':
        return TakeQuery(self, num_rows)

    def limit(self, num_rows: int) -> 'LimitQuery':
        return LimitQuery(self, num_rows)

    def sample(self, num_rows: int) -> 'SampleQuery':
        return SampleQuery(self, num_rows)

    def count(self) -> 'CountQuery':
        return CountQuery(self)

    def sort_by(self, col: Column, order: Order = None, nulls: Nulls = None) -> 'SortQuery':
        return SortQuery(self, col, order, nulls)

    def join(self, query: 'Query', kind: JoinKind = None):
        return JoinQuery(self, query, kind)

    def project(self, *args: Union[Column, AssigmentBase], **kwargs: ExpressionType) -> 'ProjectQuery':
        """
        Note: doesn't support autogenerated column names
        """
        columns: List[Column] = []
        assignments: List[AssigmentBase] = []
        for arg in args:
            if isinstance(arg, Column):
                columns.append(arg)
            elif isinstance(arg, AssigmentBase):
                assignments.append(arg)
            else:
                raise ValueError("Invalid assignment: " + arg.to_kql())
        for column_name, expression in kwargs.items():
            assignments.append(AssignmentToSingleColumn(Column(column_name), expression))
        return ProjectQuery(self, columns, assignments)

    def extend(self, *args: AssigmentBase, **kwargs: ExpressionType) -> 'ExtendQuery':
        """
        Note: doesn't support autogenerated column names
        """
        assignments: List[AssigmentBase] = list(args)
        for column_name, expression in kwargs.items():
            assignments.append(AssignmentToSingleColumn(Column(column_name), expression))
        return ExtendQuery(self, *assignments)

    def summarize(self, *args: Union[AggregationExpression, AssignmentFromAggregationToColumn],
                  **kwargs: AggregationExpression) -> 'SummarizeQuery':
        aggs: List[AggregationExpression] = []
        assignments: List[AssignmentFromAggregationToColumn] = []
        for arg in args:
            if isinstance(arg, AggregationExpression):
                aggs.append(arg)
            elif isinstance(arg, AssignmentFromAggregationToColumn):
                assignments.append(arg)
            else:
                raise ValueError("Invalid assignment: " + arg.to_kql())
        for column_name, agg in kwargs.items():
            assignments.append(AssignmentFromAggregationToColumn(Column(column_name), agg))
        return SummarizeQuery(self, aggs, assignments)

    @abstractmethod
    def _compile(self) -> KQL:
        pass

    def _compile_all(self) -> KQL:
        if self._head is None:
            if self._table is None:
                return KQL("")
            else:
                return self._table.table
        else:
            return KQL("{} | {}".format(self._head._compile_all(), self._compile()))

    def get_table(self):
        if self._head is None:
            return self._table
        else:
            return self._head.get_table()

    def render(self) -> KQL:
        result = self._compile_all()
        logger.debug("Complied query: " + result)
        return result

    def execute(self, table: Table = None):
        if self.get_table() is None:
            if table is None:
                raise RuntimeError("No table supplied")
            rendered_query = table.table + self.render()
        else:
            if table is not None:
                raise RuntimeError("This table is already bound to a query")
            table = self.get_table()
            rendered_query = self.render()

        logger.debug("Running query: " + rendered_query)
        return table.execute(rendered_query)

    def execute_to_dataframe(self, table: Table = None):
        res = self.execute(table)
        return dataframe_from_result_table(res.primary_results[0])


class ProjectQuery(Query):
    _columns: List[Column]
    _assignments: List[AssigmentBase]

    def __init__(self, head: 'Query', columns: List[Column], assignments: List[AssigmentBase]) -> None:
        super().__init__(head)
        self._columns = columns
        self._assignments = assignments

    def _compile(self) -> KQL:
        return KQL('project {}'.format(', '.join(chain(
            (c.kql for c in self._columns),
            (a.to_kql() for a in self._assignments)
        ))))


class ExtendQuery(Query):
    _assignments: Tuple[AssigmentBase, ...]

    def __init__(self, head: 'Query', *assignments: AssigmentBase) -> None:
        super().__init__(head)
        self._assignments = assignments

    def _compile(self) -> KQL:
        return KQL('extend {}'.format(', '.join(a.to_kql() for a in self._assignments)))


class WhereQuery(Query):
    _predicate: BooleanType

    def __init__(self, head: Query, predicate: BooleanType):
        super(WhereQuery, self).__init__(head)
        self._predicate = predicate

    def _compile(self) -> KQL:
        return KQL('where {}'.format(self._predicate.kql))


class SingleNumberQuery(Query):
    _num_rows: int
    _query_name: str

    def __init__(self, head: Query, query_name: str, num_rows: int):
        super(SingleNumberQuery, self).__init__(head)
        self._query_name = query_name
        self._num_rows = num_rows

    def _compile(self) -> KQL:
        return KQL('{} {}'.format(self._query_name, self._num_rows))


class TakeQuery(SingleNumberQuery):
    _num_rows: int

    def __init__(self, head: Query, num_rows: int):
        super(TakeQuery, self).__init__(head, 'take', num_rows)


class LimitQuery(SingleNumberQuery):
    _num_rows: int

    def __init__(self, head: Query, num_rows: int):
        super(LimitQuery, self).__init__(head, 'limit', num_rows)


class SampleQuery(SingleNumberQuery):
    _num_rows: int

    def __init__(self, head: Query, num_rows: int):
        super(SampleQuery, self).__init__(head, 'sample', num_rows)


class CountQuery(Query):
    _num_rows: int

    def __init__(self, head: Query):
        super(CountQuery, self).__init__(head)

    def _compile(self) -> KQL:
        return KQL('count')


class SortQuery(Query):
    _col: Column
    _order: Order
    _nulls: Nulls

    def __init__(self, head: Query, col: Column, order: Order, nulls: Nulls):
        super(SortQuery, self).__init__(head)
        self._col = col
        self._order = order
        self._nulls = nulls

    def _compile(self) -> KQL:
        result = 'sort by {}'.format(self._col.kql, self._order.value)
        if self._order is not None:
            result += " " + str(self._order.value)
        if self._nulls is not None:
            result += " nulls " + str(self._nulls.value)
        return KQL(result)


class JoinException(Exception):
    pass


class JoinQuery(Query):
    _joined_query: Query
    _kind: JoinKind
    _on_attributes: Tuple[Tuple[Column, ...], ...]

    def __init__(self, head: Query, joined_query: Query, kind: JoinKind,
                 on_attributes: Tuple[Tuple[Column, ...], ...] = tuple()):
        super(JoinQuery, self).__init__(head)
        self._joined_query = joined_query
        self._kind = kind
        self._on_attributes = on_attributes

    def on(self, col1: Column, col2: Column = None) -> 'JoinQuery':
        self._on_attributes = self._on_attributes + (((col1,),) if col2 is None else ((col1, col2),))
        return self

    @staticmethod
    def _compile_on_attribute(attribute: Tuple[Column]):
        assert len(attribute) in (1, 2)
        if len(attribute) == 1:
            return attribute[0].kql
        else:
            return "$left.{}==$right.{}".format(attribute[0].kql, attribute[1].kql)

    def _compile(self) -> KQL:
        if len(self._on_attributes) == 0:
            raise JoinException("A call to join() must be followed by a call to on()")
        if self._joined_query.get_table() is None:
            raise JoinException("The joined query must have a table")

        return KQL("join {} ({}) on {}".format(
            "" if self._kind is None else "kind={}".format(self._kind.value),
            self._joined_query.render(),
            ", ".join([self._compile_on_attribute(attr) for attr in self._on_attributes])))


class SummarizeQuery(Query):
    _aggs: List[AggregationExpression] = []
    _assignments: List[AssignmentFromAggregationToColumn] = []
    _by_columns: List[Union[Column, GroupExpression]] = []
    _by_assignments: List[AssignmentFromGroupExpressionToColumn] = []

    def __init__(self, head: Query, aggs: List[AggregationExpression],
                 assignments: List[AssignmentFromAggregationToColumn]):
        super(SummarizeQuery, self).__init__(head)
        self._aggs = aggs
        self._assignments = assignments

    def by(self, *args: Union[AssignmentFromGroupExpressionToColumn, Column, GroupExpression],
           **kwargs: GroupExpression):
        for arg in args:
            if isinstance(arg, Column) or isinstance(arg, GroupExpression):
                self._by_columns.append(arg)
            elif isinstance(arg, AssignmentFromGroupExpressionToColumn):
                self._by_assignments.append(arg)
            else:
                raise ValueError("Invalid assignment: " + arg.to_kql())
        for column_name, group_exp in kwargs.items():
            self._by_assignments.append(AssignmentFromGroupExpressionToColumn(Column(column_name), group_exp))
        return self

    def _compile(self) -> KQL:
        result = 'summarize {}'.format(', '.join(chain(
            (c.kql for c in self._aggs),
            (a.to_kql() for a in self._assignments)
        )))
        if len(self._by_assignments) != 0 or len(self._by_columns) != 0:
            result += ' by {}'.format(', '.join(chain(
                (c.kql for c in self._by_columns),
                (a.to_kql() for a in self._by_assignments)
            )))
        return KQL(result)
