import time
import threading


class Brain():
    ListOfWidget = []
    OppositeTool = ''

    enemy_row_third = 0
    enemy_row_second = 0
    enemy_row_one = 0

    enemy_column_third = 0
    enemy_column_second = 0
    enemy_column_one = 0

    Cross_list_one = []
    Cross_list_two = []
    Predicted_Cross_one = []
    Predicted_Cross_two = []

    predict_next_warning = []

    Cross_one = []
    Cross_Two = []
    two_counter = 0
    one_counter = 0

    FirstRow = []

    list_of_opponent_played= {}
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def AnalizeCurentOpponentPosition(self, ListOfWidget, OppositeTool):
        self.ListOfWidget = ListOfWidget
        self.OppositeTool = OppositeTool

        for i in ListOfWidget:
            if i.text == OppositeTool:
                self.list_of_opponent_played[i] = i.coordinate


    def PredictOpponentFuturePosition(self, ListOfWidget, OppositeTool, FinalScore):



        if FinalScore:
            self.predict_next_warning = []
        else:
            for i in ListOfWidget:
                # Cross One
                if i.coordinate[0] == i.coordinate[1]:

                    if i not in self.Cross_one:

                        self.Cross_one.append(i)

                new = i.coordinate[0] + i.coordinate[1]
                if new == 4:

                    if i not in self.Cross_Two:

                        self.Cross_Two.append(i)

            local_one = []
            for one in range(len(self.Cross_one)):

                if self.Cross_one[one].text != OppositeTool:
                    #print(f"pointed: {self.Cross_Two[two].name}")
                    if self.Cross_one[one] in self.Cross_one:

                        local_one.append(self.Cross_one[one])

            if len(local_one) == 1:
                #print(F"FINALLY!!! local_one {local_one[0].coordinate}")
                self.predict_next_warning.append(local_one[0].coordinate)

            local_two = []

            for two in range(len(self.Cross_Two)):
                #print(f"Cross two {two.coordinate}")

                if self.Cross_Two[two].text != OppositeTool:
                    #print(f"pointed: {self.Cross_Two[two].name}")
                    if self.Cross_Two[two] in self.Cross_Two:

                        local_two.append(self.Cross_Two[two])


            if len(local_two) == 1:
                #print(F"FINALLY!!! local_two {local_two[0].coordinate}")
                self.predict_next_warning.append(local_two[0].coordinate)


            for i in ListOfWidget:

                # first row

                if i.text == OppositeTool:
                    if i.coordinate[1] == 1:
                        print("first row: ", i.coordinate)
                        self.enemy_row_one += 1

                        if self.enemy_row_one == 2:
                            self.enemy_row_one = 0
                            #print("warning on first row: ")
                            for i in ListOfWidget:
                                if i.text != OppositeTool:
                                    if i.coordinate[1] == 1:
                                        #print("primary first row: ".upper(), i.coordinate)
                                        self.predict_next_warning.append(i.coordinate)

                #second row
                if i.text == OppositeTool:
                    if i.coordinate[1] == 2:
                        #print("second row: ", i.coordinate)
                        self.enemy_row_second += 1

                        if self.enemy_row_second == 2:
                            self.enemy_row_second = 0
                            #print("warning on second row: ")
                            for i in ListOfWidget:
                                if i.text != OppositeTool:
                                    if i.coordinate[1] == 2:
                                        print("primary second row: ".upper(),i.coordinate)
                                        self.predict_next_warning.append(i.coordinate)

                #third row
                if i.text == OppositeTool:
                    if i.coordinate[1] == 3:
                        #print("third row: ", i.coordinate)
                        self.enemy_row_third += 1

                        if self.enemy_row_third == 2:
                            self.enemy_row_third = 0
                            #print("warning on third row: ")
                            for i in ListOfWidget:
                                if i.text != OppositeTool:
                                    if i.coordinate[1] == 3:
                                        #print("primary third row: ".upper(),i.coordinate)
                                        self.predict_next_warning.append(i.coordinate)

                # first column
                if i.text == OppositeTool:
                    if i.coordinate[0] == 1:
                        # print("first column: ", i.coordinate)
                        self.enemy_column_one += 1
                        if self.enemy_column_one == 2:
                            self.enemy_column_one = 0
                            # print("warning on first column: ")
                            for i in ListOfWidget:
                                if i.text != OppositeTool:
                                    if i.coordinate[0] == 1:
                                        #print("primary first column: ".upper(), i.coordinate)
                                        self.predict_next_warning.append(i.coordinate)

                # second column
                if i.text == OppositeTool:
                    if i.coordinate[0] == 2:
                        # print("second column: ", i.coordinate)
                        self.enemy_column_second += 1
                        if self.enemy_column_second == 2:
                            self.enemy_column_second = 0
                            # print("warning on second column: ")
                            for i in ListOfWidget:
                                if i.text != OppositeTool:
                                    if i.coordinate[0] == 2:
                                        #print("primary second column: ".upper(), i.coordinate)
                                        self.predict_next_warning.append(i.coordinate)
                # third column
                if i.text == OppositeTool:
                    if i.coordinate[0] == 3:
                        #print("third column: ", i.coordinate)
                        self.enemy_column_third += 1
                        if self.enemy_column_third == 2:
                            self.enemy_column_third = 0
                            #print("warning on third column: ")
                            for i in ListOfWidget:
                                if i.text != OppositeTool:
                                    if i.coordinate[0] == 3:
                                        #print("primary third column: ".upper(), i.coordinate)
                                        self.predict_next_warning.append(i.coordinate)

            print("****")








"""T = threading.Thread(target=Brain().WaitForOpponent)
T.start()
"""


