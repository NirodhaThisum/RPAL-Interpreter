#include<iostream>
#include<sstream>
#include<string>
using std::cout;
using std::string;
using std::endl;
using std::stringstream;


int main() {
    int num1 = 100;
    int num2 = 400;
    string name = "Nirodha";

    stringstream ss;
    ss << num1 << num2 << name;
    string date = "12/12/12/";
    ss << date;
    string output;
    output = ss.str();
    cout << output;

}