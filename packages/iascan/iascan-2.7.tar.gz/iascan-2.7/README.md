# iascan

`iascan` est un outil de balayage d'adresses IP conçu pour être simple et efficace. Il permet aux utilisateurs de scanner rapidement des adresses IP uniques ou des plages d'adresses IP pour collecter des informations de base sur les hôtes connectés.

## Installation

Pour installer `iascan`, exécutez simplement la commande suivante :

pip install iascan


Assurez-vous d'avoir `pip` installé et de l'utiliser avec une version de Python supérieure à 3.6.

## Utilisation

Pour scanner une adresse IP spécifique, utilisez la commande suivante :

iascan -ip 192.168.1.1



Pour scanner une liste d'adresses IP à partir d'un fichier, utilisez :

iascan -list ip_list.txt



Le fichier `ip_list.txt` doit contenir une adresse IP par ligne.

## Fonctionnalités

- Recherche d'adresses IP uniques.
- Balayage d'une liste d'adresses IP.
- Affichage des informations de base telles que les hostnames, les ports ouverts, les tags associés, et potentiellement les vulnérabilités connues.
- Utilisation simple en ligne de commande.

## Contribution

Les contributions à `iascan` sont les bienvenues ! Si vous avez des suggestions ou des améliorations, n'hésitez pas à ouvrir une issue ou une pull request sur notre dépôt GitHub à l'adresse suivante : [GitHub - iascan](https://github.com/yourusername/iascan).

## Licence

`iascan` est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
