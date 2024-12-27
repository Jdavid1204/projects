/* ------------------------------------------
   Press B1 to use ADC to measure voltage
   When green LED is on, VR1 is measured
   When red LED is on, VR2 is measured
   Both measurements update 'scaled' variable    
  -------------------------------------------- */

#include <stdbool.h>
#include <stdint.h>
#include <MKL28Z7.h>
#include ".\inc\SysTick.h"
#include ".\inc\button.h"
#include ".\inc\rgb.h"
#include ".\inc\led.h"
#include ".\inc\adc.h"

/* --------------------------------------
     Documentation
     =============
     This is a cyclic system with a cycle time of 10ms

     The file has a main function, with two tasks
        1. task1PollB1 polls button B1
        2. task2MeasureVR uses the ADC to measure a voltage on each button press
 -------------------------------------- */
 
/* --------------------------------------------
  Variables for communication
*----------------------------------------------------------------------------*/
bool pressedB1_ev ;  // set by task1 (polling) and cleared by task 2

/*----------------------------------------------------------------------------
  task1pollB1
  
  This task polls button B1. Keep this task.
*----------------------------------------------------------------------------*/
int b1State ;        // Current state - corresponds to position
int b1BounceCount ;

void initTask1PollB1() {
    b1State = BOPEN ;
    pressedB1_ev = false ; 
    b1BounceCount = 0 ;
}

void task1PollB1() {
    if (b1BounceCount > 0) b1BounceCount -- ;
    switch (b1State) {
        case BOPEN:
            if (isPressed(B1)) {
                b1State = BCLOSED ;
                pressedB1_ev = true ; 
            }
          break ;

        case BCLOSED:
            if (!isPressed(B1)) {
                b1State = BBOUNCE ;
                b1BounceCount = BOUNCEDELAY ;
            }
            break ;

        case BBOUNCE:
            if (isPressed(B1)) {
                b1State = BCLOSED ;
            }
            else if (b1BounceCount == 0) {
                b1State = BOPEN ;
            }
            break ;
    }                
}


#define ShieldLEDsOn (0)
#define ShieldLEDsOff (1)
#define FlashOff (2)
#define MeasureMin (3)
#define MeasureMax (4)
#define ErrOn (5)
#define Erroff (6)
#define FLASHTIME (50) // Set time of flashing
#define NUM_LEDS 5 // Number of shield LEDs

int currentState; // Stores the current state
int flashCounter; // Count cycles for flashing

/*----------------------------------------------------------------------------
   setAllLEDs

   * Controls the state (on/off) of all shield LEDs.
   * Iterates through each defined LED in the sequence.
*----------------------------------------------------------------------------*/

const int LED_SEQUENCE[NUM_LEDS] = {LED1, LED2, LED3, LED4, LED5};

void setAllLEDs(int onOff) {
		for (int i = 0; i < NUM_LEDS; i++) {
			ledOnOff(LED_SEQUENCE[i], onOff);
		}
}


//Activity 2.3
//Min: VR1 Raw = 0x0004, Scaled = 0
//Min: VR2 Raw = 0x0004, Scaled = 0

//Max: VR1 Raw = 0xEAAF, Scaled = 302
//Min: VR2 Raw = 0xEA03, Scaled = 301


/*----------------------------------------------------------------------------
   Task: task1MeasureVR

   * Measures voltage for VR1 and VR2 using ADC.
   * Updates the scaled voltage values for VR1 and VR2.
*----------------------------------------------------------------------------*/

VR_t vrState ;        // Current state - which VR measured next

volatile uint16_t VR1in;      // raw value - single ended
volatile uint16_t VR2in;      // raw value - single ended
volatile uint16_t VR1min;      // raw value - single ended
volatile uint16_t VR2min;      // raw value - single ended
volatile uint16_t VR1max;      // raw value - single ended
volatile uint16_t VR2max;      // raw value - single ended
int scaledin1 ; // voltage as a scaled integer - 3v shown as 300
int scaledin2 ; // voltage as a scaled integer - 3v shown as 300

int onCounter; // LED timing counters
int offCounter; / LED timing counters
int counter; // Tracks number of cycles


void initTask1MeasureVR() {
    pressedB1_ev = false ; 
    vrState = VR1 ;
    setRGB(RED, RGB_OFF) ;
    setRGB(GREEN, RGB_ON) ;
		scaledin1 = 0 ; // voltage as a scaled integer - 3v shown as 300
		scaledin2 = 0; // voltage as a scaled integer - 3v shown as 300
		onCounter = 0;
		offCounter = 0;
}

void task1MeasureVR() {
    switch (vrState) {
        case VR1: // GREEN is on;
                VR1in = MeasureVR(VR1) ;
                //scaledin1 = (VR1in * 330) / 0xFFFF ;
		onCounter = ((350 * (VR1in - VR1min)) / (VR1max - VR1min)) + 50;
		vrState = VR2 ;
							
                    // Max voltage is 3.3 v
                    // Using 16 bit accuracy, raw value is 0xFFFF
                    // Result represents voltage N.NN as integer NNN
            
            break ;
        
        case VR2: // RED is on
                VR2in = MeasureVR(VR2) ;
		//scaledin2 = (VR2in * 330) / 0xFFFF ;
		offCounter = ((350 * (VR2in- VR2min)) / (VR2max- VR2min)) + 50;
		vrState = VR1 ;
							
            break ;
        
        default: // other case not needed
            break ; 
    }
}

/*----------------------------------------------------------------------------
   Task: task2MeasureVR

   * Implements extended measurement tasks with VR1 and VR2.
   * Handles additional states for error indication and LED control.
*----------------------------------------------------------------------------*/

void initTask2MeasureVR() {
//		pressedB1_ev = false;
//		counter = 0;
//		setAllLEDs(LED_ON);
	  setRGB(RED, RGB_OFF) ;
    setRGB(GREEN, RGB_ON) ;
    setRGB(BLUE, RGB_OFF) ;
		flashCounter = FLASHTIME;
		currentState = MeasureMin ;
}

void task2MeasureVR() {		
		if (flashCounter > 0) flashCounter --;
    switch (currentState) {
				case MeasureMin: // Measure min voltage
					if (pressedB1_ev) {
							pressedB1_ev = false;
							VR1min = VR1in;
							VR2min = VR2in;
							setRGB(GREEN, RGB_OFF);
							setRGB(RED, RGB_ON);
							currentState = MeasureMax;
					}
					break;
				
				case MeasureMax: // Measure maximu voltage
					if (pressedB1_ev && VR1in > VR1min && VR2in > VR2min){
							pressedB1_ev = false;
							VR1max = VR1in;
							VR2max = VR2in;
							counter = 0;
							setAllLEDs(LED_ON);
							setRGB(RED, RGB_OFF);
							setRGB(GREEN, RGB_ON);
							currentState = ShieldLEDsOn;
					}
					
					if (pressedB1_ev && (VR1in <= VR1min || VR2in <= VR2min)){
							pressedB1_ev = false;
							setRGB(RED, RGB_OFF);
							setRGB(BLUE, RGB_ON);
							flashCounter = FLASHTIME;
							currentState = ErrOn;
					}
					break;
							
				case ErrOn: // VRin is less than VRmin
					if (flashCounter == 0){
							setRGB(BLUE, RGB_OFF);
							flashCounter = FLASHTIME;
							currentState = Erroff;
					}
					break;
				
				case Erroff: // Flashes blue
					if (flashCounter == 0){
							setRGB(BLUE, RGB_ON);
							flashCounter = FLASHTIME;
							currentState = ErrOn;
					}
					break;
			
			
			        case ShieldLEDsOn: // GREEN is on;
					if (pressedB1_ev) {
							pressedB1_ev = false;
							setAllLEDs(LED_OFF);
							setRGB(GREEN, RGB_OFF);
							setRGB(RED, RGB_ON);
							counter = 0 ;
							currentState = FlashOff;
					}
					
					if (counter >= onCounter){
								setAllLEDs(LED_OFF);
								counter = 0 ;
								currentState = ShieldLEDsOff;
					}
			            break ;
        
        			case ShieldLEDsOff: // RED is on
					if (pressedB1_ev) {
							pressedB1_ev = false;
							setRGB(GREEN, RGB_OFF);
							setRGB(RED, RGB_ON);
							counter = 0 ;
							currentState = FlashOff;
					}
					if (counter >= offCounter){
							setAllLEDs(LED_ON);
							counter = 0 ;
							currentState = ShieldLEDsOn;
					}
				    break;
			        case FlashOff: // System is off
			            	if (pressedB1_ev) {
							pressedB1_ev = false;
							setAllLEDs(LED_ON);
							setRGB(RED, RGB_OFF);
							setRGB(GREEN, RGB_ON);
							counter = 0;
							currentState = ShieldLEDsOn;
					}					
					break;
				default:
					break;
    }
}


/*----------------------------------------------------------------------------
  MAIN function
 *----------------------------------------------------------------------------*/
int main (void) {

    // Initialise peripherals
    configureButtons(B1, false) ; // ConfigureButtons B1 for polling
    configureLEDs() ;                 // Configure shield LEDs
    configureRGB();                   // Configure the 3-colour LED on the FRDM board 
    
    // Initialise and calibrate ADC
    initADC() ; // Initialise ADC
    int calibrationFailed = ADC_Cal() ; // calibrate the ADC 
    while (calibrationFailed) ; // block progress if calibration failed
    initADC() ; // Reinitialise ADC
    initVR1pin() ; // Not needed usually as default use
    initVR2pin() ; // Not needed usually as default use

    // initialse SysTick every 1 ms
    Init_SysTick(1000) ;  

    // Initialise tasks and cycle counter
    initTask1PollB1() ;  
    initTask1MeasureVR();
    initTask2MeasureVR() ;
    waitSysTickCounter(10) ;  
    
    while (1) {      // this runs forever
        task1PollB1() ;    // Generate signals for a simulated button
	task1MeasureVR();
        task2MeasureVR() ; // 
        // delay
        waitSysTickCounter(10) ;  // cycle every 10 ms
	counter ++; // Increments number of cycles
    }
}
