#5.1. t
#Autors: Ernests Vīksna 12.j
#Drošu paroļu ģenerators


import json
import secrets
import string
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

PAROLU_FAILS = Path(__file__).resolve().with_name("passwords.json")

MINIMALAIS_PAROLES_GARUMS = 8
MAKSIMALAIS_PAROLES_GARUMS = 64
NOKLUSETAIS_PAROLES_GARUMS = 16
GARUMA_KLUDAS_ZINOJUMS = (
    "Paroles garumam jābūt skaitlim no "
    f"{MINIMALAIS_PAROLES_GARUMS} līdz {MAKSIMALAIS_PAROLES_GARUMS}."
)

LIELIE_BURTI = string.ascii_uppercase
MAZIE_BURTI = string.ascii_lowercase
CIPARI = string.digits
SIMBOLI = "!@#%&*?+-_="

RAKSTZIMJU_VEIDI = (
    ("Lielie burti (A-Z)", LIELIE_BURTI),
    ("Mazie burti (a-z)", MAZIE_BURTI),
    ("Cipari (0-9)", CIPARI),
    ("Speciālās rakstzīmes (!@#%&*)", SIMBOLI),
)


class PasswordGeneratorApp:

    def __init__(self, sakne):
        self.sakne = sakne
        self.sakne.title("Drošu paroļu ģenerators")
        self.sakne.geometry("820x620")
        self.sakne.minsize(760, 560)

        self.garuma_mainigais = tk.StringVar(value=str(NOKLUSETAIS_PAROLES_GARUMS))
        self.rezultata_mainigais = tk.StringVar(value="")
        self.drosuma_mainigais = tk.StringVar(value="-")
        self.rakstzimju_iespejas = self.create_character_options()

        self.build_ui()