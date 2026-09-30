# 🎨 Studio CSS Box-Shadow (PyQt5)

Un outil interactif permettant de concevoir visuellement des ombres portées CSS (`box-shadow`) et d'exporter directement le code propre et réutilisable dans vos projets Web.

---

## 🌟 Fonctionnalités

- **Ajustement en temps réel** :
  - Décalage horizontal et vertical ($X, Y$).
  - Rayon de flou (*Blur Radius*).
  - Rayon de diffusion (*Spread Radius*).
  - Opacité / Transparence de l'ombre en pourcentage.
- **Sélecteur de couleurs** :
  - Couleur de l'ombre avec canal Alpha (transparence).
  - Couleur de l'élément / bloc test.
- **Exportation rapide** :
  - Génération automatique du code CSS avec préfixe `-webkit-`.
  - Bouton de copie en un clic dans le presse-papier.

---

## 🛠️ Prérequis et Dépendances

L'application repose uniquement sur Python et PyQt5 :

```bash
pip install PyQt5