#!/bin/bash
# Lanceur KoreHosting — ne pas modifier.
# Depose automatiquement a la creation du serveur.

cd /home/container || exit 1

# Le mode d'emploi est rafraichi a chaque demarrage, pour que les serveurs
# deja crees suivent les evolutions du panel. Uniquement s'il est encore la :
# un client qui l'a supprime ne doit pas le voir revenir.
if [ -f LISEZ-MOI.txt ]; then
    cat > LISEZ-MOI.txt <<'FIN_TXT'
Bienvenue chez KoreHosting.

Votre serveur est pret, mais il est encore vide. Trois etapes et votre
bot tourne 24h/24.


1. ENVOYER VOTRE CODE

   Onglet Fichiers du panel, bouton Envoyer.

   Deposez votre fichier principal (index.js, bot.py...) et, si vous
   en avez un, package.json (JavaScript) ou requirements.txt (Python).
   Vos dependances seront installees automatiquement, vous n avez rien
   d autre a faire.

   N envoyez pas le dossier node_modules : il est reconstruit ici.


2. REGLER LE DEMARRAGE

   Onglet Demarrage du panel.

   - "Langage et version" : choisissez Node.js pour un bot JavaScript,
     Python pour un bot Python. Vous pouvez en changer quand vous
     voulez, vos fichiers ne sont pas touches.

   - "Fichier de demarrage", dans les reglages du bot : le nom exact
     de votre fichier principal, par exemple index.js ou bot.py.


3. DEMARRER

   Bouton Demarrer, en haut de la console.

   Vous verrez installation des dependances, puis le demarrage de
   votre bot. Le serveur passe en vert quand tout est en ligne.


EN CAS DE SOUCI

La console dit toujours ce qui ne va pas. Les messages qui commencent
par [KoreHosting] sont ecrits pour vous et indiquent quoi corriger.

Une question ? support@korehosting.eu

Vous pouvez supprimer ce fichier, il ne reviendra pas.
FIN_TXT
fi

if [[ -d .git ]] && [[ "${AUTO_UPDATE}" == "1" ]]; then
    echo "[KoreHosting] Mise a jour depuis Git..."
    git pull
fi

if [ -z "${MAIN_FILE}" ]; then
    echo "[KoreHosting] ERREUR : aucun fichier de demarrage indique dans onglet Demarrage."
    exit 1
fi

if [ ! -f "/home/container/${MAIN_FILE}" ]; then
    echo "[KoreHosting] ERREUR : le fichier ${MAIN_FILE} est introuvable."
    echo "[KoreHosting] Verifiez le nom dans onglet Demarrage, ou envoyez le fichier"
    echo "[KoreHosting] dans le gestionnaire de fichiers."
    exit 1
fi

# Le langage decoule de l'image Docker choisie : inutile de le demander une
# seconde fois au client. On regarde donc quel interpreteur est present.
if command -v node > /dev/null 2>&1; then

    case "${MAIN_FILE}" in
        *.py)
            echo "[KoreHosting] ERREUR : ${MAIN_FILE} est un fichier Python, mais ce serveur"
            echo "[KoreHosting] utilise une image Node. Choisissez une image Python dans"
            echo "[KoreHosting] onglet Demarrage, puis relancez."
            exit 1;;
    esac

    if [ -n "${EXTRA_PACKAGES}" ]; then
        echo "[KoreHosting] Installation des paquets npm demandes..."
        if ! npm install --no-audit --no-fund ${EXTRA_PACKAGES}; then
            echo "[KoreHosting] ERREUR : impossible installer les paquets supplementaires."
            echo "[KoreHosting] Verifiez leur nom dans onglet Demarrage, champ Paquets"
            echo "[KoreHosting] supplementaires."
            exit 1
        fi
    fi

    if [ -f package.json ]; then
        echo "[KoreHosting] Installation des dependances du projet..."
        # Sans ce controle, une dependance mal orthographiee laissait le bot
        # demarrer quand meme : le client recevait un "module introuvable" qui
        # ne disait rien de la vraie cause.
        if ! npm install --no-audit --no-fund; then
            echo "[KoreHosting] ERREUR : installation des dependances echouee."
            echo "[KoreHosting] Le detail est juste au dessus. Cause frequente : un paquet"
            echo "[KoreHosting] mal orthographie ou une version inexistante dans package.json."
            exit 1
        fi
    fi

    case "${MAIN_FILE}" in
        *.ts)
            # node ne sait pas executer du TypeScript de facon fiable selon sa
            # version : on passe par ts-node si le projet le fournit.
            if [ -x node_modules/.bin/ts-node ]; then
                echo "[KoreHosting] Demarrage du bot"
                exec node_modules/.bin/ts-node "/home/container/${MAIN_FILE}"
            fi
            echo "[KoreHosting] ERREUR : ${MAIN_FILE} est du TypeScript et ts-node est absent."
            echo "[KoreHosting] Deux solutions : compilez votre bot et pointez sur le fichier"
            echo "[KoreHosting] .js produit, ou ajoutez ts-node aux dependances de package.json."
            exit 1;;
    esac

    echo "[KoreHosting] Demarrage du bot"
    # exec : le bot devient le processus principal du conteneur, donc le bouton
    # Arreter lui parvient directement et il peut se fermer proprement.
    exec node "/home/container/${MAIN_FILE}"

else

    case "${MAIN_FILE}" in
        *.js|*.mjs|*.cjs|*.ts)
            echo "[KoreHosting] ERREUR : ${MAIN_FILE} est un fichier JavaScript, mais ce"
            echo "[KoreHosting] serveur utilise une image Python. Choisissez une image Node"
            echo "[KoreHosting] dans onglet Demarrage, puis relancez."
            exit 1;;
    esac

    # --target plutot que --prefix : --prefix range les paquets dans un chemin
    # qui contient le numero de version de Python, donc changer d'image ferait
    # disparaitre toutes les dependances installees.
    export PYTHONPATH=/home/container/.local/pysite

    if [ -n "${EXTRA_PACKAGES}" ]; then
        echo "[KoreHosting] Installation des paquets pip demandes..."
        if ! pip install -q -U --target /home/container/.local/pysite ${EXTRA_PACKAGES}; then
            echo "[KoreHosting] ERREUR : impossible installer les paquets supplementaires."
            echo "[KoreHosting] Verifiez leur nom dans onglet Demarrage, champ Paquets"
            echo "[KoreHosting] supplementaires."
            exit 1
        fi
    fi

    if [ -f requirements.txt ]; then
        echo "[KoreHosting] Installation des dependances du projet..."
        if ! pip install -q -U --target /home/container/.local/pysite -r requirements.txt; then
            echo "[KoreHosting] ERREUR : installation des dependances echouee."
            echo "[KoreHosting] Le detail est juste au dessus. Cause frequente : un paquet"
            echo "[KoreHosting] mal orthographie ou une version inexistante dans"
            echo "[KoreHosting] requirements.txt."
            exit 1
        fi
    fi

    echo "[KoreHosting] Demarrage du bot"
    # -u : sortie non tamponnee, sinon la console reste vide plusieurs minutes
    # et le client croit que son bot est plante.
    exec python -u "/home/container/${MAIN_FILE}"

fi
