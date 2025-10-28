# 💼 Système de Gestion Financière - Marate AI

Une application web complète de gestion financière avec génération de reçus PDF, suivi des dépenses et tableau de bord analytique.

## 🎯 Aperçu

Cette application Flask permet de:
- **Générer des reçus PDF** professionnels téléchargeables avec numérotation automatique
- **Suivre et enregistrer les dépenses** pour une gestion financière complète
- **Visualiser les finances** avec un tableau de bord interactif et des graphiques
- **Analyser les revenus** mensuels et le revenu net avec Chart.js
- **Gérer les paiements** récurrents et uniques avec descriptions automatiques

## ✨ Fonctionnalités Principales

### 📝 Génération de Reçus
- Numéro de reçu automatique et unique
- Deux types de paiement :
  - **Récurrent mensuel** : Description automatique "Paiement mensuel récurrent"
  - **Unique** : Champ personnalisable pour la raison du paiement
- Montant en chiffres et en lettres
- Sections signature et cachet d'entreprise
- Export PDF instantané avec téléchargement automatique
- Stockage dans la base de données et dossier `receipts/`

### 💸 Gestion des Dépenses
- Enregistrement rapide avec description et montant
- Date automatique d'enregistrement
- Historique complet accessible depuis le tableau de bord
- Calcul automatique du total des dépenses

### 📊 Tableau de Bord Analytique
- **Cartes récapitulatives compactes** :
  - Revenu Total (FCFA)
  - Dépenses Totales (FCFA)
  - Revenu Net (FCFA)
- **Graphiques interactifs** (Chart.js) :
  - Revenus mensuels (graphique à barres)
  - Tendance du revenu net (graphique linéaire)
- **Tableaux détaillés** :
  - Revenus par mois
  - 10 derniers reçus
  - 10 dernières dépenses
- **Design responsive** : S'adapte aux écrans desktop et mobile

## 🧱 Technologies

- **Backend** : Flask 3.1.2
- **Base de données** : SQLite + Flask-SQLAlchemy 3.1.1
- **Génération PDF** : WeasyPrint
- **Graphiques** : Chart.js
- **Frontend** : HTML5, CSS3, JavaScript
- **Python** : 3.13+

## 📂 Structure du Projet

```
facturation/
├── app.py                    # Application Flask avec routes
├── database.py               # Modèles SQLAlchemy (Receipt, Expense)
├── populate_db.py            # Script de génération de données de test
├── requirements.txt          # Dépendances Python
├── .gitignore               # Fichiers à ignorer par Git
│
├── templates/
│   ├── form.html            # Formulaire de génération de reçu
│   ├── add_expense.html     # Formulaire d'ajout de dépense
│   ├── dashboard.html       # Tableau de bord avec graphiques
│   └── receipt_template.html # Template HTML pour PDF
│
├── static/
│   └── css/
│       └── style.css        # Styles globaux
│
├── receipts/                # PDFs générés (créé automatiquement)
└── instance/
    └── data.db             # Base de données SQLite (créée automatiquement)
```

## 🚀 Installation Rapide

### 1. Cloner le Projet

```bash
git clone https://github.com/phil-keita/facturation.git
cd facturation
```

### 2. Créer un Environnement Virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les Dépendances Python

```bash
pip install -r requirements.txt
```

### 4. Installer les Dépendances Système

WeasyPrint nécessite des bibliothèques système :

**macOS :**
```bash
brew install pango gdk-pixbuf libffi
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt-get install python3-dev python3-pip libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
```

**Windows :**
- Télécharger GTK+ Runtime depuis [ici](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

### 5. Lancer l'Application

```bash
python app.py
```

L'application démarre sur **http://localhost:5000**

## 📖 Guide d'Utilisation

### Générer un Reçu

1. Aller sur http://localhost:5000
2. Remplir le formulaire :
   - **Nom du Client** : Nom complet ou entreprise
   - **Type de Paiement** : Récurrent ou Unique
   - **Raison** (si unique) : Description personnalisée
   - **Prix (FCFA)** : Montant numérique
   - **Montant en Lettres** : Montant écrit en toutes lettres
3. Cliquer sur **Générer PDF**
4. Le reçu se télécharge automatiquement

### Enregistrer une Dépense

1. Cliquer sur **Dépense** dans le menu
2. Entrer la description et le montant
3. Cliquer sur **Enregistrer la Dépense**
4. Redirection automatique vers le tableau de bord

### Consulter le Tableau de Bord

1. Cliquer sur **Tableau de bord** dans le menu
2. Visualiser les cartes récapitulatives et les graphiques
3. Consulter les tableaux de transactions récentes

### (Optionnel) Générer des Données de Test

Pour tester avec des données réalistes :

```bash
python populate_db.py
```

Génère automatiquement :
- 100+ reçus sur 12 mois
- 70+ dépenses variées
- Clients et montants réalistes

⚠️ **Attention** : Efface les données existantes

## 📄 Contenu du Reçu PDF

Chaque reçu contient :
- Numéro unique (format: `REC-[timestamp]-[counter]`)
- En-tête "Paiement à Marate AI"
- Date et heure de génération
- Nom du client
- Description du service
- Type de paiement
- Prix en FCFA
- Montant en lettres
- Section signature
- Zone cachet d'entreprise

## 📊 Base de Données

SQLite avec deux tables :

**Receipt (Reçus)**
- `id`, `receipt_number`, `customer_name`
- `description`, `payment_type`, `payment_reason`
- `price`, `amount_in_letters`, `date`

**Expense (Dépenses)**
- `id`, `description`, `amount`, `date`

## 🎨 Personnalisation

### Changer la Couleur d'Accentuation
Remplacer `#00bcd4` (cyan) dans `static/css/style.css` et `templates/receipt_template.html`

### Modifier les Graphiques
Éditer les options Chart.js dans `templates/dashboard.html`

### Personnaliser les Reçus
Modifier `templates/receipt_template.html` pour ajouter logo, champs personnalisés, etc.

## 🔒 Notes de Production

⚠️ Cette application est conçue pour le développement local.

Pour la production, considérer :
- PostgreSQL/MySQL au lieu de SQLite
- Authentification utilisateur (Flask-Login)
- HTTPS/SSL
- Serveur WSGI (Gunicorn)
- Variables d'environnement pour les secrets
- Sauvegardes automatiques
- Rate limiting

## 🚀 Déploiement

Compatibilité :
- Render
- Railway  
- PythonAnywhere
- Heroku
- DigitalOcean App Platform
- VPS avec Nginx + Gunicorn

## 🔮 Améliorations Futures

- [ ] Authentification multi-utilisateurs
- [ ] Export Excel/CSV
- [ ] Envoi automatique par email
- [ ] Factures multi-lignes
- [ ] Calcul TVA automatique
- [ ] Support multi-devises
- [ ] API REST
- [ ] Rapports PDF automatisés
- [ ] Filtres par période
- [ ] Catégorisation des dépenses
- [ ] Mode sombre
- [ ] Application mobile

## 🤝 Contribution

Les contributions sont bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Changelog

**v2.0** (Octobre 2025)
- ✨ Système de gestion des dépenses
- 📊 Tableau de bord avec Chart.js
- 💾 Base de données SQLite
- 🎨 Design cyan moderne
- 📱 Interface responsive
- 🔢 Devise FCFA
- 🇫🇷 Localisation française

**v1.0** (Octobre 2025)
- 🎉 Version initiale
- 📝 Génération de reçus PDF
- 💼 Types de paiement
- 🖊️ Signature et cachet

## 📄 Licence

MIT License - Usage libre personnel et commercial

## 👨‍💻 Auteur

**Philippe Keita**  
Marate AI  
Octobre 2025

---

**Made with ❤️ for Marate AI**
