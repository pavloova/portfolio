#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

double get_F1(double x, double y) {
    return x + y + x*y - 7;
}

double get_F2(double x, double y) {
    return pow(2, x) + pow(2, y) + x*y - 13;
}

double get_a(double x, double y) {
    return 1+y;
}

double get_b(double x, double y) {
    return 1+x;
}

double get_c(double x, double y) {
    return 2*x+y;
}

double get_d(double x, double y) {
    return 2*y+x;
}

double get_det(double a, double b, double c, double d) {
    return a * d - b * c;
}

double get_epsilon(double x0, double y0, double x, double y) {
    return sqrt(pow(x - x0, 2) + pow(y - y0, 2));
}

pair<double, double> Newton_method(double x0, double y0) {
    double x = x0;
    double y = y0;
    double epsilon = 0.000001;
    double epsilon_check = 1;
    int Iter = 0;

    while (epsilon < epsilon_check) {
        double a = get_a(x0, y0);
        double b = get_b(x0, y0);
        double c = get_c(x0, y0);
        double d = get_d(x0, y0);

        x = x0 - (1 / get_det(a, b, c, d)) * (d * get_F1(x0, y0) - b * get_F2(x0, y0));
        y = y0 - (1 / get_det(a, b, c, d)) * (-c * get_F1(x0, y0) + a * get_F2(x0, y0));

        epsilon_check = get_epsilon(x, y, x0, y0);
        x0 = x;
        y0 = y;
        Iter++;
    }
    cout<< "iterations number:"<< Iter <<endl;
    return make_pair(x, y);
}

int main() {
    cout << fixed << setprecision(10);
    pair<double, double> result = Newton_method(1.111, 2.859);
    cout << "Solution: x = " << result.first << ", y = " << result.second << endl;
    
    return 0;
}
