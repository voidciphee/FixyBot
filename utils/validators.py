import re

NAME_RE = re.compile(r"^[\w\s\-'éèêàâîïôûùç]{2,40}$", re.IGNORECASE)


def valid_name(value: str) -> bool:
    return bool(value and NAME_RE.match(value.strip()))


def sanitize_channel(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^\w\s\-]", "", name)
    name = re.sub(r"\s+", "-", name)
    return name[:90] or "salon"


# ══════════════════════════════════════════════════════
# VÉRIFICATION D'AUTORISATION
# ══════════════════════════════════════════════════════

# ID du serveur protégé
SERVEUR_PROTEGE_ID = 1549686244336730163

# ID de l'utilisateur autorisé (toi)
UTILISATEUR_AUTORISE_ID = 1236672232537849937


def est_autorise(interaction) -> bool:
    """Renvoie True si l'utilisateur peut utiliser la commande.
    Sur le serveur protégé, seul l'utilisateur autorisé passe.
    Ailleurs, tout le monde avec les permissions passe."""
    if not interaction.guild:
        return True

    # Si ce n'est pas le serveur protégé, on autorise
    if interaction.guild.id != SERVEUR_PROTEGE_ID:
        return True

    # Sur le serveur protégé, seul l'utilisateur autorisé passe
    return interaction.user.id == UTILISATEUR_AUTORISE_ID