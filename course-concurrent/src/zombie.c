#include <iostream>
#include <unistd.h> // Pour fork(), getpid(), sleep()
#include <sys/wait.h> // Pour wait()

int main() {
    pid_t pid = fork(); // Crée un nouveau processus

    if (pid == -1) {
        // En cas d'échec du fork()
        std::cerr << "Échec du fork()" << std::endl;
        return 1;
    } else if (pid > 0) {
        // Code exécuté par le processus parent
        std::cout << "Je suis le processus parent (PID: " << getpid() << "), et mon enfant a le PID " << pid << std::endl;
        std::cout << "Je dors 20 secondes. Vérifiez l'état du processus enfant avec 'ps -l'." << std::endl;
        sleep(20); // Le parent dort, laissant l'enfant devenir un zombie
        std::cout << "Le parent se réveille et se termine. Le processus enfant devrait être nettoyé." << std::endl;
    } else {
        // Code exécuté par le processus enfant
        std::cout << "Je suis le processus enfant (PID: " << getpid() << ") et je me termine." << std::endl;
        // L'enfant se termine immédiatement, devenant un zombie jusqu'à ce
        // que le parent termine son sommeil
    }
}