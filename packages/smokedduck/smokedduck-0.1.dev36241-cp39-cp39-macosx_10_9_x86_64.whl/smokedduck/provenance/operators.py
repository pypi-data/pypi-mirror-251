from abc import ABC, abstractmethod

class Op(ABC):
    def __init__(self, query_id: int, op: str, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        self.single_op_table_name = f"LINEAGE_{query_id}_{op}_{op_id}_0"
        self.single_op_ksemi_name = f"LINEAGE_{query_id}_{op}_{op_id}_100"
        self.id = op_id
        self.is_root = parent_join_cond is None
        self.parent_join_cond = parent_join_cond
        self.is_agg_child = False
        
        self.extra = node.get('extra', '')
        self.join_type = ''
        self.parent_join_type = parent_join_type
        if "RIGHT" in self.extra:
            self.join_type = 'right'
        if len(self.parent_join_type) > 0:
            self.join_type = 'right'

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_from_string(self) -> str:
        pass

    @abstractmethod
    def get_child_join_conds(self) -> list:
        pass
    
    @abstractmethod
    def get_child_join_cond_type(self) -> str:
        pass

    @abstractmethod
    def get_out_index(self) -> str:
        pass

    @abstractmethod
    def get_in_index(self, cid) -> str:
        pass

class SingleOp(Op):
    def __init__(self, query_id: int, name: str, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, name, op_id, parent_join_cond, node, parent_join_type)

    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_from_string(self) -> str:
        if self.is_root:
            return self.single_op_table_name
        else:
            if self.is_agg_child:
                return "JOIN "  + self.single_op_table_name \
                    + " ON " + self.parent_join_cond + " = " + "0"
            elif self.parent_join_type == 'right':
                return "LEFT JOIN " + self.single_op_table_name \
                    + " ON " + self.parent_join_cond + " = " + self.single_op_table_name + ".out_index"
            else:
                return "JOIN " + self.single_op_table_name \
                    + " ON " + self.parent_join_cond + " = " + self.single_op_table_name + ".out_index"

    def get_child_join_conds(self) -> list:
        return [self.single_op_table_name + ".in_index"]
    
    def get_child_join_cond_type(self) -> str:
        return self.join_type

    def get_out_index(self) -> str:
        if self.is_agg_child:
            return "0 as out_index"
        return self.single_op_table_name + ".out_index"

    def get_in_index(self, cid) -> str:
        return self.single_op_table_name + ".in_index"

class Limit(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "LIMIT"

class ColScan(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "COLUMN_DATA_SCAN"



class StreamingLimit(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "STREAMING_LIMIT"


class Filter(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "FILTER"


class OrderBy(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "ORDER_BY"


class Projection(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "PROJECTION"


class TableScan(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "SEQ_SCAN"


class GroupBy(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

class HashGroupBy(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "HASH_GROUP_BY"


class PerfectHashGroupBy(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "PERFECT_HASH_GROUP_BY"


class StandardJoin(Op):
    def __init__(self, query_id: int, name: str, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, name, op_id, parent_join_cond, node, parent_join_type)

    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_child_join_conds(self) -> list:
        return [self.single_op_table_name + ".lhs_index", self.single_op_table_name + ".rhs_index"]
    
    def get_child_join_cond_type(self) -> str:
        return self.join_type

    def get_out_index(self) -> str:
        if self.is_agg_child:
            return "0 as out_index"
        return self.single_op_table_name + ".out_index"
    
    def get_in_index(self, cid) -> str:
        if cid == 0:
            return self.single_op_table_name + ".lhs_index"
        else:
            return self.single_op_table_name + ".rhs_index"

    def get_from_string(self) -> str:
        print("***** " , self.parent_join_type)
        if self.is_root:
            return  self.single_op_table_name
        elif self.is_agg_child:
            return "JOIN "  + self.single_op_table_name \
                + " ON " + self.parent_join_cond + " = " + "0"
        elif self.parent_join_type == 'right':
            return "LEFT JOIN " + self.single_op_table_name \
                    + " ON " + self.parent_join_cond + " = " + self.single_op_table_name + ".out_index"
        else:
            return "JOIN " + self.single_op_table_name \
                    + " ON " + self.parent_join_cond + " = " + self.single_op_table_name + ".out_index"


class HashJoin(StandardJoin):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "HASH_JOIN"
    

class BlockwiseNLJoin(StandardJoin):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "BLOCKWISE_NL_JOIN"


class PiecewiseMergeJoin(StandardJoin):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "PIECEWISE_MERGE_JOIN"


class CrossProduct(StandardJoin):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "CROSS_PRODUCT"


class NestedLoopJoin(StandardJoin):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "NESTED_LOOP_JOIN"

class UngroupedAggregate(SingleOp):
    def __init__(self, query_id: int, op_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> None:
        super().__init__(query_id, self.get_name(), op_id, parent_join_cond, node, parent_join_type)

    def get_name(self) -> str:
        return "UNGROUPED_AGGREGATE"

    def get_from_string(self) -> str:
        return ""

class OperatorFactory:
    def get_op(self, op_str: str, query_id: int, parent_join_cond: str, node: dict, parent_join_type: str) -> Op:
        op, op_id = op_str.rsplit("_", 1)
        if op == 'LIMIT':
            return Limit(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'STREAMING_LIMIT':
            return StreamingLimit(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'FILTER':
            return Filter(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'ORDER_BY':
            return OrderBy(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'PROJECTION':
            return Projection(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'SEQ_SCAN':
            return TableScan(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'HASH_GROUP_BY':
            return HashGroupBy(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'PERFECT_HASH_GROUP_BY':
            return PerfectHashGroupBy(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'HASH_JOIN':
            return HashJoin(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'BLOCKWISE_NL_JOIN':
            return BlockwiseNLJoin(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'PIECEWISE_MERGE_JOIN':
            return PiecewiseMergeJoin(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'CROSS_PRODUCT':
            return CrossProduct(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'NESTED_LOOP_JOIN':
            return NestedLoopJoin(query_id, op_id, parent_join_cond, node, parent_join_type)
        elif op == 'UNGROUPED_AGGREGATE':
            return UngroupedAggregate(query_id, op_id, parent_join_cond, node, parent_join_type)
        else:
            raise Exception('Found unhandled operator', op)
