# 💼 Système de Gestion Financière - Marate AI

Une application web complète de gestion financière multi-utilisateurs avec authentification, génération de reçus PDF, suivi des dépenses et tableau de bord analytique.

## 🎯 Aperçu

Cette application Flask permet de:
- **Authentification sécurisée** avec gestion multi-utilisateurs
- **Générer des reçus PDF** professionnels téléchargeables avec numérotation automatique
- **Suivre et enregistrer les dépenses** pour une gestion financière complète
- **Visualiser les finances** avec un tableau de bord interactif et des graphiques
- **Analyser les revenus** mensuels et le revenu net avec Chart.js
- **Gérer les paiements** récurrents et uniques avec descriptions automatiques
- **Vue personnelle vs entreprise** pour analyser vos données ou celles de l'équipe

## ✨ Fonctionnalités Principales

### 🔐 Authentification & Gestion Utilisateurs
- Connexion sécurisée avec hashage des mots de passe
- Compte administrateur avec interface de gestion
- Création et suppression d'utilisateurs
- Modification du nom d'utilisateur et mot de passe
- Menu profil avec avatar
- Protection du compte admin

### 📝 Génération de Reçus
- Numéro de reçu automatique et unique
- Association automatique à l'utilisateur connecté
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
- Association automatique à l'utilisateur connecté
- Historique complet accessible depuis le tableau de bord
- Calcul automatique du total des dépenses

### 📊 Tableau de Bord Analytique
- **Vue personnelle** : Visualisez uniquement vos propres données
- **Vue entreprise** : Analysez les données agrégées de toute l'équipe (sans exposition des utilisateurs individuels)
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
- **Interface moderne** : Design épuré avec dégradés cyan, animations et effets glossy

## 🧱 Technologies

- **Backend** : Flask 3.1.2
- **Base de données** : SQLite (dev) / PostgreSQL 16 (production) + Flask-SQLAlchemy 3.1.1
- **Authentification** : Werkzeug password hashing, Flask sessions
- **Génération PDF** : WeasyPrint
- **Graphiques** : Chart.js
- **Icônes** : Font Awesome 6.4.0
- **Frontend** : HTML5, CSS3 (responsive design), JavaScript
- **Déploiement** : Docker + Docker Compose, Caddy (reverse proxy avec HTTPS automatique)
- **Python** : 3.11+

## 📂 Structure du Projet

```
facturation/
├── app.py                    # Application Flask avec routes et authentification
├── database.py               # Modèles SQLAlchemy (User, Receipt, Expense)
├── populate_db.py            # Script de génération de données de test
├── requirements.txt          # Dépendances Python
├── .gitignore               # Fichiers à ignorer par Git
├── Dockerfile               # Configuration Docker
├── docker-compose.yml       # Orchestration Docker (app + PostgreSQL + Caddy)
├── Caddyfile                # Configuration Caddy pour HTTPS automatique
│
├── templates/
│   ├── login.html           # Page de connexion
│   ├── admin.html           # Interface de gestion des utilisateurs
│   ├── account.html         # Page de profil utilisateur
│   ├── form.html            # Formulaire de génération de reçu
│   ├── add_expense.html     # Formulaire d'ajout de dépense
│   ├── dashboard.html       # Tableau de bord avec graphiques
│   └── receipt_template.html # Template HTML pour PDF
│
├── static/
│   └── css/
│       ├── style.css        # Styles globaux et navigation
│       ├── login.css        # Styles page de connexion
│       ├── admin.css        # Styles page admin
│       └── account.css      # Styles page compte
│
├── scripts/
│   └── migrate_add_user_id.py # Script de migration base de données
│
├── receipts/                # PDFs générés (créé automatiquement)
└── instance/
    └── data.db             # Base de données SQLite (créée automatiquement en dev)
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

### 6. Connexion Initiale

Lors du premier lancement, un compte administrateur est créé automatiquement :
- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin`

⚠️ **Important** : Changez le mot de passe admin dès votre première connexion depuis la page "Mon compte"

## 📖 Guide d'Utilisation

### Première Connexion

1. Aller sur http://localhost:5000
2. Connexion avec les identifiants admin par défaut :
   - Nom d'utilisateur : `admin`
   - Mot de passe : `admin`
3. Changer immédiatement le mot de passe depuis "Mon compte"

### Gérer les Utilisateurs (Admin)

1. Cliquer sur votre profil → **Gérer les utilisateurs**
2. Créer de nouveaux utilisateurs avec nom d'utilisateur et mot de passe
3. Les utilisateurs créés peuvent se connecter et gérer leurs propres données
4. Supprimer des utilisateurs (sauf le compte admin protégé)

### Générer un Reçu

1. Cliquer sur **Reçu** dans le menu
2. Remplir le formulaire :
   - **Nom du Client** : Nom complet ou entreprise
   - **Type de Paiement** : Récurrent ou Unique
   - **Raison** (si unique) : Description personnalisée
   - **Prix (FCFA)** : Montant numérique
   - **Montant en Lettres** : Montant écrit en toutes lettres
3. Cliquer sur **Générer PDF**
4. Le reçu se télécharge automatiquement et est associé à votre compte

### Enregistrer une Dépense

1. Cliquer sur **Dépense** dans le menu
2. Entrer la description et le montant
3. Cliquer sur **Ajouter Dépense**
4. La dépense est enregistrée et associée à votre compte
5. Redirection automatique vers le tableau de bord

### Consulter le Tableau de Bord

1. Cliquer sur **Tableau de bord** dans le menu
2. Choisir votre vue :
   - **Mes Données** : Vos reçus et dépenses uniquement
   - **Entreprise** : Données agrégées de toute l'équipe
3. Visualiser les cartes récapitulatives et les graphiques
4. Consulter les tableaux de transactions récentes

### Gérer votre Compte

1. Cliquer sur votre profil → **Mon compte**
2. Modifier votre nom d'utilisateur
3. Changer votre mot de passe (mot de passe actuel requis)

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

SQLite (développement) / PostgreSQL (production) avec trois tables :

**User (Utilisateurs)**
- `id`, `username` (unique), `password_hash`
- `created_at`

**Receipt (Reçus)**
- `id`, `receipt_number`, `customer_name`
- `description`, `payment_type`, `payment_reason`
- `price`, `amount_in_letters`, `date`
- `user_id` (foreign key vers User)

**Expense (Dépenses)**
- `id`, `description`, `amount`, `date`
- `user_id` (foreign key vers User)

## 🎨 Personnalisation

### Changer la Couleur d'Accentuation
Remplacer `#00bcd4` (cyan) dans `static/css/style.css` et `templates/receipt_template.html`

### Modifier les Graphiques
Éditer les options Chart.js dans `templates/dashboard.html`

### Personnaliser les Reçus
Modifier `templates/receipt_template.html` pour ajouter logo, champs personnalisés, etc.

## 🔒 Notes de Production

✅ L'application inclut déjà :
- **Authentification sécurisée** avec hashage des mots de passe
- **PostgreSQL** en production via Docker
- **HTTPS automatique** avec Caddy
- **Gunicorn** comme serveur WSGI
- **Variables d'environnement** pour les secrets
- **Docker Compose** pour orchestration

⚠️ Recommandations supplémentaires :
- Changez le mot de passe admin par défaut
- Configurez des sauvegardes automatiques de la base de données
- Ajoutez du rate limiting pour les endpoints sensibles
- Configurez des logs centralisés
- Mettez en place une surveillance (monitoring)

Voir `README-deploy-vps.md` pour le guide de déploiement complet sur VPS.

## 🚀 Déploiement

### Déploiement Docker (Recommandé)

L'application est prête pour le déploiement avec Docker :

```bash
# Configuration des variables d'environnement
cp .env.sample .env
# Éditer .env avec vos valeurs

# Lancer avec Docker Compose
docker-compose up -d
```

### Plateforme Compatible

- **VPS** (Ubuntu/Debian) avec Docker - Configuration incluse
- Render
- Railway  
- DigitalOcean App Platform
- AWS / GCP / Azure

Voir `README-deploy-vps.md` pour un guide détaillé de déploiement sur VPS.

## 🔮 Améliorations Futures

- [x] Authentification multi-utilisateurs
- [x] Gestion des utilisateurs (admin)
- [x] Vue personnelle vs entreprise
- [x] Design moderne et responsive
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
- [ ] Notifications en temps réel
- [ ] Permissions et rôles avancés

## 🤝 Contribution

Les contributions sont bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Changelog

**v3.0** (Novembre 2025)
- 🔐 Authentification multi-utilisateurs sécurisée
- 👥 Interface d'administration des utilisateurs
- 👤 Gestion de profil utilisateur
- 📊 Vue personnelle vs entreprise sur le tableau de bord
- 🗄️ Support PostgreSQL en production
- 🐳 Déploiement Docker avec Caddy
- 🎨 Design moderne avec effets glossy et animations
- 📱 Interface entièrement responsive
- 🇫🇷 Interface 100% en français
- 🔗 Association automatique utilisateur-données
- 🛡️ Protection du compte administrateur
- 📁 Architecture CSS modulaire (fichiers séparés par page)

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
Novembre 2025

---

**Made with ❤️ for Marate AI**

## 📸 Captures d'écran

- Page de connexion sécurisée avec design moderne
- Tableau de bord avec vue personnelle/entreprise
- Interface d'administration des utilisateurs
- Formulaires de génération de reçus et dépenses
- Graphiques interactifs avec Chart.js
- Menu profil avec gestion de compte
