# Programmation Asynchrone

Un paradigme de programmation asynchrone est un style de programmation concurrente qui permet de gérer des événements de manière non bloquante. Il traite des événements qui ne sont pas nécessairement liés au flot principal d'exécution et constitue une amélioration par rapport à la programmation concurrente classique reposant explicitement sur des threads.

Ce paradigme est devenu populaire avec l'arrivée des applications web et des interfaces graphiques. Ces applications doivent en effet réagir à des événements sans bloquer l'interface utilisateur. Le langage JavaScript illustre bien cette approche.

Prenons l'exemple d'une page web qui affiche des données provenant d'un serveur. Lorsque la page est chargée, une requête est envoyée pour récupérer ces données. Si la requête était bloquante, l'interface resterait figée jusqu'à réception de la réponse. Grâce à la programmation asynchrone, la requête est envoyée tandis que le programme continue de s'exécuter. À la réception des données, un événement est déclenché et le programme affiche le résultat. Voici un exemple simplifié :

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">
<head>
    <title>Exemple de programmation asynchrone</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
    <h1>Données</h1>
    <div id="data">Chargement des données en cours...</div>
    <script>
        // Envoi de la requête au serveur
        fetch('https://jsonplaceholder.typicode.com/posts')
            .then(response => response.json())
            .then(data => {
                // Affichage des données
                document.getElementById('data').innerText = JSON.stringify(data, null, 2);
            });
    </script>
</body>
</html>
```

Vous pouvez exécuter cet exemple en enregistrant le code dans un fichier HTML puis en l'ouvrant dans un navigateur. Les données récupérées s'affichent alors dans la page.

Dans cet exemple, la requête est envoyée grâce à la fonction `fetch`, qui renvoie une **promesse**. Lorsque cette promesse est résolue (c'est-à-dire lorsque les données sont reçues), la fonction `then` est appelée pour les afficher dans la page.

JavaScript propose une notation qui facilite le chaînage des actions, mise en œuvre en retournant l'objet courant (`this` en C++).

La méthode `fetch` retourne donc une instance de `Promise`, objet représentant la résolution ou le rejet d'une valeur asynchrone. Une promesse peut être dans l'un des trois états suivants :

1. en attente ;
2. résolue ;
3. rejetée.

Lorsqu'une promesse est résolue, la méthode `then` est appelée avec la valeur associée. Si la promesse est rejetée, la méthode `catch` est invoquée avec l'erreur.

En JavaScript, les fonctions lambda — aussi appelées fonctions fléchées (`=>`) — sont très utilisées. Elles permettent de définir des fonctions de manière concise. Le code traduit en C++ pourrait ressembler à ceci :

```cpp
fetch("https://jsonplaceholder.typicode.com/posts")
    .then([](Response response) {
        return response.json();
    })
    .then([](Data data) {
        document.getElementById("data").innerText = JSON.stringify(data, nullptr, 2);
    });
```

On remarque donc que la fonction `fetch` n'est pas bloquante : une action est associée lorsque la promesse sera résolue. On observe ainsi une chaîne d'opérations déclenchées successivement.

1. On fait la promesse qu'une réponse sera reçue.
2. Une fois les données reçues, on promet de les transformer en JSON.
3. Une fois les données transformées, on promet de les afficher dans la page.

C'est une manière de gérer des événements de manière asynchrone sans bloquer le programme.

## C++ et la programmation asynchrone

En C++, la notion de promesse et celle de `future` ont été introduites avec C++11. Leur fonctionnement est similaire à celui des promesses en JavaScript.

Un `std::future` est un objet qui contient une valeur disponible ultérieurement. Il est associé à une promesse, objet chargé de fournir cette valeur.

L'exemple JavaScript n'est pas directement transposable en C++ car le langage ne propose pas nativement de fonction `fetch` pour réaliser des requêtes HTTP asynchrones. Néanmoins, la combinaison de la bibliothèque **CURL** et de `nlohmann/json` peut nous y aider.

```bash
sudo apt install libcurl4 libcurl4-openssl-dev nlohmann-json3-dev
```

```cpp
#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <future>
#include <thread>

using json = nlohmann::json;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string fetchUrl(const std::string& url) {
    CURL *curl = curl_easy_init();
    if(!curl) return "";

    std::string readBuffer;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if(res != CURLE_OK)
        throw std::runtime_error("CURL failed: " + std::string(curl_easy_strerror(res)));
    return readBuffer;
}

int main() {
    std::string url = "https://jsonplaceholder.typicode.com/posts";

    // Création de la promesse et du futur
    std::promise<std::string> promise;
    std::future<std::string> future = promise.get_future();

    // Exécution dans un thread séparé
    std::jthread([url, &promise]() {
        try {
            std::string result = fetchUrl(url);
            promise.set_value(result);
        } catch(...) {
            promise.set_exception(std::current_exception());
        }
    });

    try {
        // Attendre et obtenir la valeur future
        std::string result = future.get();
        json j = json::parse(result);
        std::cout << j.dump(4) << std::endl;
    } catch(const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}
```


On peut observer que le code est moins concis que le code JavaScript. L'asynchronisme est plus explicite et nécessite la création d'un thread pour effectuer la requête. La promesse est utilisée pour transmettre le résultat de la requête au thread principal.

## `std::async`

La fonction `std::async` permet d'exécuter une fonction de manière asynchrone, autrement dit dans un thread séparé, sans avoir à gérer explicitement la création de ce thread.

Elle retourne un `std::future` qui contient le résultat de la fonction. C'est une manière simple de lancer une tâche asynchrone tout en récupérant son résultat ultérieurement.

```cpp
#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <future>

using json = nlohmann::json;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string fetchUrl(const std::string& url) {
    CURL *curl = curl_easy_init();
    if(!curl) return "";

    std::string readBuffer;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if(res != CURLE_OK)
        throw std::runtime_error("CURL failed: " + std::string(curl_easy_strerror(res)));
    return readBuffer;
}

int main() {
    // Lancement asynchrone de la requête HTTP
    std::future<std::string> future = std::async(
        std::launch::async, fetchUrl, "https://jsonplaceholder.typicode.com/posts");

    try {
        // Attendre et obtenir la valeur future
        std::string result = future.get();
        json j = json::parse(result);
        std::cout << j.dump(4) << std::endl;
    } catch(const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}
```
