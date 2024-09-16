# Protocoles

Cet ouvrage n'étant pas un cours consacré au réseau, il n'est pas raisonnable d'y consacrer plus d'un chapitre. Néanmoins, l'ingénieur développeur en C devra tout de même comprendre, du moins conceptuellement les différences entre les différents protocoles de communication, comment ils sont imbriqués et à quoi ils servent. *in fine* en programmation vous aurez probablement simplement besoin de savoir comment ouvrir une connexion TCP ou UDP, comment envoyer des données et comment les recevoir.

## MAC

Chaque carte réseau installée dans un ordinateur, un téléphone portable ou une tablette possède une adresse physique unique appelée adresse MAC (*Media Access Control*). Cette adresse est codée sur 48 bits (6 octets) et est attribuée par le fabricant de la carte. Ce dernier obtient un OUI (*Organizationally Unique Identifier*) qui est un préfixe de 24 bits attribué par l'IEEE (*Institute of Electrical and Electronics Engineers*) à une organisation. Avec un OUI, le fabricant peut gérer jusqu'à 16 millions d'adresses MAC. Les 24 bits restants sont attribués par le fabricant lui-même. Obtenir un OUI coûte environ 2 700 dollars. Ceci explique pourquoi les Raspberry PI ont des adresses MAC qui commencent par `b8:27:eb` qui est l'OUI de la fondation Raspberry PI.

À moins de vouloir communiquer directement avec une carte réseau, l'adresse MAC n'est pas très utile pour un développeur. En effet, c'est le système d'exploitation qui se charge de gérer les communications réseau et qui va utiliser l'adresse IP pour identifier les machines. L'adresse MAC c'est un peu comme la coordonnée GPS d'une maison. Elle est utile au cadastraliste pour identifier un terrain et y attribuer une adresse postale, mais pour le facteur, c'est l'adresse postale qui est utile.

## IP

Un réseau informatique c'est un groupement de machines qui communiquent entre elles. Mettez 8 milliards de personnes dans la même salle, donnez-leur un porte-voix assez puissant et vous aurez un réseau. Vous admettrez néanmoins qu'arbitrer les échanges pour que chacun puisse parler à son tour est irréalisable. En outre, cela ne vous intéresse probablement guère de savoir que Madame Michu a gagné 5 francs au Tribolo. C'est pourquoi les réseaux informatiques sont organisés en sous-réseau.

Les ingénieurs système utilisent le protocole IP pour associer à une adresse MAC donnée une adresse IP. L'adresse IP est une adresse logique attribuée à chaque machine sur un réseau. Elle est historiquement codée sur 32-bits et permettant ainsi d'identifier environ 4 milliards de machines. Avec l'explosion de l'Internet, cette taille est devenue très largement insuffisante. C'est pourquoi un nouveau protocole, IPv6 (version 6) a été créé. Ce protocole utilise des adresses codées sur 128 bits et permet d'identifier 340 sextillions de machines. C'est largement suffisant pour attribuer une adresse IP à chaque grain de sable sur Terre. Néanmoins les adresses IPv6 sont moins facilement mémorisables que les adresses IPv4. C'est pourquoi ces dernières sont encore largement utilisées dans des réseaux privés ou d'entreprise.

Un périphérique IP peut être cloisonné facilement en plusieurs sous-réseaux grâce à un masque de sous-réseau. Par exemple, le périphérique à l'adresse IP 192.168.1.42 avec un masque de sous-réseau 255.255.255.0 ne va s'intéresser qu'aux périphériques de la plage 192.168.1.0 à 192.168.1.255. Cela permet à la carte réseau de filtrer les paquets qui lui sont destinés et de ne pas s'intéresser aux autres. Pour reprendre notre analogie, c'est comme si vous aviez sur vos oreilles un casque antibruit qui ne laisse passer que certaines voix.

Il y a deux types d'adresses IP, celles dites publiques et routables sur Internet et celles dites privées qui sont utilisées dans les réseaux locaux. Les adresses privées sont définies par la [RFC 1918](https://tools.ietf.org/html/rfc1918) et sont les suivantes :

| Plage d'adresses | Masque de sous-réseau         | Classe |
| ---------------- | ----------------------------- | ------ |
| 10.0.0.0         | 10.255.255.255  (10/8)        | A      |
| 172.16.0.0       | 172.31.255.255   (172.16/12)  | B      |
| 192.168.0.0      | 192.168.255.255  (192.168/16) | C      |

Il est très probable que l'adresse IP de votre ordinateur ou de votre téléphone sur le réseau de votre domicile ou celui de votre travail soit l'une de ces adresses. Elles ne sont pas routables c'est-à-dire qu'elles ne peuvent pas être transportées en dehors du réseau local.

Pour communiquer publiquement, il faut utiliser une adresse IP publique. Ces adresses sont attribuées par les fournisseurs d'accès à Internet (FAI) et sont gérées par l'IANA (*Internet Assigned Numbers Authority*). Chez vous, vous avez probablement une adresse IP publique attribuée par votre FAI (Salt, Swisscom, Sunrise, Orange...) c'est l'adresse attribuée à votre routeur ou box.

À votre travail ou dans votre école, c'est pareil. Une école n'a pas les moyens ni l'intérêt d'avoir une adresse IP publique pour chaque ordinateur. Elle dispose d'une certaine quantité d'adresses IP publiques utilisées pour communiquer vers l'extérieur. Si par exemple vous allez sur le site [showmyip.com](https://www.showmyip.com/), vous pouvez voir l'adresse IP publique utilisée pour communiquer sur internet.

### NAT / PAT

On peut se demander comment les données en provenance d'internet peuvent arriver jusqu'à votre ordinateur si tout le monde dans une même institution à la même adresse. C'est là qu'intervient le NAT (*Network Address Translation*), plus précisément dans notre cas le PAT (*Port Address Translation*). Il s'agit d'un dispositif qui va traduire les adresses IP privées en adresses IP publiques. Admettons que j'aimerais envoyer un message à Monsieur Google à l'adresse 1600 Amphi-theatre Parkway, Mountain View, CA 94043, USA. Pour simplifier disons simplement que son adresse est : `142.250.203.110:80443`. Le `80443` est le numéro du port utilisé. C'est un peu comme le numéro de l'appartement dans un immeuble. Comme je crois dur comme fer à l'encapsulation, je vais indiquer sur l'enveloppe au dos de l'enveloppe l'adresse de l'expéditeur, c'est-à-dire mon adresse. Je vais donc écrire quelque chose comme : `192.168.1.42:7878`. Or, vous l'aurez compris, cette adresse n'est pas routable sur internet et Monsieur Google ne saura pas où me répondre. C'est pareil que dire que le trésor se cache sous la troisième pierre à droite du vieux chêne. Sans savoir dans quelle forêt, dans quelle contrée et dans quel pays chercher, vous ne deviendrez pas riche.

Néanmoins, rappelez-vous du NAT. Vous avez un gentil facteur qui, avant que votre lettre ne soit postée en direction des Amériques, va réécrire l'adresse de l'expéditeur. Il va mettre par exemple : `193.134.219.72:57898`. Il s'agit de l'adresse IP publique de votre institution. Quant au port, il a été choisit aléatoirement par le facteur. C'est un peu comme si le facteur avait mis un numéro de boîte postale disponible. Bien entendu il notera dans un cahier que cette boîte postale (ce port) est réservée à la réponse de Monsieur Google et qu'il vous est destiné.

Vous l'aurez compris, il n'existe pas de facteur. C'est un dispositif informatique nommé **routeur** qui se charge de faire cette traduction. C'est le routeur qui se charge de cette tâche. Il va traduire l'adresse IP privée en adresse IP publique et va conserver dans une table de traduction l'adresse IP privée et le port utilisé. Lorsque la réponse de Monsieur Google arrivera, le routeur va regarder dans sa table de traduction et va savoir à qui renvoyer la réponse. C'est un peu comme si le facteur avait un cahier avec les noms des destinataires et les numéros de boîtes postales.

Sur votre machine Linux, vous pouvez voir les connexions en cours avec `conntrack`, on y voir le type de socket (TCP, UDP), l'adresse IP source et destination, le port source et destination, et la traduction. Pour la première connexion, on voit une adresse source privée, mais une adresse de destination publique. C'est une connexion sortante. Le port de destination `34230` est probablement attribué par le mécanisme de PAT du routeur du destinataire.

```bash
➜ sudo conntrack -L
tcp      6 95 SYN_SENT src=172.24.167.101 dst=169.254.169.254 sport=34230
         dport=80 [UNREPLIED] src=169.254.169.254 dst=172.24.167.101
         sport=80 dport=34230 mark=0 use=1
udp      17 23 src=10.255.255.254 dst=10.255.255.254 sport=41319
         dport=53 src=10.255.255.254 dst=10.255.255.254
         sport=53 dport=41319 mark=0 use=1
tcp      6 99 SYN_SENT src=172.24.167.101 dst=169.254.169.254 sport=57376
         dport=80 [UNREPLIED] src=169.254.169.254 dst=172.24.167.101
         sport=80 dport=57376 mark=0 use=1
...
```

Ce mécanisme de NAT/PAT intervient à de multiples strates. Tout d'abord au niveau d'un programme complexe comme Docker qui va créer des réseaux virtuels pour isoler les conteneurs. Ensuite au niveau de votre système d'exploitation pour gérer les connexions entre les différents programmes. En effet votre PC ou votre Mac à une seule carte réseau partagée par tous les programmes. Enfin, au niveau de votre routeur qui va gérer les connexions entre votre réseau local et internet. La situation se répète de l'autre côté de l'atlantique chez Monsieur Google (du routeur à la machine, de la machine au programme...).

### DHCP

Lorsque vous connectez un périphérique à un réseau local, il a besoin d'une adresse IP. Dans de rares cas, c'est de votre responsabilité de choisir une adresse, mais comme vous ne connaissez probablement pas la configuration du réseau, vous ne saurez pas choisir une adresse valide qui n'est pas utilisée par quelqu'un d'autre. C'est le rôle du protocole DHCP (*Dynamic Host Configuration Protocol*) qui permet à un périphérique de demander une adresse IP. Le serveur DHCP va attribuer une adresse IP à ce périphérique pour une durée déterminée. Une fois allouée, vous pouvez communiquer sur le réseau.

Le serveur DHCP va stocker dans une table la correspondance entre l'adresse MAC du périphérique et l'adresse IP attribuée. Ces informations sont complétées par un bail DHCP (*DHCP Lease*) qui est la durée pendant laquelle l'adresse IP est attribuée. Une fois le bail expiré, le périphérique doit renouveler son bail pour continuer à communiquer. Selon la configuration du serveur DHCP, il peut attribuer la même adresse IP ou une nouvelle adresse. C'est pour cette raison que parfois votre adresse IP change toute seule.

Ce que vous devez savoir en tant que développeur, c'est que vous pouvez soit disposer d'une adresse IP statique, c'est-à-dire que votre adresse est stockée en dur dans la configuration de votre machine, soit d'une adresse IP dynamique, c'est-à-dire que votre adresse est attribuée par un serveur DHCP. Dans la très grande majorité des cas, c'est la deuxième option qui est utilisée.

La plupart du temps un serveur DHCP récupère également le nom de l'hôte (*hostname*), c'est-à-dire le nom de la machine.

### ARP

Nous avons vu qu'une fois dans un réseau local et que chacun a une adresse IP, il est possible de communiquer. On profite de l'encapsulation des protocoles pour faire transiter les données d'une machine à une autre sans se soucier des couches inférieures. Néanmoins, il reste un problème à résoudre.

IP est basé sur le protocole Ethernet. Chaque paquet IP est encapsulé dans un paquet Ethernet lequel contient l'adresse MAC source et destination. Vous devez donc connaître l'adresse MAC de la machine à qui vous souhaitez envoyer des données.

C'est le protocole ARP (*Address Resolution Protocol*) qui permet de faire la correspondance entre une adresse IP et une adresse MAC. Lorsque vous souhaitez communiquer avec une machine, vous envoyez un message ARP en broadcast sur le réseau (à tout le monde). Toutes les machines du réseau reçoivent ce message et celle qui possède l'adresse IP demandée répond avec son adresse MAC.

Évidemment si dix-mille ordinateurs sont dans le même sous réseau, ils ne vont pas envoyer un message *broadcast* avant chaque transmission. Chaque ordinateur conserve sa propre table ARP qui contient les correspondances entre les adresses IP et les adresses MAC qu'il connaît. C'est seulement lorsque l'adresse MAC n'est pas dans la table ou lorsque l'adresse IP change qu'une requête ARP sera envoyée.

!!! info "ARP Flood"

    Il existe une attaque informatique nommée *ARP Flood* qui consiste à envoyer un grand nombre de requêtes ARP sur un réseau pour saturer les tables ARP des machines. Cela peut être utilisé pour empêcher les machines de communiquer entre elles.

    Puisque les requêtes ARP sont diffusées en *broadcast*, tous les appareils du réseau les reçoivent.

    Heureusement les routeurs et les switchs modernes sont capables de détecter et de bloquer ce type d'attaque en limitant le nombre de requêtes ARP par seconde ou en blocant les adresses MAC suspectes.

Sous Linux vous pouvez consulter la table ARP avec la commande `ip neigh show` et sous Windows vous pouvez utiliser `arp -a`.

### ICMP

Le protocole ICMP (*Internet Control Message Protocol*) est un protocole qui permet de communiquer des messages de contrôle et d'erreur entre les machines. Par exemple, si vous essayez de communiquer avec une machine qui n'existe pas, vous allez recevoir un message ICMP de type *Destination Unreachable*.

C'est ce protocole qui permet de faire des pings pour tester la connectivité entre deux machines. Le *ping* est un message ICMP de type *Echo Request* qui est envoyé à une machine. Si la machine est connectée et qu'elle est configurée pour répondre aux pings, elle va renvoyer un message ICMP de type *Echo Reply*.

Dans la majorité des cas en ingénierie et durant le développement, les machines sont configurées pour répondre aux pings. Si vous connectez un Raspberry PI sur votre réseau local, vous pourrez le *pinger* avec la commande `ping 192.168.1.142` (où l'adresse IP est celle de votre Raspberry PI).

Vous pouvez également envoyer une requête ICMP sur un serveur public comme Google. On voit ci-dessous que le serveur répond aux pings et que le temps de réponse est d'environ 3 ms. On découvre également que l'adresse IP est 142.250.203.110

```c
➜ ping google.com
PING google.com (142.250.203.110) 56(84) bytes of data.
64 bytes from zrh04s16.net (142.250.203.110): icmp_seq=1 ttl=111 time=3.38 ms
64 bytes from zrh04s16.net (142.250.203.110): icmp_seq=2 ttl=111 time=3.35 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 2203ms
```

Des services de localisation permettent de savoir où se trouve une adresse IP. Par exemple, l'adresse IP `142.250.203.110` est attribuée à Google et est située à Zurich en Suisse. Il s'agit de l'adresse d'un *datacenter*.

Lorsque vous mettez un serveur privé sur internet. Vous voulez probablement qu'il ne réponde pas aux pings. En effet, un attaquant pourrait envoyer des pings à des adresses IP aléatoires pour découvrir les serveurs actifs. Une fois qu'il sait que votre machine répond, il peut essayer de le pirater. Désactiver le ping sous Linux se fait en modifiant le fichier `/etc/sysctl.conf` et en ajoutant la ligne `net.ipv4.icmp_echo_ignore_all = 1`.

!!! info "Traceroute"

    Le protocole ICMP est également utilisé par la commande `traceroute` qui permet de suivre le chemin emprunté par un paquet entre deux machines. La commande envoie des paquets ICMP avec un TTL (*Time To Live*) de 1, 2, 3, ... jusqu'à ce que le paquet atteigne sa destination. Chaque routeur sur le chemin va décrémenter le TTL et lorsqu'il atteint 0, il va renvoyer un message ICMP de type *Time Exceeded* à l'expéditeur. C'est ainsi que l'on peut voir le chemin emprunté par un paquet entre deux machines.

    ```bash
    traceroute to 142.250.203.110, 30 hops max, 60 byte packets
    1  172.24.160.1  0.246 ms  0.216 ms  0.207 ms
    2  10.192.77.1  0.444 ms  0.535 ms  0.425 ms
    3  10.193.255.34  0.815 ms  0.806 ms  0.799 ms
    4  10.193.255.102 0.989 ms  0.977 ms  0.966 ms
    5  185.144.39.4  1.176 ms  1.164 ms  1.155 ms
    6  rchon01-te-0-0-2_81.as203130.ch  1.046 ms  1.253 ms  1.224 ms
    7  swiyv2-ge-0-0-0-0.hessoadm.ch  2.078 ms  1.937 ms  1.822 ms
    8  swiNE1-10GE-0-0-2-3.switch.ch  2.401 ms  2.179 ms  2.285 ms
    9  swiNE2-10GE-0-0-1-1.switch.ch  4.419 ms  4.409 ms  4.403 ms
    10  swiBI1-10GE-0-0-0-18.switch.ch  3.170 ms  2.996 ms  3.333 ms
    11  swiZH3-100GE-0-0-0-1.switch.ch  3.776 ms  3.660 ms  3.626 ms
    12  72.14.242.82  3.825 ms  3.817 ms  3.814 ms
    13  * * *
    14  172.253.50.20  4.565 ms 172.253.50.22 5.579 ms
        zrh04s16-in-f14.1e100.net (142.250.203.110)  3.852 ms
    ```

    Le `* * *` indique que le routeur ne répond pas aux requêtes ICMP. C'est une configuration courante pour les routeurs de gros fournisseurs de services internet. Ci-dessus on voit que de 1 à 4, les routeurs sont dans le réseau local. `185.144.39.4` appartient à la HEIG-VD puis elle transite par la HES-SO en 7 pour arriver chez Switch à Zurich en 8. En 12 on voit que le paquet est transmis à Google.

## UDP

Le protocole UDP (*User Datagram Protocol*) est un protocole de transport qui permet de transmettre des données sans garantie de livraison. C'est un protocole simple qui ne gère pas la retransmission des paquets perdus. Il est utilisé pour les applications qui n'ont pas besoin d'une communication fiable. Par exemple, le protocole DNS utilise UDP pour transmettre les requêtes de résolution de noms de domaines. Les flux vidéos (streaming) utilisent également UDP pour transmettre les données, car il n'est pas grave de perdre quelques images si cela permet de réduire la latence et le trafic réseau.

Le protocole est relativement simple. Il est défini par la RFC 768 son en-tête est très simple :

```text
                  0      7 8     15 16    23 24    31
                 +--------+--------+--------+--------+
                 |          source address           |
                 +--------+--------+--------+--------+
                 |        destination address        |
                 +--------+--------+--------+--------+
                 |  zero  |   17   |   UDP length    |
                 +--------+--------+--------+--------+
                               Trame IP

                  0      7 8     15 16    23 24    31
                 +--------+--------+--------+--------+
                 |   Source Port   |   Dest. Port    |
                 +--------+--------+--------+--------+
                 |     Length      |    Checksum     |
                 +--------+--------+--------+--------+
                 |                                   |
                 |          Data (payload)           |
                 |                                   |
                 +-----------------------------------+
                              Trame UDP
```

On y trouve l'adresse IP source et destination, un champ réservé à zéro, le protocole utilisé (17 pour UDP), et la longueur du paquet sur 16 bits. Un paquet UDP à donc une taille maximale de 65'535 octets (ou 65 Kio). Avec un en-tête de 8 octets, cela laisse 65'527 octets pour les données. En pratique le MTU (*Maximum Transmission Unit*) des réseaux Ethernet est de 1500 octets, c'est-à-dire qu'un paquet UDP plus grand sera fragmenté au niveau de la couche IP. Comme UDP n'a pas de mécanisme pour garantir la livraison des paquets, dans le cas où un fragment est perdu, l'intégralité du paquet l'est également.

L'en-tête UDP contient le port de source et le port de destination. On peut noter également que le paquet UDP contient un champ `length` correspondant à la taille des données et de l'en-tête. Néanmoins, on constate qu'il y a déjà cette information dans la trame IP. Cette redondance est le résultat de l'encapsulation des protocoles et de la séparation des responsabilités. Cela crée de *l'overhead*, c'est-à-dire que la quantité d'information utile doit être augmentée pour contenir les informations de routage et de contrôle. Au final c'est la même chose avec les lettres papier. Le poids de l'encre par rapport au support (le papier, l'enveloppe, le timbre) et au camion du postier est très faible.

## TCP

Le protocole TCP (*Transmission Control Protocol*) est un protocole de transport qui permet de transmettre des données de manière fiable. On dit que le protocole est connecté (*connection-oriented*), car il établit une connexion entre les deux machines avant de transmettre les données. C'est un protocole complexe qui gère la retransmission des paquets perdus, le contrôle de flux, le contrôle de congestion, etc.

L'établissement d'une connexion TCP se fait avec un *3-way handshake* (une poignée de main à trois). Le client envoie un paquet SYN (*synchronize*) à la machine distante. La machine distante répond avec un paquet SYN-ACK (*synchronize-acknowledge*). Enfin, le client répond avec un paquet ACK (*acknowledge*) et la connexion est établie. Une fois la connexion établie, du point de vue d'un programme c'est comme si un tuyau avait été posé entre les deux machines. Pour envoyer des données, il suffit de les écrire dans le tuyau et elles sortiront de l'autre côté. Bien entendu les données pourraient être perdues, fragmentées en plusieurs paquets, émises par câble sous-marin ou par satellite, mais pour le programme c'est transparent. Lui, il a la garantie que les données arriveront dans l'ordre et sans erreur.

C'est pourquoi le protocole TCP est le plus utilisé. De nombreux protocoles l'utilisent :

- HTTP (port 80) pour les pages web;
- HTTPS (port 443) pour les pages web sécurisées;
- FTP (port 21) pour le transfert de fichiers;
- SSH (port 22) pour les connexions sécurisée à distance;
- SMTP (port 25) pour l'envoi de courriels;
- MQTT (port 1883) pour l'IoT, etc.

## DNS

Le protocole DNS (*Domain Name System*) est un protocole basé sur UDP qui permet de faire la correspondance entre un nom de domaine et une adresse IP. Par exemple, lorsque vous tapez `google.com` dans votre navigateur, votre ordinateur va envoyer une requête DNS pour obtenir l'adresse IP de Google. Une fois l'adresse IP obtenue, votre ordinateur va pouvoir communiquer avec le serveur de Google pour obtenir la page d'accueil.

Les noms de domaines sont arbitrés par l'ICANN (*Internet Corporation for Assigned Names and Numbers*) qui attribue les noms de domaines de premier niveau (TLD) comme `.com`, `.org`, `.net`, etc. Les noms de domaines de deuxième niveau (SLD) sont attribués par des registres de noms de domaines. Par exemple, le registre de noms de domaines pour la Suisse est SWITCH qui attribue les noms de domaines en `.ch`.

Le protocole DNS est basé sur le protocole UDP et utilise le port 53. Lorsque vous voulez disposer de votre propre serveur, vous allez déposer une requête auprès votre NIC (*Network Information Center*) pour obtenir un nom de domaine. Vous allez ensuite configurer votre serveur DNS pour faire la correspondance entre votre nom de domaine et une adresse IP.

On parle de résolution de nom lorsque l'on veut obtenir l'adresse IP d'un nom de domaine et de résolution inverse lorsque l'on veut obtenir le nom de domaine à partir d'une adresse IP. Chaque institution dispose de son propre serveur DNS qui va gérer les requêtes pour les noms de domaines qu'il connaît. Depuis votre ordinateur assis à votre bureau, vous pouvez envoyer une requête DNS à votre serveur DNS local, lequel va se charger de faire la résolution pour vous. Il pourrait répondre directement ou bien il pourrait envoyer une requête à un serveur DNS de niveau supérieur. Il y a donc une hiérarchie de serveurs DNS qui permet de résoudre les noms de domaines. Le problème c'est combien de temps est-ce qu'une entrée DNS est conservée en cache. Si vous changez l'adresse IP de votre serveur, vous allez mettre à jour les informations du domaine, mais il faudra attendre que les caches DNS soient invalidés pour que tout le monde puisse accéder à votre site. Ce paramètre est appelé le TTL (*Time To Live*) et est configuré par le propriétaire du domaine. Il est souvent de 24 heures pour les sites web, mais il peut être plus court pour les services critiques.

Une entrée DNS peut être de la forme suivante ou le nom de domaine HEIG-VD est associé à l'adresse IP `193.134.219.72` avec un temps de vie de 86400 secondes (24 heures) :

```
www.heig-vd.ch.  86400  IN  A  193.134.219.72
```

Un serveur DNS peut également fonctionner au sein d'une institution pour gérer les noms des serveurs internes. Par exemple, si vous avez un serveur de base de données nommé `eistore0` dans votre entreprise, vous pouvez configurer votre serveur DNS pour que ce nom soit associé à l'adresse IP de votre serveur.

## HTTP

Le protocole HTTP (*HyperText Transfer Protocol*) est un protocole de la couche application qui permet de transférer des données sur le web. Il est basé sur le protocole TCP et utilise le port 80. Le protocole est défini par la RFC 2616 et est un protocole texte. C'est-à-dire que les données sont transmises en clair et que les en-têtes sont des chaînes de caractères.

Lorsque vous demandez la page d'accueil de Google, votre navigateur va envoyer une requête HTTP de type GET à l'adresse `http://www.google.com/`. Cette requête aura possiblement la forme suivante :

```http
GET / HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```

La réponse du serveur sera un message HTTP de type 200 OK avec le contenu de la page d'accueil.

```http
HTTP/1.1 200 OK
Date: Tue, 15 Jun 2021 08:00:00 GMT
Server: Apache/2.4.46 (Unix)
Last-Modified: Tue, 15 Jun 2021 07:00:00 GMT
Content-Length: 1234
Content-Type: text/html

<!DOCTYPE html>
...
```

Le code de retour `200` indique que la requête a été traitée avec succès. Il existe de nombreux autres codes organisés en cinq catégories :

- 1xx : Information
- 2xx : Succès
- 3xx : Redirection
- 4xx : Erreur client
- 5xx : Erreur serveur

On retrouve l'erreur `404` pour indiquer que la page n'a pas été trouvée, `403` pour indiquer que l'accès est interdit, `500` pour indiquer une erreur interne du serveur, etc. Plus amusant, on trouve le code `418` pour indiquer que le serveur est une théière. C'est un code d'erreur qui n'est pas vraiment utilisé, mais qui est défini par la RFC 2324 (Hyper Text Coffee Pot Control Protocol).

## MQTT

Le protocole MQTT (*Message Queuing Telemetry Transport*) est un protocole de messagerie basé sur le protocole TCP. Il est utilisé pour les applications IoT (*Internet of Things*) pour transmettre des messages entre les capteurs et les serveurs. Le protocole est basé sur le principe de publication/abonnement. Un client peut publier un message sur un *topic* et un autre client peut s'abonner à ce *topic* pour recevoir les messages. Le protocole est très léger et est utilisé pour les applications qui nécessitent une faible consommation d'énergie et une faible bande passante. La spécification du protocole est définie par la norme OASIS MQTT et le protocole utilise le port 1883.

Par exemple un capteur de température peut publier un message sur le *topic* :

```text
/switzerland/vaud/weather/temperature/42
```

avec la valeur `25.5` et un client peut s'abonner à ce *topic* pour recevoir les valeurs de température en temps réel. MQTT est beaucoup utilisé pour les applications de l'internet des objets, car il permet de transmettre des messages de manière asynchrone et de manière fiable via un serveur intermédiaire nommé *broker* (courtier).