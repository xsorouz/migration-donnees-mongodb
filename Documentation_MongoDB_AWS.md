
# Documentation : Déploiement de MongoDB sur AWS

## Introduction
Cette documentation explore les solutions pour déployer MongoDB sur AWS, en mettant en lumière les services appropriés, leurs avantages et leurs limitations. Elle propose une approche stratégique pour la migration des données vers le cloud et détaille les étapes nécessaires pour configurer un environnement AWS.

---

## 1. Objectif
- Identifier les meilleures solutions pour héberger MongoDB sur AWS.
- Comparer les services Amazon DocumentDB, ECS et EC2.
- Proposer une stratégie de sauvegarde et de surveillance pour garantir la sécurité et la performance des données.

---

## 2. Services AWS pertinents

### 2.1 Amazon DocumentDB
- **Description** : Base de données entièrement gérée, compatible MongoDB, avec des sauvegardes automatiques et une haute disponibilité.
- **Avantages** :
  - Maintenance automatisée (patching, sauvegardes).
  - Haute scalabilité avec réplicas en lecture.
  - Sécurité intégrée (chiffrement des données au repos et en transit).
- **Limites** :
  - Compatibilité partielle avec MongoDB (certaines fonctionnalités ne sont pas supportées).
- **Cas d’utilisation recommandé** : Grandes bases nécessitant une disponibilité élevée et une gestion simplifiée.

### 2.2 Amazon ECS (Elastic Container Service)
- **Description** : Service pour exécuter des applications conteneurisées à l’aide de Docker.
- **Avantages** :
  - Intégration facile avec d'autres services AWS (S3, CloudWatch).
  - Flexibilité pour configurer MongoDB selon les besoins spécifiques.
  - Gestion simplifiée des conteneurs à l’échelle.
- **Limites** :
  - Nécessite une configuration manuelle pour les sauvegardes et la réplication.
- **Cas d’utilisation recommandé** : Solutions conteneurisées avec des besoins spécifiques non couverts par DocumentDB.

### 2.3 Amazon EC2 (Elastic Compute Cloud)
- **Description** : Instances virtuelles pour héberger MongoDB directement sur une machine virtuelle.
- **Avantages** :
  - Contrôle total sur la configuration et l'installation de MongoDB.
  - Possibilité de personnaliser entièrement l'environnement.
- **Limites** :
  - Nécessite une gestion manuelle (patching, sauvegardes).
- **Cas d’utilisation recommandé** : Scénarios nécessitant une personnalisation avancée et un contrôle total.

### 2.4 Amazon S3 (Simple Storage Service)
- **Description** : Service de stockage pour sauvegarder les fichiers CSV ou les bases MongoDB.
- **Avantages** :
  - Haute durabilité des données (11 9’s de durabilité).
  - Tarification flexible basée sur la quantité de stockage.
  - Intégration avec d'autres services AWS (CloudWatch, Lambda).
- **Cas d’utilisation recommandé** : Sauvegardes régulières des bases de données et stockage des fichiers source.

---

## 3. Sauvegardes et surveillance

### 3.1 Sauvegardes automatiques
- Configurez des sauvegardes régulières de MongoDB vers Amazon S3.
- Utilisez des outils natifs comme `mongodump` pour exporter les bases et les stocker dans un bucket S3.

### 3.2 Surveillance des performances
- Utilisez Amazon CloudWatch pour surveiller les performances des instances ou des conteneurs MongoDB.
- Configurez des alarmes pour détecter des anomalies ou des pannes.

---

## 4. Comparaison des solutions

| **Service**           | **Avantages**                                  | **Limites**                                  | **Cas d’utilisation**                        |
|-----------------------|-----------------------------------------------|---------------------------------------------|---------------------------------------------|
| **Amazon DocumentDB** | Gestion automatisée, haute disponibilité.     | Compatibilité partielle avec MongoDB.       | Solutions nécessitant une gestion simplifiée. |
| **Amazon ECS**        | Flexibilité, conteneurisation.                | Configuration manuelle requise.             | Déploiements Docker complexes.              |
| **Amazon EC2**        | Contrôle total, personnalisation complète.    | Gestion manuelle des sauvegardes.           | Besoins spécifiques et contrôle total.      |

---

## 5. Tarification
- **Amazon DocumentDB** : Basé sur le nombre d'instances, le stockage utilisé, et les IOPS.
- **Amazon ECS** : Tarification liée aux tâches et instances utilisées.
- **Amazon S3** : Coût de stockage en fonction des gigaoctets utilisés.

Pour une simulation des coûts, utilisez le [AWS Pricing Calculator](https://calculator.aws).

---

## 6. Étapes pour commencer avec AWS
1. **Créer un compte AWS** :
   - Inscrivez-vous sur [aws.amazon.com](https://aws.amazon.com).
   - Activez le niveau gratuit pour tester les services.
2. **Configurer les services** :
   - Créez un bucket S3 pour les sauvegardes.
   - Déployez MongoDB avec Amazon ECS ou EC2 selon vos besoins.
3. **Planifier une stratégie de sauvegarde** :
   - Automatisez les sauvegardes avec des scripts.
   - Configurez CloudWatch pour surveiller les performances.

---

## 7. Recommandation finale
Pour une solution clé en main avec peu de gestion manuelle, **Amazon DocumentDB** est recommandé. Cependant, si le client privilégie la flexibilité et le contrôle, **Amazon ECS** ou **EC2** sont des alternatives viables.

---

## 8. Schéma d'architecture proposé
Un schéma d'architecture est essentiel pour visualiser comment les services AWS interagissent dans une solution MongoDB. Voici une proposition basique :
1. Amazon ECS héberge MongoDB dans un conteneur Docker.
2. Amazon S3 est utilisé pour stocker les sauvegardes de la base de données.
3. Amazon CloudWatch surveille les performances de MongoDB et envoie des alertes en cas d'anomalies.
4. Les sauvegardes automatisées sont programmées via des scripts déclenchés par des tâches ECS ou Lambda.

---

## 9. Exemples pratiques

### 9.1 Commandes AWS CLI
- Créer un bucket S3 :
  ```bash
  aws s3 mb s3://nom-du-bucket
  ```
- Lister les buckets S3 :
  ```bash
  aws s3 ls
  ```
- Déployer une tâche ECS :
  ```bash
  aws ecs create-cluster --cluster-name NomDuCluster
  ```
- Lister les clusters ECS :
  ```bash
  aws ecs list-clusters
  ```
- Créer une instance EC2 :
  ```bash
  aws ec2 run-instances --image-id ami-123456 --count 1 --instance-type t2.micro
  ```

### 9.2 Étapes détaillées pour ECS
1. Créez un cluster ECS :
   ```bash
   aws ecs create-cluster --cluster-name MongoDBCluster
   ```
2. Créez une définition de tâche pour MongoDB :
   ```bash
   aws ecs register-task-definition --cli-input-json file://definition.json
   ```
3. Déployez la tâche :
   ```bash
   aws ecs run-task --cluster MongoDBCluster --task-definition MongoDBTask
   ```
4. Configurez des volumes pour stocker les données persistantes.

---

## 10. Étude de cas : Déploiement sur ECS
Supposons que nous devons déployer une base MongoDB pour un client avec 1 To de données et une croissance mensuelle de 10 %. Voici les étapes :
- Configurez un cluster ECS pour héberger MongoDB avec au moins deux conteneurs répliqués.
- Utilisez Amazon S3 pour sauvegarder les données toutes les nuits.
- Surveillez la charge avec CloudWatch et ajustez le nombre de conteneurs si nécessaire.
- Simulez les coûts avec AWS Pricing Calculator en prenant en compte les données stockées et les conteneurs.

---

## 11. Estimation des coûts
Voici une estimation rapide des coûts pour un scénario hypothétique :
- **Amazon ECS** :
  - Cluster ECS avec deux conteneurs : 0,1 USD/heure * 2 conteneurs * 720 heures = 144 USD/mois (environ 133 EUR/mois).
- **Amazon S3** :
  - Stockage de 1 To : environ 23 USD/mois (environ 21 EUR/mois).
- **Amazon CloudWatch** :
  - Surveillance de base : environ 10 USD/mois (environ 9 EUR/mois).

**Total estimé : ~177 USD/mois (~163 EUR/mois).**

---
