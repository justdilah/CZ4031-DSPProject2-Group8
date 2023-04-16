import psycopg2
from PyQt5.QtWidgets import *
import json
import re
from typing import List

"""
CursorManager to handle all transactions with postgres
"""
import difflib


class CursorManager(object):
    def __init__(self):
        config = {
            "TPC-H": {
                "host": "localhost",
                "dbname": "TPC-H",
                "user": "postgres",
                "pwd": "Dsp123",
                "port": "5432",
            }
        }

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
        self.step = None

    def returnExplanation(self):
        return self.explanation


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
        i = 0
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
                    i += 1
                    continue

                # node is on the same level
                # get the parent node and attach it as its child
                if self.prev_indent_size == indent_size:
                    parent = cur_node.parent
                    node.parent = parent
                    parent.children.append(node)

                # further down the tree there are child nodes
                # so have to go back up the plan to find it's parent
                elif self.prev_indent_size > indent_size:
                    p = self.findParent(self.root, indent_size)
                    if p:
                        # if len(p.children) < 2:
                        p.children.append(node)
                        node.parent = p
                else:
                    node.parent = cur_node
                    if len(cur_node.children) < 2:
                        cur_node.children.append(node)
            # Row is an explanation row (without '->')
            # Attach the explanations to the explanation list in the node
            else:
                if "Workers Planned" not in cur_row:
                    explain_results = self.transformRawExplainToNaturalLanguage(cur_row)
                else:
                    explain_results = ""

                if explain_results == None or explain_results == "":
                    i += 1
                    continue

                node.explanation.append(explain_results)

            # Update the current node pointer
            self.prev_indent_size = indent_size
            cur_node = node
            i += 1

        return self.root

    def findParent(self, node: QEP_Node, indentSize):
        stack = [node]
        while stack:
            n = stack.pop()
            if n.indent_size == indentSize:
                return n.parent
            if len(n.children) == 2:
                stack.append(n.children[0])
                stack.append(n.children[1])
            if len(n.children) == 1:
                stack.append(n.children[0])

        return None

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

    def get_explanation(self, node: QEP_Node, resultList: List[str]) -> List[str]:
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

        step = len(resultList) + 1
        if explanation == "" and (
            "join" not in operation.lower()
            and "hash" not in operation.lower()
            and "nested loop" not in operation.lower()
        ):
            result = f"Step {step}: Perform {operation}"
        elif "join" in operation.lower() or "nested loop" in operation.lower():
            result = f"Step {step}: Perform {operation} on the intermediate results of step {node.children[0].step} and {node.children[1].step}"
        elif "hash" in operation.lower() and "join" not in operation.lower():
            result = f"Step {step}: Perform {operation} on the intermediate results of step {node.children[0].step}"
        else:
            result = f"Step {step}: Perform {operation} with {self.joinExplanationList(explanation)}"

        node.step = step

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
                if explanationQ1 and explanationQ2:
                    compareExplanation = f"Step {step}: Both queries perform the same operations at this step executing a {operationQ1}. However, Q1 and Q2 have different conditions on the operations with Q1 to {self.joinExplanationList(explanationQ1)} and Q2 to {self.joinExplanationList(explanationQ2)}."
                elif explanationQ1 and not explanationQ2:
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
                else:
                    compareExplanation = f"Step {step}: Both queries are performing different operations at this step, with Q1 executing a {operationQ1} and Q2 executing a {operationQ2}."

            compareList.append(compareExplanation)
            compareExplanation = ""
            q1Pointer += 1
            q2Pointer += 1

        line = (
            "Q1 has additional steps taken due to the change in query.\nAdditional steps taken by Q1:"
            if q1Pointer < len(q1Queue)
            else "Q2 has additional steps taken due to the change in query.\nAdditional steps taken by Q2:"
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
    def __init__(self, cursorManager: CursorManager):
        # self.interface = interface
        self.cursorManager = cursorManager
        self.cursor = self.cursorManager.get_cursor()
        # self.updateSchema()

    # ROLLBACKS TRANSACTION IF THERE ARE ISSUES
    def rollback(self):
        self.cursorManager.conn.rollback()

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
            return schema

            # self.interface.setSchema(schema)
        except Exception as e:
            print(str(e))
            print("Retrieval of Schema information is unsuccessful!")

    """
    Returns the visual plan in a List[str] format
    """

    def get_visual_plan(self, node: QEP_Node) -> List[str]:
        return QEP_Tree().get_visual_plan(node, [])

    def checkRootIsEmpty(self):
        return QEP_Tree().isEmpty()

    """
    Builds the QEP tree by first getting the plan from postgres
    Then builds the tree using the QEP_Tree class
    Returns the root node of the QEP tree
    """

    def build_QEP_tree(self, query: str) -> QEP_Node:
        plan = self.cursorManager.get_QEP(r"explain " + query)
        return QEP_Tree().build(plan)

    """
    Gets the explanation for the specified QEP tree
    by passing in the root node of the specified tree
    as an argument
    Returns the arguments in a list
    """

    def get_QEP_explanation(self, node: QEP_Node) -> List[str]:
        return QEP_Tree().get_explanation(node, [])

    """
    Gets the comparisons for the specifed QEP trees by passing each tree's root
    node as arguments
    Returns the comparisons in a list
    """

    def get_QEP_comparison(self, node1: QEP_Node, node2: QEP_Node) -> List[str]:
        return QEP_Tree().compareQEP(node1, node2)

    def stripString(str):
        # remove ; at the end
        if str[-1] == ";":
            str = str[:-1]

        # Remove leading/trailing whitespace and split into lines
        sql_lines = str.lower().strip().split("\n")
        stripped_list = [s.strip() for s in sql_lines]

        # print(stripped_list)
        # Join lines back together with no separator
        result = " ".join(stripped_list)

        keywords = ["from", "where", "like", "group by", "order by"]
        sections = []
        start_index = 0
        pre = ""

        for keyword in keywords:
            index = result.find(keyword)
            if index != -1:
                sections.append(pre + " " + result[start_index:index].strip())
                # sections.append(keyword)
                start_index = index + len(keyword)
                pre = keyword

        sections.append(pre + " " + result[start_index:].strip())
        return sections

    def compare_sql(self, string1, string2):
        # Split the strings into lines
        lines1 = Explain.stripString(string1)
        lines2 = Explain.stripString(string2)

        # Compare the lines using the Differ class
        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))

        # Store the differences in a list
        differences = []
        temp = []
        sign = ""
        pre = ""
        for line in diff:
            text = line[2:]
            if (sign.startswith("-") and line.startswith("+")) or (
                sign.startswith("+") and line.startswith("-")
            ):
                differences.append(temp)
                temp = []
            if len(temp) == 0 and line.startswith("-"):
                temp.append(("### SQL old removed\n\n", text))
                sign = "-"
            elif len(temp) == 0 and line.startswith("+"):
                temp.append(("### SQL new added\n\n", text))
                sign = "+"
            elif line.startswith("+") and pre.startswith("+"):
                temp.append(("", text))  # SQL 2
            elif line.startswith("-") and pre.startswith("-"):
                temp.append(("", text))  # SQL 1
            elif line.startswith("?"):
                continue

            pre = line

        if len(temp) != 0:
            differences.append(temp)

        if differences[-1][0][0] == "### SQL old removed\n\n":
            temp = []
            temp.append(("### SQL new added\n\n", " "))
            differences.append(temp)

        return differences

    def explainSQL(self, diffArray):
        line1 = ""
        line2 = ""
        pretype = ""
        change = []
        explanation = []

        for i in diffArray:
            for diff_type, line in i:
                if (
                    diff_type == "### SQL new added\n\n"
                    or diff_type == "### SQL old removed\n\n"
                ):
                    pretype = diff_type

                if pretype == "### SQL old removed\n\n":
                    if line1 and line2:
                        string1_words = re.split(r"[ _-]+", line1)
                        string2_words = re.split(r"[ _-]+", line2)

                        if len(string1_words) == len(string2_words):
                            for i in range(min(len(string1_words), len(string2_words))):
                                if string1_words[i] != string2_words[i]:
                                    change.append([string1_words[i], string2_words[i]])
                        else:
                            change.append(
                                [" ".join(string1_words), " ".join(string2_words)]
                            )
                        line1 = ""
                        line2 = ""

                if line1 == "" or pretype == "### SQL old removed\n\n":
                    line1 += line
                    continue
                elif line2 == "" or pretype == "### SQL new added\n\n":
                    line2 += line
                    continue

        if line1 and line2:
            string1_words = re.split(r"[ _-]+", line1)
            string2_words = re.split(r"[ _-]+", line2)

            if len(string1_words) == len(string2_words):
                for i in range(min(len(string1_words), len(string2_words))):
                    if string1_words[i] != string2_words[i]:
                        change.append([string1_words[i], string2_words[i]])
            else:
                change.append([" ".join(string1_words), " ".join(string2_words)])

        for i in change:
            if i[1] == " ":
                explanation.append("The old query is removed")
            elif i[0].isnumeric() and i[1].isnumeric():
                explanation.append("There is a change in value")
            elif i[0].isnumeric() and (i[1].isalnum() or i[1].isalpha()):
                explanation.append("There is a change from a value to a variable")
            elif i[1].isnumeric() and (i[0].isalnum() or i[0].isalpha()):
                explanation.append("There is a change from a variable to a value")
            elif (i[0].isalnum() or i[0].isalpha()) and (
                i[1].isalnum() or i[1].isalpha()
            ):
                explanation.append("There is a change in variable")
            else:
                explanation.append("The query here has been changed")

        return explanation

    def printSQLexplain(differences, explain):
        oldtype = ""
        newtype = ""
        c = 0

        for i in differences:
            for diff_type, line in i:
                print(f"{diff_type} {line}")

                if diff_type == "### SQL old removed\n\n":
                    oldtype = diff_type
                elif diff_type == "### SQL new added\n\n":
                    newtype = diff_type

            if oldtype and newtype:
                print("\nExplanation : " + explain[c] + "\n=========================")
                c += 1
                oldtype = ""
                newtype = ""

    def concatDifferencesExplainSQL(self, differences, explain):
        concatString = ""
        oldtype = ""
        newtype = ""
        c = 0

        if len(differences) == 0 and len(explain) == 0:
            concatString = concatString + (
                "There are no differences between the 2 SQL queries"
            )

        else:
            for i in differences:
                for diff_type, line in i:
                    concatString = concatString + diff_type + line + "\n\n"
                    # print(f"{diff_type} {line}")
                    if diff_type == "### SQL old removed\n\n":
                        oldtype = diff_type
                    elif diff_type == "### SQL new added\n\n":
                        newtype = diff_type

                if oldtype and newtype:
                    concatString = concatString + (
                        "\n### Explanation :\n\n "
                        + explain[c]
                        + "\n===================\n"
                    )
                    c += 1
                    oldtype = ""
                    newtype = ""
        return concatString
