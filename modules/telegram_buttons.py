import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constant import *

from .apis.deputies import obj_deputy
from .apis.senators import obj_senator


def state_buttons(type):
    buttons_per_row = 2
    keyboard = []
    UFS = list(zip(UF_NOME, UF_SIGLAS))
    UFS.append(("<< Voltar", "voltar"))

    for i in range(0, len(UFS), buttons_per_row):
        button_1 = InlineKeyboardButton(UFS[i][0], callback_data=f"{type}_{UFS[i][1]}")
        button_2 = InlineKeyboardButton(
            UFS[i + 1][0], callback_data=f"{type}_{UFS[i + 1][1]}"
        )
        keyboard.append([button_1, button_2])

    return InlineKeyboardMarkup(keyboard)


def deputies_parties_buttons():
    parties = obj_deputy.list_political_parties()
    parties.sort()
    buttons_per_row = 2
    keyboard = []

    back_button = [InlineKeyboardButton("<< Voltar", callback_data="deputado_voltar")]

    for party_tuple in zip(*[iter(parties)] * buttons_per_row):
        row = [
            InlineKeyboardButton(party, callback_data="deputado_" + party)
            for party in party_tuple
        ]
        keyboard.append(row)

    if len(parties) % buttons_per_row == 0:
        keyboard.append(back_button)
    else:
        keyboard[-1].append(back_button)

    return InlineKeyboardMarkup(keyboard)


def senators_parties_buttons():
    parties = obj_senator.list_political_parties()
    parties.sort()
    buttons_per_row = 2
    keyboard = []

    back_button = [InlineKeyboardButton("<< Voltar", callback_data="senador_voltar")]

    for party_tuple in zip(*[iter(parties)] * buttons_per_row):
        row = [
            InlineKeyboardButton(party, callback_data="senador_" + party)
            for party in party_tuple
        ]
        keyboard.append(row)

    keyboard.append(back_button)
    return InlineKeyboardMarkup(keyboard)


def deputies_buttons():
    keyboard = [
        [
            InlineKeyboardButton("Por Partido ", callback_data="deputado_partido"),
            InlineKeyboardButton("Por Estado", callback_data="deputado_estado"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def senators_buttons():
    keyboard = [
        [
            InlineKeyboardButton("Por Partido ", callback_data="senador_partido"),
            InlineKeyboardButton("Por Estado", callback_data="senador_estado"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
