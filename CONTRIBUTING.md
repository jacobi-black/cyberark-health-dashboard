# Guide de contribution

Nous sommes ravis que vous envisagiez de contribuer au projet CyberArk Health Dashboard ! Ce document vous guidera à travers le processus de contribution.

## Code de conduite

En participant à ce projet, vous vous engagez à maintenir un environnement respectueux et collaboratif. Tous les contributeurs doivent adhérer à notre code de conduite.

## Comment contribuer

### Signaler des bugs

1. Vérifiez d'abord si le bug n'a pas déjà été signalé dans l'onglet "Issues".
2. Si ce n'est pas le cas, créez une nouvelle issue en utilisant le modèle de rapport de bug.
3. Incluez toutes les informations nécessaires:
   - Description claire et concise du bug
   - Étapes pour reproduire le problème
   - Comportement attendu vs comportement observé
   - Captures d'écran (si applicable)
   - Environnement (OS, version Python, version CyberArk, etc.)

### Proposer des améliorations

1. Ouvrez une nouvelle issue en décrivant votre proposition d'amélioration.
2. Expliquez pourquoi cette amélioration serait utile pour le projet.
3. Soyez ouvert à la discussion et aux feedbacks sur votre proposition.

### Soumettre des modifications de code

1. Fork le dépôt et créez une branche à partir de la branche `main`.
2. Effectuez vos modifications en suivant les conventions de codage du projet.
3. Ajoutez ou mettez à jour les tests pour refléter vos modifications.
4. Assurez-vous que tous les tests passent.
5. Mettez à jour la documentation si nécessaire.
6. Soumettez une pull request vers la branche `main` du dépôt original.

## Processus de développement

1. **Fork & Clone**: Commencez par fork le dépôt et clonez-le sur votre machine locale.
2. **Branche**: Créez une branche pour vos modifications:
   ```bash
   git checkout -b feature/nom-de-la-fonctionnalite
   ```
   ou
   ```bash
   git checkout -b fix/nom-du-bug
   ```
3. **Code**: Écrivez votre code en suivant les conventions du projet.
4. **Test**: Exécutez les tests et assurez-vous qu'ils passent tous:
   ```bash
   pytest
   ```
5. **Style**: Vérifiez que votre code respecte les conventions de style:
   ```bash
   flake8
   ```
6. **Commit**: Faites des commits avec des messages clairs et descriptifs:
   ```bash
   git commit -m "Ajout de la fonctionnalité X qui résout le problème Y"
   ```
7. **Push**: Poussez vos modifications vers votre fork:
   ```bash
   git push origin feature/nom-de-la-fonctionnalite
   ```
8. **Pull Request**: Ouvrez une pull request sur GitHub.

## Conventions de codage

- Utilisez [PEP 8](https://pep8.org/) pour le style de code Python.
- Écrivez des docstrings pour toutes les fonctions, classes et modules.
- Utilisez des noms descriptifs pour les variables, fonctions et classes.
- Commentez votre code lorsque nécessaire pour expliquer le "pourquoi", pas le "quoi".
- Écrivez des tests unitaires pour les nouvelles fonctionnalités.

## Structure du projet

```
cyberark-health-dashboard/
├── app/                  # Code principal de l'application
│   ├── api.py            # Points d'accès de l'API REST
│   ├── config.py         # Configuration de l'application
│   ├── cyberark_api.py   # Client API pour CyberArk
│   ├── health_collector.py  # Collecteur de données de santé
│   └── models.py         # Modèles de données
├── powerbi/              # Ressources PowerBI
├── tests/                # Tests unitaires et d'intégration
├── .env.example          # Exemple de fichier de configuration
├── main.py               # Point d'entrée de l'application
└── requirements.txt      # Dépendances Python
```

## Revue de code

Toutes les soumissions, y compris les soumissions des membres de l'équipe principale, nécessitent une revue. Nous utilisons les pull requests de GitHub pour ce processus.

## Merci!

Votre contribution est précieuse. Merci de nous aider à améliorer le CyberArk Health Dashboard!