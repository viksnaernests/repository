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
        self.refresh_saved_entries()

    @staticmethod
    def create_character_options():
        return tuple(
            (nosaukums, tk.BooleanVar(value=True), rakstzimes)
            for nosaukums, rakstzimes in RAKSTZIMJU_VEIDI
        )

    def build_ui(self):
        galvenais = tk.Frame(self.sakne, padx=20, pady=20)
        galvenais.pack(fill="both", expand=True)

        self.build_header(galvenais)
        self.build_length_controls(galvenais)
        self.build_character_options(galvenais)
        self.build_action_buttons(galvenais)
        self.build_result_area(galvenais)
        self.build_saved_entries(galvenais)
        self.configure_resizing(galvenais)

    def build_header(self, vecaks):
        tk.Label(
            vecaks, text="Drošu paroļu ģenerators", font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 20))

    def build_length_controls(self, vecaks):
        tk.Label(vecaks, text="Paroles garums:").grid(row=1, column=0, sticky="w")
        tk.Entry(vecaks, textvariable=self.garuma_mainigais, width=10).grid(
            row=1, column=1, sticky="w"
        )
        tk.Label(
            vecaks,
            text=f"({MINIMALAIS_PAROLES_GARUMS}-{MAKSIMALAIS_PAROLES_GARUMS} rakstzīmes)",
        ).grid(row=1, column=2, sticky="w")

    def build_character_options(self, vecaks):
        iespeju_ramis = tk.LabelFrame(vecaks, text="Rakstzīmju veidi", padx=10, pady=10)
        iespeju_ramis.grid(row=2, column=0, columnspan=4, sticky="we", pady=15)

        for rinda, (nosaukums, ieslegts_mainigais, _) in enumerate(self.rakstzimju_iespejas):
            tk.Checkbutton(
                iespeju_ramis,
                text=nosaukums,
                variable=ieslegts_mainigais,
            ).grid(row=rinda, column=0, sticky="w")

    def build_action_buttons(self, vecaks):
        darbibu_ramis = tk.Frame(vecaks)
        darbibu_ramis.grid(row=3, column=0, columnspan=4, sticky="we", pady=10)

        pogas = (
            ("Ģenerēt paroli", self.generate_password),
            ("Kopēt", self.copy_password),
            ("Saglabāt JSON", self.save_password_to_json),
            ("Notīrīt JSON failu", self.clear_json_file),
        )

        for kolonna, (teksts, komanda) in enumerate(pogas):
            tk.Button(darbibu_ramis, text=teksts, width=18, command=komanda).grid(
                row=0,
                column=kolonna,
                padx=(0, 10) if kolonna < len(pogas) - 1 else 0,
                pady=5,
            )

    def build_result_area(self, vecaks):
        tk.Label(vecaks, text="Rezultāts:").grid(
            row=4, column=0, sticky="w", pady=(10, 0)
        )
        tk.Entry(
            vecaks,
            textvariable=self.rezultata_mainigais,
            width=75,
            font=("Consolas", 11),
        ).grid(row=5, column=0, columnspan=4, sticky="we", pady=5)

        tk.Label(vecaks, text="Paroles drošums:").grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )
        tk.Label(
            vecaks,
            textvariable=self.drosuma_mainigais,
            font=("Arial", 11, "bold"),
            relief="groove",
            width=18,
            pady=4,
        ).grid(row=6, column=1, sticky="w", pady=(10, 0))

        bridinajuma_teksts = (
            "Drošības piezīme: passwords.json fails nav šifrēts. "
            "Nesaglabājiet šeit īstas kontu paroles, ja fails nav aizsargāts."
        )
        tk.Label(
            vecaks, text=bridinajuma_teksts, fg="darkred", wraplength=720, justify="left"
        ).grid(row=7, column=0, columnspan=4, sticky="w", pady=15)

    def build_saved_entries(self, vecaks):
        saglabato_ramis = tk.LabelFrame(vecaks, text="Saglabātie ieraksti", padx=10, pady=10)
        saglabato_ramis.grid(row=8, column=0, columnspan=4, sticky="nsew", pady=10)

        self.saglabato_saraksts = tk.Listbox(saglabato_ramis, height=10, width=100)
        self.saglabato_saraksts.grid(row=0, column=0, sticky="nsew")

        ritjosla = tk.Scrollbar(
            saglabato_ramis, orient="vertical", command=self.saglabato_saraksts.yview
        )
        ritjosla.grid(row=0, column=1, sticky="ns")
        self.saglabato_saraksts.config(yscrollcommand=ritjosla.set)

        tk.Button(
            saglabato_ramis, text="Atjaunot sarakstu", command=self.refresh_saved_entries
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        saglabato_ramis.columnconfigure(0, weight=1)
        saglabato_ramis.rowconfigure(0, weight=1)

    @staticmethod
    def configure_resizing(vecaks):
        vecaks.columnconfigure(0, weight=1)
        vecaks.columnconfigure(3, weight=1)
        vecaks.rowconfigure(8, weight=1)

    def generate_password(self):
        garums = self.get_password_length()
        if garums is None:
            return

        rakstzimju_kopas = self.get_selected_character_pools()
        if not rakstzimju_kopas:
            messagebox.showerror(
                "Kļūda", "Lūdzu, izvēlieties vismaz vienu rakstzīmju veidu."
            )
            return

        atlasito_veidu_skaits = len(rakstzimju_kopas)
        if garums < atlasito_veidu_skaits:
            messagebox.showerror("Kļūda", "Paroles garums ir pārāk īss.")
            return

        parole = self.create_password(garums, rakstzimju_kopas)
        self.rezultata_mainigais.set(parole)
        self.drosuma_mainigais.set(self.evaluate_strength(parole, atlasito_veidu_skaits))

    def get_password_length(self):
        try:
            garums = int(self.garuma_mainigais.get())
        except ValueError:
            messagebox.showerror("Kļūda", GARUMA_KLUDAS_ZINOJUMS)
            return None

        if not (MINIMALAIS_PAROLES_GARUMS <= garums <= MAKSIMALAIS_PAROLES_GARUMS):
            messagebox.showerror("Kļūda", GARUMA_KLUDAS_ZINOJUMS)
            return None

        return garums

    def get_selected_character_pools(self):
        return [
            rakstzimes
            for _, ieslegts_mainigais, rakstzimes in self.rakstzimju_iespejas
            if ieslegts_mainigais.get()
        ]

    @staticmethod
    def create_password(garums, rakstzimju_kopas):
        paroles_rakstzimes = [secrets.choice(kopa) for kopa in rakstzimju_kopas]
        visas_rakstzimes = "".join(rakstzimju_kopas)

        paroles_rakstzimes.extend(
            secrets.choice(visas_rakstzimes)
            for _ in range(garums - len(paroles_rakstzimes))
        )

        secrets.SystemRandom().shuffle(paroles_rakstzimes)
        return "".join(paroles_rakstzimes)
    
    @staticmethod
    def evaluate_strength(parole, atlasito_veidu_skaits):
        garums = len(parole)
        if garums >= 16 and atlasito_veidu_skaits == 4:
            return "Ļoti droša"
        if garums >= 12 and atlasito_veidu_skaits >= 3:
            return "Droša"
        if garums >= 8 and atlasito_veidu_skaits >= 2:
            return "Vidēja"
        return "Vāja"

    def copy_password(self):
        parole = self.rezultata_mainigais.get()
        if not parole:
            messagebox.showwarning("Paziņojums", "Nav paroles, ko kopēt.")
            return
        self.sakne.clipboard_clear()
        self.sakne.clipboard_append(parole)
        self.sakne.update()
        messagebox.showinfo("Paziņojums", "Parole nokopēta starpliktuvē.")

    def load_json_data(self):
        if not PAROLU_FAILS.exists():
            return []
        try:
            with PAROLU_FAILS.open("r", encoding="utf-8") as fails:
                saglabatas_paroles = json.load(fails)
                return saglabatas_paroles if isinstance(saglabatas_paroles, list) else []
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "Brīdinājums", "JSON fails ir bojāts. Sākam no jauna."
            )
            return []

    def save_password_to_json(self):
        parole = self.rezultata_mainigais.get()
        if not parole:
            messagebox.showwarning("Paziņojums", "Nav paroles, ko saglabāt.")
            return

        apstiprinajums = messagebox.askyesno(
            "Drošības brīdinājums",
            "Paroles tiks saglabātas kā vienkāršs teksts. Turpināt?",
        )
        if not apstiprinajums:
            return

        saglabatas_paroles = self.load_json_data()
        nakamais_id = max(
            (ieraksts.get("id", 0) for ieraksts in saglabatas_paroles), default=0
        ) + 1

        jauns_ieraksts = {
            "id": nakamais_id,
            "password": parole,
            "length": len(parole),
            "strength": self.drosuma_mainigais.get(),
            "createdAt": datetime.now().isoformat(timespec="seconds"),
        }

        saglabatas_paroles.append(jauns_ieraksts)

        try:
            with PAROLU_FAILS.open("w", encoding="utf-8") as fails:
                json.dump(saglabatas_paroles, fails, ensure_ascii=False, indent=4)
        except OSError as kluda:
            messagebox.showerror("Kļūda", f"Neizdevās saglabāt paroles:\n{kluda}")
            return

        self.refresh_saved_entries()
        messagebox.showinfo("Paziņojums", "Parole veiksmīgi saglabāta.")