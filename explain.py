import psycopg2
from PyQt5.QtWidgets import *
import json
import re
from typing import List

"""
CursorManager to handle all transactions with postgres
"""


class CursorManager(object):
    def __init__(self):
        self._CONFIG_PATH = "./config.json"
        try:
            with open(self._CONFIG_PATH, "r") as f:
                config = json.load(f)
        except FileNotFoundError as e:
            raise e

        self._config = config["TPC-H"]
        self.conn = None
        self.cursor = None

        self.__connect__()

    def __connect__(self):
        try:
            self.conn = psycopg2.connect(
                host=self._config["host"],
                dbname=self._config["dbname"],
                user=self._config["user"],
                password=self._config["pwd"],
                port=self._config["port"],
            )
            self.cursor = self.conn.cursor()

        except Exception as e:
            print(f"Connection attempt failed with error: {e}")

    def get_cursor(self):
        return self.cursor

    def close(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except Exception as e:
            print(f"Cursor failed to close with error: {e}")

    def get_QEP(self, query: str):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Cursor failed to execute query with error: {e}")
            return []


class QEP_Node:
    def __init__(self, indent_size: int, operation: str, details: str):
        self.indent_size = indent_size
        self.operation = operation
        self.details = details
        self.parent = None
        self.children = []
        self.explanation = []


class QEP_Tree:
    def __init__(self):
        self.root = None
        self.prev_indent_size = 0

    """
    Builds the QEP tree and returns the root node
    """

    def build(self, plan) -> QEP_Node:
        cur_node = None
        node = None
        indent_size = 0
        operation = ""
        details = None
        for row in plan:
            cur_row = row[0]

            # if this condition satisfies then this is the root node
            if "->" not in cur_row and "cost=" in cur_row:
                if self.root == None:
                    match = re.match(r"^(.+)\s\s(.+)$", cur_row)
                    node = QEP_Node(0, match.group(1).strip(), match.group(2))
                    self.root = node
                    self.root.parent = self.root
                    cur_node = self.root
                    self.prev_indent_size = 0

            # If the row has '->' in it, then it is considered an operation in the QEP
            # Process the rows with '->' and extract relevant information such as the
            # operation, depth, and details (explanation)
            # Indent size is used to determine if 2 nodes are on the same level
            if "->" in cur_row:
                match = re.match(r"(\s*->)?\s*(\w.*)\s+\((.*)\)$", cur_row)
                indent_size = len(match.group(1))
                operation = match.group(2).replace("Parallel", "")
                details = match.group(3)

                node = QEP_Node(indent_size, operation.strip(), details)

                if self.root == None:
                    self.root = node
                    self.root.parent = self.root
                    cur_node = self.root
                    self.prev_indent_size = indent_size
                    continue

                # node is on the same level
                # get the parent node and attach it as its child
                if self.prev_indent_size == indent_size:
                    parent = cur_node.parent
                    node.parent = parent
                    parent.children.append(node)
                else:
                    node.parent = cur_node
                    cur_node.children.append(node)
            # Row is an explanation row (without '->')
            # Attach the explanations to the explanation list in the node
            else:
                if "Workers Planned" not in cur_row:
                    explain_results = self.transformRawExplainToNaturalLanguage(cur_row)
                else:
                    explain_results = ""

                if explain_results == None or explain_results == "":
                    continue

                node.explanation.append(explain_results)

            # Update the current node pointer
            self.prev_indent_size = indent_size
            cur_node = node

        return self.root

    """
    Transform the raw explanation from postgres
    into a more refined natural language representation
    """

    def transformRawExplainToNaturalLanguage(self, raw_explain: List[str]) -> str:
        match = re.match(r"(.*):\s(.*)", raw_explain)
        if match:
            keyword = match.group(1).strip()
            condition = match.group(2).strip()
            condition_match = re.match(r"^([^\(])+", condition)
            if condition_match:
                condition = condition_match.group(0).strip()
                if condition.strip()[:-1] == ",":
                    condition = condition[:-1]

            return f"{keyword} on {condition}"

    def joinExplanationList(self, explanation_list: List[str]) -> str:
        return " and ".join(explanation_list)

    """
    Prints the tree recursively using 
    pre order traversal for debugging purposes
    """

    def print_tree(self, node: QEP_Node):
        if node == None:
            return

        print(" " * node.indent_size, "-> " + node.operation)
        if node.explanation:
            print(" " * (node.indent_size + 1), node.explanation)

        for child in node.children:
            self.print_tree(child)

    def get_visual_plan(self, node: QEP_Node, planList: List[str]) -> List[str]:
        if node == None:
            return

        planList.append(" " * node.indent_size + "-> " + node.operation)

        for child in node.children:
            self.get_visual_plan(child, planList)

        return planList

    """
    Traverses the QEP tree by specifying the root node of the particular tree
    recursively using post order traversal to get the steps and explanation
    for the tree
    Returns a list of explanations of each step
    """

    def get_explanation(self, node: QEP_Node, resultList=[]) -> List[str]:
        if node == None:
            return []

        for child in node.children:
            self.get_explanation(child, resultList)

        operation = node.operation
        explanation = (
            node.explanation
            if node.explanation != [] and node.explanation != None
            else ""
        )

        if explanation == "":
            result = f"Step {len(resultList) + 1}: Perform {operation}"
        else:
            result = f"Step {len(resultList) + 1}: Perform {operation} with {self.joinExplanationList(explanation)}"

        resultList.append(result)

        return resultList

    """
    Compares 2 QEP trees by taking each tree's root node as argument
    Traverses both trees to generate a queue of steps for each tree
    Uses these queues to compare the actions taken by each tree
    Returns a list of comparisons
    """

    def compareQEP(self, node1: QEP_Node, node2: QEP_Node) -> List[str]:
        def get_node_queue(node: QEP_Node, queue: List[QEP_Node]) -> List[QEP_Node]:
            if node == None:
                return

            for child in node.children:
                get_node_queue(child, queue)

            queue.append(node)

            return queue

        q1Queue = get_node_queue(node1, [])
        q2Queue = get_node_queue(node2, [])

        compareList = []
        q1Pointer = q2Pointer = 0
        while q1Pointer < len(q1Queue) and q2Pointer < len(q2Queue):
            operationQ1 = q1Queue[q1Pointer].operation
            explanationQ1 = q1Queue[q1Pointer].explanation
            operationQ2 = q2Queue[q2Pointer].operation
            explanationQ2 = q2Queue[q2Pointer].explanation
            step = min(q1Pointer + 1, q2Pointer + 1)
            if operationQ1 == operationQ2 and explanationQ1 == explanationQ2:
                if not explanationQ1:
                    compareExplanation = f"Step {step}: Both queries perform the same operations at this step executing a {operationQ1}."
                else:
                    compareExplanation = f"Step {step}: Both queries perform the same operations at this step executing a {operationQ1} with {self.joinExplanationList(explanationQ1)}."
            elif operationQ1 == operationQ2 and explanationQ1 != explanationQ2:
                if not explanationQ1:
                    compareExplanation = f"Step {step}: Both queries perform the same operations at this step executing a {operationQ1}. However, Q2 has an additional condition to {self.joinExplanationList(explanationQ2)} while Q1 is just performing a basic {operationQ1}."
                else:
                    compareExplanation = f"Step {step}: Both queries perform the same operations at this step executing a {operationQ1}. However, Q1 has an additional condition to {self.joinExplanationList(explanationQ1)} while Q2 is just performing a basic {operationQ2}."
            elif operationQ1 != operationQ2:
                if explanationQ1 and explanationQ2:
                    compareExplanation = f"Step {step}: Both queries are performing different operations at this step, with Q1 executing a {operationQ1} with {self.joinExplanationList(explanationQ1)} and Q2 executing a {operationQ2} with {self.joinExplanationList(explanationQ2)}."
                elif explanationQ1 and not explanationQ2:
                    compareExplanation = f"Step {step}: Both queries are performing different operations at this step, with Q1 executing a {operationQ1} with {self.joinExplanationList(explanationQ1)} and Q2 executing a {operationQ2}."
                elif not explanationQ1 and explanationQ2:
                    compareExplanation = f"Step {step}: Both queries are performing different operations at this step, with Q1 executing a {operationQ1} and Q2 executing a {operationQ2} with {self.joinExplanationList(explanationQ2)}."

            compareList.append(compareExplanation)
            q1Pointer += 1
            q2Pointer += 1

        line = (
            "Additional steps taken for Q1"
            if q1Pointer < len(q1Queue)
            else "Additional steps taken for Q2"
        )
        compareList.append(line)

        while q1Pointer < len(q1Queue):
            operation = q1Queue[q1Pointer].operation
            explanation = q1Queue[q1Pointer].explanation
            step = q1Pointer + 1
            if explanation:
                compareExplanation = f"Step {step}: Q1 executes {operation} due to {self.joinExplanationList(explanation)} which doesn't exist in Q2"
            else:
                compareExplanation = f"Step {step}: Q1 executes {operation}"
            compareList.append(compareExplanation)
            q1Pointer += 1

        while q2Pointer < len(q2Queue):
            operation = q2Queue[q2Pointer].operation
            explanation = q2Queue[q2Pointer].explanation
            step = q2Pointer + 1
            if explanation:
                compareExplanation = f"Step {step}: Q2 executes {operation} due to {self.joinExplanationList(explanation)} which doesn't exist in Q1"
            else:
                compareExplanation = f"Step {step}: Q2 executes {operation}"
            compareList.append(compareExplanation)
            q2Pointer += 1

        return compareList


class Explain:
    def __init__(self, interface, cursorManager: CursorManager):
        self.interface = interface
        self.cursorManager = cursorManager
        self.cursor = self.cursorManager.get_cursor()
        self.updateSchema()

    def updateSchema(self):
        try:
            query = "SELECT table_name, column_name, data_type, character_maximum_length as length FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name, ordinal_position"
            self.cursor.execute(query)
            response = self.cursor.fetchall()

            # Parse response stored in dictionary
            schema = {}
            for item in response:
                # Columns are table name, column name, data type, length
                attrs = schema.get(item[0], [])
                attrs.append(item[1])
                schema[item[0]] = attrs

            # To log our database
            print("Database schema as follows: ")
            for t, table in enumerate(schema):
                print(t + 1, table, schema.get(table))

            self.interface.setSchema(schema)
        except Exception as e:
            print(str(e))
            print("Retrieval of Schema information is unsuccessful!")

    """
    Returns the visual plan in a List[str] format
    """

    def get_visual_plan(self, node: QEP_Node) -> List[str]:
        return QEP_Tree().get_visual_plan(node)

    """
    Builds the QEP tree by first getting the plan from postgres
    Then builds the tree using the QEP_Tree class
    Returns the root node of the QEP tree
    """

    def build_QEP_tree(self, query: str) -> QEP_Node:
        plan = self.cursorManager.get_QEP("explain " + query)
        return QEP_Tree().build(plan)

    """
    Gets the explanation for the specified QEP tree
    by passing in the root node of the specified tree
    as an argument
    Returns the arguments in a list
    """

    def get_QEP_explanation(self, node: QEP_Node) -> List[str]:
        return QEP_Tree().get_explanation(node)

    """
    Gets the comparisons for the specifed QEP trees by passing each tree's root
    node as arguments
    Returns the comparisons in a list
    """

    def get_QEP_comparison(self, node1: QEP_Node, node2: QEP_Node) -> List[str]:
        return QEP_Tree().compareQEP(node1, node2)


if __name__ == "__main__":
    cursorManager = CursorManager()
    plan1 = cursorManager.get_QEP(
        r"explain select * from customer C, orders O where C.c_custkey = O.o_custkey"
    )
    plan2 = cursorManager.get_QEP(
        r"EXPLAIN select * from customer C, orders O where C.c_custkey = O.o_custkey and C.c_name like '%cheng'",
    )

    # plan1 = cursorManager.get_QEP(
    #     r"""explain select
    #   ps_partkey,
    #   sum(ps_supplycost * ps_availqty) as value
    # from
    #   partsupp,
    #   supplier,
    #   nation
    # where
    #   ps_suppkey = s_suppkey
    #   and s_nationkey = n_nationkey
    #   and n_name = 'GERMANY'
    #   and ps_supplycost > 20
    #   and s_acctbal > 10
    # group by
    #   ps_partkey having
    #     sum(ps_supplycost * ps_availqty) > (
    #       select
    #         sum(ps_supplycost * ps_availqty) * 0.0001000000
    #       from
    #         partsupp,
    #         supplier,
    #         nation
    #       where
    #         ps_suppkey = s_suppkey
    #         and s_nationkey = n_nationkey
    #         and n_name = 'GERMANY'
    #     )
    # order by
    #   value desc;"""
    # )

    # plan2 = cursorManager.get_QEP(
    #     r"""
    #     explain select
    #   l_returnflag,
    #   l_linestatus,
    #   sum(l_quantity) as sum_qty,
    #   sum(l_extendedprice) as sum_base_price,
    #   sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
    #   sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
    #   avg(l_quantity) as avg_qty,
    #   avg(l_extendedprice) as avg_price,
    #   avg(l_discount) as avg_disc,
    #   count(*) as count_order
    # from
    #   lineitem
    # where
    #   l_extendedprice > 100
    # group by
    #   l_returnflag,
    #   l_linestatus
    # order by
    #   l_returnflag,
    #   l_linestatus;
    #     """
    # )

    qep1 = QEP_Tree().build(plan1)
    qep2 = QEP_Tree().build(plan2)
    qep1_explain = QEP_Tree().get_explanation(qep1, [])
    qep2_explain = QEP_Tree().get_explanation(qep2, [])
    comparison = QEP_Tree().compareQEP(qep1, qep2)

    print("QEP1 Explain")
    for explain in qep1_explain:
        print(explain)

    print("\nQEP2 Explain")
    for explain in qep2_explain:
        print(explain)

    print("\nCompare QEP")
    for compare in comparison:
        print(compare)

    visual_plan = QEP_Tree().get_visual_plan(qep1, [])
    for r in visual_plan:
        print(r)
