import discord
from utils.permissions import perms_for_rank, couleur_par_importance
from utils.logger import get_logger
from generators.role_generator import create_roles_with_separators
from generators.category_generator import create_category
from generators.channel_generator import create_text, create_voice

log = get_logger("community_generator")


# Hiérarchie complète du serveur communautaire
HIERARCHIE_COMMU = {
    "DIRECTION": [
        ("👑", "Fondateur"),
        ("👑", "Co-Fondateur"),
        ("🏛️", "Directeur"),
        ("🏛️", "Administrateur"),
        ("📋", "Responsable"),
        ("📋", "Superviseur"),
        ("⚔️", "Head Staff"),
    ],
    "HAUTS GRADÉS": [
        ("🛡️", "Admin"),
        ("🛡️", "Modérateur Senior"),
        ("⚔️", "Modérateur"),
        ("⚔️", "Modérateur Junior"),
        ("🔥", "Helper"),
        ("🔥", "Support"),
        ("🎉", "Responsable Événements"),
        ("🤝", "Responsable Partenariats"),
        ("📣", "Responsable Communication"),
    ],
    "MEMBRES": [
        ("⭐", "Vétéran"),
        ("⭐", "Membre actif"),
        ("👊", "Membre"),
        ("🆕", "Nouveau"),
    ],
}


# Rôles Gaming
GAMING = [
    ("🎮", "Gamer"),
    ("🔫", "FPS"),
    ("⚔️", "MMO"),
    ("🏆", "Compétitif"),
    ("🎯", "Esport"),
    ("🕹️", "Rétro Gaming"),
    ("🎲", "Jeux de société"),
    ("🧩", "Puzzle"),
    ("🚗", "Course"),
    ("🏰", "Stratégie"),
    ("🎭", "RPG"),
    ("⚽", "Sport virtuel"),
    ("🌍", "Open World"),
    ("🎬", "Streamer"),
    ("📹", "Créateur de contenu"),
]


# Rôles Centres d'intérêt
INTERETS = [
    ("🎵", "Musique"),
    ("🎸", "Rock"),
    ("🎤", "Rap"),
    ("🎻", "Classique"),
    ("🎧", "DJ"),
    ("🎌", "Anime"),
    ("📚", "Manga"),
    ("💻", "Informatique"),
    ("👨‍💻", "Programmation"),
    ("🎨", "Dessin"),
    ("📷", "Photographie"),
    ("🏄", "Surf"),
    ("⚽", "Sport"),
    ("🏋️", "Musculation"),
    ("🚴", "Vélo"),
    ("🏃", "Course"),
    ("🍳", "Cuisine"),
    ("🎬", "Cinéma"),
    ("📖", "Lecture"),
    ("✈️", "Voyage"),
]


# Rôles Notifications
NOTIFS = [
    ("🔔", "Annonces"),
    ("🎉", "Événements"),
    ("🎁", "Giveaways"),
    ("📰", "News"),
    ("🤝", "Partenariats"),
    ("🆕", "Nouveautés"),
]


# Rôles Couleurs
COULEURS = [
    ("🔴", "Rouge"),
    ("🟠", "Orange"),
    ("🟡", "Jaune"),
    ("🟢", "Vert"),
    ("🔵", "Bleu"),
    ("🟣", "Violet"),
    ("⚫", "Noir"),
    ("⚪", "Blanc"),
    ("🟤", "Marron"),
    ("🩷", "Rose"),
]


async def generate_community(guild: discord.Guild, config: dict):
    """Crée un serveur communautaire complet avec ~150 rôles utiles."""
    nom = config.get("server_name", "Communauté")

    # ─── 1. Rôles ───
    specs = []
    seen = set()

    def ajouter(emoji, role, groupe):
        key = role.lower()
        if key in seen:
            return
        seen.add(key)
        specs.append({
            "name": f"{emoji} {role}",
            "emoji": emoji,
            "rank": role,
            "color": discord.Color.dark_red(),
            "permissions": perms_for_rank(role),
            "groupe": groupe,
        })

    # Hiérarchie principale
    for groupe, liste in HIERARCHIE_COMMU.items():
        for emoji, role in liste:
            ajouter(emoji, role, groupe)

    # Gaming
    for emoji, role in GAMING:
        ajouter(emoji, role, "MEMBRES")

    # Centres d'intérêt
    for emoji, role in INTERETS:
        ajouter(emoji, role, "MEMBRES")

    # Notifications
    for emoji, role in NOTIFS:
        ajouter(emoji, role, "MEMBRES")

    # Couleurs
    for emoji, role in COULEURS:
        ajouter(emoji, role, "MEMBRES")

    # Limite Discord
    if len(guild.roles) + len(specs) > 245:
        specs = specs[:max(0, 240 - len(guild.roles))]

    await create_roles_with_separators(
        guild, specs, couleur_base_hex="#5865F2",
    )

    # ─── 2. Salons ───
    cats = {
        "📌 INFORMATIONS": [
            "📜・règlement", "📢・annonces", "📖・présentation",
            "ℹ️・informations", "❓・faq", "📅・événements", "📰・news",
        ],
        "💬 COMMUNAUTÉ": [
            "💬・général", "👋・présentations", "📸・photos",
            "🎵・musique", "🎮・gaming", "😂・memes",
            "🤖・bots", "💡・suggestions",
        ],
        "🎮 GAMING": [
            "🎮・jeux", "🏆・compétitif", "👥・recherche-de-joueurs",
            "💬・discussion-gaming", "📊・classements",
        ],
        "🎉 ÉVÉNEMENTS": [
            "🎉・événements", "🎁・giveaways", "🏅・concours",
            "📅・calendrier",
        ],
        "🎫 SUPPORT": [
            "🎫・tickets", "🆘・aide", "🚨・signalement",
            "🤝・partenariat",
        ],
        "🛡️ STAFF": [
            "💼・staff", "📜・logs", "🚨・signalements-staff",
            "📊・rapports", "📝・notes-staff",
        ],
    }
    for nc, salons in cats.items():
        cat = await create_category(guild, nc)
        for s in salons:
            await create_text(guild, s, cat)

    # ─── 3. Vocaux ───
    voice_cat = await create_category(guild, "🔊 VOCAUX")
    for v in ["Général", "Gaming", "Discussion", "Musique",
              "AFK", "Réunion", "Événement"]:
        await create_voice(guild, f"🔊・{v}", voice_cat)

    log.info("Serveur communautaire créé pour %s (%d rôles)",
             guild.name, len(specs))
    return True