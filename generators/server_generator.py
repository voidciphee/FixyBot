import discord
from themes.registry import get_theme
from utils.logger import get_logger

log = get_logger("server_generator")


# ═══════════════════════════════════════════════════════
# LISTE DES ANIME QUI PASSENT PAR generate_anime
# ═══════════════════════════════════════════════════════
# Si un anime est dans cette liste, il utilise sa propre config
# du dictionnaire ANIMES dans anime_generator.py.

ANIME_DIRECT = {
    # ⚔️ ACTION
    "jujika_no_rokunin",
    "demon_slayer",
    "one_piece",
    "jujutsu_kaisen",
    "attack_on_titan",
    "vinland_saga",
    "berserk",
    "naruto",
    "bleach",
    "dragon_ball",
    "black_clover",
    "jojo",
    "chainsaw_man",
    "one_punch_man",
    "kaiju_no_8",
    "dandadan",

    # ❤️ ROMANCE
    "my_dress_up_darling",
    "darling_in_the_franxx",
    "masamune_kun_revenge",
    "a_couple_of_cuckoos",
    "tonikaku_kawaii",
    "a_silent_voice",
    "i_want_to_eat_your_pancreas",
    "horimiya",
    "kaguya_sama",
    "rent_a_girlfriend",
    "fruits_basket",
    "toradora",
    "oni_no_hanayome",
    "maboroshi",

    # 🏀 SPORT
    "blue_lock",
    "haikyuu",
    "kuroko_no_basket",
    "hajime_no_ippo",
    "initial_d",

    # 🧠 PSYCHOLOGIQUE
    "death_note",
    "code_geass",
    "steins_gate",
    "psycho_pass",
    "classroom_of_elite",

    # 👻 HORREUR
    "another",
    "tokyo_ghoul",
    "parasyte",
    "highschool_of_the_dead",

    # ✨ FANTASY / ISEKAI
    "re_zero",
    "overlord",
    "konosuba",
    "frieren",
    "no_game_no_life",

    # 🚀 SCI-FI
    "cowboy_bebop",
    "gundam",
    "nier_automata",

    # 🎭 TRANCHES DE VIE
    "barakamon",
    "hyouka",
    "bocchi_the_rock",

    # 🎵 MUSIQUE
    "euphonium",
    "given",

    # 🎮 JEUX / COMPÉTITION
    "kakegurui",
    "kings_avatar",

    # 🔎 MYSTÈRE
    "detective_conan",
    "gosick",

    # 📚 MANGA / MANHWA
    "pumpkin_night",
    "legendary_hero_academy",
    "lookism",
    "solo_leveling",
    "star_embracing_swordmaster",
}

# Univers qui utilisent le système de gang (Tokyo Revengers, Reality Quest, Wind Breaker)
UNIVERS_GANG = {"tokyo_revengers", "reality_quest", "wind_breaker"}


async def generate(guild: discord.Guild, config: dict):
    theme = get_theme(config.get("theme", "urban"))
    universe = (config.get("universe") or "").lower().replace(" ", "_")
    gang = config.get("gang")
    all_salons = bool(config.get("all_salons"))

    log.info("═══ server_generator ═══")
    log.info("Œuvre sélectionnée : %s", universe)

    # ─── 1. GANG (Tokyo Revengers, Reality Quest, Wind Breaker) ───
    if universe in UNIVERS_GANG:
        log.info("Configuration chargée : GANG (%s)", universe)
        if universe == "tokyo_revengers":
            from generators.tokyo_revengers_generator import generate_tokyo_revengers
            await generate_tokyo_revengers(guild, gang=gang, all_salons=all_salons)
        elif universe == "reality_quest":
            from generators.reality_quest_generator import generate_reality_quest
            await generate_reality_quest(guild, gang=gang, all_salons=all_salons)
        elif universe == "wind_breaker":
            from generators.wind_breaker_generator import generate_wind_breaker
            await generate_wind_breaker(guild, gang=gang, all_salons=all_salons)
        log.info("Rôles spécifiques : OK")
        log.info("Salons spécifiques : OK")
        return True

    # ─── 2. ANIME DIRECT (Action, Romance, Manga/Manhwa, etc.) ───
    if universe in ANIME_DIRECT:
        log.info("Configuration chargée : %s", universe)
        try:
            from generators.anime_generator import generate_anime, ANIMES
        except ImportError as e:
            log.error("❌ Impossible d'importer anime_generator : %s", e)
            return False

        if universe not in ANIMES:
            log.error("❌ Configuration '%s' absente du dictionnaire ANIMES.", universe)
            log.error("❌ Vérifie generators/anime_generator.py.")
            return False

        await generate_anime(guild, universe)
        log.info("Rôles spécifiques : OK")
        log.info("Salons spécifiques : OK")
        return True

    # ─── 3. FALLBACK CUSTOM (uniquement si aucune config spécifique) ───
    log.warning("⚠ Aucune configuration spécifique pour '%s'.", universe)
    log.warning("⚠ Utilisation du générateur CUSTOM (rôles génériques).")
    from generators.custom_generator import generate_custom_gangs
    config["theme_obj"] = theme
    await generate_custom_gangs(guild, config)
    return True