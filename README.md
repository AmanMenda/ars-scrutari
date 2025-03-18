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
France:
- java (12 occurrences)
- react (9)
- aws (7)

=== CV Formats ===
- pdf: 83% (n=15)
- docx: 17% 

=== Response Time ===
μ=5.2 days | σ=1.8 (n=23 valid responses)

=== Platform Success ===
LinkedIn FR: 18.4% response rate (35 applications)
```