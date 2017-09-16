#ifndef CONFIG_H
#define CONFIG_H

/*
 ____ ___      ___.                 .__  .__           __________                   __               __   
|    |   \_____\_ |_________   ____ |  | |  | _____    \______   \_______  ____    |__| ____   _____/  |_ 
|    |   /     \| __ \_  __ \_/ __ \|  | |  | \__  \    |     ___/\_  __ \/  _ \   |  |/ __ \_/ ___\   __\
|    |  /  Y Y  \ \_\ \  | \/\  ___/|  |_|  |__/ __ \_  |    |     |  | \(  <_> )  |  \  ___/\  \___|  |  
|______/|__|_|  /___  /__|    \___  >____/____(____  /  |____|     |__|   \____/\__|  |\___  >\___  >__|  
              \/    \/            \/               \/                          \______|    \/     \/      
*/

//--------------------------------------------------------------------------------------------------------------
//CONFIGURATION PARAMETERS FOR BEGINNERS
//--------------------------------------------------------------------------------------------------------------


const int DEBUG_MODE = 1; //when set to 1, debug mode shows blue LEDs depending on the highest signal strength

const int CACHE_SIZE = 3; //The number of scans that must match in a row before the state changes internally.  3 works well.
                          //Higher number = less flickery at the cost of a longer time to adjust to signal changes.
                          //Setting to 1 will disable the smoothing feature entirely.


const float MEDIUM_INTENSITY = 50; //intensity of medium color out of 100
const float FAR_INTENSITY = 3;//intensity of far color out of 100

float MEDIUM_SIGNAL_AMOUNT = -100;//Minimum RSSI to activate the "medium" state
float CLOSE_SIGNAL_AMOUNT = -60;//Minimum RSSI to activate the "close" state
//NOTE, RSSI is from 100(farthest/weakest)- to 0(closest/strongest)

//The "pulse" pattern of array size 200.
//If you want to change this you should probably just write a scipt in python to generate these numbers
//Or you can change it frame-by-frame to whatever you like
int intensityarr[] =
{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 9, 9, 10, 10, 11, 12, 12, 13, 14, 15,
16, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 42, 43, 44, 46, 47, 49, 50,
51, 53, 54, 56, 57, 59, 60, 62, 64, 65, 67, 68, 70, 72, 73, 75, 77, 79, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81,
81, 81, 81, 81, 81, 81, 81, 79, 77, 75, 73, 72, 70, 68, 67, 65, 64, 62, 60, 59, 57, 56, 54, 53, 51, 50, 49, 47, 46, 44, 43, 42,
40, 39, 38, 37, 36, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 16, 15, 14, 13, 12, 12, 11, 10,
10, 9, 9, 8, 7, 7, 6, 6, 5, 5, 4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};


//--------------------------------------------------------------------------------------------------------------
//Other things that you can change but shouldn't really unless you've modified some other part of the project
//--------------------------------------------------------------------------------------------------------------
int cache[CACHE_SIZE]; //cache of the past signal results
int cache_counter = 0; //temp counter

//GLOBAL VARIABLES USED FOR TEMP STORAGE

float last_pulse = 0; //keep track of last light update
float max_intensity = FAR_INTENSITY; //max intensity
float intensity = 0; //current intensity
int current_dist = 2; //Current state
int streak = 0; //Don't worry about this
const int STREAK_MAX = 1; //how many times in a row the dist must be the same to register a change
int last_dist  = 2;
const float CLOSE_INTENSITY = 10; //intensity of the ccolor out of 100

painlessMesh  mesh;
int highest = 0;
int sent = 0;
int c = 0;

#endif


