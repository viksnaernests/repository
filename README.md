# Drošu paroļu ģenerators
## Projekta apraksts
Šis projekts ir Python programma ar grafisko interfeisu, kas ļauj lietotājam ģenerēt drošas paroles. Lietotājs var izvēlēties paroles garumu, rakstzīmju tipus, ģenerēt paroli, novērtēt paroles drošību, kopēt paroli un saglabāt to JSON failā.

Programma ir izstrādāta kā mācību projekts saskaņā ar tehnisko specifikāciju.

## Galvenās funkcijas
* Izvēlēties paroles garumu no 8 līdz 64 simboliem.
* * Izvēlēties rakstzīmju tipus:
    
  * lielie burti;
  * mazie burti;
  * cipari;
  * speciālās rakstzīmes.
* Ģenerēt nejaušu paroli.
* Novērtēt paroles drošuma līmeni.
* Kopēt paroli starpliktuvē.
* Saglabāt paroli `passwords.json` failā.
* Apskatīt saglabātās paroles programmas logā.
* Notīrīt JSON failu pēc lietotāja apstiprinājuma.

## Izmantotās tehnoloģijas

* Python
* Tkinter
* JSON
* Git un GitHub

## Projekta faili

* `drosu_parolu_generators.py` - galvenais programmas fails.
* `passwords.json` - fails, kurā pēc izvēles tiek saglabātas ģenerētās paroles.
* `README.md` - projekta apraksts.
* Tehniskā specifikācija - programmatūras prasību dokuments.
* Testēšanas dokumentācija - programmas testēšanas plāns.

  ## Kā palaist programmu

1. Lejupielādēt vai noklonēt projektu.
2. Atvērt projekta mapi.
3. Palaist programmu ar komandu:

```bash
python drosu_parolu_generators.py
```

## Drošības piezīme

`passwords.json` fails nav šifrēts. Tāpēc īstu kontu paroles nevajadzētu tajā saglabāt, ja fails nav aizsargāts.

## Autors

Ernests Vīksna
