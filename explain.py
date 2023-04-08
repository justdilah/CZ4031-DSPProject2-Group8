import psycopg2
from PyQt5.QtWidgets import *
import json
import re
from typing import List


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

    def get_QEP(self, cursor, query: str):
        try:
            cursor.execute(query)
            return cursor.fetchall()
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

    # builds the QEP tree and returns the root node
    def build(self, plan) -> QEP_Node:
        cur_node = None
        node = None
        indent_size = 0
        operation = ""
        details = None
        for row in plan:
            cur_row = row[0]

            # if this condition satisfies then this is the root node
            if "->" not in cur_row and "Gather" not in cur_row and "cost=" in cur_row:
                if self.root == None:
                    match = re.match(r"^(.+)\s\s(.+)$", cur_row)
                    node = QEP_Node(0, match.group(1).strip(), match.group(2))
                    self.root = node
                    self.root.parent = self.root
                    cur_node = self.root
                    self.prev_indent_size = 0

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
                if self.prev_indent_size == indent_size:
                    parent = cur_node.parent
                    node.parent = parent
                    parent.children.append(node)
                else:
                    node.parent = cur_node
                    cur_node.children.append(node)
            else:
                if "Workers Planned" not in cur_row:
                    explain_results = self.transformRawExplainToNaturalLanguage(cur_row)
                else:
                    explain_results = ""

                if explain_results == None or explain_results == "":
                    continue

                node.explanation.append(explain_results)

            self.prev_indent_size = indent_size
            cur_node = node

        return self.root

    def transformRawExplainToNaturalLanguage(self, raw_explain: List[str]) -> str:
        match = re.match(r"(.*):\s(.*)", raw_explain)
        if match:
            keyword = match.group(1).strip()
            condition = match.group(2).strip()
            condition_match = re.match(r"^([^\(])+", condition)
            if condition_match:
                condition = condition_match.group(0).strip()
                if condition[:-1] == ",":
                    condition = condition[:-1]

            return f"{keyword} on {condition}"

    # for now prints the tree
    # later will need to adapt this to create the visuals
    def print_tree(self, node: QEP_Node):
        if node == None:
            return

        print(" " * node.indent_size, "-> " + node.operation)
        if node.explanation:
            print(" " * (node.indent_size + 1), node.explanation)

        for child in node.children:
            self.print_tree(child)

    def get_explanation(self, node: QEP_Node, resultList=[]) -> List[str]:
        if node == None:
            return []

        for child in node.children:
            self.get_explanation(child, resultList)

        # print(node.operation)

        operation = node.operation
        explanation = (
            node.explanation
            if node.explanation != [] and node.explanation != None
            else ""
        )

        if explanation == "":
            result = f"Step {len(resultList) + 1}: Perform {operation}"
        else:
            result = f"Step {len(resultList) + 1}: Perform {operation} with {' and '.join(explanation)}"

        resultList.append(result)

        return resultList


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

    def get_QEP_tree(query: str) -> QEP_Node:
        plan = cursorManager.get_QEP(query)
        return QEP_Tree.build(plan)

    def get_QEP_explanation(query: str) -> List[str]:
        result = []


if __name__ == "__main__":
    cursorManager = CursorManager()
    cursor = cursorManager.get_cursor()
    # plan = cursorManager.get_QEP(
    #     cursor,
    #     r"EXPLAIN select * from customer C, orders O where C.c_custkey = O.o_custkey and C.c_name like '%cheng'",
    # )

    plan = cursorManager.get_QEP(
        cursor,
        r"""explain select
      ps_partkey,
      sum(ps_supplycost * ps_availqty) as value
    from
      partsupp,
      supplier,
      nation
    where
      ps_suppkey = s_suppkey
      and s_nationkey = n_nationkey
      and n_name = 'GERMANY'
      and ps_supplycost > 20
      and s_acctbal > 10
    group by
      ps_partkey having
        sum(ps_supplycost * ps_availqty) > (
          select
            sum(ps_supplycost * ps_availqty) * 0.0001000000
          from
            partsupp,
            supplier,
            nation
          where
            ps_suppkey = s_suppkey
            and s_nationkey = n_nationkey
            and n_name = 'GERMANY'
        )
    order by
      value desc;""",
    )

    # plan = cursorManager.get_QEP(
    #     cursor,
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
    #     """,
    # )

    # plan = cursorManager.get_QEP(
    #     cursor,
    #     r"""explain
    #   select
    #   supp_nation,
    #   cust_nation,
    #   l_year,
    #   sum(volume) as revenue
    # from
    #   (
    #     select
    #       n1.n_name as supp_nation,
    #       n2.n_name as cust_nation,
    #       DATE_PART('YEAR',l_shipdate) as l_year,
    #       l_extendedprice * (1 - l_discount) as volume
    #     from
    #       supplier,
    #       lineitem,
    #       orders,
    #       customer,
    #       nation n1,
    #       nation n2
    #     where
    #       s_suppkey = l_suppkey
    #       and o_orderkey = l_orderkey
    #       and c_custkey = o_custkey
    #       and s_nationkey = n1.n_nationkey
    #       and c_nationkey = n2.n_nationkey
    #       and (
    #         (n1.n_name = 'FRANCE' and n2.n_name = 'GERMANY')
    #         or (n1.n_name = 'GERMANY' and n2.n_name = 'FRANCE')
    #       )
    #       and l_shipdate between '1995-01-01' and '1996-12-31'
    #       and o_totalprice > 100
    #       and c_acctbal > 10
    #   ) as shipping
    # group by
    #   supp_nation,
    #   cust_nation,
    #   l_year
    # order by
    #   supp_nation,
    #   cust_nation,
    #   l_year;
    #   """,
    # )

    # to check on the QEP from PGadmin
    for row in plan:
        print(row)

    qep_tree = QEP_Tree().build(plan)
    QEP_Tree().print_tree(qep_tree)
    result = QEP_Tree().get_explanation(qep_tree)
    
    for item in result:
        print(item)
