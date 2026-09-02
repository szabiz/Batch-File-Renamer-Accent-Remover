#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File and folder name accent-remover and batch renaming tool
================================================================
- Import files/folders
- Optional accent removal & space replacement with exception list
- Custom replacement options
- Character position delete & insert
- Auto-numbering support
- Revert / Undo functionality
- English / Hungarian bilingual UI
"""

import os
import re
import unicodedata
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ======================================================================
# Translations
# ======================================================================
TRANSLATIONS = {
    "title": {
        "hu": "Fájl- és mappanév ékezetmentesítő / kötegelt átnevező",
        "en": "File & Folder Name Accent Remover / Batch Renamer",
    },
    "add_files": {"hu": "Fájlok hozzáadása...", "en": "Add files..."},
    "add_folder": {"hu": "Mappa hozzáadása...", "en": "Add folder..."},
    "remove_selected": {"hu": "Kijelölt törlése a listából", "en": "Remove selected from list"},
    "clear_list": {"hu": "Lista ürítése", "en": "Clear list"},
    "undo": {"hu": "Visszaállítás (undo)", "en": "Undo last rename"},
    "exit": {"hu": "Kilépés", "en": "Exit"},
    "rename_button": {"hu": "Kötegelt átnevezés végrehajtása", "en": "Run batch rename"},
    "col_original": {"hu": "Eredeti név", "en": "Original name"},
    "col_new": {"hu": "Új név (előnézet)", "en": "New name (preview)"},
    "status_no_items": {"hu": "Nincs betöltött elem.", "en": "No items loaded."},
    "status_loaded": {
        "hu": "{db} elem betöltve — ebből {valtozo} névben lesz változás.",
        "en": "{db} items loaded — {valtozo} of them will change.",
    },

    "menu_settings": {"hu": "Beállítások", "en": "Settings"},
    "menu_accent_removal": {"hu": "Ékezetmentesítés...", "en": "Accent removal..."},
    "menu_custom_replacements": {"hu": "Egyéni karaktercserék...", "en": "Custom character replacements..."},
    "menu_position_delete": {
        "hu": "Karakterek törlése pozíció szerint...",
        "en": "Delete characters by position...",
    },
    "menu_position_insert": {
        "hu": "Karakterek beszúrása pozíció szerint...",
        "en": "Insert characters by position...",
    },
    "menu_autonumber": {
        "hu": "Automatikus számozás...",
        "en": "Auto-numbering...",
    },
    "menu_language": {"hu": "Nyelv", "en": "Language"},
    "lang_hu": {"hu": "Magyar", "en": "Hungarian"},
    "lang_en": {"hu": "Angol", "en": "English"},
    "menu_help": {"hu": "Súgó", "en": "Help"},
    "menu_help_item": {"hu": "Súgó", "en": "Help"},
    "menu_about": {"hu": "Névjegy", "en": "About"},

    "accent_title": {"hu": "Ékezetmentesítés és szóközkezelés", "en": "Accent & Space Removal"},
    "accent_desc": {
        "hu": "A funkció eltávolítja az ékezeteket és a szóközöket '_' jelre cseréli.\n"
              "Ha vannak olyan karakterek vagy szóköz, amiket meg szeretnél tartani,\n"
              "írd be őket az alábbi mezőbe (kivételek).",
        "en": "Removes accents and replaces spaces with '_'.\n"
              "Type any characters (or space) you want to keep intact\n"
              "into the exception field below.",
    },
    "accent_exclude_label": {"hu": "Kivételek (megtartandó karakterek):", "en": "Exceptions (characters to keep):"},

    "custom_replace_title": {"hu": "Egyéni karaktercserék", "en": "Custom character replacements"},
    "custom_replace_desc": {
        "hu": "Add meg, mely karaktert (vagy szövegrészt) mire cseréljen le\n"
              "a program. Pl.: '&' -> 'es'",
        "en": "Specify which character (or text) should be replaced\n"
              "with what. E.g.: '&' -> 'and'",
    },
    "col_from": {"hu": "Erről", "en": "From"},
    "col_to": {"hu": "Erre", "en": "To"},
    "from_label": {"hu": "Erről:", "en": "From:"},
    "to_label": {"hu": "Erre:", "en": "To:"},
    "add_button": {"hu": "Hozzáadás", "en": "Add"},
    "delete_selected_replacement": {"hu": "Kijelölt törlése", "en": "Remove selected"},
    "close": {"hu": "Bezárás", "en": "Close"},
    "missing_data_title": {"hu": "Hiányzó adat", "en": "Missing data"},
    "missing_data_msg": {"hu": "Az 'Erről' / 'Szöveg' mező nem lehet üres.", "en": "The input field cannot be empty."},

    "position_delete_title": {
        "hu": "Karakterek törlése pozíció szerint",
        "en": "Delete characters by position",
    },
    "position_delete_desc": {
        "hu": "Add meg, mely karakterpozíció(ka)t törölje a program a névből\n"
              "(a kiterjesztés nélkül számolva, balról jobbra, 1-től indulva).\n\n"
              "Például:\n"
              "  1        -> csak az 1. karaktert törli\n"
              "  1-5      -> az 1-től az 5. karakterig mindet törli",
        "en": "Specify which character position(s) should be deleted\n"
              "from the name (extension excluded, counted left to right,\n"
              "starting at 1).\n\n"
              "Examples:\n"
              "  1        -> deletes only the 1st character\n"
              "  1-5      -> deletes characters 1 through 5",
    },
    "position_input_label": {"hu": "Pozíció(k):", "en": "Position(s):"},
    "apply_button": {"hu": "Alkalmaz", "en": "Apply"},
    "clear_button": {"hu": "Törlés / Kikapcsolás", "en": "Clear / Disable"},
    "position_current_label": {
        "hu": "Jelenleg alkalmazott pozíciók: {lista}",
        "en": "Currently applied positions: {lista}",
    },
    "position_none": {"hu": "nincs", "en": "none"},

    "insert_title": {
        "hu": "Karakterek beszúrása pozíció szerint",
        "en": "Insert characters by position",
    },
    "insert_desc": {
        "hu": "Add meg, hogy melyik karakterpozícióhoz és mit szeretnél beszúrni\n(pl. 1-es pozíció elé). Ha üresen hagyod a pozíciót,\na név leggelejére (Elé) vagy legvégére (Utána) szúrja be.",
        "en": "Specify where and what you want to insert\n(e.g., before position 1). Leave position empty to\ninsert at the very beginning (Before) or end (After).",
    },
    "col_pos": {"hu": "Poz.", "en": "Pos."},
    "col_mode": {"hu": "Hely", "en": "Placement"},
    "col_text": {"hu": "Szöveg", "en": "Text"},
    "mode_before": {"hu": "Elé", "en": "Before"},
    "mode_after": {"hu": "Utána", "en": "After"},

    "autonumber_title": {
        "hu": "Automatikus számozás",
        "en": "Auto-numbering",
    },
    "autonumber_desc": {
        "hu": "A fájlok nevét lecseréli egy növekvő sorszámra (1, 2, 3...).\n"
              "Ha elő- vagy utótagot adsz meg, a szám elé/mögé illeszti őket.",
        "en": "Replaces filenames with sequential numbers (1, 2, 3...).\n"
              "If prefix or suffix is defined, they will be attached.",
    },
    "autonumber_enable": {
        "hu": "Automatikus számozás bekapcsolása",
        "en": "Enable auto-numbering",
    },
    "autonumber_prefix": {
        "hu": "Előtag (szám elé):",
        "en": "Prefix (before number):",
    },
    "autonumber_suffix": {
        "hu": "Utótag (szám után):",
        "en": "Suffix (after number):",
    },
    "autonumber_start": {
        "hu": "Kezdősorszám:",
        "en": "Start number:",
    },
    "autonumber_digits": {
        "hu": "Min. számjegyek (pl. 2 -> 01, 02):",
        "en": "Min. digits (e.g. 2 -> 01, 02):",
    },

    "scope_selected": {
        "hu": "A módosítás csak a kijelölt {n} elemre lesz alkalmazva.",
        "en": "The change will only apply to the {n} selected items.",
    },
    "scope_all": {
        "hu": "Nincs kijelölés (vagy teljes a kijelölés) — a módosítás mind a(z) {n} elemre lesz alkalmazva.",
        "en": "Nothing selected (or all selected) — the change will apply to all {n} items.",
    },

    "help_title": {"hu": "Súgó", "en": "Help"},
    "help_text": {
        "hu": (
            "Használati útmutató\n"
            "────────────────────\n\n"
            "1. Kattints a 'Fájlok hozzáadása...' vagy 'Mappa hozzáadása...'\n"
            "   gombra elemek betöltéséhez.\n\n"
            "2. A táblázatban azonnal látod az eredeti és az új nevet.\n\n"
            "3. Ékezetmentesítés (Beállítások > Ékezetmentesítés):\n"
            "   - Eltávolítja az ékezeteket és a szóközöket '_' jelekre cseréli.\n"
            "   - Megadhatsz kivétel karaktereket is.\n\n"
            "4. Automatikus számozás (Beállítások > Automatikus számozás):\n"
            "   - Sorszámozhatod a fájlokat (1, 2, 3...) opcionális elő- és utótaggal.\n\n"
            "5. A Beállítások menüben beállíthatsz egyéni karaktercseréket,\n"
            "   valamint pozíció szerinti törlést és beszúrást is.\n\n"
            "6. A 'Kötegelt átnevezés végrehajtása' gombra kattintva futtatható az átnevezés.\n\n"
            "7. A 'Visszaállítás (undo)' gombbal visszavonhatod a legutóbbi műveletet.\n\n"
            "8. A nyelv a Beállítások > Nyelv menüben változtatható meg."
        ),
        "en": (
            "How to use\n"
            "────────────────────\n\n"
            "1. Click 'Add files...' or 'Add folder...' to load items into the list.\n\n"
            "2. The table displays original and preview names immediately.\n\n"
            "3. Accent Removal (Settings > Accent removal):\n"
            "   - Removes accents and replaces spaces with '_'.\n"
            "   - You can specify exceptions to keep.\n\n"
            "4. Auto-numbering (Settings > Auto-numbering):\n"
            "   - Number files sequentially (1, 2, 3...) with optional prefix and suffix.\n\n"
            "5. In Settings, you can configure custom replacements, position-based\n"
            "   deletion, and text insertion.\n\n"
            "6. Click 'Run batch rename' to execute changes.\n\n"
            "7. Use 'Undo last rename' to restore previous filenames.\n\n"
            "8. Switch language via Settings > Language."
        ),
    },

    "about_title": {"hu": "Névjegy", "en": "About"},
    "about_app_title": {
        "hu": "Fájl- és mappanév ékezetmentesítő",
        "en": "File & Folder Name Accent Remover",
    },
    "about_desc": {
        "hu": (
            "Kötegelt átnevező program ékezetmentesítéshez,\n"
            "egyéni karaktercserékhez, beszúrásokhoz,\n"
            "automatikus számozáshoz és visszaállításhoz.\n\n"
            "Verzió: 1.6  MIT License\n"
            "Copyright (c) szabiz 2026 - Soli Deo Gloria"
        ),
        "en": (
            "Batch renaming tool for removing accents,\n"
            "custom replacements, insertions, auto-numbering\n"
            "and undo support.\n\n"
            "Version: 1.6 MIT License\n"
            "Copyright (c) szabiz 2026 - Soli Deo Gloria"
        ),
    },

    "folder_contents_title": {"hu": "Mappa tartalma", "en": "Folder contents"},
    "folder_contents_msg": {
        "hu": "Szeretnéd a mappán belüli fájlokat és almappákat is "
              "hozzáadni a listához (nem rekurzívan, csak az első szint)?",
        "en": "Do you also want to add the files and subfolders inside "
              "this folder to the list (non-recursive, first level only)?",
    },
    "error_title": {"hu": "Hiba", "en": "Error"},
    "error_reading_folder": {
        "hu": "Nem sikerült beolvasni a mappát:\n{hiba}",
        "en": "Could not read the folder:\n{hiba}",
    },

    "nothing_to_rename_title": {"hu": "Nincs mit átnevezni", "en": "Nothing to rename"},
    "nothing_to_rename_msg": {"hu": "A lista üres.", "en": "The list is empty."},
    "no_changes_title": {"hu": "Nincs teendő", "en": "Nothing to do"},
    "no_changes_msg": {
        "hu": "Egyik névben sincs változás.",
        "en": "No names would change.",
    },
    "confirm_title": {"hu": "Megerősítés", "en": "Confirm"},
    "confirm_msg": {
        "hu": "Biztosan átnevezed a kijelölt {n} elemet?\nA művelet visszaállítható az Undo gombbal.",
        "en": "Are you sure you want to rename {n} items?\nThis can be reverted with the Undo button.",
    },
    "rename_done_title": {"hu": "Átnevezés kész", "en": "Rename complete"},
    "rename_done_msg": {"hu": "{n} elem sikeresen átnevezve.", "en": "{n} items renamed successfully."},
    "rename_done_errors_title": {
        "hu": "Átnevezés kész — hibákkal",
        "en": "Rename complete — with errors",
    },
    "errors_occurred": {"hu": "\n\n{n} hiba történt:\n{lista}", "en": "\n\n{n} errors occurred:\n{lista}"},
    "and_more_errors": {"hu": "\n... és még {n} további hiba.", "en": "\n... and {n} more errors."},
    "already_exists": {"hu": "{nev} -> már létezik: {uj}", "en": "{nev} -> already exists: {uj}"},

    "undo_nothing_title": {"hu": "Nincs mit visszaállítani", "en": "Nothing to undo"},
    "undo_nothing_msg": {
        "hu": "Még nem történt átnevezés, amit vissza lehetne állítani.",
        "en": "No rename has been performed yet that could be undone.",
    },
    "undo_done_title": {"hu": "Visszaállítás kész", "en": "Undo complete"},
    "undo_done_msg": {
        "hu": "{n} elem visszaállítva az eredeti nevére.",
        "en": "{n} items restored to their original name.",
    },
    "undo_done_errors_title": {
        "hu": "Visszaállítás kész — hibákkal",
        "en": "Undo complete — with errors",
    },
    "not_found": {"hu": "nem található", "en": "not found"},
}


class Ny:
    """Simple language-switch helper class."""

    def __init__(self, nyelv="en"):
        self.nyelv = nyelv

    def t(self, kulcs, **kwargs):
        szoveg = TRANSLATIONS[kulcs][self.nyelv]
        if kwargs:
            return szoveg.format(**kwargs)
        return szoveg


# ======================================================================
# Name Generation Logic
# ======================================================================
def ekezettelenit_egyeni(szoveg: str, ekezet_beallitasok: dict) -> str:
    """Removes accents and replaces spaces with '_' based on user exceptions."""
    if not ekezet_beallitasok or not ekezet_beallitasok.get("aktiv", False):
        return szoveg

    kivetelek = set(ekezet_beallitasok.get("kivetelek", ""))

    eredmeny = []
    for c in szoveg:
        if c in kivetelek:
            eredmeny.append(c)
        elif c == ' ':
            eredmeny.append('_')
        else:
            nfkd = unicodedata.normalize('NFKD', c)
            stripped = ''.join(ch for ch in nfkd if not unicodedata.combining(ch))
            eredmeny.append(stripped)

    return ''.join(eredmeny)


def pozicio_lista_ertelmezese(szoveg: str) -> set:
    halmaz = set()
    if not szoveg:
        return halmaz

    for resz in szoveg.split(','):
        resz = resz.strip()
        if not resz:
            continue
        if '-' in resz:
            darabok = resz.split('-')
            if len(darabok) == 2 and darabok[0].strip().isdigit() and darabok[1].strip().isdigit():
                a = int(darabok[0].strip())
                b = int(darabok[1].strip())
                if a > b:
                    a, b = b, a
                if a >= 1:
                    halmaz.update(range(a, b + 1))
        elif resz.isdigit():
            szam = int(resz)
            if szam >= 1:
                halmaz.add(szam)

    return halmaz


def pozicio_alapu_torles(nev: str, pozicio_halmaz) -> str:
    if not pozicio_halmaz:
        return nev
    return ''.join(c for i, c in enumerate(nev, start=1) if i not in pozicio_halmaz)


def pozicio_alapu_beszuras(nev: str, beszurasok) -> str:
    if not beszurasok:
        return nev

    beszurasok_kiszamolva = []
    for pos, mod, szoveg in beszurasok:
        if pos is None:
            idx = 0 if mod == "ele" else len(nev)
        else:
            idx = max(0, min(pos - 1, len(nev)))
            if mod == "utana":
                idx += 1
        beszurasok_kiszamolva.append((idx, szoveg))

    beszurasok_kiszamolva.sort(key=lambda x: x[0], reverse=True)
    for idx, szoveg in beszurasok_kiszamolva:
        nev = nev[:idx] + szoveg + nev[idx:]
    return nev


_TILTOTT_KARAKTEREK = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def uj_nev_kepzes(eredeti_nev: str, egyeni_cserek=None, pozicio_halmaz=None, beszurasok=None, szam_beallitasok=None, ekezet_beallitasok=None, sorszam=1) -> str:
    nev, kiterjesztes = os.path.splitext(eredeti_nev)

    # 0. Automatikus számozás ha be van kapcsolva
    if szam_beallitasok and szam_beallitasok.get("aktiv", False):
        kezdoszam = szam_beallitasok.get("kezdoszam", 1)
        szamjegyek = szam_beallitasok.get("szamjegyek", 1)
        elotag = szam_beallitasok.get("elotag", "")
        utotag = szam_beallitasok.get("utotag", "")

        aktualis_szam = (sorszam - 1) + kezdoszam
        szam_str = str(aktualis_szam).zfill(szamjegyek)
        nev = f"{elotag}{szam_str}{utotag}"

    # 1. Törlés pozíció szerint
    nev = pozicio_alapu_torles(nev, pozicio_halmaz)
    # 2. Beszúrás pozíció szerint
    nev = pozicio_alapu_beszuras(nev, beszurasok)

    # 3. Ékezetmentesítés (csak ha külön be van kapcsolva)
    nev = ekezettelenit_egyeni(nev, ekezet_beallitasok)
    kiterjesztes = ekezettelenit_egyeni(kiterjesztes, ekezet_beallitasok)

    # 4. Egyéni cserék
    if egyeni_cserek:
        for honnan, hova in egyeni_cserek:
            if honnan == "":
                continue
            nev = nev.replace(honnan, hova)
            kiterjesztes = kiterjesztes.replace(honnan, hova)

    nev = _TILTOTT_KARAKTEREK.sub('_', nev)
    kiterjesztes = _TILTOTT_KARAKTEREK.sub('_', kiterjesztes)

    # Eltávolítja a felesleges pontot és szóközt a név végéről, de az alulvonás (_) megmarad!
    nev = nev.rstrip('. ')

    return nev + kiterjesztes


# ======================================================================
# Application
# ======================================================================
class AtnevezoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        # Induljon angol nyelven alapértelmezetten
        self.ny = Ny("en")

        self.root.geometry("900x580")
        self.root.minsize(700, 420)

        self.elemek = []
        self.egyeni_cserek = []
        self.pozicio_string = ""
        self.pozicio_beszurasok = []
        self.ekezet_beallitasok = {
            "aktiv": False,
            "kivetelek": "",
        }
        self.szam_beallitasok = {
            "aktiv": False,
            "elotag": "",
            "utotag": "",
            "kezdoszam": 1,
            "szamjegyek": 1,
        }
        self.atnevezesi_naplo = []

        self._forditando_widgetek = []
        self._forditando_menuk = []

        self._epitsd_menusavot()
        self._epitsd_felulet()
        self._nyelv_alkalmazasa()

    # ------------------------------------------------------------------
    # Nyelvváltás
    # ------------------------------------------------------------------
    def nyelv_valtasa(self, uj_nyelv):
        if uj_nyelv == self.ny.nyelv:
            return
        self.ny.nyelv = uj_nyelv
        self._nyelv_alkalmazasa()

    def _nyelv_alkalmazasa(self):
        self.root.title(self.ny.t("title"))
        for widget, kulcs in self._forditando_widgetek:
            widget.config(text=self.ny.t(kulcs))
        for menu, index, kulcs in self._forditando_menuk:
            menu.entryconfig(index, label=self.ny.t(kulcs))
        self.fa.heading("eredeti", text=self.ny.t("col_original"))
        self.fa.heading("uj", text=self.ny.t("col_new"))
        self._frissitsd_undo_gombot()
        self._frissitsd_tablat()

    # ------------------------------------------------------------------
    # Menüsáv
    # ------------------------------------------------------------------
    def _epitsd_menusavot(self):
        menusav = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=menusav)

        beallitasok_menu = tk.Menu(menusav, tearoff=0)

        beallitasok_menu.add_command(command=self.ekezetmentesites_ablak_megnyitasa)
        self._forditando_menuk.append((beallitasok_menu, 0, "menu_accent_removal"))

        beallitasok_menu.add_command(command=self.karaktercsere_ablak_megnyitasa)
        self._forditando_menuk.append((beallitasok_menu, 1, "menu_custom_replacements"))

        beallitasok_menu.add_command(command=self.pozicio_torles_ablak_megnyitasa)
        self._forditando_menuk.append((beallitasok_menu, 2, "menu_position_delete"))

        beallitasok_menu.add_command(command=self.pozicio_beszuras_ablak_megnyitasa)
        self._forditando_menuk.append((beallitasok_menu, 3, "menu_position_insert"))

        beallitasok_menu.add_command(command=self.szamozas_ablak_megnyitasa)
        self._forditando_menuk.append((beallitasok_menu, 4, "menu_autonumber"))

        nyelv_menu = tk.Menu(beallitasok_menu, tearoff=0)
        nyelv_menu.add_command(command=lambda: self.nyelv_valtasa("hu"))
        nyelv_menu.add_command(command=lambda: self.nyelv_valtasa("en"))
        self._forditando_menuk.append((nyelv_menu, 0, "lang_hu"))
        self._forditando_menuk.append((nyelv_menu, 1, "lang_en"))

        beallitasok_menu.add_cascade(menu=nyelv_menu)
        self._forditando_menuk.append((beallitasok_menu, 5, "menu_language"))

        menusav.add_cascade(menu=beallitasok_menu)
        self._forditando_menuk.append((menusav, 0, "menu_settings"))

        sugo_menu = tk.Menu(menusav, tearoff=0)
        sugo_menu.add_command(command=self.sugo_ablak_megnyitasa)
        sugo_menu.add_separator()
        sugo_menu.add_command(command=self.nevjegy_ablak_megnyitasa)
        self._forditando_menuk.append((sugo_menu, 0, "menu_help_item"))
        self._forditando_menuk.append((sugo_menu, 2, "menu_about"))

        menusav.add_cascade(menu=sugo_menu)
        self._forditando_menuk.append((menusav, 1, "menu_help"))

    # ------------------------------------------------------------------
    # Fő felület felépítése
    # ------------------------------------------------------------------
    def _epitsd_felulet(self):
        also_keret = ttk.Frame(self.root)
        also_keret.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        felso_gombsor = ttk.Frame(self.root)
        felso_gombsor.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        gomb = ttk.Button(felso_gombsor, command=self.fajlok_hozzaadasa)
        gomb.pack(side=tk.LEFT, padx=(0, 8))
        self._forditando_widgetek.append((gomb, "add_files"))

        gomb = ttk.Button(felso_gombsor, command=self.mappa_hozzaadasa)
        gomb.pack(side=tk.LEFT, padx=(0, 8))
        self._forditando_widgetek.append((gomb, "add_folder"))

        gomb = ttk.Button(felso_gombsor, command=self.kijelolt_torlese)
        gomb.pack(side=tk.LEFT, padx=(0, 8))
        self._forditando_widgetek.append((gomb, "remove_selected"))

        gomb = ttk.Button(felso_gombsor, command=self.lista_uritese)
        gomb.pack(side=tk.LEFT, padx=(0, 8))
        self._forditando_widgetek.append((gomb, "clear_list"))

        tabla_keret = ttk.Frame(self.root)
        tabla_keret.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        oszlopok = ("eredeti", "uj")
        self.fa = ttk.Treeview(
            tabla_keret, columns=oszlopok, show="headings", selectmode="extended"
        )
        self.fa.column("eredeti", width=400, anchor="w")
        self.fa.column("uj", width=400, anchor="w")
        self.fa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        gordito = ttk.Scrollbar(tabla_keret, orient="vertical", command=self.fa.yview)
        gordito.pack(side=tk.RIGHT, fill=tk.Y)
        self.fa.configure(yscrollcommand=gordito.set)
        self.fa.bind("<Escape>", lambda e: self.fa.selection_remove(self.fa.selection()))
        self.fa.bind("<Control-a>", lambda e: (self.fa.selection_set(self.fa.get_children()), "break"))
        self.fa.bind("<Control-A>", lambda e: (self.fa.selection_set(self.fa.get_children()), "break"))
        self.fa.bind("<Control-Shift-A>", lambda e: (self.fa.selection_remove(self.fa.selection()), "break"))
        def _bg_click(ev):
            if not self.fa.identify_row(ev.y):
                self.fa.selection_remove(self.fa.selection())
        self.fa.bind("<Button-1>", _bg_click, add="+")
        self.fa.bind("<<TreeviewSelect>>", lambda e: self._allapotsor_frissitese())

        self.allapot_szoveg = tk.StringVar(value="")
        ttk.Label(self.root, textvariable=self.allapot_szoveg, anchor="w").pack(
            side=tk.TOP, fill=tk.X, padx=10
        )

        self.atnevez_gomb = ttk.Button(also_keret, command=self.atnevezes_inditasa)
        self.atnevez_gomb.pack(side=tk.RIGHT)
        self._forditando_widgetek.append((self.atnevez_gomb, "rename_button"))

        self.undo_gomb = ttk.Button(also_keret, command=self.visszaallitas_inditasa)
        self.undo_gomb.pack(side=tk.RIGHT, padx=(0, 8))
        self._forditando_widgetek.append((self.undo_gomb, "undo"))

        kilepes_gomb = ttk.Button(also_keret, command=self.root.quit)
        kilepes_gomb.pack(side=tk.LEFT)
        self._forditando_widgetek.append((kilepes_gomb, "exit"))

    # ------------------------------------------------------------------
    # Fájlok / mappák hozzáadása
    # ------------------------------------------------------------------
    def fajlok_hozzaadasa(self):
        utvonalak = filedialog.askopenfilenames(title=self.ny.t("add_files"))
        if utvonalak:
            self._utvonalak_hozzaadasa(utvonalak)

    def mappa_hozzaadasa(self):
        mappa = filedialog.askdirectory(title=self.ny.t("add_folder"))
        if mappa:
            self._utvonalak_hozzaadasa([mappa])
            valasz = messagebox.askyesno(
                self.ny.t("folder_contents_title"),
                self.ny.t("folder_contents_msg"),
            )
            if valasz:
                try:
                    belso_elemek = [
                        os.path.join(mappa, nev) for nev in os.listdir(mappa)
                    ]
                    self._utvonalak_hozzaadasa(belso_elemek)
                except OSError as hiba:
                    messagebox.showerror(
                        self.ny.t("error_title"),
                        self.ny.t("error_reading_folder", hiba=hiba),
                    )

    def _utvonalak_hozzaadasa(self, utvonalak):
        meglevo = {elem["eredeti_ut"] for elem in self.elemek}
        for ut in utvonalak:
            if ut in meglevo:
                continue
            eredeti_nev = os.path.basename(ut.rstrip(os.sep))
            if not eredeti_nev:
                continue
            self.elemek.append({
                "eredeti_ut": ut,
                "eredeti_nev": eredeti_nev,
                # Alapból az eredeti névvel egyezzen meg, nehogy üresen
                # jelenjen meg, ha épp más elemekre van korlátozva a hatókör
                # (pl. mert közben másik elem van kijelölve).
                "uj_nev": eredeti_nev,
            })
        self._elonezet_frissitese()

    def _pozicio_halmaz(self):
        return pozicio_lista_ertelmezese(self.pozicio_string)

    def _hatokor_lekerdezese(self):
        """
        Meghatározza, hogy a következő módosítás mely elemekre vonatkozzon.

        - Ha nincs kijelölés, vagy a kijelölés lefedi az összes betöltött
          elemet (teljes kijelölés), akkor a módosítás mindegyik elemre
          vonatkozik.
        - Ha csak egy részhalmaz van kijelölve, akkor kizárólag azokra az
          elemekre vonatkozik a módosítás, a többi változatlan marad.

        Visszatér: (reszleges: bool, erintett_indexek: list[int])
        Az erintett_indexek mindig a self.elemek listára vonatkozó,
        növekvő sorrendbe rendezett indexek listája.
        """
        darabszam = len(self.elemek)
        if darabszam == 0:
            return False, []

        nyers_kijelolt = self.fa.selection()
        ervenyes_kijelolt = sorted(
            {int(iid) for iid in nyers_kijelolt if int(iid) < darabszam}
        )

        if not ervenyes_kijelolt or len(ervenyes_kijelolt) >= darabszam:
            # Nincs kijelölés vagy teljes kijelölés -> minden elem érintett
            return False, list(range(darabszam))

        return True, ervenyes_kijelolt

    def _elonezet_frissitese(self, mind=False):
        """
        Újraszámolja az elemek előnézeti (uj_nev) nevét.

        mind=False (alapértelmezett): a hatókör a kijelöléstől függ -
            ha nincs kijelölés vagy teljes a kijelölés, minden elem
            frissül; ha részleges a kijelölés, csak a kijelölt elemek.
        mind=True: mindig minden elemet újraszámol, a kijelöléstől
            függetlenül. Ezt kell használni olyan műveletek után, amelyek
            ténylegesen módosítják a fájlrendszert (átnevezés, undo),
            hogy az adatok biztosan konzisztensek maradjanak.
        """
        if mind:
            erintett_indexek = list(range(len(self.elemek)))
        else:
            _, erintett_indexek = self._hatokor_lekerdezese()
        for sorszam, idx in enumerate(erintett_indexek, start=1):
            elem = self.elemek[idx]
            elem["uj_nev"] = uj_nev_kepzes(
                elem["eredeti_nev"],
                self.egyeni_cserek,
                self._pozicio_halmaz(),
                self.pozicio_beszurasok,
                self.szam_beallitasok,
                self.ekezet_beallitasok,
                sorszam=sorszam
            )
        self._frissitsd_tablat()

    def kijelolt_torlese(self):
        kijelolt_indexek = self.fa.selection()
        if not kijelolt_indexek:
            return
        torolt_utvonalak = {
            self.elemek[int(iid)]["eredeti_ut"] for iid in kijelolt_indexek
        }
        self.elemek = [e for e in self.elemek if e["eredeti_ut"] not in torolt_utvonalak]
        # A törölt elemek kijelölése már nem értelmezhető, ezért töröljük,
        # nehogy véletlenül más (megmaradt) elemekre értelmeződjön a hatókör.
        self.fa.selection_remove(self.fa.selection())
        self._elonezet_frissitese()

    def lista_uritese(self):
        self.elemek = []
        self._frissitsd_tablat()

    # ------------------------------------------------------------------
    # Tábla és állapotsor frissítése
    # ------------------------------------------------------------------
    def _frissitsd_tablat(self):
        elozo_kijelolt = self.fa.selection()
        self.fa.delete(*self.fa.get_children())
        for index, elem in enumerate(self.elemek):
            self.fa.insert(
                "", "end", iid=str(index),
                values=(elem["eredeti_nev"], elem["uj_nev"])
            )
        ervenyes_kijelolt = [
            iid for iid in elozo_kijelolt if int(iid) < len(self.elemek)
        ]
        if ervenyes_kijelolt:
            self.fa.selection_set(ervenyes_kijelolt)

        self._allapotsor_frissitese()

    def _allapotsor_frissitese(self):
        db = len(self.elemek)
        if db == 0:
            self.allapot_szoveg.set(self.ny.t("status_no_items"))
            return

        valtozo_db = sum(1 for e in self.elemek if e["eredeti_nev"] != e["uj_nev"])
        szoveg = self.ny.t("status_loaded", db=db, valtozo=valtozo_db)

        reszleges, erintett_indexek = self._hatokor_lekerdezese()
        if reszleges:
            szoveg += "\n" + self.ny.t("scope_selected", n=len(erintett_indexek))
        else:
            szoveg += "\n" + self.ny.t("scope_all", n=db)
        self.allapot_szoveg.set(szoveg)

    def _frissitsd_undo_gombot(self):
        self.undo_gomb.config(state=("normal" if self.atnevezesi_naplo else "disabled"))

    # ------------------------------------------------------------------
    # Ékezetmentesítés beállító ablaka
    # ------------------------------------------------------------------
    def ekezetmentesites_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("accent_title"))
        ablak.geometry("460x280")
        ablak.transient(self.root)
        ablak.grab_set()

        ttk.Label(
            ablak, text=self.ny.t("accent_desc"), justify="left"
        ).pack(fill=tk.X, padx=10, pady=(10, 10))

        bevitel_keret = ttk.Frame(ablak)
        bevitel_keret.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(bevitel_keret, text=self.ny.t("accent_exclude_label")).pack(anchor="w", pady=(0, 4))
        kivetele_mezo = ttk.Entry(bevitel_keret, width=35)
        kivetele_mezo.insert(0, self.ekezet_beallitasok["kivetelek"])
        kivetele_mezo.pack(fill=tk.X, expand=True)

        def alkalmaz():
            self.ekezet_beallitasok = {
                "aktiv": True,
                "kivetelek": kivetele_mezo.get()
            }
            self._elonezet_frissitese()

        def kikapcsol():
            self.ekezet_beallitasok["aktiv"] = False
            self._elonezet_frissitese()

        also_gombsor = ttk.Frame(ablak)
        also_gombsor.pack(fill=tk.X, padx=10, pady=(20, 10))

        ttk.Button(also_gombsor, text=self.ny.t("clear_button"), command=kikapcsol).pack(side=tk.LEFT)
        ttk.Button(also_gombsor, text=self.ny.t("apply_button"), command=alkalmaz).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(also_gombsor, text=self.ny.t("close"), command=ablak.destroy).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # Egyéni karaktercserék beállító ablaka
    # ------------------------------------------------------------------
    def karaktercsere_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("custom_replace_title"))
        ablak.geometry("420x420")
        ablak.transient(self.root)
        ablak.grab_set()

        ttk.Label(
            ablak, text=self.ny.t("custom_replace_desc"), justify="left"
        ).pack(fill=tk.X, padx=10, pady=(10, 5))

        lista_keret = ttk.Frame(ablak)
        lista_keret.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        oszlopok = ("honnan", "hova")
        fa = ttk.Treeview(
            lista_keret, columns=oszlopok, show="headings", selectmode="browse", height=10
        )
        fa.heading("honnan", text=self.ny.t("col_from"))
        fa.heading("hova", text=self.ny.t("col_to"))
        fa.column("honnan", width=150, anchor="w")
        fa.column("hova", width=150, anchor="w")
        fa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        gordito = ttk.Scrollbar(lista_keret, orient="vertical", command=fa.yview)
        gordito.pack(side=tk.RIGHT, fill=tk.Y)
        fa.configure(yscrollcommand=gordito.set)

        def lista_ujratoltese():
            fa.delete(*fa.get_children())
            for i, (honnan, hova) in enumerate(self.egyeni_cserek):
                fa.insert("", "end", iid=str(i), values=(honnan, hova))

        lista_ujratoltese()

        bevitel_keret = ttk.Frame(ablak)
        bevitel_keret.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(bevitel_keret, text=self.ny.t("from_label")).grid(row=0, column=0, padx=(0, 4))
        honnan_mezo = ttk.Entry(bevitel_keret, width=12)
        honnan_mezo.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(bevitel_keret, text=self.ny.t("to_label")).grid(row=0, column=2, padx=(0, 4))
        hova_mezo = ttk.Entry(bevitel_keret, width=12)
        hova_mezo.grid(row=0, column=3, padx=(0, 10))

        def csere_hozzaadasa():
            honnan = honnan_mezo.get()
            hova = hova_mezo.get()
            if not honnan:
                messagebox.showwarning(
                    self.ny.t("missing_data_title"),
                    self.ny.t("missing_data_msg"),
                    parent=ablak,
                )
                return
            self.egyeni_cserek.append((honnan, hova))
            honnan_mezo.delete(0, tk.END)
            hova_mezo.delete(0, tk.END)
            lista_ujratoltese()
            self._elonezet_frissitese()

        ttk.Button(bevitel_keret, text=self.ny.t("add_button"), command=csere_hozzaadasa).grid(row=0, column=4, padx=(4, 0))

        def kijelolt_csere_torlese():
            kijelolt = fa.selection()
            if not kijelolt:
                return
            index = int(kijelolt[0])
            del self.egyeni_cserek[index]
            lista_ujratoltese()
            self._elonezet_frissitese()

        also_gombsor = ttk.Frame(ablak)
        also_gombsor.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(
            also_gombsor, text=self.ny.t("delete_selected_replacement"),
            command=kijelolt_csere_torlese
        ).pack(side=tk.LEFT)

        ttk.Button(also_gombsor, text=self.ny.t("close"), command=ablak.destroy).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # Pozíció szerinti karaktertörlés beállító ablaka
    # ------------------------------------------------------------------
    def pozicio_torles_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("position_delete_title"))
        ablak.geometry("460x360")
        ablak.transient(self.root)
        ablak.grab_set()

        ttk.Label(
            ablak, text=self.ny.t("position_delete_desc"), justify="left"
        ).pack(fill=tk.X, padx=10, pady=(10, 10))

        bevitel_keret = ttk.Frame(ablak)
        bevitel_keret.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(bevitel_keret, text=self.ny.t("position_input_label")).pack(side=tk.LEFT, padx=(0, 8))

        mezo = ttk.Entry(bevitel_keret, width=20)
        mezo.insert(0, self.pozicio_string)
        mezo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        jelenlegi_szoveg = tk.StringVar()

        def jelenlegi_frissitese():
            halmaz = pozicio_lista_ertelmezese(mezo.get())
            if halmaz:
                lista = ", ".join(str(x) for x in sorted(halmaz))
            else:
                lista = self.ny.t("position_none")
            jelenlegi_szoveg.set(self.ny.t("position_current_label", lista=lista))

        jelenlegi_frissitese()
        ttk.Label(ablak, textvariable=jelenlegi_szoveg, justify="left").pack(
            fill=tk.X, padx=10, pady=(0, 10)
        )

        def alkalmaz():
            self.pozicio_string = mezo.get().strip()
            jelenlegi_frissitese()
            self._elonezet_frissitese()

        def torles():
            mezo.delete(0, tk.END)
            self.pozicio_string = ""
            jelenlegi_frissitese()
            self._elonezet_frissitese()

        also_gombsor = ttk.Frame(ablak)
        also_gombsor.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(also_gombsor, text=self.ny.t("clear_button"), command=torles).pack(side=tk.LEFT)
        ttk.Button(also_gombsor, text=self.ny.t("apply_button"), command=alkalmaz).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        ttk.Button(also_gombsor, text=self.ny.t("close"), command=ablak.destroy).pack(side=tk.RIGHT)

        mezo.bind("<Return>", lambda esemeny: alkalmaz())

    # ------------------------------------------------------------------
    # Pozíció szerinti karakterbeszúrás beállító ablaka
    # ------------------------------------------------------------------
    def pozicio_beszuras_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("insert_title"))
        ablak.geometry("560x400")
        ablak.transient(self.root)
        ablak.grab_set()

        ttk.Label(
            ablak, text=self.ny.t("insert_desc"), justify="left"
        ).pack(fill=tk.X, padx=10, pady=(10, 5))

        lista_keret = ttk.Frame(ablak)
        lista_keret.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        oszlopok = ("pos", "mod", "szoveg")
        fa = ttk.Treeview(
            lista_keret, columns=oszlopok, show="headings", selectmode="browse", height=8
        )
        fa.heading("pos", text=self.ny.t("col_pos"))
        fa.heading("mod", text=self.ny.t("col_mode"))
        fa.heading("szoveg", text=self.ny.t("col_text"))
        fa.column("pos", width=60, anchor="center")
        fa.column("mod", width=80, anchor="center")
        fa.column("szoveg", width=250, anchor="w")
        fa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        gordito = ttk.Scrollbar(lista_keret, orient="vertical", command=fa.yview)
        gordito.pack(side=tk.RIGHT, fill=tk.Y)
        fa.configure(yscrollcommand=gordito.set)

        def lista_ujratoltese():
            fa.delete(*fa.get_children())
            for i, (pos, mod, szoveg) in enumerate(self.pozicio_beszurasok):
                mod_szoveg = self.ny.t("mode_before") if mod == "ele" else self.ny.t("mode_after")
                pos_megjelenites = str(pos) if pos is not None else "-"
                fa.insert("", "end", iid=str(i), values=(pos_megjelenites, mod_szoveg, szoveg))

        lista_ujratoltese()

        bevitel_keret = ttk.Frame(ablak)
        bevitel_keret.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(bevitel_keret, text=self.ny.t("col_pos")+":").grid(row=0, column=0, padx=(0, 4))
        pos_mezo = ttk.Entry(bevitel_keret, width=5)
        pos_mezo.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(bevitel_keret, text=self.ny.t("col_mode")+":").grid(row=0, column=2, padx=(0, 4))
        mod_kivalasztott = tk.StringVar(value=self.ny.t("mode_before"))
        mod_mezo = ttk.Combobox(bevitel_keret, textvariable=mod_kivalasztott, state="readonly", width=8)
        mod_mezo['values'] = (self.ny.t("mode_before"), self.ny.t("mode_after"))
        mod_mezo.grid(row=0, column=3, padx=(0, 10))

        ttk.Label(bevitel_keret, text=self.ny.t("col_text")+":").grid(row=0, column=4, padx=(0, 4))
        szoveg_mezo = ttk.Entry(bevitel_keret, width=15)
        szoveg_mezo.grid(row=0, column=5, padx=(0, 10))

        def beszuras_hozzaadasa():
            pos_szoveg = pos_mezo.get().strip()
            if pos_szoveg == "":
                pos = None
            else:
                try:
                    pos = int(pos_szoveg)
                    if pos < 1:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning(self.ny.t("error_title"), "A pozíció 1 vagy nagyobb szám kell legyen (vagy hagyd üresen).", parent=ablak)
                    return

            mod = "ele" if mod_kivalasztott.get() == self.ny.t("mode_before") else "utana"
            szoveg = szoveg_mezo.get()
            if not szoveg:
                messagebox.showwarning(self.ny.t("missing_data_title"), self.ny.t("missing_data_msg"), parent=ablak)
                return

            self.pozicio_beszurasok.append((pos, mod, szoveg))
            pos_mezo.delete(0, tk.END)
            szoveg_mezo.delete(0, tk.END)
            lista_ujratoltese()
            self._elonezet_frissitese()

        ttk.Button(bevitel_keret, text=self.ny.t("add_button"), command=beszuras_hozzaadasa).grid(row=0, column=6, padx=(4, 0))

        def kijelolt_torlese():
            kijelolt = fa.selection()
            if not kijelolt:
                return
            index = int(kijelolt[0])
            del self.pozicio_beszurasok[index]
            lista_ujratoltese()
            self._elonezet_frissitese()

        also_gombsor = ttk.Frame(ablak)
        also_gombsor.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(
            also_gombsor, text=self.ny.t("delete_selected_replacement"),
            command=kijelolt_torlese
        ).pack(side=tk.LEFT)

        ttk.Button(also_gombsor, text=self.ny.t("close"), command=ablak.destroy).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # Automatikus számozás beállító ablaka
    # ------------------------------------------------------------------
    def szamozas_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("autonumber_title"))
        ablak.geometry("450x280")
        ablak.transient(self.root)
        ablak.grab_set()

        ttk.Label(
            ablak, text=self.ny.t("autonumber_desc"), justify="left"
        ).pack(fill=tk.X, padx=10, pady=(10, 10))

        form_keret = ttk.Frame(ablak)
        form_keret.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(form_keret, text=self.ny.t("autonumber_prefix")).grid(row=0, column=0, sticky="w", pady=4)
        elotag_mezo = ttk.Entry(form_keret, width=22)
        elotag_mezo.insert(0, self.szam_beallitasok["elotag"])
        elotag_mezo.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=4)

        ttk.Label(form_keret, text=self.ny.t("autonumber_suffix")).grid(row=1, column=0, sticky="w", pady=4)
        utotag_mezo = ttk.Entry(form_keret, width=22)
        utotag_mezo.insert(0, self.szam_beallitasok["utotag"])
        utotag_mezo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=4)

        ttk.Label(form_keret, text=self.ny.t("autonumber_start")).grid(row=2, column=0, sticky="w", pady=4)
        kezdoszam_mezo = ttk.Entry(form_keret, width=10)
        kezdoszam_mezo.insert(0, str(self.szam_beallitasok["kezdoszam"]))
        kezdoszam_mezo.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=4)

        ttk.Label(form_keret, text=self.ny.t("autonumber_digits")).grid(row=3, column=0, sticky="w", pady=4)
        szamjegyek_mezo = ttk.Entry(form_keret, width=10)
        szamjegyek_mezo.insert(0, str(self.szam_beallitasok["szamjegyek"]))
        szamjegyek_mezo.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=4)

        def alkalmaz():
            try:
                k_szam = int(kezdoszam_mezo.get().strip())
                sz_jegy = int(szamjegyek_mezo.get().strip())
                if k_szam < 0 or sz_jegy < 1:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    self.ny.t("error_title"),
                    "A kezdősorszám és a számjegyek száma érvényes pozitív szám kell legyen!",
                    parent=ablak
                )
                return

            self.szam_beallitasok = {
                "aktiv": True,
                "elotag": elotag_mezo.get(),
                "utotag": utotag_mezo.get(),
                "kezdoszam": k_szam,
                "szamjegyek": sz_jegy,
            }
            self._elonezet_frissitese()

        def kikapcsol():
            self.szam_beallitasok["aktiv"] = False
            self._elonezet_frissitese()

        also_gombsor = ttk.Frame(ablak)
        also_gombsor.pack(fill=tk.X, padx=10, pady=(15, 10))

        ttk.Button(also_gombsor, text=self.ny.t("clear_button"), command=kikapcsol).pack(side=tk.LEFT)
        ttk.Button(also_gombsor, text=self.ny.t("apply_button"), command=alkalmaz).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(also_gombsor, text=self.ny.t("close"), command=ablak.destroy).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # Súgó és Névjegy ablakok
    # ------------------------------------------------------------------
    def sugo_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("help_title"))
        ablak.geometry("520x460")
        ablak.transient(self.root)
        ablak.grab_set()

        szoveg_widget = tk.Text(ablak, wrap="word", padx=10, pady=10)
        szoveg_widget.insert("1.0", self.ny.t("help_text"))
        szoveg_widget.config(state="disabled")
        szoveg_widget.pack(fill=tk.BOTH, expand=True)

        ttk.Button(ablak, text=self.ny.t("close"), command=ablak.destroy).pack(pady=8)

    def nevjegy_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("about_title"))
        ablak.geometry("360x240")
        ablak.resizable(False, False)
        ablak.transient(self.root)
        ablak.grab_set()

        keret = ttk.Frame(ablak, padding=20)
        keret.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            keret, text=self.ny.t("about_app_title"),
            font=("TkDefaultFont", 11, "bold")
        ).pack(pady=(0, 8))

        ttk.Label(keret, text=self.ny.t("about_desc"), justify="center").pack(pady=(0, 12))

        ttk.Button(keret, text=self.ny.t("close"), command=ablak.destroy).pack()

    # ------------------------------------------------------------------
    # Átnevezés végrehajtása
    # ------------------------------------------------------------------
    def atnevezes_inditasa(self):
        if not self.elemek:
            messagebox.showinfo(self.ny.t("nothing_to_rename_title"), self.ny.t("nothing_to_rename_msg"))
            return

        valtozok = [e for e in self.elemek if e["eredeti_nev"] != e["uj_nev"]]
        if not valtozok:
            messagebox.showinfo(self.ny.t("no_changes_title"), self.ny.t("no_changes_msg"))
            return

        megerosites = messagebox.askyesno(
            self.ny.t("confirm_title"),
            self.ny.t("confirm_msg", n=len(valtozok)),
        )
        if not megerosites:
            return

        sikeres = 0
        hibak = []
        koteg_naplo = []

        for elem in valtozok:
            regi_ut = elem["eredeti_ut"]
            mappa_ut = os.path.dirname(regi_ut)
            uj_ut = os.path.join(mappa_ut, elem["uj_nev"])

            if os.path.exists(uj_ut) and uj_ut != regi_ut:
                hibak.append(self.ny.t("already_exists", nev=elem["eredeti_nev"], uj=elem["uj_nev"]))
                continue

            try:
                os.rename(regi_ut, uj_ut)
                koteg_naplo.append((uj_ut, regi_ut))
                elem["eredeti_ut"] = uj_ut
                elem["eredeti_nev"] = elem["uj_nev"]
                sikeres += 1
            except OSError as hiba:
                hibak.append(f"{elem['eredeti_nev']}: {hiba}")

        if koteg_naplo:
            self.atnevezesi_naplo.append(koteg_naplo)

        self._elonezet_frissitese(mind=True)
        self._frissitsd_undo_gombot()

        uzenet = self.ny.t("rename_done_msg", n=sikeres)
        if hibak:
            lista_15 = hibak[:15]
            uzenet += self.ny.t("errors_occurred", n=len(hibak), lista="\n".join(lista_15))
            if len(hibak) > 15:
                uzenet += self.ny.t("and_more_errors", n=len(hibak) - 15)
            messagebox.showwarning(self.ny.t("rename_done_errors_title"), uzenet)
        else:
            messagebox.showinfo(self.ny.t("rename_done_title"), uzenet)

    # ------------------------------------------------------------------
    # Visszaállítás (undo)
    # ------------------------------------------------------------------
    def visszaallitas_inditasa(self):
        if not self.atnevezesi_naplo:
            messagebox.showinfo(self.ny.t("undo_nothing_title"), self.ny.t("undo_nothing_msg"))
            return

        koteg_naplo = self.atnevezesi_naplo.pop()

        sikeres = 0
        hibak = []

        for uj_ut, regi_ut in reversed(koteg_naplo):
            if not os.path.exists(uj_ut):
                hibak.append(f"{os.path.basename(uj_ut)}: {self.ny.t('not_found')}")
                continue
            if os.path.exists(regi_ut) and regi_ut != uj_ut:
                hibak.append(self.ny.t("already_exists", nev=os.path.basename(uj_ut), uj=os.path.basename(regi_ut)))
                continue
            try:
                os.rename(uj_ut, regi_ut)
                for elem in self.elemek:
                    if elem["eredeti_ut"] == uj_ut:
                        elem["eredeti_ut"] = regi_ut
                        elem["eredeti_nev"] = os.path.basename(regi_ut)
                        break
                sikeres += 1
            except OSError as hiba:
                hibak.append(f"{os.path.basename(uj_ut)}: {hiba}")

        self._elonezet_frissitese(mind=True)
        self._frissitsd_undo_gombot()

        uzenet = self.ny.t("undo_done_msg", n=sikeres)
        if hibak:
            lista_15 = hibak[:15]
            uzenet += self.ny.t("errors_occurred", n=len(hibak), lista="\n".join(lista_15))
            if len(hibak) > 15:
                uzenet += self.ny.t("and_more_errors", n=len(hibak) - 15)
            messagebox.showwarning(self.ny.t("undo_done_errors_title"), uzenet)
        else:
            messagebox.showinfo(self.ny.t("undo_done_title"), uzenet)


def main():
    root = tk.Tk()
    try:
        stilus = ttk.Style()
        if "clam" in stilus.theme_names():
            stilus.theme_use("clam")
    except tk.TclError:
        pass
    AtnevezoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
