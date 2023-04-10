import psycopg2
import time
from PyQt5.QtWidgets import *
import sys
import json
import re


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
                port=self._config["port"]
            )
            self.cursor = self.conn.cursor()

        except Exception as e:
            print(f'Connection attempt failed with error: {e}')

    def get_cursor(self):
        return self.cursor

    def close(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except Exception as e:
            print(f'Cursor failed to close with error: {e}')
            
    def get_QEP(self, cursor, query: str):
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f'Cursor failed to execute query with error: {e}')
            return []

class QEP_Node():
    def __init__(self, indent_size: int, operation: str, details: str, raw: list):
        self.indent_size = indent_size
        self.operation = operation
        self.details = details
        self.parent = None
        self.children = []
        self.raw = raw

class QEP_Tree():
    def __init__(self):
        self.root = None
        self.prev_indent_size = 0

    # builds the QEP tree and returns the root node
    def build(self, plan):
        cur_node = None
        node = None
        indent_size = 0
        cur_list = []
        operation = "Ending Steps"
        details = "NULL"
        for row in plan:
            cur_row = row[0]
            
            # if this condition satisfies then this is the root node
            if "->" not in cur_row and "Gather" not in cur_row and "cost=" in cur_row:
                if self.root == None:
                    match = re.match(r"^(.+)\s\s(.+)$", cur_row)
                    node = QEP_Node(0, match.group(1).strip(), match.group(2),cur_list)
                    cur_list = []
                    self.root = node
                    self.root.parent = self.root
                    cur_node = self.root
                    self.prev_indent_size = 0


            if "->" in cur_row:
                node = QEP_Node(indent_size, operation.strip(), details,cur_list)
                match = re.match(r"(\s*->)?\s*(\w.*)\s+\((.*)\)$", cur_row)
                indent_size = len(match.group(1))
                operation = match.group(2).replace("Parallel", "")
                details = match.group(3)

                # node = QEP_Node(indent_size, operation.strip(), details,cur_list)
                
                cur_list = []
                
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

                self.prev_indent_size = indent_size
                cur_node = node
                   
            else : 
                # print(cur_row)
                cur_list.append(cur_row)
                
        # add the last item       
        node = QEP_Node(indent_size, operation.strip(), details,cur_list)
        # node is on the same level
        if self.prev_indent_size == indent_size:
            parent = cur_node.parent
            node.parent = parent
            parent.children.append(node)
        else:
            node.parent = cur_node
            cur_node.children.append(node)
                

        return self.root
    
    # for now prints the tree
    # later will need to adapt this to create the visuals
    def print_tree(self, node: QEP_Node):
        self.traverse(node)

    # traverse the tree recursively
    def traverse(self, node: QEP_Node):
        if node == None:
            return

        print(" " * node.indent_size, "-> " + node.operation)
        print(node.raw)

        for child in node.children:
            self.traverse(child)
        

class Explain():
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

if __name__ == "__main__":
    test = "   YOYUOYOO"
    print(test.count(" "))

    strTest = " -> Ending Steps\n" + "['Gather  (cost=5366.32..65519.75 rows=151 width=266)', '  Workers Planned: 2']\n" + "     -> Hash Join\n" + "['        Hash Cond: (o.o_custkey = c.c_custkey)']\n" + "           -> Seq Scan on orders o\n" + "[]\n" + "           -> Hash\n" + "[]\n" + "                 -> Seq Scan on customer c\n" +"[                    Filter: ((c_name)::text ~~ '%cheng'::text)]\n"

    strArray = strTest.split("\n")
    strArray = strArray[:-1]

    strArray = [x for x in strArray if "[" not in x]
    # for str in strArray:
    print(strArray)
    for strVar in strArray:
        print(strVar)
        print(strVar.split("-")[0].count(" "))

    cursorManager = CursorManager()
    cursor = cursorManager.get_cursor()
    plan = cursorManager.get_QEP(cursor, r"EXPLAIN select * from customer C, orders O where C.c_custkey = O.o_custkey and C.c_name like '%cheng'")
    # plan = cursorManager.get_QEP(cursor, r'''explain select
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
    #   value desc;''')
    
    # plan = cursorManager.get_QEP(cursor, r'''explain
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
    #   ''')
    
    
## to cheeck on the QEP from gp admin
    # for row in plan:
    #     print(row)
    #
    # qep_tree = QEP_Tree().build(plan)
    # QEP_Tree().print_tree(qep_tree)

    # #----------------------------------- Text-to-Speech -----------------------------------------------------
    # def onClickedOldPlayButton(self):
    #     self.interface.playOldButton.clicked.connect(lambda: self.playAudioFile("oldQuery"))
    #
    # def onClickedOldStopButton(self):
    #     self.interface.stopOldButton.clicked.connect(self.stopAudioFile)
    #
    # def onClickedNewPlayButton(self):
    #     self.interface.playNewButton.clicked.connect(lambda: self.playAudioFile("newQuery"))
    #
    # def onClickedNewStopButton(self):
    #     self.interface.stopNewButton.clicked.connect(self.stopAudioFile)
    # def textToSpeech(self,text, typeOfQuery):
    #
    #     speaker = gTTS(text=text, lang="en", slow=False)
    #
    #     file_path = os.path.join(os.getcwd(), typeOfQuery + str(".mp3"))
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #
    #     # saves the text speech as an MP3
    #     speaker.save(typeOfQuery + str(".mp3"))
    #
    #     # returns stat_result object
    #     statbuf = os.stat(typeOfQuery + str(".mp3"))
    #
    #     # statbuf.st_size -> represents the size of the file in kbytes -> convert to MBytes
    #     mbytes = statbuf.st_size / 1024
    #
    #     # MB / 200 MBPS -> to get the duration of the mp3 in seconds
    #     duration = mbytes / 200
    #
    # def stopAudioFile(self):
    #     self.player.pause()
    # def playAudioFile(self,typeOfQuery):
    #     mp3_name = typeOfQuery + str(".mp3")
    #     file_path = os.path.join(os.getcwd(), mp3_name)
    #     url = QUrl.fromLocalFile(file_path)
    #
    #     content = QMediaContent(url)
    #     self.player.setMedia(QMediaContent())  # reset the media player
    #     self.player.setMedia(content)
    #     self.player.play()