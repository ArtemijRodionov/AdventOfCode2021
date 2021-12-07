#include <iostream>
#include <fstream>
#include <functional>
#include <string>
#include <vector>
#include <cmath>

std::vector<std::vector<bool>> readInput(const char* filename)
{
    std::ifstream fs;
    fs.open(filename);
    std::vector<std::vector<bool>> result;
    std::string str;
    while (fs >> str) {
        std::vector<bool> row;
        for (auto x : str) {
            row.push_back(x != '0');
        }
        result.push_back(row);
    }
    return result;
}

std::vector<bool> countGammaRate(std::vector<std::vector<bool>> rows){
    std::vector<int> count (rows[0].size(), 0);
    for (const auto& row : rows) {
        for (size_t j = 0; j < row.size(); j++) {
            if (row[j]) {
                count[j]++;
            } else {
                count[j]--;
            }
        }
    }

    std::vector<bool> result(count.size());
    for (size_t i = 0; i < count.size(); i++) {
        result[i] = count[i] >= 0;
    }

    return result;
}

std::vector<bool> subvector(const std::vector<bool> &xs, size_t i, size_t pos) {
    std::vector<bool> res;
    res.reserve(pos - i);
    for (int j = i; j < pos; j++) {
        res.push_back(xs[j]);
    }
    return res;
}

std::vector<bool> subvector(const std::vector<bool> &xs, size_t i) {
    return subvector(xs, i, xs.size()); 
}

std::vector<bool> operator+(std::vector<bool> &lhs, const std::vector<bool> &rhs) {
    std::vector<bool> res;
    res.reserve(lhs.size() + rhs.size());
    for (auto x : lhs) {
        res.push_back(x);
    }
    for (auto x : rhs) {
        res.push_back(x);
    }
    return res;
}


struct Trie
{
    int count;
    std::vector<bool> hold;
    std::vector<Trie> children;

    Trie() 
        : hold(), count(0)
        {}
    Trie(std::vector<bool> xs) 
        : hold(xs), count(1)
        {}
    Trie(std::vector<bool> xs, std::vector<Trie> children, int count)
        : hold(xs), children(children), count(count)
        {}

    bool add(const std::vector<bool> &value) {
        if (value.size() == 0) return true;

        size_t i = 0;
        size_t minSize = std::min(hold.size(), value.size());
        for (; i < minSize; i++) {
            if (value[i] != hold[i])
                break;
        }

        // mismatched node
        if (hold.size() != 0 && i == 0) return false;

        if (i == minSize && hold.size() == value.size()) {
            // inc count only
        }
        else if (i == hold.size()) {
            auto substrValue = subvector(value, i);
            if (!addToChildren(substrValue))
                children.emplace_back(substrValue);
        } else if (i == value.size()) {
            auto newTrie = Trie(subvector(hold, i), children, count);
            hold = value;
            children = std::vector<Trie>(); 
            children.push_back(newTrie);
        } else {
            auto newTrie = Trie(subvector(hold, i), children, count);
            hold = subvector(hold, 0, i);
            children = std::vector<Trie>(); 
            children.push_back(newTrie);
            children.emplace_back(subvector(value, i));
        }

        count++;
        return true;
    }

    bool addToChildren(const std::vector<bool> &value) {
        for (auto &node : children) {
            if (node.add(value)) return true;
        }
        return false;
    }

    std::vector<bool> commonBitCriteria(std::function<bool(int, int)> fn) {
        int z = 0;
        int o = 0;

        for (auto& x : children) {
            if (x.hold[0]) {
                o = std::max(x.count, o);
            } else {
                z = std::max(x.count, z);
            }
        }

        for (auto& x : children) {
            if (!fn(z, o) && !x.hold[0]) {
                return hold + x.commonBitCriteria(fn);
            }
            if (fn(z, o) && x.hold[0]) {
                return hold + x.commonBitCriteria(fn);
            }
        }

        return hold;
    }
};

int to_decimal(const std::vector<bool>& xs) {
    int res = 0;
    size_t i = 0;
    size_t j = xs.size() - 1; 
    while(true) { 
        res += int(xs[j]) * std::pow(2, i);
        if(j == 0) break;
        i++, j--;
    }
    return res;
}

std::vector<bool>& inv(std::vector<bool>& xs) {
    for (size_t i = 0; i < xs.size(); i++) {
        xs[i] = !xs[i];
    }
    return xs;
}


int main(int argc, char* argv[])
{
    assert(argc == 2);
    auto input = readInput(argv[1]);

    Trie t;
    for (auto& x : input) {
        t.add(x);
    }

    auto rate = countGammaRate(input);
    std::cout << to_decimal(rate) * to_decimal(inv(rate)) << std::endl;

    auto oxygen = t.commonBitCriteria([](int zeroCount, int oneCount){
        return zeroCount <= oneCount;
    });
    auto co2 = t.commonBitCriteria([](int zeroCount, int oneCount){
        return zeroCount > oneCount;
    });

    std::cout << to_decimal(oxygen) * to_decimal(co2) << std::endl;
}

