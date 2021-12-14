#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>

enum class Direction { Forward, Up, Down };
static const std::unordered_map<std::string, Direction> nameDirection = {
    {"forward", Direction::Forward},
    {"up", Direction::Up},
    {"down", Direction::Down},
};

struct Steps 
{
    Direction direction;
    int value;
    Steps(std::string name, int value) : direction(nameDirection.at(name)), value(value) {}
};

struct Coordinates { int x; int y; };

std::vector<Steps> getInput(const char* filename)
{
    std::ifstream file(filename);
    std::vector<Steps> input;

    std::string directionName;
    int value;

    while(file >> directionName >> value) {
        input.push_back(Steps(directionName, value));
    }

    return input;
}

template <typename S> Coordinates coordinatesFromPlan(const std::vector<Steps>& steps)
{
    Coordinates xy {0, 0};
    S s;
    for (auto& step : steps) {
        switch (step.direction) {
            case Direction::Forward:
                s.forward(xy, step.value);
                break;
            case Direction::Up:
                s.up(xy, step.value);
                break;
            case Direction::Down:
                s.down(xy, step.value);
                break;
        }
    }
    return xy;
}

class Strategy1
{
public:
    void forward(Coordinates& xy, int value) {
        xy.x += value;
    }

    void up(Coordinates& xy, int value) {
        xy.y -= value;
    }

    void down(Coordinates& xy, int value) {
        xy.y += value;
    }
};

class Strategy2
{
    int aim = 0;
public:
    void forward(Coordinates& xy, int value) {
        xy.x += value;
        xy.y += aim * value;
    }

    void up(Coordinates& xy, int value) {
        aim -= value;
    }

    void down(Coordinates& xy, int value) {
        aim += value;
    }
};

int main(int argc, char* argv[]) 
{
    assert(argc == 2);
    char* filename = argv[1];
    auto input = getInput(filename);

    auto xy = coordinatesFromPlan<Strategy1>(input);
    std::cout << xy.x * xy.y << std::endl;

    xy = coordinatesFromPlan<Strategy2>(input);
    std::cout << xy.x * xy.y << std::endl;
}

