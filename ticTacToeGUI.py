import tkinter
import random
import copy

class Tic_tac_toe:
    def __init__(self, name):
        self.playerName = name #The name the player entered at the start of the program
#        self.winnerLabel = None #Display the winner of the game on the GUI at the end of the game
#        self.playAgainLabel = None #Asks the user to play again on the GUI at the end of the game
#        self.playAgainButtonYes = None #Displays the buttons yes, if clicked clears the state and the game is restarted without propmpting for name
#        self.playAgainButtonNo = None #Displays the button no, if clicked destroys the window of the game
#        self.yesNoFrame = None
        self.players = {'X': self.playerName, 'O': 'Computer'} #The dictionary is used in displaying the winner of the game
        self.winner = '' #Stores the name of the winner of the game
        self.state = [[' ' for c in range(3)] for r in range(3)] #Saves the current of the game
        self.buttons = [[0 for c in range(3)] for r in range(3)] #Displays the buttons to be clicked on the GUI, the callback function is self.click(r,c)
        for r in range(3):
            for c in range(3):
                self.buttons[r][c] = tkinter.Button(font=('Sans-serif', 42, 'bold roman'), width=3, fg='black', bg='white', command = lambda row=r, col=c: self.click(row, col))
                self.buttons[r][c].grid(row = r, column = c)

    def printState(self):
        ''' Prints the current state of the game on the console'''
        print('\n')
        for r in range(3):
            for c in range(3):
                print(self.state[r][c], end=' ')
                if c != 2:
                    print('| ', end='')
            if r != 2:
                print('\n_________')

    def availableSpaces(self):
        ''' Returns a list of the available spaces in the current state of the game. The positions are saved as a tuple of two values (row, column)'''
        return  [(r, c) for c in range(3) for r in range(3) if self.state[r][c] == ' ']

    def click(self, r, c):
        ''' The callback function for the button on the GUI. Recieves the row and column of the button clicked as parameters. Checks if the position is free 
            (self.validMove(r,c) -> bool) and if there is winner(self.checkWinner()->bool). If the condition is true, make corresponding changes on the state of the game (self.state[r])[c]),
            changes the corresponding postion on the GUI (self.changeColor(r, c, 'X')), checks if there is a winner(self.checkWinner()->bool). If there is winner, it displays
            the winner, and if there is no winner and there are still moves to play, prompts the computer to play and repeats the whole process.'''
        if self.validMove(r,c) == True and self.checkWinner() == False:
            self.state[r][c] = 'X'
            self.changeColor(r, c, 'X')
            self.printState()
            if self.checkWinner() == False:
                self.compPlay()
                if self.checkWinner():
                    print(f'{self.players[self.winner]} wins.' if self.winner != 'D' else f'Draw!')
                    self.displayWinner()
            else:
                print(f'{self.players[self.winner]} wins.' if self.winner != 'D' else f'Draw!')
                self.displayWinner()
            

    def validMove(self, r, c):
        ''' Recieves the row and column of the position played as parameters. It checks if the corresponding postion in free. Hence making it valid by returning True, or
            invalid by returning False.'''
        if self.state[r][c] == 'X' or self.state[r][c] == 'O':
            return False
        return True

    def compPlay(self):
        '''Calls the self.getBoardCopy(self.state) function and uses the self.compAI() function to make the best move and makes the corresponding changes on the self.state and
         position's GUI.'''
#        if len(self.availableSpaces()) != 0:
#            p = random.choice(self.availableSpaces())
#            self.state[p[0]][p[1]] = 'O'
#            self.changeColor(p[0], p[1], 'O')
#        self.printState()
        boardCopy = self.getBoardCopy(self.state)
        play = self.compAI(boardCopy)
        self.state[play[0]][play[1]] = 'O'
        self.changeColor(play[0], play[1], 'O')
        self.printState()

    def getBoardCopy(self, board: list):
        '''Makes a deep copy of the current state of the game and returns it. This is used in making the best move by the computer. This is done in order not to alter the
           current state of the game.'''
        boardCopy = copy.deepcopy(self.state)
        return boardCopy

    def compAI(self, board):
        ''' Makes a move based on a copy of the current state of the game.'''

        #checks if the computer can win in the next move
        for pos in self.availableSpaces():
            board[pos[0]][pos[1]] = 'O'
            for i in range(3):
                if (board[i][0] == board[i][1] == board[i][2]  == 'O'):
                    return pos
                elif (board[0][i] == board[1][i] == board[2][i] == 'O'):
                    return pos
            if (board[0][0] == board[1][1] == board[2][2] == 'O'):
                return pos
            elif (board[0][2] == board[1][1] == board[2][0] == 'O'):
                return pos
            board[pos[0]][pos[1]] = ' '

        #check if player can win in next move and blocks it
        for pos in self.availableSpaces():
            board[pos[0]][pos[1]] = 'X'
            for i in range(3):
                if (board[i][0] == board[i][1] == board[i][2]  == 'X'):
                    return pos
                elif (board[0][i] == board[1][i] == board[2][i] == 'X'):
                    return pos
            if (board[0][0] == board[1][1] == board[2][2] == 'X'):
                return pos
            elif (board[0][2] == board[1][1] == board[2][0] == 'X'):
                return pos
            board[pos[0]][pos[1]] = ' '

        #checks if the middle is free            
        for pos in self.availableSpaces():
            if pos == (1, 1):
                return pos

        #checks if the corner is free 
        for pos in self.availableSpaces():
            if pos in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                return pos
            else: 
                #plays on any of the sides
                p = random.choice(self.availableSpaces())   
                return p  
              

    def checkWinner(self):
        ''' Checks if there is winner or if there are no available moves by returning True, and False if otherwise. It stores the letter of the winner ('X' or 'O') in the 
            self.winner variable, and ('D') if the game ends in a draw'''
        for i in range(3):
            if (self.state[i][0] == self.state[i][1] == self.state[i][2]  != ' '):
                self.buttons[i][0].configure(fg = 'white', bg = 'green')
                self.buttons[i][1].configure(fg = 'white', bg = 'green')
                self.buttons[i][2].configure(fg = 'white', bg = 'green')
                self.winner = self.state[i][0]
                return  True
            elif (self.state[0][i] == self.state[1][i] == self.state[2][i] != ' '):
                self.buttons[0][i].configure(fg = 'white', bg = 'green')
                self.buttons[1][i].configure(fg = 'white', bg = 'green')
                self.buttons[2][i].configure(fg = 'white', bg = 'green')
                self.winner = self.state[0][i]
                return True
        if (self.state[0][0] == self.state[1][1] == self.state[2][2] != ' '):
            self.buttons[0][0].configure(fg = 'white', bg = 'green')
            self.buttons[1][1].configure(fg = 'white', bg = 'green')
            self.buttons[2][2].configure(fg = 'white', bg = 'green')
            self.winner = self.state[0][0]
            return True
        elif (self.state[0][2] == self.state[1][1] == self.state[2][0] != ' '):
            self.buttons[0][2].configure(fg = 'white', bg = 'green')
            self.buttons[1][1].configure(fg = 'white', bg = 'green')
            self.buttons[2][0].configure(fg = 'white', bg = 'green')
            self.winner = self.state[0][2]
            return True
        if len(self.availableSpaces()) == 0:
            self.winner = 'D'
            return True
        return False      

    def changeColor(self, r, c, let):
        ''' Recieves the row, column and the letter ('X'->User or 'O'->Computer) of the button clicked and the changes the color based on the values of the recieved parameters.'''
        if let == 'X':
            self.buttons[r][c].configure(text='X', fg='blue', bg='orange')
        elif let == 'O':
            self.buttons[r][c].configure(text='O', fg='red', bg='grey')

    def displayWinner(self):
        ''' Displays the winner at the end of the game, or if the game ends in a draw.'''
        self.winnerLabel = tkinter.Label(text=f'{self.players[self.winner]} wins!' if self.winner != 'D' else f'Draw!', font=('Sans-serif', 20, 'bold roman'), height=2, fg = 'purple')
        self.winnerLabel.grid(row=3, column=0, columnspan=3) 
        self.playAgainLabel = tkinter.Label(text='Do you want to play again?', font=('Sans-serif', 13, 'bold roman'), fg='brown')
        self.playAgainLabel.grid(row=4, column=0, columnspan=2)
        #Send 'y'->yes of 'n'->no, to the self.playAgain(opt) funtion after prompting the user to play again.
        self.yesNoFrame = tkinter.Frame()
        self.playAgainButtonYes = tkinter.Button(self.yesNoFrame ,text='YES', font=('Sans-serif', 13, 'bold roman'), bg='green', fg='white', command = lambda option='y': self.playAgain(option))
        self.playAgainButtonNo = tkinter.Button(self.yesNoFrame ,text='NO', font=('Sans-serif', 13, 'bold roman'), bg='red', fg='white',  command = lambda option='n': self.playAgain(option))
        self.yesNoFrame.grid(row=4, column=2)
        self.playAgainButtonYes.grid(row=0, column=0)
        self.playAgainButtonNo.grid(row=0, column=1)

    def playAgain(self, opt):
        ''' Based of the value of the parameter opt ('y', 'n') recieved. If opt == 'y' destroys the play again prompt, changes the global firstTime variable and calls the main() 
            function. If the user doesn't want to play again, destroys the window.'''
        global firstTime
        if opt == 'y':
            firstTime = False
            self.winnerLabel.destroy(); self.playAgainLabel.destroy(); self.playAgainButtonYes.destroy(); self.playAgainButtonNo.destroy(); self.yesNoFrame.destroy()
            main()
        else:
            root.destroy()


root = tkinter.Tk() #opens the tkinter window
firstTime = True #This global variable returns False if the user wants a replay. This prevents prompting the name of the user again.
name = '' #A global variable which stores the name the user entered at the begining of the game. 
def main():
    ''' First prompts the user for a name if the global firstTime variable is True, and goes directly to creating an instance of the Tic_tac_toe class if the variable is False.'''
    def getName():
        '''Gets the name of the player, assigns the value 'User', if the name is ''(blank). It then creates an instance of the Tic_tac_toe class.'''
        global name, firstTime
        if firstTime == True: 
            name = playerNameEntry.get()
            if name == '':
                name = 'User'
            playerNameLabel.destroy(); playerNameEntry.destroy(); nameButton.destroy()
            game = Tic_tac_toe(name)
        else:
            game = Tic_tac_toe(name)
    
    if firstTime == True: #Does don't run command if it is a replay, because the global fistTime variable will be False.
        playerNameLabel = tkinter.Label(text='Input Name ', font=('Sans-serif', 20, 'bold roman'))
        playerNameEntry = tkinter.Entry()
        nameButton = tkinter.Button(text='Ok', font=('Sans-serif', 20, 'bold roman'), bg='green', fg='white', command=getName)
        playerNameLabel.grid(row=0, column=0)
        playerNameEntry.grid(row=0, column=1)
        nameButton.grid(row=0, column=3)
    else:
        getName()

if __name__ == '__main__':
    main()
tkinter.mainloop()
