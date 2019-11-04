from gui import *
#from program import *

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())

    #program = Program()
    #window.interface()
    '''program = Program()
    program.ImportData()

    program.InitializePopulation(1,100)'''

    #program.ShowPopulation()
    #print(program.GetPopulation().Getn(0).GetLength())
    #program.GetPopulation().AddStart(START,END)
    '''for i in range(0,1):
        program.PlayRound("capacity")
    #print("aaaa")
    program.ShowLengths()
    program.ShowBest()
    print(program.GetPopulation().BestIndividual().GetLength())'''
    #sys.exit(app.exec_())

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
