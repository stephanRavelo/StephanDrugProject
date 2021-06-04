# Considérations à prendre en compte face à des données massives 
Le projet comportait des données de petites volumétries. Ainsi le fait
d'enchaîner en série les traitements n'a pas d'impact sur l'exécution du pipeline. 


Mais face à des fichiers de données plus importants 
(ex: plusieurs milliers de fichiers de pubmed ou clinical_trials) et plus divers 
(e.g: autres formats de fichiers comme .avro, .parquets etc), il est important de faire quelques modifications. 
Voici quelques pistes: 
- éviter les boucles sur les dataframes Pandas et privilégier les opérations vectorielles. 
- paralleliser certaines opérations:
par exemple paraleliser dans Airflow le chargement des fichiers input csv et des jsons avant de tout fusionner dans une table de référence.
  Il existe aussi des bibliothèques permettant de faire du parallel computing en précisant le nombre de node worker et de taches associées. Dask comporte des arrays et dataframe dédiés aux larges datasets comme pandas. On gagne également en scalabilité.  
- utiliser des frameworks big data comme PySpark pourrait également aider à réduire le temps de d'éxécution 
- sécuriser le pipeline à travers des briques d'alerting: dans le cas où l'on travaille à avec plus de données, 
il faut mettre en place des briques qui vont sécuriser le pipeline. Par exemple si un ou plusieurs fichiers sont incohérents en terme de contenus (nom de colonnes qui a changé, beaucoup données manquantes, etc), on peut automatiser l'envoi de mails aux métiers ou aux équipes IT pour alerter.
- travailler dans un environnnement cloud comme GCP pour bénéficier des services optimisés (e.g: Big Query pour fusionner rapidement les tables de références pubmed et clinical_trials ).
- monitorer le temps de traitement des jobs afin de comprendre et d'être réactif si l'on voit des lenteurs et apporter des améliorations en conséquence. Airflow prévoit une interface pour suivre ces jobs par exemple. 

# Axes d'amélioration sur la qualité du code:
Voici quelques axes d'amélioration sur la qualité du code:
- Mettre en place des tests automatisés afin de rendre le code robuste si des évolutions ou changments sont à prévoir.
Pytest est un bon candidat pour répondre à ce besoin. 
- Automatiser la documentation avec Sphynx
- Construire un package dédié afin de pouvoir partager facilement le code si besoin. 








