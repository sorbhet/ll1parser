from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Grammar import Grammar, parsel


class ScrollMessageBox(QMessageBox):
   def __init__(self, l, *args, **kwargs):
      QMessageBox.__init__(self, *args, **kwargs)
      scroll = QScrollArea(self)
      scroll.setWidgetResizable(True)
      self.content = QWidget()
      scroll.setWidget(self.content)
      lay = QVBoxLayout(self.content)
      for item in l.split('\n'):
         lay.addWidget(QLabel(item, self))
      self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
      self.setStyleSheet("QScrollArea{min-width:500 px; min-height: 400px}")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.GrammarLabel = QtWidgets.QLabel(self.centralwidget)
        self.GrammarLabel.setGeometry(QtCore.QRect(70, 50, 321, 61))
        self.GrammarLabel.setObjectName("GrammarLabel")
        self.GrammarLabel.setWordWrap(True)

        self.grammarButton = QtWidgets.QPushButton(self.centralwidget)
        self.grammarButton.setGeometry(QtCore.QRect(440, 50, 211, 61))
        self.grammarButton.setObjectName("grammarButton")
        self.grammarButton.clicked.connect(self.browse)

        self.parsetableButton = QtWidgets.QPushButton(self.centralwidget)
        self.parsetableButton.setGeometry(QtCore.QRect(60, 190, 211, 61))
        self.parsetableButton.setObjectName("parsetableButton")
        self.parsetableButton.clicked.connect(self.get_parsetable)

        self.dispgrammarButton = QtWidgets.QPushButton(self.centralwidget)
        self.dispgrammarButton.setGeometry(QtCore.QRect(60, 260, 211, 61))
        self.dispgrammarButton.setObjectName("dispgrammarButton")
        self.dispgrammarButton.clicked.connect(self.get_grammar)

        self.firstButton = QtWidgets.QPushButton(self.centralwidget)
        self.firstButton.setGeometry(QtCore.QRect(60, 330, 211, 61))
        self.firstButton.setObjectName("firstButton")
        self.firstButton.clicked.connect(self.get_first)

        self.followButton = QtWidgets.QPushButton(self.centralwidget)
        self.followButton.setGeometry(QtCore.QRect(60, 400, 211, 61))
        self.followButton.setObjectName("followButton")
        self.followButton.clicked.connect(self.get_follow)

        self.parseButton = QtWidgets.QPushButton(self.centralwidget)
        self.parseButton.setGeometry(QtCore.QRect(60, 470, 211, 61))
        self.parseButton.setObjectName("parseButton")
        self.parseButton.clicked.connect(self.parse_str)
        

        self.parseTable = QtWidgets.QTableWidget(self.centralwidget)
        self.parseTable.setGeometry(QtCore.QRect(300, 150, 471, 411))
        self.parseTable.setObjectName("parseTable")
        self.parseTable.setColumnCount(0)
        self.parseTable.setRowCount(0)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LL(1) Parser"))
        self.GrammarLabel.setText(_translate("MainWindow", "No Grammar Selected"))
        self.grammarButton.setText(_translate("MainWindow", "Browse"))
        self.parsetableButton.setText(_translate("MainWindow", "Get LL(1) Parse Table"))
        self.dispgrammarButton.setText(_translate("MainWindow", "Display Grammar"))
        self.firstButton.setText(_translate("MainWindow", "Display Grammar First"))
        self.followButton.setText(_translate("MainWindow", "Display Grammar Follow"))
        self.parseButton.setText(_translate("MainWindow", "Parse String"))

    def browse(self):
        try:
            self.grammar_path, _ = QFileDialog.getOpenFileName(None, 'Open Grammar', '*.txt')
            self.grammar = Grammar(self.grammar_path)
            self.GrammarLabel.setText(f'Selected Grammar: {self.grammar_path}')
        except Exception:
            box = self.get_msgbox('Invalid file', 'Selected grammar is not valid')
            box.exec_()
    
    def get_first(self):
        msg = self.dict_to_str(self.grammar.grammar_first, ':')
        box = self.get_msgbox('First', msg)
        box.exec_()
    
    def get_follow(self):
        msg = self.dict_to_str(self.grammar.grammar_follow, ':')
        box = self.get_msgbox('Follow', msg)
        box.exec_()
    
    def get_grammar(self):
        msg = self.dict_to_str(self.grammar.grammar, '->')
        box = self.get_msgbox('Grammar', msg)
        box.exec_()

    def get_msgbox(self, win_title, win_msg, scroll = False):
        if scroll: box = ScrollMessageBox(None)
        else: box = QtWidgets.QMessageBox(None)
        box.setText(win_msg)
        box.setWindowTitle(win_title)
        return box
    
    def get_inpbox(self, win_title, win_msg):
        box = QtWidgets.QInputDialog(None)
        box.setTextValue(win_msg)
        box.setWindowTitle(win_title)
        return box
    
    def dict_to_str(self, d, sep):
        l = []
        for key, value in d.items():
            l.append(f'{key} {sep} {value}')
        s = '\n'.join([str(elem) for elem in l])
        return s

    def get_parsetable(self):
        self.pt = self.grammar.get_parse_table()
        pt = []
        x = self.grammar.terminals.copy()
        x.insert(0, 'LL(1)')
        pt.insert(0, x)

        for nonterminal in self.grammar.non_terminals:
            l = [nonterminal]
            for terminal in self.grammar.terminals:
                x = self.pt[self.grammar.non_terminals.index(nonterminal)][self.grammar.terminals.index(terminal)]
                l.append(x)
            pt.append(l)
        
        print(pt)

        r, c = len(pt), len(pt[0])
        self.parseTable.setRowCount(r)
        self.parseTable.setColumnCount(c)
        for i in range(r):
            for j in range(c):
                self.parseTable.setItem(i, j, QtWidgets.QTableWidgetItem((pt[i][j])))
    
    def parse_str(self):
        try:
            box = self.get_inpbox('Enter String', 'Enter String to parse')
            box.exec_()
            expr = box.textValue() + '$'
            msg = parsel(expr, self.grammar.get_parse_table(), self.grammar.terminals, self.grammar.non_terminals)
            if msg == -1:
                box = self.get_msgbox('Invalid String', "String doesn't belong to grammar", True)
                box.exec_()
            else:
                msg = '\n'.join([elem for elem in msg])
                box = ScrollMessageBox(msg, None)
                box.setWindowTitle('String Parsing')
                box.exec_()
        except:
            box = self.get_msgbox('Invalid String', 'Selected string is not a member of the given grammar')
            box.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())