# ars-scrutari
*"Quand l'IA dissèque ta quête désespérée d'alternance tech en France"*

## DESCRIPTION 
Un script qui transforme ton tableau Excel/Google Sheet de candidatures en:  
- Stats de ghosting LinkedIn™  
- Compétences les plus demandées par pays (spoiler : pas mon C++ apparemment)  
- CV avec le plus de réponses et peut-être plus par la suite

## DETAILS D'IMPLEMENTATION
Utilisation de deux Designs Patterns, précisément Strategy (permettant d'isoler la logique métier via la méthode polymorphique "results") et Factory sur la classe coordinatrice. J'ai également adopté l'approche de Yegor Bugayenko dans le livre [Elegant Objects](https://github.com/agrism/books/blob/master/Elegant%20Objects%20by%20Yegor%20Bugayenko%20(z-lib.org).pdf) concernant la définition de classes immutables afin d'éviter ce qu'il a appelé des "effets secondaires" durant les différents types d'analyses.

## INSTALLATION 
S'assurer d'avoir son fichier `.csv` à la racine du repo et lancer les commandes suivantes.

```bash
pip install -r requirements.txt  
python main.py
```

## EXEMPLES D'OUTPUT
```
=== Skill Trends ===
Compétences les plus recherchées par pays :

France:
- typescript (3 occurrences)
- docker (3 occurrences)
- react (2 occurrences)
- postgresql (2 occurrences)
- azure (2 occurrences)


=== Cv Formats ===
Formats de CV utilisés :
- com: 9 utilisations


=== Patterns ===
Mots-clés récurrents dans les descriptions :
- knowledge (6 occurrences)
- experience (5 occurrences)
- développement (5 occurrences)
- systèmes (4 occurrences)
- relationnel (4 occurrences)
- anglais (3 occurrences)
- travail (3 occurrences)
- capacité (3 occurrences)
- autonome (3 occurrences)
- équipe (3 occurrences)


=== Platform Success ===
Taux de réponse par plateforme et pays :

France - LinkedIn:
- Taux de réponse: 22.2%
- Candidatures: 9


=== Response Time ===
Durée moyenne de réponse : nan jours
Basé sur 2 réponses reçues

=== Rejection Rate ===
Taux de refus global : 100.0%
(2 refus sur 2 réponses)

Aman@LAPTOP-2362G6TO MINGW64 ~/source/perso/ars-scrutari (main)
$ git add .

Aman@LAPTOP-2362G6TO MINGW64 ~/source/perso/ars-scrutari (main)
$ git commit -m "docs: add README.md"
[main f2ce55a] docs: add README.md
 2 files changed, 46 insertions(+), 9 deletions(-)

Aman@LAPTOP-2362G6TO MINGW64 ~/source/perso/ars-scrutari (main)
$ git push
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 16 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 1.44 KiB | 1.44 MiB/s, done.
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/AmanMenda/ars-scrutari.git
   4321279..f2ce55a  main -> main

Aman@LAPTOP-2362G6TO MINGW64 ~/source/perso/ars-scrutari (main)
$
 *  History restored 


Aman@LAPTOP-2362G6TO MINGW64 ~/source/perso/ars-scrutari (main)
$ python main.py 

=== Skill Trends ===
Compétences les plus recherchées par pays :

France:
- typescript (3 occurrences)
- docker (3 occurrences)
- react (2 occurrences)
- postgresql (2 occurrences)
- azure (2 occurrences)


=== Cv Formats ===
Formats de CV utilisés :
- "cv_amanmenda.pdf": 9 utilisations


=== Patterns ===
Mots-clés récurrents dans les descriptions :
- knowledge (6 occurrences)
- experience (5 occurrences)
- développement (5 occurrences)
- systèmes (4 occurrences)
- relationnel (4 occurrences)
- anglais (3 occurrences)
- travail (3 occurrences)
- capacité (3 occurrences)
- autonome (3 occurrences)
- équipe (3 occurrences)


=== Platform Success ===
Taux de réponse par plateforme et pays :

France - LinkedIn:
- Taux de réponse: 22.2%
- Candidatures: 9


=== Response Time ===
Durée moyenne de réponse : nan jours
Basé sur 2 réponses reçues

=== Rejection Rate ===
Taux de refus global : 100.0%
(2 refus sur 2 réponses)
```