# Le modèle OSI

## Introduction

Le modèle OSI (Open Systems Interconnection) est un modèle de référence pour les communications entre ordinateurs. Il a été créé par l'ISO (International Organization for Standardization) en 1984.

Le modèle OSI est divisé en 7 couches, chacune ayant un rôle spécifique dans le processus de communication. Chaque couche communique avec les couches adjacentes pour transmettre les données.

## Les couches

La figure suivante illustre les 7 couches du modèle OSI en comparaison du PDU (Protocol Data Unit) associé à chaque couche et du modèle internet TCP/IP qui est apparu avant la standardisation du modèle OSI. En effet ce modèle est plus ancien et ne comporte que 4 couches et ses couches ne sont pas conformes au modèle OSI. En effet, comme nous le verrons plus tard, une pile de protocoles ne doit pas dépendre des protocoles des autres couches, or dans TCP/IP la somme de contrôle de la couche de transport fait intervenir une partie de l'en-tête IP.

![Modèle OSI](/assets/images/osi-model.drawio)

1. **Couche physique (Physical Layer)**: Cette couche est responsable de la transmission des données brutes sur le support de communication. Elle définit les caractéristiques électriques, mécaniques et fonctionnelles du matériel de communication.

2. **Couche liaison de données (Data Link Layer)**: Cette couche est responsable de la transmission des données entre les nœuds voisins sur le réseau local. Elle gère les erreurs de transmission, le contrôle de flux et l'accès au support.

3. **Couche réseau (Network Layer)**: Cette couche est responsable de la transmission des données entre les nœuds distants sur le réseau. Elle gère le routage des données à travers le réseau.

4. **Couche transport (Transport Layer)**: Cette couche est responsable de la transmission des données de bout en bout entre les applications. Elle gère le contrôle de flux, la segmentation et le réassemblage des données.

5. **Couche session (Session Layer)**: Cette couche est responsable de l'établissement, de la gestion et de la fin des sessions de communication entre les applications.

6. **Couche présentation (Presentation Layer)**: Cette couche est responsable de la traduction, de la compression et du chiffrement des données pour la communication entre les applications.

7. **Couche application (Application Layer)**: Cette couche est responsable de la communication entre les applications. Elle fournit des services de haut niveau tels que l'authentification, la messagerie et le partage de fichiers.

## Encapsulation

L'interopérabilité entre différents systèmes est souvent rendue possible grâce à un concept nommé encapsulation. C'est un concept également clé en programmation orientée objet. L'encapsulation consiste à dissimuler de la complexité non nécessaire à comprendre la partie intéressante d'un problème dans un ensemble isolé et qui peut être considéré comme *une boîte noire*.

En communication réseau, par exemple lorsque vous êtes au téléphone, vous n'avez pas besoin de savoir quelle est la nature de la ligne de transport qui véhicule votre voix. Est-ce une ligne de cuivre, une fibre optique, une liaison satellite, cela n'a pas d'importance. Néanmoins vous n'êtes que l'utilisateur final de cette communication, il y a d'autres étapes intermédiaires. Celle qui véhicule réellement votre voix accompagnée éventuellement de votre vidéo et des touches que vous appuyez sur votre téléphone. Cette étape est la couche application, son besoin c'est de pouvoir communiquer d'un téléphone à l'autre, le reste d'a pas d'importance. En dessous de cette couche, il y a la couche transport qui va s'occuper de découper les différentes données en paquets qui pourront être acheminés par différentes routes (via le Wi-Fi, le réseau cellulaire, etc.). Cette couche ne sait pas ce qu'elle transporte comme données et ne sait pas non plus sur quoi sont transportées ces données. Tout en bas de la pile, il y a la couche physique, c'est précisément le type de média qui est utilisé pour transporter les données (câble, fibre optique ...).

Vous imaginez probablement que les données sont transmises sous forme de bits, ce qui est vrai en partie. En effet, en transmission par câble ou sans fil, les données ne sont pas simplement des états logiques 0 ou 1, souvent elles sont modulées pour être transportées plus efficacement. Cela donne d'ailleurs le nom aux dispositifs qui s'occupent de moduler et démoduler les signaux, les [modems](https://fr.wikipedia.org/wiki/Modem).

L'encapsulation ici sert donc à découper les responsabilités. Si vous souhaitez véhiculer des bits d'un point à un autre, vous n'avez pas besoin de savoir comment cela se fait, vous devez juste vous reposer sur la couche physique.

## Protocoles Internet

La pile de protocoles Internet est assez complexe, mais elle est très bien documentée. Les RFC (*Request For Comments*) sont des documents qui décrivent les protocoles Internet. Ils sont publiés par l'IETF (*Internet Engineering Task Force*) et sont des standards de facto. Chaque protocole que l'on utilise pour communiquer sur un réseau informatique est décrit dans un RFC. Par exemple, le protocole HTTP (HyperText Transfer Protocol) responsable de communiquer les pages web visibles dans votre navigateur est décrit dans le [RFC 2616](https://tools.ietf.org/html/rfc2616). Ce protocole est encapsulé dans le protocole TCP normalisé par le [RFC 793](https://tools.ietf.org/html/rfc793) (Transmission Control Protocol) qui lui-même est encapsulé dans le protocole IP ([RFC 791](https://tools.ietf.org/html/rfc791)). Ce dernier est également encapsulé dans le protocole MAC [RFC 3422](https://tools.ietf.org/html/rfc3422) (Media Access Control) qui est lui-même encapsulé dans le protocole Ethernet ([RFC 894](https://tools.ietf.org/html/rfc894)).

!!! info "RFC"

    Un fait notable avec les RFC est le format de rédaction. Ces documents sont écrits en pur texte ASCII sans outils de mise en page. Ce n'est pas du Markdown, du Word, du LaTeX, c'est du texte brut mais très bien structuré avec des figures, des tables des matières, des références croisées, etc.

    La raison à cela est que les RFC sont des documents de référence et doivent être accessibles par tous et à toute époque. Les informaticiens savaient déjà que les formats de fichiers sont éphémères et que les outils de traitement de texte ne sont pas toujours compatibles entre eux. Le texte brut est donc le format le plus sûr pour garantir la pérennité des documents. Et ils ont raison car depuis 50 ans, les RFC sont toujours lisibles et utilisables.

En termes informatiques, et surtout en programmation, chaque protocole dispose de ses propres champs de données. Par exemple voici le la figure 3 du RFC 793 telle que publiée en 1981 :

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Ce schéma décrit l'en-tête du protocole TCP. Il est composé de plusieurs champs qui sont utilisés pour la communication entre les machines. On voit par exemple que ce protocole utilise la notion de **port** pour identifier les applications qui communiquent. Les ports sont des numéros qui sont attribués à chaque application. Par exemple, le port 80 est utilisé pour le protocole HTTP, le port 443 pour le protocole HTTPS, le 21 est utilisé pour le protocole FTP tandis que le port 22 est utilisé pour le protocole SSH. Outre les ports, les données peuvent être fragmentées en plusieurs paquets c'est pourquoi chaque paquet contient un numéro de séquence et un numéro d'acquittement. À la fin de l'en-tête se trouvent les données des couches supérieures.

Le protocole de transport TCP est basé sur le protocole IP. On trouve également dans son standard (RFC 791, figure 4) un en-tête similaire qui va contenir l'adresse IP (p. ex. 192.168.45.20) source et destination, le protocole utilisé en dessus (TCP, UDP, ICMP, etc.), la taille du paquet, etc.

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

En C, si l'on devait réimplémenter ces protocoles, on pourrait utiliser des structures. Voici par exemple comment on pourrait définir les en-têtes des protocoles MAC et IP :

```c
struct mac_header {
    uint8_t destination_mac[6];  // Adresse MAC de destination
    uint8_t source_mac[6];       // Adresse MAC source
    uint16_t ethertype;  // Protocole encapsulé (p. ex. 0x0800 pour IPv4)
};

struct ip_header {
    uint8_t version_ihl;
    uint8_t dscp_ecn;
    uint16_t total_length;
    uint16_t identification;
    uint16_t flags_fragment_offset;
    uint8_t ttl;                 // Time To Live (durée de vie)
    uint8_t protocol;            // Protocole de couche supérieure (ex. TCP = 6)
    uint16_t checksum;
    uint32_t source_ip;          // Adresse IP source
    uint32_t destination_ip;     // Adresse IP de destination
};
```

En pratique c'est plus complexe que cela, d'une part par que les données sont véhiculées en big-endian (octets de poids fort en premier) et que les champs de données sont de taille variable. Par exemple, l'adresse IP est codée sur 32 bits, mais elle peut être représentée en IPv4 (4 octets) ou en IPv6 (16 octets).

L'idée ici est juste de montrer l'intérêt des structures dans ce type de situation.
