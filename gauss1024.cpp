#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

void createMatrix(vector<vector<double>>& M, int N) {
    
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            M[i][j] = rand()%50;
        }
    }
}

void createVector(vector<double>& V, int N) {
    //cout << "Введите элементы вектора длины " << N << ":\n";
    for (double i = 0; i < N; ++i) {
        V[i]=i;
    }
}

void printMatrix(const vector<vector<double>>& M, int N) {
    cout << "Матрица " << N << "x" << N << ":\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            cout << M[i][j] << " ";
        }
        cout << "\n";
    }
}

void printVector(const vector<double>& V, int N) {
  
    cout << "Исходный вектор:\n";
    cout << fixed << setprecision(10);
    cout << "Первые 10 элементов:\n";
    for (int i = 0; i < 10; ++i) {
        cout << V[i] << " ";
    }
  cout << "\n";
  cout << "Последние 10 элементов:\n";
  for (int i = N-10; i < N; ++i) {
      cout << V[i] << " ";
  }
    cout << "\n";
}
void solveMatrixEquation( vector<vector<double>>& M,  vector<double>& V) {
    int n = M.size();

    // Прямой ход метода Гаусса
    for (int i = 0; i < n; ++i) {
        int pivot_row = i;
        for (int j = i + 1; j < n; ++j) {
            if (abs(M[j][i]) > abs(M[pivot_row][i])) {
                pivot_row = j;
            }
        }

        if (pivot_row != i) {
            swap(M[i], M[pivot_row]);
            swap(V[i], V[pivot_row]);
        }

        for (int j = i + 1; j < n; ++j) {
            double factor = M[j][i] / M[i][i];
            for (int k = i; k < n; ++k) {
               M[j][k]  = M[j][k] - factor * M[i][k];

            }
            V[j] -= factor * V[i];
        }
    }

    // Обратный ход метода Гаусса
    vector<double> X(n);
    for (int i = n - 1; i >= 0; --i) {
        double sum = 0;
        for (int j = i + 1; j < n; ++j) {
            sum += M[i][j] * X[j];
        }
        X[i] = (V[i] - sum) / M[i][i];
    }

    // Вывод вектора X
    cout << fixed << setprecision(10);
    cout << "Решение X:" << endl;
    cout << "Первые 10 элементов:\n";
    for (int i = 0; i < 10; ++i) {
        cout << "X[" << i << "] = " << X[i] << endl;
    }
    cout << "последние 10 элементов:\n";
    for (int i = n-10; i < n; ++i) {
        cout << "X[" << i << "] = " << X[i] << endl;
  }
}
void MultiplyMatrix(vector<vector<double>>& M, vector<double>& V, vector<double>& R){
  int n = M.size();
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j)
      R[i] += M[i][j] * V[j];
  // Вывод вектора R
  cout << fixed << setprecision(10);
  cout << "Результат умножения:" << endl;
  cout << "Первые 10 элементов:\n";
  for (int i = 0; i < 10; ++i) {
      cout << "R[" << i << "] = " << R[i] << endl;
  }
  cout << "Последние 10 элементов:\n";
  for (int i = n-10; i < n; ++i) {
      cout << "R[" << i << "] = " << R[i] << endl;
  }
}
int main() {
    const int N = 1024;
    vector<vector<double>> M(N, vector<double>(N));
    vector<double> V(N);
    vector<double> R(N);

    createMatrix(M, N);
    createVector(V, N);

    //printMatrix(M, N);
    printVector(V, N);
  
    MultiplyMatrix(M, V, R);
    solveMatrixEquation(M, R);
    return 0;
}
