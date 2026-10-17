# NOVA CORE — Plan de vérification

Cette liste distingue les vérifications manuelles des fonctions déjà présentes dans la version statique. Ne pas annoncer la mise en production avant d'avoir exécuté les tests et validé les intégrations.

## Vérifications navigateur (mobile et bureau)

- [ ] Ouvrir `NOVA-CORE/index.html` sur Android Chrome et un navigateur de bureau.
- [ ] Vérifier l'affichage à 320 px, 360 px, 768 px et 1280 px sans défilement horizontal.
- [ ] Cocher/décocher les quatre tâches ; contrôler le pourcentage et le compteur.
- [ ] Recharger la page ; confirmer la persistance locale des tâches, objectifs et chiffres.
- [ ] Réinitialiser les tâches et vérifier que les quatre cases sont décochées.
- [ ] Générer un plan avec objectif et contraintes vides puis renseignés.
- [ ] Générer un message avec nom, service et prix personnalisés ; vérifier le texte.
- [ ] Tester la copie du message dans un contexte HTTPS et vérifier le comportement de repli si le presse-papiers est bloqué.
- [ ] Tester revenus 5000 / dépenses 2000 (net 3000), puis revenus 1000 / dépenses 2500 (net -1500).
- [ ] Exporter les données JSON et vérifier que le fichier est lisible et ne contient pas de secrets.
- [ ] Tester avec stockage local désactivé ou plein ; la page doit rester utilisable sans planter.
- [ ] Vérifier le clavier, les libellés, les états de focus et la réduction des animations.

## Contrôles de sécurité avant production

- [ ] Authentification réelle et gestion de session.
- [ ] Appliquer la migration à un projet Supabase actif et non ambigu.
- [ ] Vérifier les politiques RLS avec deux comptes différents.
- [ ] Déployer la fonction Edge avec vérification JWT et secrets uniquement côté serveur.
- [ ] Connecter le fournisseur de modèle via un secret serveur ; tester les erreurs, limites et coûts.
- [ ] Ajouter tests automatisés, journalisation sans secrets, limitation de débit et contrôle des entrées.
- [ ] Déployer sur Vercel puis vérifier HTTPS, en-têtes, routes et variables d'environnement.
- [ ] Effectuer une revue de sécurité et une sauvegarde avant toute donnée réelle.

## État honnête

Les outils de plan, de message, de suivi des tâches, de calcul et d'export sont côté navigateur. Ils ne prouvent pas qu'une vente a eu lieu et ne se connectent pas à des services externes. Toute intégration cloud doit être testée séparément.
