#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath> 
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


void solveHolezki(vector<vector<double>>& M, vector<double>& V) {
    int N = M.size();
    vector<double> Y(N);
    vector<vector<double>> U(N);
    vector<vector<double>> D(N);

    for (int i = 0; i < N; ++i) {
        U[i].resize(N);
        D[i].resize(N);
    }
// разложение 
 
  D[0][0] = -1.0;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (i == j) {
                double summ = 0;
              if (i!=0){
                for (int k = 0; k < i; k++) {
                    summ += U[k][i] * U[k][i]; //* D[k][k];
                }
                if (M[i][i] - summ< 0)
                  D[i][i] = -1;
                if (M[i][i] - summ == 0)
                    D[i][i] = 0;
                else
                  D[i][i] = 1;}
              double sum = 0;
              for (int k = 0; k < i; k++) {
                  sum += U[k][i] * U[k][i]* D[k][k];
              }
              U[i][i] = sqrt(abs(M[i][i] - sum));
              } 
          if (i<j){
                double summ = 0;
                for (int k = 0; k < i; k++) {
                    summ += U[k][i] * U[k][j]*D[k][k];
                }
                U[i][j] = (M[i][j] - summ) / (U[i][i]*D[i][i]);
            }
                 
        }
    }
printMatrix(U,N);
printMatrix(D,N);
// Sт*Y = V
  for (int i = 0; i < N; ++i) {
        double summ = 0;
        for (int j = 0; j < i; ++j) {
            summ += U[j][i] * Y[j];
        }
        Y[i] = (V[i] - summ) / U[i][i];
    }

//S*X = D*Y
 for (int i = 0; i < N; ++i)
    {double summ = 0;
    for (int j = 0; j < N; ++j)
      summ += D[i][j]*Y[j];
    Y[i] = summ;} 
  vector<double> X(N);
    for (int i = N - 1; i >= 0; --i) {
        double summ = 0;
        for (int j = 0 ; j < N; ++j) {
            summ += U[i][j] * X[j];
        }
        X[i] = (Y[i] - summ) / U[i][i];
    }

    cout << "Solution:" << endl;
   cout << fixed << setprecision(10);
    for (int i = 0; i < N; ++i) {
        cout << "X[" << i << "] = " << X[i] << endl;
    }
}

int main() {
  const int N = 3;
  vector<vector<double>> M(N, vector<double>(N));
  vector<double> V(N);
  readMatrix(M, N);
  readVector(V, N);
  solveHolezki(M,V);

}
  
