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
