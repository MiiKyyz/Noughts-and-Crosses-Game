import datetime
import math
import random
from kivy.animation import Animation
from kivy.clock import Clock
import NPC
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget, ThreeLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
from kivymd.utils.fitimage import FitImage
import DataBase
from kivymd.uix.dialog import MDDialog


class MainLayout(Widget):

    X= 0
    Y = 600
    Y_container = []
    X_container = []
    SnowColor = []
    SnowShape = []

    SnowCope = []
    NPCTool = ''

    width_number = []
    PX = []
    PY = []
    frequency = []
    ListOfWidget = []

    FinalScore = False
    Players = True

    StatePlay = ""
    Wait = False

    oldPrediction = []
    StateGame = ""

    Prediction = []

    predicted_warning_move = []





    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        """MDRectangleFlatButton:
                            text: "Log Out!"
                            theme_text_color: "Custom"
                            text_color: [14/255, 84/255, 0/255, 1]
                            line_color: [14/255, 84/255, 0/255, 1]
                            pos_hint: {"right": 0.95, "top": 0.7}"""


        self.ids.Over.opacity = 0
        self.ids.Over.size_hint = (0,0)



        self.dialog = MDDialog(text="If you quit or log out, you current game progress will be lost.",title="Do you want to Log Out?",
                               buttons=[
                                   MDRectangleFlatButton(text="Quit Game!",
                                                         theme_text_color= "Custom",text_color= [14 / 255, 84 / 255, 0 / 255, 1],
        line_color= [14 / 255, 84 / 255, 0 / 255, 1], on_press=self.Menu),
                                   MDRectangleFlatButton(text="Cancel",
                                                         theme_text_color="Custom",
                                                         text_color=[14 / 255, 84 / 255, 0 / 255, 1],
                                                         line_color=[14 / 255, 84 / 255, 0 / 255, 1], on_press= self.CloseDialog),


                               ]


                               )




        DataBase.DataPlayer().InitializeData()

        self.ids.D1.disabled = True
        self.ids.D2.disabled = True
        self.ids.D3.disabled = True
        self.ids.D4.disabled = True
        self.ids.D5.disabled = True
        self.ids.D6.disabled = True
        self.ids.D7.disabled = True
        self.ids.D8.disabled = True
        self.ids.D9.disabled = True


        self.SnowPosition()
        self.ToolPlayer = ''
        self.ready = False
        self.ListOfWidget = [self.ids.B1, self.ids.B2, self.ids.B3, self.ids.B4, self.ids.B5, self.ids.B6, self.ids.B7, self.ids.B8, self.ids.B9]

        Clock.schedule_interval(self.RealTimeApp, 0.1/60)
        Clock.schedule_interval(self.Snow, 0.01/60)


    def CloseDialog(self, instance):
        self.dialog.dismiss()
    def Dialog(self):
        self.dialog.open()

    def Menu(self, instance):
        self.ids.screen_manager.current = 'menu'
        self.Restart()
        self.dialog.dismiss()
        self.ids.tool.right_action_items = [[""]]

    def Restart(self):

        self.predicted_warning_move.clear()
        self.ids.Over.opacity = 0
        self.ids.Over.size_hint = (0, 0)
        self.FinalScore = False
        self.Players = True

        self.StatePlay = ""
        self.Wait = False

        self.oldPrediction.clear()

        self.StateGame = ""

        self.Prediction.clear()

        NPC.Brain().predict_next_warning.clear()
        self.predicted_warning_move = []
        self.ids.second_panel.opacity = 1
        self.ids.second_panel.size_hint = (0.6, 0.7)


        for widget in self.ListOfWidget:

            widget.text = ''
            widget.opacity = 0
            widget.own = ''


    def LoginAccount(self):
        record = DataBase.DataPlayer().ShowDate()
        names = []
        passw = []
        for name in record:
            names.append(name[0])
            passw.append(name[2])



        if self.ids.LoginName.text in names and self.ids.LoginPassword.text in passw:

            self.ids.PlayerNamePost.text = self.ids.LoginName.text
            self.ids.screen_manager.current = 'menu'
        else:
            print("Account was not found! ")


    def CreateAccount(self):



        if len(self.ids.CNP.text) == 0 or len(self.ids.CLP.text) == 0 or len(self.ids.CPP.text) == 0:

            print("One of the Text Input is empty!")


        else:

            record = DataBase.DataPlayer().ShowDate()
            names = []
            for name in record:
                names.append(name[0])


            if self.ids.CNP.text not in names:

                self.ids.screen_manager.current = 'login'

                DataBase.DataPlayer().CreateAccount(self.ids.CNP.text, self.ids.CLP.text, self.ids.CPP.text)
                print("Date Saved!")

                DataBase.DataPlayer().ShowDate()

            elif self.ids.CPP.text in self.ids.CNP.text:
                print("The password cannot be related to your Name")
            elif len(self.ids.CPP.text) < 8:
                print("password too short!")

            else:
                print("Name is on used!")



    def ForgotPass(self):

        if self.ids.screen_manager.current_screen == self.ids.screen_manager.get_screen('login'):

            self.ids.screen_manager.current = 'Forgot'

        elif self.ids.screen_manager.current_screen == self.ids.screen_manager.get_screen('Forgot'):


            if len(self.ids.newpass.text) == 0 or len(self.ids.renewpass.text) == 0 or len(self.ids.NamePlayer.text) == 0:
                print("One of the input box is empty!")

            else:

                record = DataBase.DataPlayer().ShowDate()
                names = []
                for name in record:

                    names.append(name[0])
                if self.ids.NamePlayer.text in names:

                    if self.ids.newpass.text != self.ids.renewpass.text:
                        print("Password Do not match! ")
                    elif self.ids.newpass.text in self.ids.NamePlayer.text:
                        print("The password cannot be related to your Name")
                    elif len(self.ids.newpass.text) <8:
                        print("password too short!")

                    elif self.ids.newpass.text == self.ids.renewpass.text:
                        self.ids.screen_manager.current = 'login'
                        DataBase.DataPlayer().UpdatePassword(self.ids.NamePlayer.text, self.ids.newpass.text)

                else:
                    print("Name was not found! ")

    def SnowPosition(self):
        for i in range(120):
            self.Y_container.append(1400)
            self.frequency.append(random.randint(90, 110))
            self.width_number.append(random.randint(-40, 40))
            self.PX.append(random.randint(100, 1500))
            self.PY.append(random.randint(-500, 500))
            initial_x = random.randint(100, 800)
            self.X_container.append(initial_x)
            initial_y = random.randint(1000, 1200)
            self.img = FitImage(source="snow.png", pos=(initial_x,initial_y), size_hint=(0.02,0.02))

            self.ids.Game.add_widget(self.img)

            self.SnowShape.append(self.img)

        """for i in range(100):
            self.Y_container.append(1000)
            self.frequency.append(random.randint(80, 150))
            self.width_number.append(random.randint(30,80))
            self.PX.append(random.randint(100, 1500))
            self.PY.append(random.randint(-300, 300))
            initial_x = random.randint(100, 800)
            self.X_container.append(initial_x)
            initial_y = random.randint(980, 1000)
            with self.ids.background_Register.canvas.before:
                self.color = Color(3 / 255, 252 / 255, 94 / 255, 1)

                self.rect = RoundedRectangle(pos=(initial_x, initial_y),
                                             size=(10,
                                                   10), radius=[50])
                self.SnowColor.append(self.color)
                self.SnowShape.append(self.rect)"""


    def Snow(self, ins):

        for i in range(len(self.SnowShape)):

            if self.SnowShape[i].pos[1] < -20:
                self.Y_container[i] = 1400

        for i in range(len(self.PX)):
            self.Y_container[i] -= 0.6
            self.X = (math.cos((2*math.pi) * (self.Y_container[i]/self.frequency[i]))) * self.width_number[i] + self.PX[i]
            self.SnowShape[i].pos = (self.X-(self.frequency[i]), self.Y_container[i]+(self.PY[i]))






    def GamePlay(self):

        over_anim = Animation(opacity=1, size_hint=(0.5,0.5))


        if self.FinalScore is False:

            if self.ids.B1.own == "Player" and self.ids.B2.own == "Player" and self.ids.B3.own == "Player":
                print("Player wins")
                self.FinalScore = True

                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                over_anim.start(self.ids.Over)
                self.ids.img_over.source = 'Winner.jpg'

            elif self.ids.B4.own == "Player" and self.ids.B5.own == "Player" and self.ids.B6.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B7.own == "Player" and self.ids.B8.own == "Player" and self.ids.B9.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B1.own == "Player" and self.ids.B4.own == "Player" and self.ids.B7.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B2.own == "Player" and self.ids.B5.own == "Player" and self.ids.B8.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"
            elif self.ids.B3.own == "Player" and self.ids.B6.own == "Player" and self.ids.B9.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"
            elif self.ids.B1.own == "Player" and self.ids.B5.own == "Player" and self.ids.B9.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"
            elif self.ids.B3.own == "Player" and self.ids.B5.own == "Player" and self.ids.B7.own == "Player":
                print("Player wins")
                self.ids.label_over.text = "[font=SNAP____] Winner [/font]"
                self.ids.img_over.source = 'Winner.jpg'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True

            #NPC
            if self.ids.B1.own == "NPC" and self.ids.B2.own == "NPC" and self.ids.B3.own == "NPC":
                print("NPC wins")
                self.ids.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True

                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B4.own == "NPC" and self.ids.B5.own == "NPC" and self.ids.B6.own == "NPC":
                print("NPC wins")
                self.ids.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B7.own == "NPC" and self.ids.B8.own == "NPC" and self.ids.B9.own == "NPC":
                print("NPC wins")
                self.ids.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B1.own == "NPC" and self.ids.B4.own == "NPC" and self.ids.B7.own == "NPC":
                print("NPC wins")
                self.ids.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"

            elif self.ids.B2.own == "NPC" and self.ids.B5.own == "NPC" and self.ids.B8.own == "NPC":
                print("NPC wins")
                self.ids.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"
            elif self.ids.B3.own == "NPC" and self.ids.B6.own == "NPC" and self.ids.B9.own == "NPC":
                print("NPC wins")
                self.ids.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"
            elif self.ids.B1.own == "NPC" and self.ids.B5.own == "NPC" and self.ids.B9.own == "NPC":
                print("NPC wins")
                self.ids.Over.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True
                self.StateGame = "Over!"
            elif self.ids.B3.own == "NPC" and self.ids.B5.own == "NPC" and self.ids.B7.own == "NPC":
                print("NPC wins")
                self.ids.Over.label_over.text = "[font=SNAP____] You lost [/font]"
                self.ids.img_over.source = 'lost.png'
                over_anim.start(self.ids.Over)
                self.FinalScore = True
                self.ids.D1.disabled = True
                self.ids.D2.disabled = True
                self.ids.D3.disabled = True
                self.ids.D4.disabled = True
                self.ids.D5.disabled = True
                self.ids.D6.disabled = True
                self.ids.D7.disabled = True
                self.ids.D8.disabled = True
                self.ids.D9.disabled = True

            if self.StateGame != "Over!":

                if self.ids.B1.opacity == 1 and self.ids.B2.opacity == 1 and self.ids.B3.opacity == 1 and self.ids.B4.opacity == 1 and self.ids.B5.opacity == 1 and self.ids.B6.opacity == 1 and self.ids.B7.opacity == 1 and self.ids.B8.opacity == 1 and self.ids.B9.opacity == 1:
                    self.ids.D1.disabled = True
                    self.ids.D2.disabled = True
                    self.ids.D3.disabled = True
                    self.ids.D4.disabled = True
                    self.ids.D5.disabled = True
                    self.ids.D6.disabled = True
                    self.ids.D7.disabled = True
                    self.ids.D8.disabled = True
                    self.ids.D9.disabled = True
                    self.ids.img_over.source = 'tie.jpg'
                    self.ids.label_over.text = "[font=SNAP____] Game Tie! [/font]"
                    over_anim.start(self.ids.Over)
                    print("Game Tied!")
                    self.FinalScore = True





    def RealTimeApp(self, ins):



        self.GamePlay()

        if self.ready is False:

            if self.ids.panel.opacity == 0 and self.ids.second_panel.opacity == 0:
                self.ids.B1.disabled = False
                self.ids.B2.disabled = False
                self.ids.B3.disabled = False
                self.ids.B4.disabled = False
                self.ids.B5.disabled = False
                self.ids.B6.disabled = False
                self.ids.B7.disabled = False
                self.ids.B8.disabled = False
                self.ids.B9.disabled = False

                self.ready = True

        elif self.ready is True:
            pass



    def StartToPlay(self):


        if self.ids.SelectX.state == "normal" and self.ids.Select0.state == "normal":
            print("select one")

        else:

            self.ids.D1.disabled = False
            self.ids.D2.disabled = False
            self.ids.D3.disabled = False
            self.ids.D4.disabled = False
            self.ids.D5.disabled = False
            self.ids.D6.disabled = False
            self.ids.D7.disabled = False
            self.ids.D8.disabled = False
            self.ids.D9.disabled = False

            anim = Animation(opacity=0, size_hint=(0,0))
            anim.start(self.ids.panel)
            anim.start(self.ids.second_panel)

            if self.ids.SelectX.state == "down":
                self.ToolPlayer = f"[font=CHILLER]X[/font]"
                self.NPCTool = f"[font=CHILLER]O[/font]"

            if self.ids.Select0.state == "down":
                self.NPCTool = f"[font=CHILLER]X[/font]"
                self.ToolPlayer = f"[font=CHILLER]O[/font]"

    def ButtonPlay(self):
        self.Play()
    def Play(self):

        NPC.Brain().predict_next_warning.clear()
        self.predicted_warning_move = []
        self.ids.second_panel.opacity = 1
        self.ids.second_panel.size_hint= (0.6,0.7)
        self.ids.tool.right_action_items = [["microsoft-xbox-controller-menu", lambda x: self.Dialog(), "Menu"]]



        self.FinalScore = False

        self.ids.screen_manager.current = "game"

        self.FinalScore = False

        self.StatePlay = ""
        self.Wait = False

        self.StateGame = ""

        self.Prediction = []

        self.ids.B1.text = ""
        self.ids.B2.text = ""
        self.ids.B3.text = ""
        self.ids.B4.text = ""
        self.ids.B5.text = ""
        self.ids.B6.text = ""
        self.ids.B7.text = ""
        self.ids.B8.text = ""
        self.ids.B9.text = ""

        self.oldPrediction = []
        self.ids.Over.opacity = 0
        self.ids.Over.size_hint = (0, 0)



    def Crossed(self, widget):

        if self.StateGame != "Over!":
            self.ids.D1.disabled = True
            self.ids.D2.disabled = True
            self.ids.D3.disabled = True
            self.ids.D4.disabled = True
            self.ids.D5.disabled = True
            self.ids.D6.disabled = True
            self.ids.D7.disabled = True
            self.ids.D8.disabled = True
            self.ids.D9.disabled = True
            widget.text =  self.ToolPlayer
            self.WidgetCoor = widget
            anim = Animation(opacity=1)
            anim.start(widget)

            widget.own = "Player"
            self.oldPrediction.append(widget.coordinate)



            NPC.Brain().AnalizeCurentOpponentPosition(self.ListOfWidget, self.ToolPlayer)
            NPC.Brain().PredictOpponentFuturePosition(self.ListOfWidget, self.ToolPlayer, self.FinalScore)
            self.predicted_warning_move = NPC.Brain().predict_next_warning
            predicted_warning_move_new = []
            for moves in self.predicted_warning_move:

                if moves not in predicted_warning_move_new:
                    predicted_warning_move_new.append(moves)
                else:
                    pass

            if len(predicted_warning_move_new) == 0:
                pass
            else:

                for i in predicted_warning_move_new:
                    if i not in self.Prediction:

                        self.Prediction.append(i)

                predicted_warning_move_new = []

            Clock.schedule_once(self.TheWait, 2)
        else:
            print("Game Over!")


    def TheWait(self, instance):



        if self.StateGame != "Over!":
            print("predicted",self.Prediction)


            for i in self.Prediction:
                if i in self.oldPrediction:

                    print("joser: ", i)
                    print("deleted!")
                    print("predicted : ", self.Prediction)
                    print("predicted left", self.oldPrediction)

                    self.Prediction.remove(i)
                    print("predicted deleted: ", self.Prediction)

                    break

            if len(self.Prediction) == 0:
                print("no threat")
                guess_list = []
                for i in self.ListOfWidget:
                    if i.text == '':
                        guess_list.append(i)


                try:

                    ran = random.randint(0, len(guess_list) -1)
                    new_play = guess_list[ran]
                    new_play.text = self.NPCTool
                    A = Animation(opacity=1)
                    new_play.own = "NPC"
                    self.oldPrediction.append(new_play.coordinate)
                    print(self.oldPrediction)
                    A.start(new_play)

                except:
                    pass

                """for i in range(1):
                    print(self.WidgetCoor.name)
                    l = self.WidgetCoor.coordinate[0]
                    l -= 1
                    if l < 1 or l > 3:
                        pass
                    else:

                        print(f"left: ({l} {self.WidgetCoor.coordinate[1]})")
                        next_play.append([l, self.WidgetCoor.coordinate[1]])
                        break

                    r = self.WidgetCoor.coordinate[0]
                    r += 1
                    if r < 1 or r > 3:
                        pass
                    else:

                        print(f"right: ({r} {self.WidgetCoor.coordinate[1]})")
                        next_play.append([r, self.WidgetCoor.coordinate[1]])
                        break


                    u = self.WidgetCoor.coordinate[1]
                    u += 1
                    if u < 1 or u > 3:
                        pass
                    else:

                        print(f"up: ({self.WidgetCoor.coordinate[0]} {u})")
                        next_play.append([self.WidgetCoor.coordinate[0], u])
                        break

                    d = self.WidgetCoor.coordinate[1]
                    d -= 1

                    if d < 1 or d > 3:
                        pass
                    else:

                        print(f"down: ({self.WidgetCoor.coordinate[0]} {d})")
                        next_play.append([self.WidgetCoor.coordinate[0], d])
                        break

                for i in self.ListOfWidget:

                    if i.coordinate == next_play[0]:
                        #print(f"NEXT PLAY: {i.coordinate}")
                        print(f"NEXT! {next_play}")
                        i.text = f"[font=CHILLER]{self.NPCTool}[/font]"
                        i.own = "NPC"
                        A = Animation(opacity=1)
                        A.start(i)"""

            elif len(self.Prediction) != 0:


                self.Players = True
                #print(f"NPC Played {self.Prediction}")
                for i in self.ListOfWidget:

                    for a in self.Prediction:

                        if i.coordinate == a:

                            #print(f"is here {i.coordinate}")

                            if i.opacity == 1:
                                pass
                                #print(f"already {i.coordinate}")

                            if self.Players is True and i.opacity != 1:
                                i.text = self.NPCTool
                                A = Animation(opacity=1)
                                A.start(i)
                                i.own = "NPC"


                                self.Players = False
                                print("before: ",self.Prediction)

                                self.Prediction.remove(i.coordinate)
                                self.oldPrediction.append(i.coordinate)
                                print("after: ",self.Prediction)




        self.ids.D1.disabled = False
        self.ids.D2.disabled = False
        self.ids.D3.disabled = False
        self.ids.D4.disabled = False
        self.ids.D5.disabled = False
        self.ids.D6.disabled = False
        self.ids.D7.disabled = False
        self.ids.D8.disabled = False
        self.ids.D9.disabled = False


        """elif len(self.Prediction) != 0:
                guess_list = []
                for i in self.ListOfWidget:
                    if i.text == '':
                        guess_list.append(i)

                ran = random.randint(0, len(guess_list) - 1)
                new_play = guess_list[ran]
                new_play.text = self.NPCTool
                A = Animation(opacity=1)
                new_play.own = "NPC"
                A.start(new_play)
"""

class Noughts(MDApp):
    def build(self):
        Window.size = (900, 650)
        return MainLayout()

Noughts().run()
