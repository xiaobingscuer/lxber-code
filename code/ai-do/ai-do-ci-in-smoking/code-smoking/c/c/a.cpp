
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <cstdio>
#include <ctime>
#include <algorithm>
using namespace std;

const int nmax=10000000;
int a[nmax];

void permute(int* a, int n)
{
    for (int i = n; i > 0; i--)swap(a[i-1], a[rand()%i]);
}

void printa(const int* a, int n)
{
    for (int i = 0; i < 10; i++)printf("%d
", a[i]);
}

int main(){
    n = 10;
    for (int i = 0; i < n; i++)a[i] = i; 
    permute(a, n);
    printa(a, n);
    return 0;
}
        