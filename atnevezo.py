#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fájl- és mappanév ékezetmentesítő és kötegelt átnevező program
================================================================
File and folder name accent-remover and batch renaming tool
================================================================
- Fájlok és/vagy mappák importálása (fájlválasztó ablakkal)
- Az ékezetes karakterek automatikus eltávolítása (á->a, ő->o, stb.)
- A szóközök alulvonásra (_) cserélése
- Egyéni karaktercserék (pl. '&' -> 'es')
- Előnézet az új nevekről az átnevezés előtt
- Kötegelt (batch) átnevezés egy gombnyomással
- Visszaállítás (undo) az utoljára végrehajtott átnevezés(ek)re
- Magyar / angol nyelv választása
"""

import os
import re
import unicodedata
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ======================================================================
# Fordítások / Translations
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
    "menu_custom_replacements": {"hu": "Egyéni karaktercserék...", "en": "Custom character replacements..."},
    "menu_position_delete": {
        "hu": "Karakterek törlése pozíció szerint...",
        "en": "Delete characters by position...",
    },
    "menu_language": {"hu": "Nyelv", "en": "Language"},
    "lang_hu": {"hu": "Magyar", "en": "Hungarian"},
    "lang_en": {"hu": "Angol", "en": "English"},
    "menu_help": {"hu": "Súgó", "en": "Help"},
    "menu_help_item": {"hu": "Súgó", "en": "Help"},
    "menu_about": {"hu": "Névjegy", "en": "About"},

    "custom_replace_title": {"hu": "Egyéni karaktercserék", "en": "Custom character replacements"},
    "custom_replace_desc": {
        "hu": "Add meg, mely karaktert (vagy szövegrészt) mire cseréljen le\n"
              "a program az ékezetmentesítés után. Pl.: '&' -> 'es'",
        "en": "Specify which character (or text) should be replaced\n"
              "with what, after accents are removed. E.g.: '&' -> 'and'",
    },
    "col_from": {"hu": "Erről", "en": "From"},
    "col_to": {"hu": "Erre", "en": "To"},
    "from_label": {"hu": "Erről:", "en": "From:"},
    "to_label": {"hu": "Erre:", "en": "To:"},
    "add_button": {"hu": "Hozzáadás", "en": "Add"},
    "delete_selected_replacement": {"hu": "Kijelölt csere törlése", "en": "Remove selected replacement"},
    "close": {"hu": "Bezárás", "en": "Close"},
    "missing_data_title": {"hu": "Hiányzó adat", "en": "Missing data"},
    "missing_data_msg": {"hu": "Az 'Erről' mező nem lehet üres.", "en": "The 'From' field cannot be empty."},

    "position_delete_title": {
        "hu": "Karakterek törlése pozíció szerint",
        "en": "Delete characters by position",
    },
    "position_delete_desc": {
        "hu": "Add meg, mely karakterpozíció(ka)t törölje a program a névből\n"
              "(a kiterjesztés nélkül számolva, balról jobbra, 1-től indulva).\n\n"
              "Például:\n"
              "  1        -> csak az 1. karaktert törli\n"
              "  5        -> csak az 5. karaktert törli\n"
              "  1,4,6    -> az 1., 4. és 6. karaktert törli\n"
              "  1-5      -> az 1-től az 5. karakterig mindet törli\n"
              "  1-3,7,9-10 -> ezek kombinációja is megadható",
        "en": "Specify which character position(s) should be deleted\n"
              "from the name (extension excluded, counted left to right,\n"
              "starting at 1).\n\n"
              "Examples:\n"
              "  1        -> deletes only the 1st character\n"
              "  5        -> deletes only the 5th character\n"
              "  1,4,6    -> deletes the 1st, 4th and 6th characters\n"
              "  1-5      -> deletes characters 1 through 5\n"
              "  1-3,7,9-10 -> combinations like this are also allowed",
    },
    "position_input_label": {"hu": "Pozíció(k):", "en": "Position(s):"},
    "apply_button": {"hu": "Alkalmaz", "en": "Apply"},
    "clear_button": {"hu": "Törlés", "en": "Clear"},
    "position_current_label": {
        "hu": "Jelenleg alkalmazott pozíciók: {lista}",
        "en": "Currently applied positions: {lista}",
    },
    "position_none": {"hu": "nincs", "en": "none"},
    "scope_selected": {
        "hu": "A módosítás csak a kijelölt {n} elemre lesz alkalmazva.",
        "en": "The change will only apply to the {n} selected items.",
    },
    "scope_all": {
        "hu": "Nincs kijelölés — a módosítás mind a(z) {n} elemre lesz alkalmazva.",
        "en": "Nothing selected — the change will apply to all {n} items.",
    },

    "help_title": {"hu": "Súgó", "en": "Help"},
    "help_text": {
        "hu": (
            "Használati útmutató\n"
            "────────────────────\n\n"
            "1. Kattints a 'Fájlok hozzáadása...' vagy 'Mappa hozzáadása...'\n"
            "   gombra, hogy elemeket tölts be a listába.\n\n"
            "2. A táblázatban azonnal látod az eredeti és az új\n"
            "   (ékezetmentesített) nevet.\n\n"
            "3. A Beállítások menüben, az 'Egyéni karaktercserék...'\n"
            "   pontban megadhatod, hogy bizonyos karaktereket vagy\n"
            "   szövegrészeket mire cseréljen le a program\n"
            "   (pl. '&' -> 'es', '@' -> 'kukac').\n\n"
            "4. A Beállítások menüben, a 'Karakterek törlése pozíció\n"
            "   szerint...' pontban megadhatod, hogy a névből mely\n"
            "   karakterpozíciókat törölje a program (pl. '1', '5',\n"
            "   '1,4,6' vagy '1-5').\n\n"
            "5. A szóközök mindig alulvonásra (_) cserélődnek.\n\n"
            "6. Ha megvagy az előnézettel, kattints a 'Kötegelt\n"
            "   átnevezés végrehajtása' gombra. A program\n"
            "   megerősítést kér, mielőtt bármit is átnevez.\n\n"
            "7. Ha meggondoltad magad, a 'Visszaállítás (undo)' gombbal\n"
            "   visszaállíthatod a legutóbb végrehajtott átnevezést\n"
            "   (akár több lépésben, ha egymás után többször neveztél át).\n\n"
            "8. Ha a fő táblázatban kijelölsz egy vagy több elemet, mielőtt\n"
            "   az Egyéni karaktercserék vagy a Pozíció szerinti törlés\n"
            "   beállításokon módosítasz, a változtatás csak a kijelölt\n"
            "   elemekre lesz érvényes. Ha nincs kijelölés, mindenkire\n"
            "   vonatkozik. A kijelölés crt+egér bal, shift+egér bal, crt+a.\n\n"
            "9. A nyelv a Beállítások > Nyelv menüben váltható."
        ),
        "en": (
            "How to use\n"
            "────────────────────\n\n"
            "1. Click 'Add files...' or 'Add folder...' to load\n"
            "   items into the list.\n\n"
            "2. The table immediately shows the original and the\n"
            "   new (accent-free) name.\n\n"
            "3. In the Settings menu, under 'Custom character\n"
            "   replacements...' you can define which characters\n"
            "   or text pieces should be replaced with what\n"
            "   (e.g. '&' -> 'and', '@' -> 'at').\n\n"
            "4. In the Settings menu, under 'Delete characters by\n"
            "   position...' you can define which character\n"
            "   positions should be removed from the name\n"
            "   (e.g. '1', '5', '1,4,6' or '1-5').\n\n"
            "5. Spaces are always replaced with underscores (_).\n\n"
            "6. Once you're happy with the preview, click 'Run\n"
            "   batch rename'. The program will ask for confirmation\n"
            "   before renaming anything.\n\n"
            "7. If you change your mind, use 'Undo last rename' to\n"
            "   revert the most recent renaming operation (you can\n"
            "   undo several times if you renamed more than once).\n\n"
            "8. If you select one or more items in the main table before\n"
            "   changing the Custom character replacements or the\n"
            "   Position-based deletion settings, the change will only\n"
            "   apply to the selected items. If nothing is selected, it\n"
            "   applies to all of them.\n"
            "   Selection: Ctrl+Left Mouse, Shift+Left Mouse, Ctrl + A.\n\n"
            "9. The language can be changed under Settings > Language."
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
            "szóköz -> alulvonás cseréhez, egyéni\n"
            "karaktercserékhez, pozíció szerinti törléshez\n"
            "és visszaállításhoz.\n\n"
            "Verzió: 1.3  MIT License\n"
            "Copyright (c) szabiz 2026 - Soli Deo Gloria"
        ),
        "en": (
            "Batch renaming tool for removing accents,\n"
            "replacing spaces with underscores, custom\n"
            "character replacements, position-based deletion\n"
            "and undo support.\n\n"
            "Version: 1.3 MIT License\n"
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
        "hu": "Egyik névben sincs változás (nincs ékezet vagy szóköz).",
        "en": "No names would change (no accents, spaces, or custom replacements apply).",
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
    """Egyszerű nyelvváltó segédosztály. / Simple language-switch helper."""

    def __init__(self, nyelv="hu"):
        self.nyelv = nyelv

    def t(self, kulcs, **kwargs):
        szoveg = TRANSLATIONS[kulcs][self.nyelv]
        if kwargs:
            return szoveg.format(**kwargs)
        return szoveg


# ======================================================================
# Névképzési logika
# ======================================================================
def ekezettelenit(szoveg: str) -> str:
    """Eltávolítja az ékezeteket egy szövegből (pl. á -> a, ő -> o, ű -> u)."""
    nfkd = unicodedata.normalize('NFKD', szoveg)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def pozicio_lista_ertelmezese(szoveg: str) -> set:
    """
    Egy pozíció-megadó szöveget (pl. "1", "5", "1,4,6", "1-5", "1-3,7,9-10")
    értelmez, és visszaadja a törlendő karakterpozíciók (1-alapú) halmazát.
    Az érvénytelen/hibás részek figyelmen kívül maradnak.
    """
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
    """Eltávolítja a nevből az adott (1-alapú) pozíciókon lévő karaktereket."""
    if not pozicio_halmaz:
        return nev
    return ''.join(c for i, c in enumerate(nev, start=1) if i not in pozicio_halmaz)


# Windows alatt tiltott karakterek fájl-/mappanevekben: < > : " / \ | ? *
# és a vezérlőkarakterek (0x00-0x1f). Ezeket mindig alulvonásra cseréljük,
# hogy a rendszer soha ne utasítsa el az átnevezést.
_TILTOTT_KARAKTEREK = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def uj_nev_kepzes(eredeti_nev: str, egyeni_cserek=None, pozicio_halmaz=None) -> str:
    """
    Kiszámolja az új fájl-/mappanevet:
    - pozíció szerinti karaktertörlés (az eredeti névre alkalmazva, kiterjesztés nélkül)
    - ékezetek eltávolítása
    - egyéni karaktercserék alkalmazása (pl. '&' -> 'es')
    - Windows alatt tiltott karakterek (<>:"/\\|?*) cseréje alulvonásra
    - szóközök cseréje alulvonásra
    - felesleges/ismétlődő alulvonások összevonása
    - névvégi pontok/szóközök eltávolítása (Windows ezt sem engedi)

    egyeni_cserek: lista (honnan, hova) párokból, pl. [("&", "es"), ("+", "plusz")]
    pozicio_halmaz: törlendő karakterpozíciók (1-alapú) halmaza, pl. {1, 4, 6}
    """
    nev, kiterjesztes = os.path.splitext(eredeti_nev)

    nev = pozicio_alapu_torles(nev, pozicio_halmaz)

    nev = ekezettelenit(nev)
    kiterjesztes = ekezettelenit(kiterjesztes)

    if egyeni_cserek:
        for honnan, hova in egyeni_cserek:
            if honnan == "":
                continue
            nev = nev.replace(honnan, hova)
            kiterjesztes = kiterjesztes.replace(honnan, hova)

    # Windows alatt tiltott karakterek kiszűrése (a kiterjesztésből is,
    # bár ott ritkán fordulnak elő)
    nev = _TILTOTT_KARAKTEREK.sub('_', nev)
    kiterjesztes = _TILTOTT_KARAKTEREK.sub('_', kiterjesztes)

    nev = nev.replace(' ', '_')
    nev = re.sub(r'_+', '_', nev)
    nev = nev.strip('_')

    # Windows nem enged pontra vagy szóközre végződő nevet
    nev = nev.rstrip('. ')

    return nev + kiterjesztes


# ======================================================================
# Alkalmazás
# ======================================================================
class AtnevezoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.ny = Ny("hu")

        self.root.geometry("900x580")
        self.root.minsize(700, 420)

        # elemek: lista of dict {"eredeti_ut": str, "eredeti_nev": str, "uj_nev": str}
        self.elemek = []

        # egyéni karaktercserék: lista (honnan, hova) párokból
        self.egyeni_cserek = []

        # pozíció szerinti karaktertörléshez: a felhasználó által beírt nyers
        # szöveg (pl. "1,4,6" vagy "1-5"), amiből a pozíció-halmazt számoljuk
        self.pozicio_string = ""

        # visszaállítási napló: lista "kötegekről"; minden köteg egy lista
        # (uj_ut, regi_ut) párokból - ez teszi lehetővé a többszörös undo-t
        self.atnevezesi_naplo = []

        # widgetek, amiket nyelvváltáskor frissíteni kell:
        # (widget, fordítási_kulcs, "text" | egyéb)
        self._forditando_widgetek = []
        self._forditando_menuk = []  # (menu, index, kulcs)

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
        beallitasok_menu.add_command(
            command=self.karaktercsere_ablak_megnyitasa
        )
        self._forditando_menuk.append((beallitasok_menu, 0, "menu_custom_replacements"))

        beallitasok_menu.add_command(
            command=self.pozicio_torles_ablak_megnyitasa
        )
        self._forditando_menuk.append((beallitasok_menu, 1, "menu_position_delete"))

        nyelv_menu = tk.Menu(beallitasok_menu, tearoff=0)
        nyelv_menu.add_command(
            command=lambda: self.nyelv_valtasa("hu")
        )
        nyelv_menu.add_command(
            command=lambda: self.nyelv_valtasa("en")
        )
        self._forditando_menuk.append((nyelv_menu, 0, "lang_hu"))
        self._forditando_menuk.append((nyelv_menu, 1, "lang_en"))

        beallitasok_menu.add_cascade(menu=nyelv_menu)
        self._forditando_menuk.append((beallitasok_menu, 2, "menu_language"))

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

        # Tábla (Treeview) az elemek megjelenítéséhez
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


        # Állapotsor
        self.allapot_szoveg = tk.StringVar(value="")
        ttk.Label(self.root, textvariable=self.allapot_szoveg, anchor="w").pack(
            side=tk.TOP, fill=tk.X, padx=10
        )

        # Alsó gombsor: átnevezés, undo, kilépés
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
            uj_nev = uj_nev_kepzes(eredeti_nev, self.egyeni_cserek, self._pozicio_halmaz())
            self.elemek.append({
                "eredeti_ut": ut,
                "eredeti_nev": eredeti_nev,
                "uj_nev": uj_nev,
            })
        self._frissitsd_tablat()

    def _pozicio_halmaz(self):
        return pozicio_lista_ertelmezese(self.pozicio_string)

    def _celzott_indexek(self):
        """
        Visszaadja, mely elemekre (self.elemek indexeire) vonatkozzon a
        beállítás-módosítás: ha van kijelölés a fő táblázatban, csak azokra;
        ha nincs kijelölés, az összesre.
        """
        kijelolt = self.fa.selection()
        if kijelolt:
            return [int(iid) for iid in kijelolt]
        return list(range(len(self.elemek)))

    def _hatokor_szoveg(self):
        """Ember számára olvasható szöveg arról, hogy a beállítás mely elemekre fog hatni."""
        kijelolt = self.fa.selection()
        if kijelolt:
            return self.ny.t("scope_selected", n=len(kijelolt))
        return self.ny.t("scope_all", n=len(self.elemek))

    def _elonezet_frissitese(self):
        """
        Az egyéni karaktercserék / pozíció-törlés módosítása után újraszámolja
        az érintett elemek előnézetét: ha a fő táblázatban van kijelölés,
        csak a kijelölt elemekét, egyébként az összesét.
        """
        for idx in self._celzott_indexek():
            if 0 <= idx < len(self.elemek):
                elem = self.elemek[idx]
                elem["uj_nev"] = uj_nev_kepzes(
                    elem["eredeti_nev"], self.egyeni_cserek, self._pozicio_halmaz()
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
        self._frissitsd_tablat()

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
        # a kijelölés visszaállítása, ha a megfelelő elemek még léteznek
        ervenyes_kijelolt = [
            iid for iid in elozo_kijelolt if int(iid) < len(self.elemek)
        ]
        if ervenyes_kijelolt:
            self.fa.selection_set(ervenyes_kijelolt)

        db = len(self.elemek)
        if db == 0:
            self.allapot_szoveg.set(self.ny.t("status_no_items"))
        else:
            valtozo_db = sum(1 for e in self.elemek if e["eredeti_nev"] != e["uj_nev"])
            self.allapot_szoveg.set(self.ny.t("status_loaded", db=db, valtozo=valtozo_db))

    def _frissitsd_undo_gombot(self):
        self.undo_gomb.config(state=("normal" if self.atnevezesi_naplo else "disabled"))

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

        ttk.Label(
            ablak, text=self._hatokor_szoveg(), justify="left",
            font=("TkDefaultFont", 9, "italic")
        ).pack(fill=tk.X, padx=10, pady=(0, 5))

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

        cimke_honnan = ttk.Label(bevitel_keret, text=self.ny.t("from_label"))
        cimke_honnan.grid(row=0, column=0, padx=(0, 4))
        honnan_mezo = ttk.Entry(bevitel_keret, width=12)
        honnan_mezo.grid(row=0, column=1, padx=(0, 10))

        cimke_hova = ttk.Label(bevitel_keret, text=self.ny.t("to_label"))
        cimke_hova.grid(row=0, column=2, padx=(0, 4))
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

        hozzaad_gomb = ttk.Button(bevitel_keret, text=self.ny.t("add_button"), command=csere_hozzaadasa)
        hozzaad_gomb.grid(row=0, column=4, padx=(4, 0))

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

        torol_gomb = ttk.Button(
            also_gombsor, text=self.ny.t("delete_selected_replacement"),
            command=kijelolt_csere_torlese
        )
        torol_gomb.pack(side=tk.LEFT)

        bezar_gomb = ttk.Button(also_gombsor, text=self.ny.t("close"), command=ablak.destroy)
        bezar_gomb.pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # Pozíció szerinti karaktertörlés beállító ablaka
    # ------------------------------------------------------------------
    def pozicio_torles_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("position_delete_title"))
        ablak.geometry("460x400")
        ablak.transient(self.root)
        ablak.grab_set()

        ttk.Label(
            ablak, text=self.ny.t("position_delete_desc"), justify="left"
        ).pack(fill=tk.X, padx=10, pady=(10, 10))

        ttk.Label(
            ablak, text=self._hatokor_szoveg(), justify="left",
            font=("TkDefaultFont", 9, "italic")
        ).pack(fill=tk.X, padx=10, pady=(0, 10))

        bevitel_keret = ttk.Frame(ablak)
        bevitel_keret.pack(fill=tk.X, padx=10, pady=5)

        cimke = ttk.Label(bevitel_keret, text=self.ny.t("position_input_label"))
        cimke.pack(side=tk.LEFT, padx=(0, 8))

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

        # Enter lenyomására is alkalmazza a beállítást
        mezo.bind("<Return>", lambda esemeny: alkalmaz())

    # ------------------------------------------------------------------
    # Súgó és Névjegy ablakok
    # ------------------------------------------------------------------
    def sugo_ablak_megnyitasa(self):
        ablak = tk.Toplevel(self.root)
        ablak.title(self.ny.t("help_title"))
        ablak.geometry("480x400")
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
        koteg_naplo = []  # ehhez a művelethez tartozó (uj_ut, regi_ut) párok

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

        self._frissitsd_tablat()
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

        # fordított sorrendben állítjuk vissza, a legutóbb átnevezettől az elsőig
        for uj_ut, regi_ut in reversed(koteg_naplo):
            if not os.path.exists(uj_ut):
                hibak.append(f"{os.path.basename(uj_ut)}: {self.ny.t('not_found')}")
                continue
            if os.path.exists(regi_ut) and regi_ut != uj_ut:
                hibak.append(self.ny.t("already_exists", nev=os.path.basename(uj_ut), uj=os.path.basename(regi_ut)))
                continue
            try:
                os.rename(uj_ut, regi_ut)
                # frissítsük a lista megfelelő elemét, ha még benne van
                for elem in self.elemek:
                    if elem["eredeti_ut"] == uj_ut:
                        elem["eredeti_ut"] = regi_ut
                        elem["eredeti_nev"] = os.path.basename(regi_ut)
                        elem["uj_nev"] = uj_nev_kepzes(elem["eredeti_nev"], self.egyeni_cserek, self._pozicio_halmaz())
                        break
                sikeres += 1
            except OSError as hiba:
                hibak.append(f"{os.path.basename(uj_ut)}: {hiba}")

        self._frissitsd_tablat()
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
