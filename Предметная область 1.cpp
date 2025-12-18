#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cstdlib>
#include <ctime>
using namespace std;

class ExternalSorter {
    size_t chunkSize;
    struct Node { 
        int val; 
        size_t idx; 
        bool operator>(const Node& o) const { 
            return val > o.val; 
        } 
    };
    
public:
    ExternalSorter(size_t size = 100) : chunkSize(size) {}
    
    void sortFile(const string& inFile, const string& outFile) {
        vector<string> temps = createChunks(inFile);
        mergeChunks(temps, outFile);
        for(auto& f : temps) remove(f.c_str());
    }
    
    void generateTestFile(const string& filename, int count) {
        ofstream out(filename);
        srand(time(0));
        for(int i = 0; i < count; i++) {
            out << rand() % 1000 << "\n"; // числа от 0 до 999
        }
        out.close();
    }
    
private:
    vector<string> createChunks(const string& inFile) {
        ifstream in(inFile); 
        vector<int> chunk; 
        vector<string> temps; 
        int num; 
        int cnt = 0;
        
        while(in >> num) {
            chunk.push_back(num);
            if(chunk.size() >= chunkSize) {
                sort(chunk.begin(), chunk.end());
                string name = "temp_" + to_string(cnt++) + ".txt";
                ofstream out(name); 
                for(auto& n : chunk) out << n << "\n";
                temps.push_back(name); 
                chunk.clear();
            }
        }
        if(!chunk.empty()) {
            sort(chunk.begin(), chunk.end());
            string name = "temp_" + to_string(cnt++) + ".txt";
            ofstream out(name); 
            for(auto& n : chunk) out << n << "\n";
            temps.push_back(name);
        }
        in.close();
        return temps;
    }
    
    void mergeChunks(const vector<string>& temps, const string& outFile) {
        vector<ifstream> inputs(temps.size());
        priority_queue<Node, vector<Node>, greater<Node>> heap;
        
        for(size_t i = 0; i < temps.size(); ++i) {
            inputs[i].open(temps[i]); 
            int num;
            if(inputs[i] >> num) heap.push({num, i});
        }
        
        ofstream out(outFile);
        while(!heap.empty()) {
            Node node = heap.top(); 
            heap.pop(); 
            out << node.val << "\n";
            int num; 
            if(inputs[node.idx] >> num) heap.push({num, node.idx});
        }
        out.close();
    }
};

int main() {
    ExternalSorter sorter(50); // блок по 50 чисел
    
    // 1. Создаём тестовый файл
    sorter.generateTestFile("numbers.txt", 200);
    cout << "Создан файл numbers.txt с 200 случайными числами\n";
    
    // 2. Сортируем
    sorter.sortFile("numbers.txt", "sorted_numbers.txt");
    cout << "Сортировка завершена! Результат в sorted_numbers.txt\n";
    
    // 3. Показываем первые 10 чисел из отсортированного файла
    ifstream in("sorted_numbers.txt");
    cout << "Первые 10 отсортированных чисел:\n";
    for(int i = 0; i < 10; i++) {
        int num;
        if(in >> num) cout << num << " ";
    }
    cout << endl;
    
    return 0;
}