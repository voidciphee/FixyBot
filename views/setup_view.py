import discord
from utils.database import list_universes


UNIVERS_PAR_CATEGORIE = {
    "🥷 GANG": [
        ("🔥", "tokyo_revengers", "Tokyo Revengers"),
        ("⚡", "reality_quest", "Reality Quest"),
        ("🏫", "wind_breaker", "Wind Breaker"),
    ],
    "⚔️ ACTION": [
        ("🩸", "jujika_no_rokunin", "Jujika no Rokunin"),
        ("⚔️", "demon_slayer", "Demon Slayer"),
        ("🏴‍☠️", "one_piece", "One Piece"),
        ("🥋", "jujutsu_kaisen", "Jujutsu Kaisen"),
        ("🧱", "attack_on_titan", "L'Attaque des Titans"),
        ("🌊", "vinland_saga", "Vinland Saga"),
        ("🦅", "berserk", "Berserk"),
        ("🍥", "naruto", "Naruto"),
        ("⚔️", "bleach", "Bleach"),
        ("🐉", "dragon_ball", "Dragon Ball"),
        ("🍀", "black_clover", "Black Clover"),
        ("💎", "jojo", "JoJo's Bizarre Adventure"),
        ("🪚", "chainsaw_man", "Chainsaw Man"),
        ("👊", "one_punch_man", "One Punch Man"),
        ("👹", "kaiju_no_8", "Kaiju No. 8"),
        ("👻", "dandadan", "Dandadan"),
    ],
    "❤️ ROMANCE": [
        ("💄", "my_dress_up_darling", "My Dress-Up Darling"),
        ("🤖", "darling_in_the_franxx", "Darling in the Franxx"),
        ("💙", "masamune_kun_revenge", "Masamune-kun's Revenge"),
        ("💛", "a_couple_of_cuckoos", "A Couple of Cuckoos"),
        ("💖", "tonikaku_kawaii", "Tonikaku Kawaii"),
        ("🎵", "a_silent_voice", "A Silent Voice"),
        ("🌸", "i_want_to_eat_your_pancreas", "I Want to Eat Your Pancreas"),
        ("🩷", "horimiya", "Horimiya"),
        ("💕", "kaguya_sama", "Kaguya-sama: Love is War"),
        ("💗", "rent_a_girlfriend", "Rent-a-Girlfriend"),
        ("💞", "fruits_basket", "Fruits Basket"),
        ("💓", "toradora", "Toradora!"),
        ("👹", "oni_no_hanayome", "Oni no Hanayome"),
        ("🌧️", "maboroshi", "Maboroshi"),
    ],
    "🏀 SPORT": [
        ("⚽", "blue_lock", "Blue Lock"),
        ("🏐", "haikyuu", "Haikyuu!!"),
        ("🏀", "kuroko_no_basket", "Kuroko no Basket"),
        ("🥊", "hajime_no_ippo", "Hajime no Ippo"),
        ("🚗", "initial_d", "Initial D"),
    ],
    "🧠 PSYCHOLOGIQUE": [
        ("📓", "death_note", "Death Note"),
        ("👑", "code_geass", "Code Geass"),
        ("⏰", "steins_gate", "Steins;Gate"),
        ("🚔", "psycho_pass", "Psycho-Pass"),
        ("🏫", "classroom_of_elite", "Classroom of the Elite"),
    ],
    "👻 HORREUR": [
        ("💀", "another", "Another"),
        ("👁️", "tokyo_ghoul", "Tokyo Ghoul"),
        ("👽", "parasyte", "Parasyte"),
        ("🧟", "highschool_of_the_dead", "Highschool of the Dead"),
    ],
    "✨ FANTASY / ISEKAI": [
        ("⏳", "re_zero", "Re:Zero"),
        ("👑", "overlord", "Overlord"),
        ("💥", "konosuba", "KonoSuba"),
        ("🧝", "frieren", "Frieren"),
        ("🎲", "no_game_no_life", "No Game No Life"),
    ],
    "🚀 SCI-FI": [
        ("🌌", "cowboy_bebop", "Cowboy Bebop"),
        ("🤖", "gundam", "Mobile Suit Gundam"),
        ("🤖", "nier_automata", "Nier:Automata Ver1.1a"),
    ],
    "🎭 TRANCHE DE VIE": [
        ("🏝️", "barakamon", "Barakamon"),
        ("🔍", "hyouka", "Hyouka"),
        ("🎸", "bocchi_the_rock", "Bocchi the Rock!"),
    ],
    "🎵 MUSIQUE": [
        ("🎺", "euphonium", "Sound! Euphonium"),
        ("🎸", "given", "Given"),
    ],
    "🎮 JEUX / COMPÉTITION": [
        ("🎲", "kakegurui", "Kakegurui"),
        ("🎮", "kings_avatar", "The King's Avatar"),
    ],
    "🔎 MYSTÈRE": [
        ("🕵️", "detective_conan", "Detective Conan"),
        ("📚", "gosick", "Gosick"),
    ],
    "📚 MANGA / MANHWA": [
        ("🎃", "pumpkin_night", "Pumpkin Night"),
        ("🏫", "legendary_hero_academy", "The Legendary Hero is an Academy Honors Student"),
        ("🥊", "lookism", "Lookism"),
        ("⚔️", "solo_leveling", "Solo Leveling"),
        ("🗡️", "star_embracing_swordmaster", "Star-Embracing Swordmaster"),
    ],
}


def _index_anime():
    index = []
    for cat, liste in UNIVERS_PAR_CATEGORIE.items():
        for emoji, key, nom in liste:
            index.append((cat, emoji, key, nom))
    return index


ANIME_INDEX = _index_anime()


def rechercher_anime(query: str, limite: int = 25):
    q = query.lower().strip()
    if not q:
        return []
    resultats = []
    for cat, emoji, key, nom in ANIME_INDEX:
        if q in nom.lower() or q in key.lower():
            resultats.append((cat, emoji, key, nom))
    return resultats[:limite]


UNIVERS_GANG = {"tokyo_revengers", "reality_quest", "wind_breaker"}


# ═══════════════════════════════════════════════════════
# MODALE : nom du serveur
# ═══════════════════════════════════════════════════════

class ServerNameModal(discord.ui.Modal, title="Nom du serveur"):
    name = discord.ui.TextInput(
        label="Nom du serveur",
        placeholder="Crimson Community",
        max_length=80,
    )

    def __init__(self, state: dict):
        super().__init__()
        self.state = state

    async def on_submit(self, interaction: discord.Interaction):
        self.state["server_name"] = self.name.value
        await interaction.response.send_message(
            "🏯 Choisis une option :",
            view=MainMenuView(self.state),
            ephemeral=True,
        )


# ═══════════════════════════════════════════════════════
# MODALE : recherche
# ═══════════════════════════════════════════════════════

class SearchModal(discord.ui.Modal, title="🔍 Rechercher un anime"):
    query = discord.ui.TextInput(
        label="Nom de l'anime",
        placeholder="Ex: Solo Leveling, Naruto, Horimiya...",
        max_length=80,
    )

    def __init__(self, state: dict):
        super().__init__()
        self.state = state

    async def on_submit(self, interaction: discord.Interaction):
        resultats = rechercher_anime(self.query.value)
        if not resultats:
            await interaction.response.send_message(
                f"❌ Aucun anime trouvé pour « **{self.query.value}** ».",
                ephemeral=True,
            )
            return

        options = [
            discord.SelectOption(
                label=nom[:100],
                value=key,
                emoji=emoji,
                description=f"Catégorie : {cat}"[:100],
            )
            for cat, emoji, key, nom in resultats
        ]
        select = discord.ui.Select(
            placeholder=f"Résultats pour « {self.query.value} » ({len(options)})",
            options=options,
        )
        view = discord.ui.View(timeout=600)
        view.add_item(select)

        async def cb(inter: discord.Interaction):
            key = inter.data["values"][0]
            nom = next(n for _, _, k, n in resultats if k == key)
            self.state["universe"] = key
            self.state["theme"] = "urban"
            await _continuer_vers_anime(inter, self.state, key, nom)

        select.callback = cb
        await interaction.response.send_message(
            f"🔍 **{len(resultats)} résultat(s)** pour « {self.query.value} » :",
            view=view,
            ephemeral=True,
        )


# ═══════════════════════════════════════════════════════
# VUE : menu principal
# ═══════════════════════════════════════════════════════

class MainMenuView(discord.ui.View):
    def __init__(self, state: dict):
        super().__init__(timeout=600)
        self.state = state

    @discord.ui.button(
        label="Choisir un anime", emoji="🎌",
        style=discord.ButtonStyle.primary, row=0,
    )
    async def choisir_anime(self, it: discord.Interaction, _):
        await it.response.edit_message(
            content="📚 Choisis une catégorie d'anime :",
            view=SetupUniversView(self.state),
        )

    @discord.ui.button(
        label="Rechercher un anime", emoji="🔍",
        style=discord.ButtonStyle.success, row=0,
    )
    async def rechercher(self, it: discord.Interaction, _):
        await it.response.send_modal(SearchModal(self.state))

    @discord.ui.button(
        label="Univers disponibles", emoji="📚",
        style=discord.ButtonStyle.secondary, row=1,
    )
    async def univers(self, it: discord.Interaction, _):
        us = list_universes()
        txt = "\n".join(f"• {u}" for u in us) if us else "Aucun univers disponible."
        await it.response.send_message(
            f"📚 **Univers disponibles :**\n{txt}", ephemeral=True,
        )

    @discord.ui.button(
        label="Suggestion", emoji="💡",
        style=discord.ButtonStyle.secondary, row=1,
    )
    async def suggestion(self, it: discord.Interaction, _):
        from views.suggestion_view import SuggestionView
        await it.response.send_message(
            "💡 **Tu as une idée ?**\n"
            "Rejoins notre serveur Discord officiel.",
            view=SuggestionView(), ephemeral=True,
        )

    @discord.ui.button(
        label="Informations", emoji="ℹ️",
        style=discord.ButtonStyle.secondary, row=1,
    )
    async def info(self, it: discord.Interaction, _):
        await it.response.send_message(
            "🏯 **Gang Server Builder**\n"
            "Génère automatiquement une structure Discord complète.",
            ephemeral=True,
        )


# ═══════════════════════════════════════════════════════
# VUE : catégories → anime
# ═══════════════════════════════════════════════════════

class SetupUniversView(discord.ui.View):
    def __init__(self, state: dict):
        super().__init__(timeout=600)
        self.state = state

        options = [
            discord.SelectOption(label=cat, value=cat)
            for cat in UNIVERS_PAR_CATEGORIE
        ]
        select = discord.ui.Select(
            placeholder="Choisis une catégorie d'anime",
            options=options,
        )
        select.callback = self.pick_cat
        self.add_item(select)

    async def pick_cat(self, it: discord.Interaction):
        cat = it.data["values"][0]
        univers = UNIVERS_PAR_CATEGORIE.get(cat, [])
        if not univers:
            await it.response.edit_message(
                content="❌ Aucun anime dans cette catégorie.", view=None,
            )
            return

        options = [
            discord.SelectOption(
                label=nom[:100], value=key, emoji=emoji,
            )
            for emoji, key, nom in univers[:25]
        ]
        select = discord.ui.Select(
            placeholder=f"Choisis un anime ({cat})",
            options=options,
        )
        view = discord.ui.View(timeout=600)
        view.add_item(select)

        async def cb(inter: discord.Interaction):
            key = inter.data["values"][0]
            nom = next(n for _, k, n in univers if k == key)
            self.state["universe"] = key
            self.state["theme"] = "urban"
            await _continuer_vers_anime(inter, self.state, key, nom)

        select.callback = cb
        await it.response.edit_message(
            content=f"📚 **{cat}** — Choisis un anime :",
            view=view,
        )


# ═══════════════════════════════════════════════════════
# FONCTION : continuer après le choix de l'anime
# ═══════════════════════════════════════════════════════

async def _continuer_vers_anime(
    it: discord.Interaction,
    state: dict,
    key: str,
    nom: str,
):
    """
    GANG   → sélection du gang
    ANIME  → prévisualisation directe (plus de thème)
    """

    # GANG → étape de sélection de gang
    if key in UNIVERS_GANG:
        from views.gang_picker_view import GangPickerView
        state["universe"] = key
        await it.response.edit_message(
            content=f"🌍 Anime : **{nom}**\nChoisis un gang/groupe :",
            view=GangPickerView(state, key),
        )
        return

    # ANIME → on va directement à la prévisualisation
    from views.gang_view import GangView
    state["universe"] = key
    state["gangs"] = [nom]
    state["gang"] = nom

    # On passe par GangView pour la prévisualisation,
    # mais SANS passer par le choix du thème.
    await it.response.edit_message(
        content=f"🎬 **{nom}**\nConfirme pour lancer la génération :",
        view=GangView(state),
    )


# ═══════════════════════════════════════════════════════
# VUE PRINCIPALE
# ═══════════════════════════════════════════════════════

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)

    @discord.ui.button(
        label="Créer mon serveur", emoji="🚀",
        style=discord.ButtonStyle.primary, row=0,
    )
    async def start(self, it: discord.Interaction, _):
        state: dict = {}
        await it.response.send_modal(ServerNameModal(state))

    @discord.ui.button(
        label="Rechercher un anime", emoji="🔍",
        style=discord.ButtonStyle.success, row=0,
    )
    async def search(self, it: discord.Interaction, _):
        state: dict = {}
        await it.response.send_modal(SearchModal(state))

    @discord.ui.button(
        label="Suggestion", emoji="💡",
        style=discord.ButtonStyle.secondary, row=1,
    )
    async def suggestion(self, it: discord.Interaction, _):
        from views.suggestion_view import SuggestionView
        await it.response.send_message(
            "💡 **Tu as une idée ?**\n"
            "Rejoins notre serveur Discord officiel.",
            view=SuggestionView(), ephemeral=True,
        )

    @discord.ui.button(
        label="Informations", emoji="ℹ️",
        style=discord.ButtonStyle.secondary, row=1,
    )
    async def info(self, it: discord.Interaction, _):
        await it.response.send_message(
            "🏯 **Gang Server Builder**\n"
            "Génère automatiquement une structure Discord complète.",
            ephemeral=True,
        )