# 🧾 Générateur de Reçus - Marate AI

Une application web simple qui génère des reçus PDF téléchargeables à partir d'un formulaire.

## 🎯 Aperçu

Cette application Flask permet aux utilisateurs de:
- Remplir un formulaire avec les informations du client
- Générer un reçu PDF professionnel automatiquement
- Télécharger le reçu instantanément
- Choisir entre paiement récurrent ou unique
- Inclure automatiquement un numéro de reçu unique

## ✨ Fonctionnalités

- **Numéro de reçu automatique**: Généré automatiquement pour chaque reçu
- **Types de paiement**: 
  - Paiement Mensuel Récurrent
  - Paiement Unique (avec champ raison optionnel)
- **Montant en lettres**: Saisie du montant en toutes lettres
- **Section signature**: Ligne de signature pour validation
- **Zone cachet**: Emplacement dédié pour le cachet de l'entreprise
- **Interface en français**: Totalement localisée pour les entreprises francophones
- **Design cyan**: Couleur d'accentuation cyan moderne

## 🧱 Technologies Utilisées

- **Backend**: Flask (framework web Python)
- **Moteur de templates**: Jinja2 (inclus avec Flask)
- **Génération PDF**: WeasyPrint
- **Frontend**: HTML + CSS + JavaScript
- **Version Python**: 3.10+

## 📂 Project Structure

```
facturation/
│
├── app.py                    # Flask application entry point
│
├── templates/
│   ├── form.html             # Input form page
│   └── receipt_template.html # HTML template for the PDF
│
├── static/
│   └── css/
│       └── style.css         # Styles for the form
│
├── receipts/                 # Generated PDFs stored here
│
├── requirements.txt          # Python dependencies
│
└── README.md                 # This file
```

## 🚀 Instructions d'Installation

### 1. Cloner ou Naviguer vers le Projet

```bash
cd /Users/philippekeita/Documents/GitHub/facturation
```

### 2. Créer un Environnement Virtuel (Recommandé)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les Dépendances Python

```bash
pip install -r requirements.txt
```

### 4. Installer les Dépendances Système (macOS)

> **Important**: WeasyPrint nécessite des bibliothèques système supplémentaires sur macOS:
> ```bash
> brew install pango gdk-pixbuf libffi
> ```

### 5. Lancer l'Application

```bash
python app.py
```

L'application démarre sur **http://localhost:5000**

### 6. Utiliser l'Application

1. Ouvrir votre navigateur et aller sur `http://localhost:5000`
2. Remplir le formulaire:
   - **Nom du Client**: Nom complet du client
   - **Description**: Description du service ou produit
   - **Type de Paiement**: Choisir entre récurrent ou unique
   - **Raison** (si paiement unique): Expliquer la raison
   - **Prix ($)**: Montant numérique
   - **Montant en Lettres**: Montant écrit en toutes lettres
3. Cliquer sur **Générer PDF**
4. Le reçu PDF se télécharge automatiquement
5. Les reçus générés sont sauvegardés dans le dossier `receipts/`

## 📝 Comment ça Marche

1. **L'utilisateur visite la page d'accueil** (`/`) - affiche le formulaire
2. **L'utilisateur soumet le formulaire** - envoie une requête POST à `/generate`
3. **Flask traite les données**:
   - Extrait les données du formulaire (nom, description, prix, type de paiement, etc.)
   - Génère un numéro de reçu unique basé sur le timestamp
   - Rend le template de reçu avec les données
   - Utilise WeasyPrint pour convertir HTML en PDF
   - Sauvegarde le PDF dans le dossier `receipts/`
4. **L'utilisateur reçoit le PDF** - téléchargement automatique

## 📄 Contenu du Reçu

Chaque reçu PDF généré contient:
- **Numéro de reçu**: Identifiant unique (format: REC-timestamp)
- **En-tête**: "Paiement à Marate AI" en cyan
- **Date**: Date et heure de génération
- **Client**: Nom du client
- **Description**: Description du service/produit
- **Type de Paiement**: Récurrent ou unique (avec raison si applicable)
- **Prix**: Montant en dollars
- **Montant en Lettres**: Montant écrit en toutes lettres
- **Section Signature**: Ligne pour signature manuscrite
- **Zone Cachet**: Espace pour apposer le cachet de l'entreprise

## 🎨 Personnalisation

### Modifier le Design du Reçu

Éditer `templates/receipt_template.html` pour modifier:
- La mise en page
- Les couleurs (actuellement cyan: #00bcd4)
- Ajouter un logo d'entreprise
- Ajouter des champs supplémentaires

### Modifier le Style du Formulaire

Éditer `static/css/style.css` pour personnaliser l'apparence du formulaire.

### Changer la Couleur d'Accentuation

Rechercher et remplacer `#00bcd4` (cyan) dans les fichiers CSS et HTML.

## 🔮 Améliorations Futures

- Ajouter plusieurs articles avec quantités
- Calculer les totaux et taxes automatiquement
- Ajouter le logo de l'entreprise
- Envoyer les reçus par email automatiquement
- Stocker les reçus dans une base de données
- Ajouter une page d'historique des reçus
- Support multi-devises
- Déployer sur une plateforme cloud (Render, Railway, Heroku)

## 📄 Licence

Ce projet est open source et disponible pour un usage personnel et commercial.

## 🤝 Contribution

N'hésitez pas à forker ce projet et à soumettre des pull requests pour des améliorations!

---

**Créé**: Octobre 2025  
**Auteur**: Philippe Keita  
**Entreprise**: Marate AI
