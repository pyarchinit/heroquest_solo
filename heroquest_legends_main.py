# -*- coding: utf-8 -*-

"""
/***************************************************************************
        Heroquest's Legends Solo by Mandor the Druid
                             -------------------
    begin                : 2021-01-02
    copyright            : (C) 2021 by Luca Mandolesi
    email                : mandoluca at gmail.com
    version              : 0.83 ALPHA
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import locale
import sys, os
import random

from PyQt5 import QtWidgets, uic, QtCore

#codeadded
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QLabel

#codeadde d/
from heroquest_solo_function import Heroquest_solo


from adventure_panel_settings_main import AdventurePanelSettings

class Ui(QtWidgets.QMainWindow):
    #TODO aggiungere come posizione il mostro davanti alla porta fuori o dentro la stanza
    #TODO aggiungere oltre che davanti, davanti ed adiacente a te.
    #TODO aggiungere opzione per circondare l'eroe
    CONFIG = ""
    local_language = locale.getdefaultlocale()
    #file_name = 'en_EN.txt'
    if local_language[0] == 'it_IT':
        CONFIG = open('./languages/IT_it.txt', "rb+")
    else :
        CONFIG = open('./languages/EN_en.txt', "rb+")
    data_config = CONFIG.read()
    CONFIG.close()
    CONFIG_DICT = eval(data_config)

    HQ_SOLO = ""

    CURRENT_ROUND = 1

    MONSTER_LIST = ''

    TREASURES_FINDS = 0

    CHRONICLE = ""


    #todo messaggio con punto di partenza
    #todo aggiungere segnalatore di fine avventura scale trovate
    #todo se il mostro prima attacca poi si sposta per lasciare spazio ad un altro mostro se è nella stanza


    def __init__(self):
        super(Ui, self).__init__()
        self.acceptDrops()
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        uic.loadUi(os.path.join(os.path.dirname(__file__),'heroquest_legends.ui'), self)

        self.HQ_SOLO = Heroquest_solo(self.CONFIG_DICT)
        self.pushButton_close.clicked.connect(self.close)

        bg_img_path = './background.png'  #os.path.join(os.path.dirname(__file__),'mappa.png')
        oImage = QImage(bg_img_path)
        sImage = oImage.scaled(QSize(800, 768))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))

        self.setPalette(palette)
        self.charge_list()
        self.show()


    def on_pushButton_settings_pressed(self):
        dlg = AdventurePanelSettings(self)
        dlg.DICT = self.CONFIG_DICT
        dlg.insertItems()

        dlg.exec_()
        #open the panel and freeze the process

        #then pass to variables data from settings
        """
        items, order_type = dlg.ITEMS, dlg.TYPE_ORDER
        self.SORT_ITEMS_CONVERTED = []
        for i in items:
            # QMessageBox.warning(self, "Messaggio",i, QMessageBox.Ok)
            self.SORT_ITEMS_CONVERTED.append(
                self.CONVERSION_DICT[str(i)])  # apportare la modifica nellle altre schede
        self.SORT_MODE = order_type
        self.empty_fields()
        id_list = []
        for i in self.DATA_LIST:
            id_list.append(eval("i." + self.ID_TABLE))
        self.DATA_LIST = []
        temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE,
                                                    self.MAPPER_TABLE_CLASS, self.ID_TABLE)
        for i in temp_data_list:
            self.DATA_LIST.append(i)
        self.BROWSE_STATUS = 'b'
        self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
        if type(self.REC_CORR) == "<type 'str'>":
            corr = 0
        else:
            corr = self.REC_CORR
        self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
        self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
        self.SORT_STATUS = "o"
        self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
        self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR + 1)
        self.fill_fields()
        """


    def charge_list(self):
        db_monsters_charged = self.HQ_SOLO.MONSTERS_CATEGORY

        self.MONSTER_LIST = []

        for value in db_monsters_charged.values():

            self.MONSTER_LIST.append(self.CONFIG_DICT['monster_name_conversion_dict'][value])

        self.comboBox_monster_attack.clear()

        self.comboBox_monster_attack.addItems(self.MONSTER_LIST)

        fornitures_list = self.CONFIG_DICT['forniture_name_reconversion_dict']
        self.comboBox_fornitures.addItems([*fornitures_list])


    def on_pushButton_the_mission_pressed(self):
        rng_base = random.SystemRandom()

        mission_number_rand = rng_base.randint(4,4)

        self.HQ_SOLO.special_data_mission_charged(mission_number_rand)

        the_mission_dict = self.CONFIG_DICT['missions_dict']

        rng_base = random.SystemRandom()

        wanderer_monster_number_rand = rng_base.randint(1, 7)
        wanderer_monster = self.CONFIG_DICT['monsters_dict'][wanderer_monster_number_rand]
        wanderer_monster_text = self.CONFIG_DICT['monsters_msg_3']

        the_mission_text = '{}\n{}{}'.format(the_mission_dict[mission_number_rand][1],wanderer_monster_text,wanderer_monster)
        self.textEdit_the_mission.setText(the_mission_text)
        self.QLabel_the_title.setText(the_mission_dict[mission_number_rand][0])
        self.CHRONICLE = the_mission_text
        self.textEdit_chronicle.setText(self.CHRONICLE)

        self.pushButton_aisles.setEnabled(True)
        self.pushButton_rooms.setEnabled(True)
        self.pushButton_treasures_finds.setEnabled(True)
        self.pushButton_treasures_random.setEnabled(True)
        self.pushButton_treasure_card.setEnabled(True)
        self.pushButton_traps_and_secret_doors_finder.setEnabled(True)
        self.pushButton_hero_attack.setEnabled(True)
        self.pushButton_monster_attack.setEnabled(True)
        self.pushButton_round.setEnabled(True)

    def on_pushButton_round_pressed(self):
        self.textEdit_aisles.setText("")
        self.textEdit_monsters.setText("")
        self.textEdit_room_description.setText("")
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_description.setText("")
        self.textEdit_traps.setText("")
        self.textEdit_secret_doors.setText("")
        self.textEdit_treasure_cards_description.setText("")
        self.textEdit_combat_text.setText("")
        self.CURRENT_ROUND = int(self.lineEdit_round.text())
        next_turn = self.CURRENT_ROUND+1
        self.lineEdit_round.setText(str(next_turn))
        self.CURRENT_ROUND = next_turn


    def on_pushButton_aisles_pressed(self):
        self.textEdit_traps.setText("")
        current_turn = int(self.lineEdit_round.text())
        self.textEdit_aisles.setText("")
        if self.radioButton_aisles_not_explored.isChecked() == True:
            if current_turn == 1 or current_turn == 2:
                msg_num = self.HQ_SOLO.random_numbers()
                while (msg_num) >= 21:
                    msg_num = self.HQ_SOLO.random_numbers()  # return always door at first and second turn
                msg = self.HQ_SOLO.aisles(msg_num)
            else:
                msg = self.HQ_SOLO.aisles(self.HQ_SOLO.random_numbers())
        else:
            print("gigi 2")
            print("TOTAL TURNS: "+str(self.HQ_SOLO.TOTAL_NUMBER_OF_TURNS))
            print("current turns"+str(self.CURRENT_ROUND))
            print("percent"+str(self.HQ_SOLO.MISSION_PERCENT_MADE))
            msg = self.HQ_SOLO.random_monsters_on_aisles(self.CURRENT_ROUND)


        self.textEdit_aisles.setText("")
        self.textEdit_aisles.setText(str(msg))
        self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))

    def on_pushButton_treasures_finds_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_treasures_description.setText("")
        res = self.HQ_SOLO.treasures(self.HQ_SOLO.random_numbers())
        msg = res[0]
        self.TREASURES_FINDS = res[1]
        if self.TREASURES_FINDS == 1:
            self.pushButton_treasures_random.setEnabled(True)
        self.textEdit_treasures_finder.setText("")
        self.textEdit_treasures_finder.setText(str(msg))


    def on_pushButton_treasure_card_pressed(self):
        self.textEdit_traps.setText("")
        msg = self.HQ_SOLO.treasure_card(self.HQ_SOLO.random_numbers())
        self.textEdit_treasure_cards_description.setText("")
        self.textEdit_treasure_cards_description.setText(str(msg))


    def on_pushButton_treasures_random_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_treasures_description.setText("")
        forniture = self.comboBox_fornitures.currentText()
        msg = self.HQ_SOLO.treasure_random(self.HQ_SOLO.random_numbers(), forniture)
        self.pushButton_treasures_random.setEnabled(False)
        self.TREASURES_FINDS = 0
        self.textEdit_treasures_description.setText(str(msg))
        self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))


    def on_pushButton_traps_and_secret_doors_finder_pressed(self):
        self.textEdit_traps.setText("")
        msg_traps = self.HQ_SOLO.traps(self.HQ_SOLO.random_numbers())
        msg_secret_door = self.HQ_SOLO.secret_doors(self.HQ_SOLO.random_numbers())

        self.textEdit_traps.setText(str(msg_traps))
        self.textEdit_secret_doors.setText(str(msg_secret_door))


    def on_pushButton_rooms_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_room_description.setText('')
        self.textEdit_monsters.setText('')
        if self.radioButton_explored.isChecked() == True:
            ##print("room pressed_1")
            room_explored = 1
            self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))
        else:
            ##print("room pressed_2")
            room_explored = 0

        current_turn = int(self.lineEdit_round.text())
        ##print("room pressed_3-uscita da room pressed")
        msg_temp = self.HQ_SOLO.room_generator(self.lineEdit_room_dimension.text(), current_turn,room_explored)
        ##print("room pressed_4-rientrato da room pressed")

        if current_turn == 1 or current_turn == 2:
            msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_1'].format(msg_temp[0])
            self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))
        else:
            if msg_temp[2] != '':
                #print("puppa 1")
                self.CHRONICLE = '{} \n\n --- \n\n {}'.format(self.CHRONICLE, msg_temp[2])
                #print("puppa 2")
                self.textEdit_chronicle.setText(self.CHRONICLE)
                #print("puppa 3")
                msg_room = msg_temp[2]
                #print("puppa 4")
                self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))
            elif msg_temp[0] == '' and msg_temp[2] == '' and room_explored == 1:
                msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_7']
                self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))
            elif msg_temp[0] == '' and msg_temp[2] == '' and room_explored == 0:
                msg_room = self.HQ_SOLO.CONFIG_DICT['aux_msg_6']
                self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))
            else:
                msg_room = msg_temp[0]
                self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))

        msg_room = msg_room.replace(';.', '.')

        self.textEdit_room_description.setText(str(msg_room))

        self.textEdit_monsters.setText(str(msg_temp[1]))


    def on_pushButton_monster_attack_pressed(self):
        self.textEdit_combat_text.setText("")
        self.textEdit_traps.setText("")
        monster_category = self.comboBox_monster_attack.currentText()
        monster_group = 0
        monster_sight = 0

        if self.checkBox_group.isChecked() == True:
            monster_group = 1

        if self.checkBox_sight.isChecked() == True:
            monster_sight = 1

        mode_result = self.HQ_SOLO.fighting_system(monster_category, monster_group, monster_sight) #1 attack - 0 escape

        if mode_result == 1:
            msg_attack = self.CONFIG_DICT['attack_messages'][1]

            rng_base = random.SystemRandom()
            msg_attack = msg_attack[rng_base.randint(0, 1)]

            rng_base = random.SystemRandom()
            msg_attack_choice = msg_attack.format(self.CONFIG_DICT['choice_dict'][rng_base.randint(1, 5)])

            rng_base = random.SystemRandom()
            msg_attack_choice_direction = msg_attack_choice.format(self.CONFIG_DICT['monster_direction_dict'][rng_base.randint(1, 4)])

            self.textEdit_combat_text.setText(str(msg_attack_choice_direction))
        else:
            rng_base = random.SystemRandom()
            msg_escape = self.CONFIG_DICT['attack_messages'][2][rng_base.randint(0, 3)]
            self.textEdit_combat_text.setText(msg_escape)

    def on_pushButton_hero_attack_pressed(self):
        self.textEdit_traps.setText("")
        self.textEdit_traps.setText(self.HQ_SOLO.random_trap(self.CURRENT_ROUND))
        rand_value = self.HQ_SOLO.random_numbers()
        self.textEdit_combat_text.setText(self.HQ_SOLO.hero_attack(rand_value))

app = QtWidgets.QApplication(sys.argv)

#load language
translator = QtCore.QTranslator()
local_language = locale.getdefaultlocale()
if local_language[0] == 'it_IT':
    translator.load("./languages/IT_it.qm")
elif local_language[0] == 'en_EN':
    translator.load("./languages/EN_en.qm")
elif local_language[0] == 'es_ES':
    translator.load("./languages/ES_es.qm")
else:
    translator.load("./languages/EN_en.qm")

app.installTranslator(translator)
window = Ui()
app.exec_()



