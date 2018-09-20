// C++ Program to implement random walk with Metropolis Monte-Carlo Type Algorithm

#include <iostream>
#include <fstream>
#include <cstdlib> 
#include <ctime>
#include <cstdio>

using namespace std;

/* Define Variables */
int x[100] = {}; // Empty array for x coordinates
int y[100] = {}; // Empty array for y coordinates
int tmax = 10;

/* Declare functions */
int randNumber();

int main()
{
	srand( (time(NULL)) );
	// CREATE SIMULATION ENVIRONMENT Set up simulation cell
	// Initially 2D so x is whatever, y is whatever range etc
	int i;
	for (i = 0; i < 100; i++)
	{
	    x[i] = i;
	    y[i] = i;
	}

	cout << "8th x component is " << x[7] << endl;
	cout << "27th y component is " << y[26] << endl;
	cout << "I have " << sizeof(x) << "x components" << endl; //400 apparently...
		

	//Naieve random walk for a single spectrin
	int specX = 0;
	int specY = 0;
	int t;
	int specCoords[10][2] = {};

		for(t=0; t<tmax; t++){
			cout << "time step is " << t << endl;
			int step = randNumber();
			if (step == 0){
				specX++;
			}
			else if (step == 1){
				specX--;
			}
			else if (step == 2){
				specY++;
			}
			else {
				specY--;
			}

		specCoords[t][0] = specX;
		specCoords[t][1] = specY;
		}

ofstream outdata; // outdata is like cin

outdata.open("output8.dat"); // opens the file
   	if( !outdata ) { // file couldn't be opened
	cerr << "Error: file could not be opened" << endl;
        exit(1);
   	}
int j;
	
for (j = 0; j<tmax; j++){
outdata << j << " ," << specCoords[j][0] << " ," << specCoords[j][1] << endl;
}
outdata.close();

return 0; 
}

//Function to return a random number 0,1,2 or 3
int randNumber()
{
	return rand() % 4;
}
