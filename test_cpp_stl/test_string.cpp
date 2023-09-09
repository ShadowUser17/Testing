#include <iostream>
#include <string>

int main(int argc, char** argv) {
    std::string buff;

    std::cout << "Enter your text: ";
    std::cin >> buff;
    std::cout << "your text: " << buff << std::endl;

    return 0;
}
