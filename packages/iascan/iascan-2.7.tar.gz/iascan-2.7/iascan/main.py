

"""
Auteur : Aheshman Itibar
Version : 2.6
"""

import requests
import json
import argparse
from sys import exit
from re import findall, match
from time import sleep

# Définition de la fonction pour scanner une adresse IP
def scanner_ip(adresse_ip):
    if match("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", adresse_ip):
        try:
            entête = {"User-Agent": "Mozilla/5.0"}
            url = f"https://internetdb.shodan.io/{adresse_ip}"
            réponse = requests.get(url, headers=entête, timeout=20).text
            données = json.loads(réponse)
            afficher_résultats(données, adresse_ip)
        except requests.Timeout:
            print("Erreur de délai d'attente pour l'adresse IP :", adresse_ip)
        except requests.ConnectionError:
            print("Erreur de connexion pour l'adresse IP :", adresse_ip)
        except Exception as e:
            print(f"Erreur lors du scan de l'adresse IP {adresse_ip}: {e}")
    else:
        print("Adresse IP invalide :", adresse_ip)

# Fonction pour afficher les résultats
def afficher_résultats(données, adresse_ip):
    if 'detail' in données and données['detail'] == 'Aucune information disponible':
        print(f"Aucune information disponible pour l'adresse IP {adresse_ip}.")
    else:
        print(f"Résultats pour {adresse_ip}:")
        print(f"CPES: {', '.join(données.get('cpes', ['Non trouvés']))}")
        print(f"Hostnames: {', '.join(données.get('hostnames', ['Non trouvés']))}")
        print(f"IP: {données.get('ip', 'Non trouvée')}")
        print(f"Ports: {', '.join(map(str, données.get('ports', ['Non trouvés'])))}")
        print(f"Tags: {', '.join(données.get('tags', ['Non trouvés']))}")
        vulns = données.get('vulns', ['Non trouvées'])
        if vulns != ['Non trouvées']:
            print("Vulnérabilités :")
            for vuln in vulns:
                print(f"  - {vuln}")
        else:
            print("Vulnérabilités : Non trouvées")

# Configuration de l'analyse des arguments en ligne de commande
parser = argparse.ArgumentParser(description="Scanner des adresses IP.")
parser.add_argument("-ip", type=str, help="Adresse IP spécifique à scanner")
parser.add_argument("-list", type=str, help="Fichier contenant une liste d'adresses IP à scanner")
args = parser.parse_args()

def main():
    # Exécution basée sur les arguments
    if args.ip:
        scanner_ip(args.ip)
    elif args.list:
        with open(args.list, "r") as fichier:
            for ligne in fichier:
                scanner_ip(ligne.strip())
    else:
        print("Aucun argument fourni. Utilisez '-ip' pour scanner une adresse IP spécifique ou '-list' pour scanner des adresses à partir d'un fichier.")
        parser.print_help()

if __name__ == "__main__":
    main()