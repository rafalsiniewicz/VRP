from gui import *

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = App()
    #program = Program()
    #window.interface()
    '''program = Program()
    program.ImportData()
    program.InitializePopulation()
    program.ShowBest()'''
    sys.exit(app.exec_())

'''program = Program()
program.ImportData()

#program.ShowData()

names = ["A", "B","C"]
program.SelectData(names)

program.ShowData()

program.InitializePopulation(1,100)

program.ShowLengths()

for i in range(0,1):
    program.PlayRound()

program.ShowLengths()

program.ShowBest()'''
