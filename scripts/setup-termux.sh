#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

REPO_URL="https://github.com/gelasegash-ship-it/houmba-omega.git"
PROJECT_DIR="$HOME/houmba-omega"

if [ -z "${PREFIX:-}" ] || [[ "${PREFIX}" != *com.termux* ]]; then
  echo "Ce script est prévu pour Termux sur Android."
  exit 1
fi

echo "=== Préparation du poste Android pour NOA H / houmba-omega ==="
echo "1/3 — Mise à jour des paquets Termux"
pkg update -y
pkg install -y git python nodejs-lts openssh curl nano

echo "2/3 — Préparation du dépôt"
if [ -d "$PROJECT_DIR/.git" ]; then
  echo "Dépôt déjà présent : $PROJECT_DIR"
  git -C "$PROJECT_DIR" pull --ff-only
elif [ -e "$PROJECT_DIR" ]; then
  echo "Le chemin $PROJECT_DIR existe mais n'est pas un dépôt Git."
  echo "Aucun fichier existant n'a été modifié. Déplace-le ou renomme-le puis relance."
  exit 2
else
  git clone "$REPO_URL" "$PROJECT_DIR"
fi

echo "3/3 — Vérification des outils"
printf '\nVersions installées :\n'
git --version
python --version
node --version
npm --version

printf '\nTerminé. Projet local : %s\n' "$PROJECT_DIR"
printf 'Pour consulter le projet : cd "$HOME/houmba-omega" && ls -la\n'
printf '\nSécurité : ce script ne demande aucun mot de passe, jeton GitHub ni clé API.\n'
printf 'Il ne déploie rien et ne lance pas le backend automatiquement.\n'
