from themes import urban, dark, anime, japanese, custom

THEMES = {
    "urban": urban.THEME,
    "dark": dark.THEME,
    "anime": anime.THEME,
    "japanese": japanese.THEME,
    "custom": custom.THEME,
}


def get_theme(key: str) -> dict:
    return THEMES.get(key, urban.THEME)


def theme_choices() -> list[tuple[str, str]]:
    return [(k, t["label"]) for k, t in THEMES.items()]