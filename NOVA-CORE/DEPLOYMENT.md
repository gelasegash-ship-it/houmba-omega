# NOVA CORE — état de déploiement et configuration

## Ce qui est actif
- Dashboard mobile dans `NOVA-CORE/index.html`: mode local, registre manuel, checklist et export JSON.
- Authentification Supabase par e-mail/mot de passe intégrée à l’interface.
- Edge Function `nova-plan` déployée avec JWT obligatoire (version 2).
- Planificateur serveur avec repli sûr si le fournisseur de modèle n’est pas configuré ou indisponible.
- CI backend : import de modules corrigé avec `PYTHONPATH=.`.

## Projet Supabase
- Projet : `ALPHA TECH`
- Référence : `mbrxsitcnlmwlpmdwxhf`
- URL : `https://mbrxsitcnlmwlpmdwxhf.supabase.co`
- Région : `eu-west-1`

La clé publishable peut être exposée dans une application web; elle ne remplace jamais les politiques RLS. Ne jamais publier une clé service-role ni une clé OpenAI dans le frontend ou dans Git.

## À configurer dans le tableau de bord Supabase
1. Authentication → URL Configuration : définir l’URL du site déployé comme Site URL et ajouter l’URL du site + chemins de retour comme Redirect URLs.
2. Authentication → Providers / Email : choisir si la confirmation d’e-mail reste obligatoire.
3. Edge Functions → Secrets : ajouter `OPENAI_API_KEY` côté serveur pour activer la génération via OpenAI; facultatif `OPENAI_MODEL` (défaut `gpt-4o-mini`), facultatif `NOVA_ALLOWED_ORIGIN` avec l’origine exacte du site public.
4. Ne jamais coller ces secrets dans le dépôt, le HTML, un ticket ou le chat.

Sans `OPENAI_API_KEY`, le planificateur renvoie explicitement un plan de base et `connected_model: false`. Aucun revenu ou aucune action externe ne sont garantis.

## Limites connues
- Les tâches, le registre financier et les préférences de la page sont encore enregistrés localement; la synchronisation multi-appareil n’est pas activée.
- Pas de paiements, virements, retraits, messagerie sociale, ni publication Android native.
- Les paiements et actions irréversibles nécessitent une intégration dédiée, des tests et une validation humaine.
- Vérifier GitHub Actions après chaque commit et tester le flux d’inscription/confirmation/connexion sur le domaine public.
- Vérifier la facturation Supabase dans le tableau de bord avant de laisser le projet actif.

## Vérification
- CI : https://github.com/gelasegash-ship-it/houmba-omega/actions
- Dashboard : https://github.com/gelasegash-ship-it/houmba-omega/blob/main/NOVA-CORE/index.html
- Fonction : https://github.com/gelasegash-ship-it/houmba-omega/blob/main/supabase/functions/nova-plan/index.ts
