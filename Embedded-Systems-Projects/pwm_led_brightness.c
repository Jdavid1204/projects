/* ------------------------------------------
   The green LED is displayed at different brightness levels using PWM
   The PIT is used to time the transition between the brightness levels
   A button press switches between two rates (by changing the PIT load value): 
       * a fast one cycles through all the brightness levels in 2 s
       * a slow one takes 10 s
  -------------------------------------------- */

#include <MKL28Z7.h>
#include <stdbool.h>
#include "./inc/SysTick.h"
#include "./inc/button.h"

#include "./inc/clock.h"
#include "./inc/lpit.h"
#include "./inc/TPMPWM.h"
#include "./inc/triColorLedPWM.h"


/* --------------------------------------
     Documentation
     =============
     This is a cyclic system with a cycle time of 10ms

     The file has a main function, two tasks
       1. pollB1Task: this polls shield button B1
       2. toggleRateTask: this toggles between a fast and slow rate for changing the LED brightness
     and the PIT interrupt service routine which changes the brightness of 
     one of the LEDs
 -------------------------------------- */
 
/* --------------------------------------------
  Variables for communication
*----------------------------------------------------------------------------*/
bool pressedB1_ev ;  // set by task1 (polling) and cleared by task 2
bool pressedB2_ev ;  // set by task1 (polling) and cleared by task 2

/*----------------------------------------------------------------------------
  task1pollB1
  
  This task polls button B1. Keep this task.
*----------------------------------------------------------------------------*/
int b1State ;        // Current state - corresponds to position
int b1BounceCount ;

void initPollB1Task() {
    b1State = BOPEN ;
    pressedB1_ev = false ; 
    b1BounceCount = 0 ;
}

void pollB1Task() {
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

//pollb2
void initPollB2Task() {
    b1State = BOPEN ;
    pressedB2_ev = false ; 
    b1BounceCount = 0 ;
}

void pollB2Task() {
    if (b1BounceCount > 0) b1BounceCount -- ;
    switch (b1State) {
        case BOPEN:
            if (isPressed(B2)) {
                b1State = BCLOSED ;
                pressedB2_ev = true ; 
            }
          break ;

        case BCLOSED:
            if (!isPressed(B2)) {
                b1State = BBOUNCE ;
                b1BounceCount = BOUNCEDELAY ;
            }
            break ;

        case BBOUNCE:
            if (isPressed(B2)) {
                b1State = BCLOSED ;
            }
            else if (b1BounceCount == 0) {
                b1State = BOPEN ;
            }
            break ;
    }                
}

/* -------------------------------------
    Programmable Interrupt Timer (PIT) interrupt handler

      Check each channel to see if caused interrupt
      Write 1 to TIF to reset interrupt flag

    Changes the LED brightness. KEEP THIS ISR but changes are needed
   ------------------------------------- */

//For activity 1
// PIT load values
// The larger the count, the lower the frequency of interrupts
//const uint32_t pitSlowCount = PITCLOCK * 10 / 32 ; // all 32 levels in 10 s
// const uint32_t pitFastCount = PITCLOCK * 2 / 32 ; // all 32 levels in 2 s

//For activity 2
// PIT load values
// The larger the count, the lower the frequency of interrupts
//const uint32_t pitSlowCount = 375499; // cycle time of 9 s
//const uint32_t pitMediumCount = 208332; // cycle time of 5 s
//const uint32_t pitFastCount = 83332; // cycle time of 2 s

// 32 * 6 = 192 transitions

// Step Time - 0.046875
// Step Time - 0.026042
// Step Time - 0.010417


// Brightness level
unsigned int bright = 0 ;  // the current brightness



// For Activity 3
uint32_t pitSlowCount;
uint32_t pitMediumCount;
uint32_t pitFastCount; 

#define BlueInc (0)
#define RedDec (1)
#define GreenInc (2)
#define BlueDec (3)
#define RedInc (4)
#define GreenDec (5)

#define StateW (6)
#define StateX (7)
#define StateY (8)
#define StateZ (9)

#define PatternA (10)
#define PatternB (11)

#define FAST (12)
#define SLOW (13)
#define MEDIUM (14)

int patternAState; // this variable holds the current state
int patternBState; // this variable holds the current state
int currentPattern;
int rateState ;  // this variable holds the current state

// colour brightness
unsigned int r;
unsigned int g;
unsigned int b;




void updateLoadValues() {
	if (currentPattern == PatternA) {
		r = 0;
		g = 0;
		b = 0;
		pitSlowCount = 562499; // cycle time of 9 s
		pitMediumCount = 312499; // cycle time of 5 s
		pitFastCount = 124999; // cycle time of 2 s
		currentPattern = PatternB;
		patternBState = StateW;
	}
	else if (currentPattern == PatternB) {
		r = MAXBRIGHTNESS;
		g = 0;
		b = 0;				
		pitSlowCount = 375499; // cycle time of 9 s
		pitMediumCount = 208332; // cycle time of 5 s
		pitFastCount = 83332; // cycle time of 2 s

		currentPattern = PatternA;
		patternAState = BlueInc;
	}
	setTimer(0,pitSlowCount) ;
	rateState = SLOW ;
}

void initPattern(){
	r = MAXBRIGHTNESS;
	g = 0;
	b = 0;
	pitSlowCount = 375499; // cycle time of 9 s
	pitMediumCount = 208332; // cycle time of 5 s
	pitFastCount = 83332; // cycle time of 2 s
	currentPattern = PatternA;
	patternAState = BlueInc;
	pressedB2_ev = false;

}

void twoPatternSequence() {
	if (pressedB2_ev) {
		pressedB2_ev = false;
		updateLoadValues();
	}
	
	switch (currentPattern) {
		case PatternA:
			switch (patternAState) {
				case BlueInc:
					if (b < MAXBRIGHTNESS){
							b ++;
					}
					else if (b == MAXBRIGHTNESS){
							patternAState = RedDec;
					}
					break;
				case RedDec:
					if (r > 0) {
							r --;
					}
					
					else if (r ==0){
							patternAState = GreenInc;
					}
					break;
						
				case GreenInc:
					if (g < MAXBRIGHTNESS){
							g ++;
					}
					else if (g == MAXBRIGHTNESS){
							patternAState = BlueDec;
					}
					break;
				case BlueDec:
					if (b > 0) {
							b --;
					}
					
					else if (b ==0){
							patternAState = RedInc;
					}
					break;
					
				case RedInc:
					if (r < MAXBRIGHTNESS){
							r ++;
					}
					else if (r == MAXBRIGHTNESS){
							patternAState = GreenDec;
					}
					break;
				case GreenDec:
					if (g > 0) {
							g --;
					}
					
					else if (g ==0){
							patternAState = BlueInc;
					}
					break;
			}
			break;
			
		case PatternB:
			switch (patternBState) {
				case StateW:
					if (r < MAXBRIGHTNESS && b < MAXBRIGHTNESS){
							r++;
							b ++;
					}
					else if (r == MAXBRIGHTNESS && b == MAXBRIGHTNESS){
							patternBState = StateX;
					}
					break;
					
				case StateX:
					if (b > 0 && g < MAXBRIGHTNESS) {
							b --;
							g ++;
					}
					
					else if (b ==0 && g == MAXBRIGHTNESS){
							patternBState = StateY;
					}
					break;
						
				case StateY:
					if (r > 0 && b < MAXBRIGHTNESS){
							r --;
							b	++;
					}
					else if (r == 0 && b == MAXBRIGHTNESS){
							patternBState = StateZ;
					}
					break;
						
				case StateZ:
					if (b > 0 && g > 0) {
							b --;
							g --;
					}
					
					else if (b ==0 && g == 0){
							patternBState = StateW;
					}
					break;
				}
			break;
	}

}

void LPIT0_IRQHandler() {
  NVIC_ClearPendingIRQ(LPIT0_IRQn);

  // check source of interrupt - LPIT0 channel 0
  if (LPIT0->MSR & LPIT_MSR_TIF0_MASK) {
//      bright = (bright + 1) % (MAXBRIGHTNESS + 1);        
//	Task1ColourSequence();
	twoPatternSequence();
     	setLEDBrightness(Red, r); 
 	setLEDBrightness(Green, g);
     	setLEDBrightness(Blue, b);

  }

//  // check source of interrupt - LPIT0 channel xxxx
//  if (LPIT0->MSR & LPIT_MSR_TIFxxxx_MASK) {
//     add code here
//  }

  // Clear all
  LPIT0->MSR = LPIT_MSR_TIF0(1) | LPIT_MSR_TIF1(1) | LPIT_MSR_TIF2(1)
             | LPIT_MSR_TIF3(1) ; // write to clear
}  

/*----------------------------------------------------------------------------
   Task: toggleRateTask

   Toggle the rate of upadtes to the LEDs on every signal

   KEEP THIS TASK, but changes may be needed
*----------------------------------------------------------------------------*/



// initial state of task
void initToggleRateTask() {
    setTimer(0,pitSlowCount) ;
    rateState = SLOW ;
}

//For activity 1
//void toggleRateTask() {
//    switch (rateState) {
//        case FAST:  
//            if (pressedB1_ev) {                   // signal received
//                pressedB1_ev = false ;            // acknowledge
//                setTimer(0, pitSlowCount) ;  // update PIT
//                rateState = SLOW ;           // ... the new state
//            }
//            break ;
//            
//        case SLOW:
//            if (pressedB1_ev) {                   // signal received
//                pressedB1_ev = false ;            // acknowledge
//                setTimer(0, pitFastCount) ;  // update PIT
//                rateState = FAST ;           // ... the new state
//            }
//            break ;
//  }
//}

void toggleRateTask() {
    switch (rateState) {
        case FAST:  
            if (pressedB1_ev) {                   // signal received
                pressedB1_ev = false ;            // acknowledge
                setTimer(0, pitSlowCount) ;  // update PIT
                rateState = SLOW ;           // ... the new state
            }
            break ;
				case MEDIUM:  
            if (pressedB1_ev) {                   // signal received
                pressedB1_ev = false ;            // acknowledge
                setTimer(0, pitFastCount) ;  // update PIT
                rateState = FAST ;           // ... the new state
            }
            break ;
            
        case SLOW:
            if (pressedB1_ev) {                   // signal received
                pressedB1_ev = false ;            // acknowledge
                setTimer(0, pitMediumCount) ;  // update PIT
                rateState = MEDIUM ;           // ... the new state
            }
            break ;
  }
}



/*----------------------------------------------------------------------------
  MAIN function
 *----------------------------------------------------------------------------*/
int main (void) {
    // enable the peripheralclock
    enablePeripheralClock() ;

    // Configure pin multiplexing
    configureLEDforPWM() ;            // Configure LEDs for PWM control
  
    // Configure button B1
    configureButtons(B1, false) ; // ConfigureButtons B1 for polling
    configureButtons(B2, false) ; // ConfigureButtons B1 for polling
  
    // Configure LPIT0 channel 0 to generate interrupts
    configureLPIT_interrupt(0) ;

    // Configure TPM
    configureTPMClock() ;    // clocks to all TPM modules
    configureTPM0forPWM() ;  // configure PWM on TPM0 (all LEDs)
   
    Init_SysTick(1000) ;  // initialse SysTick every 1 ms

    // start everything
    setLEDBrightness(Red, 0) ;
    setLEDBrightness(Green, 0) ;
    setLEDBrightness(Blue, 0) ;

    initPollB1Task() ; 		// initialise task state
    initPollB2Task();
    initPattern();
    initToggleRateTask() ;   // initialise task state
    // start the PIT
    startTimer(0) ;
    waitSysTickCounter(10) ;  // initialise delay counter
    while (1) {      // this runs forever
        pollB1Task() ;       // Poll button B1
				pollB2Task();
        toggleRateTask();    // Toggle LED update rate on every press signal
        // delay
        waitSysTickCounter(10) ;  // cycle every 10 ms 
    }
}
