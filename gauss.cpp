#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

void readMatrix(vector<vector<double>>& M, int N) {
    cout << "Введите элементы матрицы " << N << "x" << N << ":\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            cin >> M[i][j];
        }
    }
}

void readVector(vector<double>& V, int N) {
    cout << "Введите элементы вектора длины " << N << ":\n";
    for (int i = 0; i < N; ++i) {
        cin >> V[i];
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
    cout << "Вектор:\n";
    for (int i = 0; i < N; ++i) {
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
    cout << "Решение X:" << endl;
    for (int i = 0; i < n; ++i) {
        cout << "X[" << i << "] = " << X[i] << endl;
    }
}
void MultiplyMatrix(vector<vector<double>>& M, vector<double>& V, vector<double>& R){
  int n = M.size();
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j)
      R[i] += M[i][j] * V[j];
  // Вывод вектора R
  cout << "Результат умножения:" << endl;
  for (int i = 0; i < n; ++i) {
      cout << "R[" << i << "] = " << R[i] << endl;
  }
}
int main() {
    const int N = 3;
    vector<vector<double>> M(N, vector<double>(N));
    vector<double> V(N);
    vector<double> R(N);

    readMatrix(M, N);
    readVector(V, N);
  cout << fixed << setprecision(10);
    printMatrix(M, N);
    printVector(V, N);
    //MultiplyMatrix(M, V, R);
    solveMatrixEquation(M, V);
    return 0;
}
