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