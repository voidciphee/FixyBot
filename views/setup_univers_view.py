import discord


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


# Univers qui passent par le système de gang
UNIVERS_GANG = {"tokyo_revengers", "reality_quest", "wind_breaker"}


class SetupUniversView(discord.ui.View):
    def __init__(self, state: dict):
        super().__init__(timeout=600)
        self.state = state

        options = [
            discord.SelectOption(label=cat, value=cat)
            for cat in UNIVERS_PAR_CATEGORIE
        ]
        select = discord.ui.Select(
            placeholder="Choisis une catégorie d'univers",
            options=options,
        )
        select.callback = self.pick_cat
        self.add_item(select)

    async def pick_cat(self, it: discord.Interaction):
        cat = it.data["values"][0]
        univers = UNIVERS_PAR_CATEGORIE.get(cat, [])
        if not univers:
            await it.response.edit_message(
                content="❌ Aucun univers dans cette catégorie.", view=None,
            )
            return

        # Discord limite à 25 options par select
        options = [
            discord.SelectOption(label=nom[:100], value=key, emoji=emoji)
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
            self.state["universe"] = key

            if key in UNIVERS_GANG:
                from views.gang_picker_view import GangPickerView
                await inter.response.edit_message(
                    content=f"🌍 Univers : **{key}**\nChoisis un gang/groupe :",
                    view=GangPickerView(self.state, key),
                )
                return

            from views.direct_universe_view import DirectUniverseView
            nom = next((n for _, k, n in univers if k == key), key)
            await inter.response.edit_message(
                content=f"🎬 **{nom}**\nQue veux-tu faire ?",
                view=DirectUniverseView(self.state, key, nom),
            )

        select.callback = cb
        await it.response.edit_message(
            content=f"📚 **{cat}** — Choisis un anime :",
            view=view,
        )