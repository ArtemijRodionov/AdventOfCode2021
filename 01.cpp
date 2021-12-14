#include <iostream>
#include <fstream>
#include <vector>


std::vector<int> getInput(const char* filename)
{
    std::ifstream file(filename);
    std::vector<int> floorDepths;
    int depth;
    while(file >> depth) {
        floorDepths.push_back(depth);
    }
    return floorDepths;
}

int countIncrements(std::vector<int> xs)
{
    assert(xs.size() > 0);
    int x = xs[0];
    int incrementCount = 0;
    for (int i = 1; i < xs.size(); ++i) {
        if (x < xs[i])
            incrementCount++;
        x = xs[i];
    }
    return incrementCount;
}

int countSlidingWindowIncrements(std::vector<int> xs)
{
    const int windowSize = 3;
    assert(xs.size() >= windowSize);

    int window = 0;
    for (size_t i = 0; i < windowSize; ++i) {
        window += xs[i];
    }

    int incrementCount = 0;
    for (size_t i = windowSize; i < xs.size(); ++i) {
        int newWindow = window + xs[i] - xs[i-windowSize];
        if (window < newWindow)
            incrementCount++;
        window = newWindow;
    }
    return incrementCount;
}

int main(int argc, char* argv[]) 
{
    assert(argc == 2);
    char* filename = argv[1];
    auto input = getInput(filename);

    std::cout << countIncrements(input) << std::endl; 
    std::cout << countSlidingWindowIncrements(input) << std::endl; 
}
