import asyncio
import discord
from utils.permissions import perms_for_rank, couleur_par_importance
from utils.logger import get_logger

log = get_logger("anime_generator")


ANIMES = {
    # ═══════════════ ⚔️ ACTION ═══════════════
    "jujika_no_rokunin": {
        "nom": "Jujika no Rokunin", "couleur_base": "#8B0000",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🩸","Légende de la Vengeance"),("👑","Maître des Ombres"),("🎯","Architecte du Châtiment"),("🗡️","Fantôme Écarlate")],
            "👑 HAUTS GRADÉS": [("🩸","Chef de la vengeance"),("⚔️","Bras droit"),("🎯","Maître chasseur"),("🗡️","Assassin d'élite")],
            "🗡️ SPÉCIALISATIONS": [("🩸","Exécuteur"),("🎯","Chasseur de cibles"),("🔥","Combattant d'élite"),("⚔️","Combattant")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ MISSIONS":["⚔️・missions","🎯・cibles"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général","🎨・fanarts"]},
        "vocaux": ["Discussion","RP","Détente"],
    },
    "demon_slayer": {
        "nom": "Demon Slayer", "couleur_base": "#228B22",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Seigneur des Souffles"),("🌸","Légende du Corps"),("🌙","Chasseur de Lunes Suprêmes")],
            "👑 HAUTS GRADÉS": [("👑","Pilier"),("⚔️","Pourfendeur de Lune"),("🌊","Maître de l'Eau"),("🔥","Maître du Feu")],
            "🌸 SOUFFLES": [("🌸","Souffle de la Fleur"),("🌫️","Souffle de la Brume"),("🐍","Souffle du Serpent"),("💗","Souffle de l'Amour")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Pourfendeur"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ CORPS":["⚔️・missions","🌊・souffles"],"🩸 DÉMONS":["🩸・démons","🌙・lunes"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général","🎨・fanarts"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "one_piece": {
        "nom": "One Piece", "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Empereur des Mers"),("🌊","Seigneur des Océans"),("💰","Légende des Trésors")],
            "👑 HAUTS GRADÉS": [("👑","Capitaine"),("⚔️","Second"),("🧭","Maître navigateur"),("💰","Maître pillard")],
            "⚓ ÉQUIPAGE": [("🍳","Cuisinier"),("💉","Médecin"),("🔫","Sniper"),("🎵","Musicien"),("🌊","Marin")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("⚓","Membre d'équipage"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⛵ ÉQUIPAGE":["⛵・équipage","📋・missions"],"💰 TRÉSORS":["💰・trésors","🏆・primes"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général","🎨・fanarts"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "jujutsu_kaisen": {
        "nom": "Jujutsu Kaisen", "couleur_base": "#4B0082",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende du Jujutsu"),("🔮","Maître des Fléaux"),("⚔️","Exorciste Légendaire")],
            "👑 HAUTS GRADÉS": [("👑","Grade Spécial"),("⚔️","Grade 1"),("🔮","Maître des techniques"),("🧠","Stratège en chef")],
            "🔮 JUTSU": [("🔮","Grade 2"),("🌀","Grade 3"),("🎓","Étudiant"),("🩸","Fléau")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Combattant"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔮 JUTSU":["🔮・techniques","⚔️・missions"],"🩸 FLÉAUX":["🩸・fléaux"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "attack_on_titan": {
        "nom": "L'Attaque des Titans", "couleur_base": "#8B4513",
        "groupes_roles": {
            "🏛️ GOUVERNEMENT": [("👑","Roi"),("👑","Famille Royale"),("🏛️","Gouvernement Royal"),("⚖️","Conseil Royal")],
            "👑 AUTORITÉ ROYALE": [("👑","Garde Royale"),("⚔️","Police Militaire"),("🪖","Soldat de la Police Militaire")],
            "⚔️ FORCES MILITAIRES": [("🛡️","Garnison"),("🗡️","Bataillon d'Exploration"),("🎖️","Commandant"),("🪖","Soldat")],
            "🗡️ SPÉCIALISATIONS": [("🗡️","Combattant"),("🧭","Éclaireur"),("🎯","Tireur"),("🩺","Médecin"),("📡","Stratège")],
            "🌍 ORIGINES": [("🛡️","Eldien"),("🌍","Marley"),("⚔️","Guerrier de Marley"),("🌎","Monde Extérieur")],
            "🧬 ORIGINE DES TITANS": [("👑","Ymir — Fondatrice des Titans"),("🌳","Arbre de Ymir"),("⚡","Pouvoir des Titans"),("🔗","Chemins"),("🌌","Monde des Chemins")],
            "🏷️ COMMUNAUTÉ": [("🎨","Créateur"),("🎮","Joueur"),("💬","Actif"),("🌟","Vétéran")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ MILITAIRE":["🛡️・bataillon-exploration","🎖️・brigade"],"🧟 TITANS":["🧟・titans","🔬・recherche"],"🌍 HORS DES MURS":["🌍・hors-des-murs"],"🎭 RP":["🎭・rp"],"💬 COMMUNAUTÉ":["💬・général","🎨・fanarts"]},
        "vocaux": ["Discussion","Militaire","RP","Titans","Détente"],
    },
    "vinland_saga": {
        "nom": "Vinland Saga", "couleur_base": "#4A6FA5",
        "groupes_roles": {
            "⚔️ GUERRIERS": [("⚔️","Guerrier"),("🛡️","Viking"),("🪓","Jomsviking"),("👑","Chef de guerre")],
            "👑 ROYAUMES": [("👑","Royaume de Danemark"),("👑","Royaume d'Angleterre"),("👑","Royaume de Norvège"),("⚔️","Armée danoise")],
            "🌊 EXPLORATION": [("🌊","Voyageur"),("🧭","Explorateur"),("⛵","Navigateur"),("🌱","Vinland")],
            "🧑‍🌾 SOCIÉTÉ": [("🧑‍🌾","Agriculteur"),("🏘️","Villageois"),("💰","Marchand")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ GUERRE":["⚔️・guerres","🎯・batailles"],"🌊 EXPLORATION":["🌊・voyages","🗺️・territoires"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Guerre","Détente"],
    },
    "berserk": {
        "nom": "Berserk", "couleur_base": "#2F1B0C",
        "groupes_roles": {
            "⚔️ BAND OF THE HAWK": [("🦅","Band of the Hawk"),("👑","Commandant"),("⚔️","Guerrier"),("🏹","Archer"),("🛡️","Soldat")],
            "🩸 APOSTLES": [("👹","Apôtre"),("🩸","Marque du Sacrifice"),("🌑","Éclipse")],
            "🌑 GOD HAND": [("🌑","God Hand"),("🕳️","Dimension Astrale"),("🩸","Sacrifice")],
            "⚔️ COMBAT": [("⚔️","Mercenaire"),("🗡️","Épéiste"),("🏹","Archer"),("🐎","Cavalier")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・batailles","🩸・massacres"],"🩸 APOSTLES":["🩸・apôtres","👹・démons"],"🌑 GOD HAND":["🌑・god-hand"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "naruto": {
        "nom": "Naruto", "couleur_base": "#FF8C00",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🔥","Hokage"),("👑","Sannin"),("🍥","Ninja Légendaire"),("🦊","Jinchûriki")],
            "⚔️ NINJAS": [("🥷","Ninja"),("🎯","Jōnin"),("🛡️","Chūnin"),("🔰","Genin")],
            "🏯 VILLAGES": [("🍥","Konohagakure"),("🌊","Kirigakure"),("⛰️","Iwagakure"),("🔥","Kumogakure")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ MISSIONS":["⚔️・missions","🎯・combats"],"🏯 VILLAGES":["🏯・konoha","🌊・kiri"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "bleach": {
        "nom": "Bleach", "couleur_base": "#000000",
        "groupes_roles": {
            "🌟 LÉGENDES": [("⚔️","Shinigami Légendaire"),("👑","Capitaine Commandant"),("🦋","Vasto Lorde")],
            "⚔️ SHINIGAMIS": [("⚔️","Shinigami"),("🎖️","Capitaine"),("🛡️","Lieutenant"),("🔰","Shinigami Rookie")],
            "🕳️ HUECO MUNDO": [("👹","Hollow"),("👹","Arrancar"),("👑","Espada"),("🦋","Vasto Lorde")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・batailles","🗡️・zanpakuto"],"🕳️ HUECO MUNDO":["👹・hollow","👑・espada"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "dragon_ball": {
        "nom": "Dragon Ball", "couleur_base": "#FF4500",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🐉","Super Saiyan Légendaire"),("👑","Dieu de la Destruction"),("💫","Super Saiyan Blue")],
            "⚔️ GUERRIERS": [("💪","Saiyan"),("⚡","Super Saiyan"),("🥋","Guerrier Z"),("🍥","Kaiō")],
            "🌌 UNIVERS": [("🌌","Univers 7"),("🐉","Dragon Ball"),("👹","Vilain"),("🤖","Androïde")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","⚡・transformations"],"🌌 UNIVERS":["🌌・univers","🐉・dragon-ball"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "black_clover": {
        "nom": "Black Clover", "couleur_base": "#2F4F4F",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Empereur-Mage"),("🍀","Légende des Clovers"),("👹","Démon")],
            "⚔️ CHEVALIERS-MAGES": [("🍀","Chevalier-Mage"),("🎖️","Capitaine"),("🛡️","Chevalier"),("🔰","Recrue")],
            "🏰 BRIGADES": [("🐂","Taureau Noir"),("🦅","Aigle d'Or"),("🦁","Lion Écarlate"),("🌹","Rose Bleue")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","📖・grimoires"],"🏰 BRIGADES":["🐂・taureau-noir","🦅・aigle-or"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "jojo": {
        "nom": "JoJo's Bizarre Adventure", "couleur_base": "#8B008B",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🌟","Stand Légendaire"),("👑","Famille Joestar"),("🩸","Vampire")],
            "👤 STANDS": [("👊","Star Platinum"),("🌍","The World"),("🔥","Magician's Red"),("💎","Crazy Diamond")],
            "🏛️ FAMILLE JOESTAR": [("👑","Joestar"),("⚔️","Hamon"),("🩸","Vampire"),("🌀","Spin")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","🌟・stands"],"🏛️ FAMILLE":["👑・joestar","🩸・vampires"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "chainsaw_man": {
        "nom": "Chainsaw Man", "couleur_base": "#B22222",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🪚","Chainsaw Man"),("👹","Démon Primordial"),("🩸","Hybride")],
            "👹 DÉMONS": [("🪚","Démon Tronçonneuse"),("🔫","Démon Gun"),("👊","Démon"),("🩸","Hybride")],
            "🗡️ CHASSEURS": [("🗡️","Chasseur de Démons"),("🎯","Chasseur d'élite"),("🛡️","Chasseur"),("🔰","Recrue")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ CHASSE":["⚔️・missions","👹・démons"],"🩸 SPÉCIALISATIONS":["🪚・chainsaw","🔫・gun"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "one_punch_man": {
        "nom": "One Punch Man", "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👊","Saitama Class"),("👑","Classe S"),("😈","Menace Dieu")],
            "🦸 HÉROS": [("🦸","Héros"),("⭐","Classe S"),("🎖️","Classe A"),("🛡️","Classe B"),("🔰","Classe C")],
            "😈 MENACES": [("😈","Monstre"),("🐉","Menace Dragon"),("👹","Menace Démon"),("🐺","Menace Tigre")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","😈・monstres"],"🦸 HÉROS":["🦸・héros","⭐・classes"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "kaiju_no_8": {
        "nom": "Kaiju No. 8", "couleur_base": "#2E8B57",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Commandant Suprême"),("🦖","Kaiju Légendaire"),("🩸","Kaiju Hybride")],
            "⚔️ DÉFENSE": [("⚔️","Membre des Forces"),("🎖️","Capitaine"),("🛡️","Officier"),("🔰","Recrue")],
            "🦖 KAIJU": [("🦖","Kaiju"),("💀","Kaiju Fortifié"),("👹","Kaiju Identifié")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・missions","🦖・kaijus"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "dandadan": {
        "nom": "Dandadan", "couleur_base": "#FF69B4",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👽","Phénomène Légendaire"),("👻","Esprit Suprême"),("⚡","Pouvoir Ultime")],
            "👽 ALIENS": [("👽","Alien"),("🛸","Soucoupe"),("👑","Chef Alien")],
            "👻 ESPRITS": [("👻","Fantôme"),("😈","Yokai"),("👑","Esprit Suprême")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","👽・aliens","👻・esprits"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },

    # ═══════════════ ❤️ ROMANCE ═══════════════
    "my_dress_up_darling": {
        "nom": "My Dress-Up Darling", "couleur_base": "#FF69B4",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🎭","Légende du Cosplay"),("👑","Reine des Créations"),("🧵","Maître Couturier Suprême")],
            "👑 HAUTS GRADÉS": [("🎭","Maître Cosplayeur"),("👗","Créateur de mode"),("📸","Photographe officiel"),("🧵","Maître couturier")],
            "🎭 COSPLAY & MODE": [("🎭","Cosplay"),("👗","Mode"),("🧵","Couture"),("💄","Maquillage")],
            "📸 PHOTOGRAPHIE": [("📸","Photographe"),("📷","Shooting"),("💡","Direction artistique")],
            "💕 ROMANCE": [("💕","Romance"),("💌","Relations"),("🌸","Moments")],
            "🏷️ COMMUNAUTÉ": [("🎨","Créateur"),("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"📸 COSPLAY":["🎭・cosplay","👗・créations"],"🎬 SHOOTING":["🎬・shooting","📷・photos"],"💬 UNIVERS":["💬・discussion"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Cosplay","Détente"],
    },
    "darling_in_the_franxx": {
        "nom": "Darling in the Franxx", "couleur_base": "#FF69B4",
        "groupes_roles": {
            "🩷 02": [("🩷","02")],
            "🌟 LÉGENDES": [("🩷","Légende du Franxx"),("👑","Reine des Plantations"),("🤖","Maître Pilote Suprême")],
            "🤖 FRANXX": [("🤖","Pilote d'élite"),("⚔️","Commandant de squad"),("🚀","Stamen d'élite")],
            "🚀 PILOTAGE": [("🤖","Pilote Franxx"),("🚀","Stamen"),("🩸","Pistil"),("💉","Médecin")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🤖 FRANXX":["🤖・franxx","⚔️・missions"],"🌌 UNIVERS":["🌌・plantation","📚・lore"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "masamune_kun_revenge": {
        "nom": "Masamune-kun's Revenge", "couleur_base": "#4169E1",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Roi de la Vengeance"),("💼","Maître des Stratagèmes"),("🎯","Légende du Lycée")],
            "👑 HAUTS GRADÉS": [("💼","Maître stratège"),("🎯","Maître vengeur"),("💕","Idole de la romance")],
            "🎓 LYCÉE": [("🎓","Étudiant"),("🎀","Mode"),("🎭","Comédien"),("🎨","Créatif")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏫 LYCÉE":["🎓・lycée","📚・études"],"💕 ROMANCE":["💕・relations"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Détente","Musique"],
    },
    "a_couple_of_cuckoos": {
        "nom": "A Couple of Cuckoos", "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende de la Famille"),("💍","Fiancé(e) Suprême"),("🎯","Maître des Objectifs")],
            "👑 HAUTS GRADÉS": [("💍","Fiancé(e) officiel(le)"),("💕","Idole de la romance"),("🎓","Major de promo"),("🏠","Pilier de la famille")],
            "🏠 VIE QUOTIDIENNE": [("📚","Studieux"),("🎭","Comédie"),("🎨","Créatif"),("📸","Photographe")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏠 VIE QUOTIDIENNE":["🏠・maison","📚・études"],"💕 ROMANCE":["💕・relations"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Détente","Musique"],
    },
    "tonikaku_kawaii": {
        "nom": "Tonikaku Kawaii", "couleur_base": "#FFB6C1",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende du Couple"),("💍","Marié(e) Suprême"),("🌸","Gardien de l'Amour Éternel")],
            "👑 HAUTS GRADÉS": [("💍","Marié(e) fondateur(trice)"),("💕","Couple modèle"),("🌸","Idole de la romance"),("🍳","Chef cuisinier")],
            "🏠 VIE QUOTIDIENNE": [("🏠","Vie commune"),("📖","Lecture"),("🎵","Musique"),("🎓","Étudiant")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"💍 MARIAGE":["💍・mariage","🎉・préparatifs"],"🏠 VIE QUOTIDIENNE":["🏠・vie"],"💕 ROMANCE":["💕・couple"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","Couple/RP","Détente","Musique"],
    },
    "a_silent_voice": {
        "nom": "A Silent Voice", "couleur_base": "#87CEEB",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende du Pardon"),("💙","Maître de la Rédemption"),("🌊","Gardien de l'Amitié")],
            "👑 HAUTS GRADÉS": [("💙","Maître de la rédemption"),("🌊","Ambassadeur du pardon"),("🎨","Artiste d'élite"),("🤝","Pilier de l'amitié")],
            "🎨 CRÉATION": [("📚","Lecture"),("💕","Romance"),("🎵","Musique"),("📸","Photographie")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏫 VIE SCOLAIRE":["🎓・cours","📸・souvenirs"],"🎨 CRÉATION":["🎨・art","🎵・musique"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Art","Musique"],
    },
    "i_want_to_eat_your_pancreas": {
        "nom": "I Want to Eat Your Pancreas", "couleur_base": "#FFB347",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende du Printemps"),("🌸","Gardien des Souvenirs"),("📖","Maître Conteur Suprême")],
            "👑 HAUTS GRADÉS": [("🌸","Idole de la romance"),("📖","Maître conteur"),("☕","Hôte du café"),("💕","Confident d'élite")],
            "🎬 CULTURE": [("🎬","Cinéma"),("🎵","Musique"),("📸","Photographie"),("🎨","Créatif")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"📚 LYCÉE":["🎓・études","📖・bibliothèque"],"🌸 MOMENTS":["🌟・souvenirs","✈️・voyages"],"🎵 CULTURE":["🎵・musique","🎬・cinéma"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","Musique","RP","Lecture"],
    },
    "horimiya": {
        "nom": "Horimiya", "couleur_base": "#FFA07A",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Idole Légendaire"),("💼","Maître du Travail"),("🎨","Légende Créative")],
            "👑 HAUTS GRADÉS": [("👑","Idole du lycée"),("💼","Maître travailleur"),("🎨","Maître créatif"),("💕","Idole de la romance")],
            "🏫 LYCÉE": [("🎓","Lycéen(ne)"),("📚","Studieux"),("🏠","Famille"),("📸","Photographe")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏫 LYCÉE":["🎓・lycée","📚・études"],"💕 ROMANCE":["💕・romance"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Détente","Musique"],
    },
    "kaguya_sama": {
        "nom": "Kaguya-sama: Love is War", "couleur_base": "#C8102E",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Empereur du Conseil"),("🎯","Maître Suprême des Stratagèmes"),("💰","Légende du Trésor")],
            "👑 HAUTS GRADÉS": [("👑","Président du conseil"),("🏛️","Vice-président"),("📋","Secrétaire en chef"),("🎯","Maître stratège")],
            "🏫 CONSEIL": [("💕","Romance"),("🎭","Comédie"),("🎓","Étudiant"),("📚","Studieux")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏫 CONSEIL":["🏛️・conseil","🎯・stratégie"],"💕 ROMANCE":["💕・romance"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Conseil","Musique"],
    },
    "rent_a_girlfriend": {
        "nom": "Rent-a-Girlfriend", "couleur_base": "#FF69B4",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende de la Romance"),("💕","Idole Suprême"),("🎬","Maître Réalisateur")],
            "👑 HAUTS GRADÉS": [("💕","Idole de la romance"),("🎬","Réalisateur"),("🎭","Maître comédien"),("🎨","Maître créatif")],
            "💕 HISTOIRE": [("🎓","Étudiant"),("💼","Travailleur"),("📸","Photographe"),("🏠","Famille")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"💕 HISTOIRE":["💕・histoire","📖・manga"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Détente","Musique"],
    },
    "fruits_basket": {
        "nom": "Fruits Basket", "couleur_base": "#FFB6C1",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Légende du Zodiaque"),("🌸","Gardien de la Famille"),("💕","Idole Suprême du Cœur")],
            "👑 HAUTS GRADÉS": [("🌸","Gardien du zodiaque"),("🏠","Pilier de la famille"),("💕","Idole de la romance"),("🍰","Maître pâtissier")],
            "🌸 HISTOIRE": [("📚","Lecture"),("🎵","Musique"),("🌟","Moments"),("🎓","Étudiant")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🌸 HISTOIRE":["🌸・histoire","🏠・famille"],"💕 ROMANCE":["💕・romance"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Détente","Musique"],
    },
    "toradora": {
        "nom": "Toradora!", "couleur_base": "#FF6347",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Reine du Lycée"),("🎄","Légende de Noël"),("💕","Idole Romantique Suprême")],
            "👑 HAUTS GRADÉS": [("👑","Idole du lycée"),("🌸","Idole de la romance"),("💕","Maître confident"),("🎭","Maître comédien")],
            "🏫 LYCÉE": [("🎓","Étudiant"),("😤","Tsundere"),("🏠","Famille"),("🎵","Musique")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏫 LYCÉE":["🎓・lycée","🌸・moments"],"💕 ROMANCE":["💕・romance"],"🎭 RP":["💬・rp"],"💬 COMMUNAUTÉ":["💬・général"]},
        "vocaux": ["Discussion","RP","Détente","Musique"],
    },
    "oni_no_hanayome": {
        "nom": "Oni no Hanayome", "couleur_base": "#8B0000",
        "groupes_roles": {
            "👹 AYAKASHI": [("👹","Ayakashi"),("🦊","Youkai"),("🌸","Esprit"),("✨","Pouvoir surnaturel")],
            "💍 MARIAGE": [("💍","Mariage"),("💐","Mariée"),("❤️","Lien d'âme"),("🌸","Destin")],
            "🏯 FAMILLES": [("🏯","Famille Kiryuuin"),("🏠","Famille Shinonome"),("👑","Famille Ayakashi")],
            "🌸 UNIVERS": [("🌸","Monde des Ayakashi"),("🎎","Tradition"),("🏮","Japon"),("✨","Coexistence")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"💍 MARIAGE":["💍・mariage","🌸・destin"],"👹 AYAKASHI":["👹・ayakashi","🦊・youkai"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Détente"],
    },
    "maboroshi": {
        "nom": "Maboroshi", "couleur_base": "#FFB6C1",
        "groupes_roles": {
            "🌸 MABOROSHI": [("🌸","Gardien du Temps"),("✨","Phénomène"),("🎭","Étrange"),("💭","Souvenir")],
            "👑 LÉGENDES": [("👑","Légende de Maboroshi"),("🌟","Maître des Illusions"),("🕰️","Seigneur du Temps")],
            "🏫 LYCÉE": [("🎓","Lycéen(ne)"),("📚","Étudiant"),("🎭","Comité"),("📸","Photographe")],
            "💕 ROMANCE": [("💕","Romance"),("💌","Relations"),("🌸","Moments"),("❤️","Couple")],
            "🌌 MYSTÈRE": [("🌌","Mystère"),("🔮","Prophétie"),("💭","Rêve"),("🎭","Symbolique")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🌸 MABOROSHI":["🌸・maboroshi","✨・phénomènes"],"🏫 LYCÉE":["🎓・lycée","📚・études"],"💕 ROMANCE":["💕・romance","💌・relations"],"🌌 MYSTÈRE":["🌌・mystère","🔮・prophétie"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Détente","Romance"],
    },

    # ═══════════════ 🏀 SPORT ═══════════════
    "blue_lock": {
        "nom": "Blue Lock", "couleur_base": "#1E90FF",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Meilleur Attaquant"),("⚽","Roi du Blue Lock")],
            "⚽ ATTAQUANTS": [("⚽","Attaquant"),("🎯","Buteur"),("🔥","Ailier"),("🥅","Avant-centre")],
            "🏟️ BLUE LOCK": [("👑","Équipe Z"),("⚔️","Équipe V"),("⚡","Équipe X"),("🏆","Équipe Top 11")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚽ FOOTBALL":["⚽・matchs","🎯・entraînement"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Matchs","Détente"],
    },
    "haikyuu": {
        "nom": "Haikyuu!!", "couleur_base": "#FF6347",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Meilleur Joueur"),("🏐","Légende du Volley")],
            "🏐 ÉQUIPES": [("🏐","Karasuno"),("🏐","Nekoma"),("🏐","Aoba Jōsai"),("🏐","Shiratorizawa")],
            "🏟️ POSTES": [("🎯","Attaquant"),("🛡️","Libero"),("🎩","Passeur"),("🚧","Central")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏐 VOLLEY":["🏐・matchs","🎯・entraînement"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Matchs","Détente"],
    },
    "kuroko_no_basket": {
        "nom": "Kuroko no Basket", "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Génération des Miracles"),("🏀","Légende du Basket")],
            "🏀 ÉQUIPES": [("🏀","Seirin"),("🏀","Kaijō"),("🏀","Shūtoku"),("🏀","Tōō")],
            "🏟️ POSTES": [("🎯","Meneur"),("🛡️","Ailier"),("🔥","Pivot"),("🎩","Arrière")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏀 BASKET":["🏀・matchs","🎯・entraînement"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Matchs","Détente"],
    },
    "hajime_no_ippo": {
        "nom": "Hajime no Ippo", "couleur_base": "#B22222",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Champion du Monde"),("🥊","Légende de la Boxe")],
            "🥊 BOXEURS": [("🥊","Boxeur"),("🎯","Poids Plume"),("🔥","Poids Lourd"),("🏆","Champion")],
            "🏟️ SALLES": [("🏟️","Kamogawa"),("🏟️","Ōta"),("🏟️","Champion")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🥊 BOXE":["🥊・combats","🎯・entraînement"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combats","Détente"],
    },
    "initial_d": {
        "nom": "Initial D", "couleur_base": "#2F4F4F",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🏎️","Roi du Col"),("👑","Légende du Racing")],
            "🏎️ PILOTES": [("🏎️","Pilote"),("🎯","Drifteur"),("🔥","Racer"),("🔰","Débutant")],
            "🏔️ ÉQUIPES": [("🏔️","Project D"),("🏔️","RedSuns"),("🏔️","Akina Speed Stars")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🏎️ RACING":["🏎️・courses","🎯・drift"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Courses","Détente"],
    },

    # ═══════════════ 🧠 PSYCHOLOGIQUE ═══════════════
    "death_note": {
        "nom": "Death Note", "couleur_base": "#2F4F4F",
        "groupes_roles": {
            "🌟 LÉGENDES": [("📓","Détenteur du Death Note"),("🕵️","Détective L")],
            "🕵️ ENQUÊTE": [("🕵️","Détective"),("📁","Enquêteur"),("🔎","Investigateur"),("🔰","Recrue")],
            "📓 KIRA": [("📓","Kira"),("🎭","Disciple de Kira"),("👑","Shinigami")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔎 ENQUÊTE":["🔎・enquête","🕵️・investigation"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Enquête","Détente"],
    },
    "code_geass": {
        "nom": "Code Geass", "couleur_base": "#8B008B",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Empereur"),("⚡","Geass Ultime"),("🎭","Zero")],
            "⚔️ CHEVALIERS": [("⚔️","Chevalier du Saint-Graal"),("🎖️","Chevalier"),("🛡️","Pilote Knightmare")],
            "🏴 ORDRES": [("🏴","Black Knights"),("⚔️","Britannia"),("⚖️","Gouvernement")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・batailles","🎭・geass"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "steins_gate": {
        "nom": "Steins;Gate", "couleur_base": "#4682B4",
        "groupes_roles": {
            "🌟 LÉGENDES": [("⏰","Voyageur Temporel"),("🧠","Génie Scientifique")],
            "🔬 LABO": [("🔬","Chercheur"),("🧪","Scientifique"),("⚙️","Ingénieur"),("🔰","Membre du Labo")],
            "⏰ VOYAGE": [("⏰","Voyage Temporel"),("📡","SERN"),("🎭","Espion")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔬 SCIENCE":["🔬・recherche","⏰・voyage-temporel"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Science","Détente"],
    },
    "psycho_pass": {
        "nom": "Psycho-Pass", "couleur_base": "#2F4F4F",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Chef du Bureau"),("🧠","Criminel Latent")],
            "🕵️ BUREAU": [("🕵️","Inspecteur"),("🎯","Exécuteur"),("📡","Analyste"),("🔰","Recrue")],
            "⚖️ SYSTÈME": [("⚖️","Sibyl"),("🔫","Dominator"),("🧠","Psycho-Pass")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔎 ENQUÊTE":["🔎・enquête","⚖️・sibyl"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Enquête","Détente"],
    },
    "classroom_of_elite": {
        "nom": "Classroom of the Elite", "couleur_base": "#8B0000",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🧠","Stratège Suprême"),("🎭","Manipulateur")],
            "🏫 CLASSES": [("👑","Classe A"),("⚔️","Classe B"),("🛡️","Classe C"),("🔰","Classe D")],
            "⚔️ CONFLITS": [("⚔️","Conflit"),("🎯","Stratégie"),("📊","Points")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🧠 STRATÉGIE":["🧠・stratégies","📊・classement"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Stratégie","Détente"],
    },

    # ═══════════════ 👻 HORREUR ═══════════════
    "another": {
        "nom": "Another", "couleur_base": "#8B0000",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👁️","Œil du Destin"),("🎭","Personne de l'Année")],
            "🎭 CLASSE": [("🎭","Élève"),("🎓","Professeur"),("👁️","Élève Fictif"),("🔰","Recrue")],
            "💀 MALÉDICTION": [("💀","Malédiction"),("👁️","Mort"),("🎭","Coupable")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"💀 MALÉDICTION":["💀・morts","👁️・énigme"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Horreur","Détente"],
    },
    "tokyo_ghoul": {
        "nom": "Tokyo Ghoul", "couleur_base": "#8B0000",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Roi des Goules"),("🩸","SSS"),("🎭","One-Eyed Ghoul")],
            "👁️ GOULES": [("👁️","Goule"),("⚔️","Combattant"),("🎯","Chasseur"),("🔰","Recrue")],
            "⚔️ CCG": [("⚔️","Enquêteur CCG"),("🎖️","Enquêteur Spécial"),("🛡️","Enquêteur Associé")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","👁️・goules"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "parasyte": {
        "nom": "Parasyte", "couleur_base": "#2E8B57",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👽","Parasite Suprême"),("🎭","Hôte Ultime")],
            "👽 PARASITES": [("👽","Parasite"),("👁️","Hôte"),("🩸","Chasseur"),("🔰","Recrue")],
            "🧠 HÔTES": [("🧠","Hôte Conscient"),("🩸","Combattant"),("🎯","Traqueur")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","👽・parasites"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "highschool_of_the_dead": {
        "nom": "Highschool of the Dead", "couleur_base": "#556B2F",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🧟","Survivant Légendaire"),("👑","Chef")],
            "🧟 SURVIVANTS": [("🧟","Survivant"),("🛡️","Défenseur"),("🎯","Éclaireur"),("🔰","Recrue")],
            "🎒 LYCÉE": [("🎒","Lycéen"),("🎓","Professeur"),("🛡️","Garde")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🧟 ZOMBIES":["🧟・zombies","⚔️・combats"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },

    # ═══════════════ ✨ FANTASY / ISEKAI ═══════════════
    "re_zero": {
        "nom": "Re:Zero", "couleur_base": "#4169E1",
        "groupes_roles": {
            "🌟 LÉGENDES": [("⏳","Boucle Temporelle"),("👑","Roi Dragon")],
            "🏰 ROYAUME": [("👑","Chevalier Royal"),("🎖️","Chevalier"),("🛡️","Garde"),("🔰","Recrue")],
            "🎭 SORCIERS": [("✨","Sorcier"),("❄️","Esprit"),("🔥","Magicien"),("🌙","Démon")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⏳ BOUCLE":["⏳・revival","🎭・routes"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Aventure","Détente"],
    },
    "overlord": {
        "nom": "Overlord", "couleur_base": "#4B0082",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Roi Sorcier"),("💀","Seigneur Suprême")],
            "👑 NAZARICK": [("👑","Gardien de Niveau"),("🎖️","Commandant"),("🛡️","Garde"),("🔰","Recrue")],
            "💀 MORTS-VIVANTS": [("💀","Mort-vivant"),("👑","Seigneur"),("🩸","Nécromancien")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"👑 NAZARICK":["👑・nazarick","⚔️・gardes"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Aventure","Détente"],
    },
    "konosuba": {
        "nom": "KonoSuba", "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Roi Démon"),("⚔️","Héros")],
            "🛡️ AVENTURIERS": [("🛡️","Aventurier"),("⚔️","Combattant"),("✨","Mage"),("🔰","Recrue")],
            "🏰 GUILDE": [("🏰","Guilde"),("👑","Chef de Guilde"),("💰","Marchand")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ AVENTURE":["⚔️・quêtes","🎯・monstres"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Aventure","Détente"],
    },
    "frieren": {
        "nom": "Frieren", "couleur_base": "#9370DB",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🧝","Mage Légendaire"),("⚔️","Héros")],
            "🧝 MAGES": [("🧝","Elfe"),("✨","Mage"),("⚔️","Guerrier"),("🔰","Recrue")],
            "🏰 ROYAUMES": [("👑","Royaume"),("🛡️","Garde"),("💰","Marchand")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"✨ MAGIE":["✨・magie","⚔️・combats"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Aventure","Détente"],
    },
    "no_game_no_life": {
        "nom": "No Game No Life", "couleur_base": "#FF1493",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Roi"),("🎲","Maître des Jeux")],
            "🎲 JOUEURS": [("🎲","Joueur"),("🧠","Stratège"),("🎯","As"),("🔰","Recrue")],
            "🏰 ROYAUMES": [("👑","Royaume"),("🎯","Défi"),("⚖️","Serment")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🎲 JEU":["🎲・parties","🧠・stratégies"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Jeu","Détente"],
    },

    # ═══════════════ 🚀 SCI-FI ═══════════════
    "cowboy_bebop": {
        "nom": "Cowboy Bebop", "couleur_base": "#FF4500",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🎯","Chasseur Légendaire"),("🚀","Capitaine")],
            "🚀 CHASSEURS": [("🚀","Chasseur de Primes"),("🎯","Tireur"),("🛡️","Pilote"),("🔰","Recrue")],
            "🌌 ESPACE": [("🌌","Space Cowboy"),("🚀","Vaisseau"),("🎯","Mission")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🚀 AVENTURE":["🚀・missions","🎯・combats"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Aventure","Détente"],
    },
    "gundam": {
        "nom": "Mobile Suit Gundam", "couleur_base": "#1E90FF",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🤖","Pilote Légendaire"),("👑","Commandant Suprême")],
            "🤖 PILOTES": [("🤖","Pilote Gundam"),("⚔️","Pilote"),("🛡️","Défenseur"),("🔰","Recrue")],
            "🌌 FÉDÉRATIONS": [("🌌","Fédération Terrienne"),("⚔️","Zeon"),("👑","Commandement")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・batailles","🤖・gundams"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "nier_automata": {
        "nom": "Nier:Automata Ver1.1a", "couleur_base": "#696969",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🤖","Androïde Légendaire"),("👑","Commandant")],
            "🤖 ANDROÏDES": [("🤖","Androïde"),("⚔️","Combattant"),("🛡️","Défenseur"),("🔰","Recrue")],
            "🌍 YORHA": [("🌍","YoRHa"),("🤖","Machine"),("⚔️","Unités")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"⚔️ COMBAT":["⚔️・combats","🤖・machines"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },

    # ═══════════════ 🎭 TRANCHES DE VIE ═══════════════
    "barakamon": {
        "nom": "Barakamon", "couleur_base": "#87CEEB",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🖌️","Calligraphe Légendaire")],
            "🖌️ ARTISTES": [("🖌️","Calligraphe"),("🎨","Artiste"),("📚","Écrivain"),("🔰","Recrue")],
            "🏝️ VILLAGE": [("🏝️","Villageois"),("🧑‍🌾","Agriculteur"),("🎣","Pêcheur")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🖌️ ART":["🖌️・calligraphie","🎨・art"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Détente"],
    },
    "hyouka": {
        "nom": "Hyouka", "couleur_base": "#9370DB",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🕵️","Détective Légendaire"),("🧠","Génie")],
            "🕵️ ENQUÊTE": [("🕵️","Détective"),("🔎","Enquêteur"),("📁","Enquête"),("🔰","Recrue")],
            "🏫 LYCÉE": [("🎓","Élève"),("📚","Étudiant"),("🎭","Club")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔎 ENQUÊTE":["🔎・enquête","📁・mystère"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Détente"],
    },
    "bocchi_the_rock": {
        "nom": "Bocchi the Rock!", "couleur_base": "#FF69B4",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🎸","Guitariste Légendaire"),("🎤","Chanteuse")],
            "🎸 MUSIQUE": [("🎸","Guitariste"),("🥁","Batteur"),("🎹","Clavier"),("🔰","Recrue")],
            "🏫 LYCÉE": [("🎓","Élève"),("🎭","Club"),("📚","Étudiant")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🎸 MUSIQUE":["🎸・musique","🎤・concerts"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Musique","Détente"],
    },

    # ═══════════════ 🎵 MUSIQUE ═══════════════
    "euphonium": {
        "nom": "Sound! Euphonium", "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🎺","Soliste Légendaire"),("🏆","Champion")],
            "🎺 FANFARE": [("🎺","Trompettiste"),("🎷","Saxophoniste"),("🥁","Percussionniste"),("🔰","Recrue")],
            "🏫 LYCÉE": [("🎓","Élève"),("🎭","Club"),("📚","Étudiant")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🎺 MUSIQUE":["🎺・fanfare","🏆・concours"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Musique","Détente"],
    },
    "given": {
        "nom": "Given", "couleur_base": "#9370DB",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🎸","Guitariste Légendaire"),("🎤","Chanteur")],
            "🎸 MUSIQUE": [("🎸","Guitariste"),("🥁","Batteur"),("🎹","Bassiste"),("🔰","Recrue")],
            "🎭 BAND": [("🎭","Groupe"),("🎤","Vocal"),("🎼","Composition")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🎸 MUSIQUE":["🎸・musique","🎤・concerts"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Musique","Détente"],
    },

    # ═══════════════ 🎮 JEUX / COMPÉTITION ═══════════════
    "kakegurui": {
        "nom": "Kakegurui", "couleur_base": "#DC143C",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Président du Conseil"),("🎲","Joueuse Légendaire")],
            "🎲 JOUEURS": [("🎲","Joueur"),("🧠","Stratège"),("🃏","Tricheur"),("🔰","Recrue")],
            "🏫 ACADÉMIE": [("🏫","Hyakkaou"),("👑","Conseil"),("💰","Dette")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🎲 JEU":["🎲・parties","🧠・stratégies"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Jeu","Détente"],
    },
    "kings_avatar": {
        "nom": "The King's Avatar", "couleur_base": "#4169E1",
        "groupes_roles": {
            "🌟 LÉGENDES": [("👑","Roi de la Gloire"),("🏆","Champion")],
            "🎮 JOUEURS": [("🎮","Joueur Pro"),("⚔️","Combattant"),("🧠","Stratège"),("🔰","Recrue")],
            "🏆 ÉQUIPES": [("🏆","Team Excellent Era"),("⚔️","Team Blue Rain"),("🎯","Team Samsara")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🎮 JEU":["🎮・compétitions","🏆・tournois"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Compétition","Détente"],
    },

    # ═══════════════ 🔎 MYSTÈRE ═══════════════
    "detective_conan": {
        "nom": "Detective Conan", "couleur_base": "#191970",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🕵️","Détective Légendaire"),("👑","Kaito Kid")],
            "🕵️ ENQUÊTE": [("🕵️","Détective"),("🔎","Enquêteur"),("📁","Enquête"),("🔰","Recrue")],
            "🔫 ORGANISATION": [("🔫","Organisation"),("👑","Chef"),("🎭","Espion")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔎 ENQUÊTE":["🔎・enquête","📁・dossiers"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Enquête","Détente"],
    },
    "gosick": {
        "nom": "Gosick", "couleur_base": "#8B008B",
        "groupes_roles": {
            "🌟 LÉGENDES": [("🕵️","Détective Légendaire"),("📚","Génie")],
            "🕵️ ENQUÊTE": [("🕵️","Détective"),("🔎","Enquêteur"),("📁","Enquête"),("🔰","Recrue")],
            "🏫 ACADÉMIE": [("🏫","Académie"),("📚","Bibliothèque"),("👑","Noblesse")],
            "🏷️ COMMUNAUTÉ": [("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue")],
        },
        "categories": {"📌 INFORMATIONS":["📜・règlement","📢・annonces"],"🔎 ENQUÊTE":["🔎・enquête","📁・mystère"],"🎭 RP":["💬・rp"]},
        "vocaux": ["Discussion","RP","Enquête","Détente"],
    },

    # ═══════════════ 📚 MANGA / MANHWA ═══════════════
    "pumpkin_night": {
        "nom": "Pumpkin Night", "couleur_base": "#FF8C00",
        "groupes_roles": {
            "🎃 HORREUR": [
                ("🎃","Pumpkin Night"),("🔪","Tueur"),("🩸","Massacre"),
                ("💀","Victime"),("👹","Monstre"),
            ],
            "🏥 VICTIMES": [
                ("🏥","Patient"),("🩸","Blessé"),("💀","Décédé"),
                ("🩹","Survivant"),("🔰","Recrue"),
            ],
            "🌃 VILLE": [
                ("🌃","Habitant"),("👮","Police"),("🏥","Hôpital"),
                ("🏫","Lycée"),("🏚️","Zone abandonnée"),
            ],
            "🩸 SURVIVANTS": [
                ("🩸","Survivant"),("🛡️","Défenseur"),("🎯","Chasseur"),
                ("🔥","Combattant"),("🔰","Recrue"),
            ],
            "🏷️ COMMUNAUTÉ": [
                ("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue"),
            ],
        },
        "categories": {
            "📌 INFORMATIONS": ["📜・règlement","📢・annonces"],
            "🎃 HORREUR": ["🎃・pumpkin-night","🩸・massacres","💀・morts"],
            "🌃 VILLE": ["🌃・ville","🏥・hôpital","🏫・lycée"],
            "🩸 SURVIVANTS": ["🩸・survivants","🛡️・défense"],
            "🎭 RP": ["💬・rp","🎭・personnages-rp"],
        },
        "vocaux": ["Discussion","RP","Horreur","Détente"],
    },
    "legendary_hero_academy": {
        "nom": "The Legendary Hero is an Academy Honors Student",
        "couleur_base": "#FFD700",
        "groupes_roles": {
            "🌟 LÉGENDES": [
                ("👑","Héros Légendaire"),("🏆","Élu"),
                ("⚔️","Champion"),("✨","Béni des dieux"),
                ("🌟","Légende Vivante"),
            ],
            "🏫 ACADÉMIE": [
                ("🏫","Étudiant d'honneur"),("🎓","Élève"),
                ("📚","Professeur"),("🏛️","Directeur"),
                ("🔰","Recrue"),
            ],
            "⚔️ COMBAT": [
                ("⚔️","Combattant"),("🔥","Mage"),
                ("🛡️","Défenseur"),("🎯","Tireur"),
                ("🗡️","Épéiste"),
            ],
            "✨ MAGIE": [
                ("✨","Magie"),("🔮","Sort"),
                ("⚡","Élémentaire"),("🌌","Arcane"),
                ("🧪","Alchimie"),
            ],
            "🏷️ COMMUNAUTÉ": [
                ("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue"),
            ],
        },
        "categories": {
            "📌 INFORMATIONS": ["📜・règlement","📢・annonces"],
            "🏫 ACADÉMIE": ["🏫・académie","🎓・cours","📚・études"],
            "⚔️ COMBAT": ["⚔️・combats","🔥・magie"],
            "✨ MAGIE": ["✨・magie","🔮・sorts"],
            "🎭 RP": ["💬・rp","🎭・personnages-rp"],
        },
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "lookism": {
        "nom": "Lookism", "couleur_base": "#FF1493",
        "groupes_roles": {
            "🥊 GANGS": [
                ("👑","Roi du Lycée"),("💪","Boss"),
                ("🥊","Membre de Gang"),("⚔️","Combattant"),
                ("🛡️","Garde"),("🔰","Recrue"),
            ],
            "🏫 LYCÉE": [
                ("🎓","Élève"),("📚","Étudiant"),
                ("🎭","Comité"),("🎨","Artiste"),
                ("⭐","Populaire"),
            ],
            "💼 ENTREPRISES": [
                ("💼","Homme d'affaires"),("💰","Marchand"),
                ("📊","Gestionnaire"),("🏢","PDG"),
                ("🤝","Partenaire"),
            ],
            "🥊 COMBAT": [
                ("🥊","Boxeur"),("⚔️","Combattant"),
                ("🥋","Arts martiaux"),("🛡️","Défenseur"),
                ("🔥","Bagarreur"),
            ],
            "🏷️ COMMUNAUTÉ": [
                ("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue"),
            ],
        },
        "categories": {
            "📌 INFORMATIONS": ["📜・règlement","📢・annonces"],
            "🥊 GANGS": ["🥊・gangs","⚔️・combats"],
            "🏫 LYCÉE": ["🎓・lycée","📚・études"],
            "💼 ENTREPRISES": ["💼・entreprises","💰・business"],
            "🎭 RP": ["💬・rp","🎭・personnages-rp"],
        },
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "solo_leveling": {
        "nom": "Solo Leveling", "couleur_base": "#1E90FF",
        "groupes_roles": {
            "🌟 LÉGENDES": [
                ("👑","Monarque des Ombres"),("🐉","Monarque"),
                ("⚔️","Chasseur S"),("💀","Roi des Morts"),
                ("🌌","Souverain"),
            ],
            "⚔️ CHASSEURS": [
                ("⚔️","Chasseur S"),("⚔️","Chasseur A"),
                ("🛡️","Chasseur B"),("🎯","Chasseur C"),
                ("🔰","Chasseur E"),
            ],
            "🌑 OMBRES": [
                ("🌑","Ombre"),("👑","Maréchal d'Ombres"),
                ("⚔️","Chevalier d'Ombre"),("🐜","Soldat d'Ombre"),
                ("🐉","Dragon d'Ombre"),
            ],
            "🏢 GUILDES": [
                ("🏢","Guilde"),("👑","Maître de Guilde"),
                ("🎯","Chasseur d'élite"),("🛡️","Chasseur"),
                ("🔰","Recrue"),
            ],
            "🏷️ COMMUNAUTÉ": [
                ("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue"),
            ],
        },
        "categories": {
            "📌 INFORMATIONS": ["📜・règlement","📢・annonces"],
            "⚔️ COMBAT": ["⚔️・donjons","🌑・ombres"],
            "🏢 GUILDES": ["🏢・guildes","🎯・missions"],
            "🎭 RP": ["💬・rp","🎭・personnages-rp"],
        },
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
    "star_embracing_swordmaster": {
        "nom": "Star-Embracing Swordmaster", "couleur_base": "#4169E1",
        "groupes_roles": {
            "🌟 LÉGENDES": [
                ("👑","Maître Épéiste Légendaire"),("⭐","Élu des Étoiles"),
                ("⚔️","Champion"),("✨","Béni par les Astres"),
                ("🌌","Seigneur des Lames"),
            ],
            "🗡️ ÉPÉISTES": [
                ("🗡️","Épéiste"),("⚔️","Maître d'armes"),
                ("🛡️","Chevalier"),("🎯","Duelliste"),
                ("🔰","Recrue"),
            ],
            "⭐ ÉTOILES": [
                ("⭐","Étoile"),("✨","Bénédiction"),
                ("🌌","Constellation"),("💫","Destin"),
                ("🔮","Prophétie"),
            ],
            "🏰 ROYAUMES": [
                ("👑","Royaume"),("🏛️","Académie"),
                ("🛡️","Garde royale"),("⚔️","Armée"),
                ("📚","Bibliothèque"),
            ],
            "🏷️ COMMUNAUTÉ": [
                ("⭐","Membre actif"),("👊","Membre"),("🔰","Recrue"),
            ],
        },
        "categories": {
            "📌 INFORMATIONS": ["📜・règlement","📢・annonces"],
            "🗡️ COMBAT": ["🗡️・combats","⚔️・duels"],
            "⭐ ÉTOILES": ["⭐・étoiles","✨・bénédiction"],
            "🏰 ROYAUMES": ["🏰・royaume","🏛️・académie"],
            "🎭 RP": ["💬・rp","🎭・personnages-rp"],
        },
        "vocaux": ["Discussion","RP","Combat","Détente"],
    },
}


# ═══════════════════════════════════════════════════════
# FONCTIONS
# ═══════════════════════════════════════════════════════

def _hex_to_color(hex_str: str) -> discord.Color:
    try:
        return discord.Color(int(hex_str.lstrip("#"), 16))
    except Exception:
        return discord.Color.blurple()


async def _creer_role(guild, nom, couleur, permissions, hoist):
    try:
        ex = discord.utils.get(guild.roles, name=nom)
        if ex:
            return ex
        role = await asyncio.wait_for(
            guild.create_role(name=nom, colour=couleur, permissions=permissions,
                              mentionable=False, hoist=hoist, reason="FixyBot"),
            timeout=15.0,
        )
        log.info("  ✅ Créé : %s", nom)
        return role
    except asyncio.TimeoutError:
        log.error("  ⏱ TIMEOUT sur '%s'", nom); return None
    except discord.Forbidden:
        log.error("  ❌ FORBIDDEN sur '%s'", nom); return None
    except discord.HTTPException as e:
        log.error("  ❌ HTTP %s sur '%s' : %s", e.status, nom, e)
        if e.status == 429:
            await asyncio.sleep((getattr(e, "retry_after", 5) or 5) + 1)
        return None
    except Exception as e:
        log.exception("  ❌ Exception sur '%s' : %s", nom, e); return None


async def _creer_categorie(guild, nom):
    try:
        cat = discord.utils.get(guild.categories, name=nom)
        if cat:
            return cat
        return await asyncio.wait_for(
            guild.create_category(name=nom, reason="FixyBot"), timeout=15.0)
    except Exception as e:
        log.error("  ❌ Catégorie %s : %s", nom, e); return None


async def _creer_salon_text(guild, nom, cat):
    if not cat:
        return None
    try:
        ex = discord.utils.get(guild.text_channels, name=nom)
        if ex:
            return ex
        return await asyncio.wait_for(
            guild.create_text_channel(name=nom, category=cat, reason="FixyBot"),
            timeout=15.0)
    except Exception as e:
        log.error("  ❌ Salon %s : %s", nom, e); return None


async def _creer_salon_vocal(guild, nom, cat):
    if not cat:
        return None
    try:
        ex = discord.utils.get(guild.voice_channels, name=nom)
        if ex:
            return ex
        return await asyncio.wait_for(
            guild.create_voice_channel(name=nom, category=cat, reason="FixyBot"),
            timeout=15.0)
    except Exception as e:
        log.error("  ❌ Vocal %s : %s", nom, e); return None


async def generate_anime(guild: discord.Guild, universe_key: str):
    cfg = ANIMES.get(universe_key)
    if not cfg:
        log.warning("Anime inconnu : %s", universe_key)
        return False

    log.info("[ANIME] Début : %s", cfg["nom"])

    me = guild.me
    if not me or not me.guild_permissions.manage_roles:
        log.error("❌ Permission manage_roles manquante"); return False

    for groupe, liste in cfg["groupes_roles"].items():
        sep_nom = f"━━━━━━━━━━ {groupe} ━━━━━━━━━━"
        await _creer_role(guild, sep_nom, discord.Color.darker_grey(),
                           discord.Permissions.none(), False)
        for emoji, nom_role in liste:
            if len(guild.roles) >= 240:
                break
            couleur = couleur_par_importance(nom_role, cfg["couleur_base"])
            perms = perms_for_rank(nom_role)
            await _creer_role(guild, f"{emoji} {nom_role}", couleur, perms, True)

    for nom_cat, salons in cfg["categories"].items():
        cat = await _creer_categorie(guild, nom_cat)
        if not cat:
            continue
        for s in salons:
            await _creer_salon_text(guild, s, cat)

    vcat = await _creer_categorie(guild, "🔊 VOCAUX")
    for v in cfg["vocaux"]:
        await _creer_salon_vocal(guild, f"🔊・{v}", vcat)

    log.info("[ANIME] Terminé : %s", cfg["nom"])
    return True