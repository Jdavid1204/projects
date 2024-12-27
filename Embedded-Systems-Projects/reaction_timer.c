/* ------------------------------------------
  1. To investigate and measure timings:
        - the cycle time of the cyclic system
        - the proportion of the cycle spent execute code / waiting
  2. Implement a reaction timer, timing in milliseconds
  -------------------------------------------- */
  
#include <stdbool.h>
#include <stdint.h>
#include <MKL28Z7.h>

#include ".\inc\SysTick.h"
#include ".\inc\button.h"
#include ".\inc\rgb.h"

/* --------------------------------------
    Documentation of the Given Code
    ==============================

    Behaviour
    ---------     
    There is one task: Task1LEDs
    * Flashes RED and GREEN, one second each
    * Turns on the BLUE led when button B5 is pressed for a 
       random duration between 3sec and 0.5sec (approx)

    One button is configured with an interrupt:
        Button B5 - this has hardware debounce and is designed for 
                    use with an interrupt

     Files
     -----
     The following file may need to be changed to complete the exercise
     
     main.c     Contains the main loop with 1 task and an interrupt handler
     SySTick.c  Code for SySTick timer ISR
     SysTick.h  Definitions and API for SysTick timer
     
     The following files should not be changed:
       mask.h     Definition of the MASK macro
       button.h   Definitions and API for shield buttons
       button.c   Code to configure buttons and detect button position
       rgb.h      Definitions and API for tri-colour LEDs on the development board
       rgb.c      Code to configure and operate the tri-colour LEDs on the development board
 -------------------------------------- */

/*----------------------------------------------------------------------------
  Configuration of additional GPIO outputs
       PTE23 - known as OUT1
       PTE30 - known as OUT2
  These outputs are used for measurements
*----------------------------------------------------------------------------*/
#define OUT1 (23)
#define OUT2 (30)

void configureOUT() {
  // Configuration steps
  //   1. Enable clock to GPIO port E
  //   2. Connect GPIO pins to GPIO 
  //   3. Set GPIO direction to output
  //   4. Ensure outputs are off

  // Enable clock to ports E
  PCC_PORTE |= PCC_CLKCFG_CGC(1) ;


  // Make 2 pins GPIO
  PORTE->PCR[OUT1] &= ~PORT_PCR_MUX_MASK;
  PORTE->PCR[OUT1] |= PORT_PCR_MUX(1);
  PORTE->PCR[OUT2] &= ~PORT_PCR_MUX_MASK;
  PORTE->PCR[OUT2] |= PORT_PCR_MUX(1);

  // Set ports to outputs
  PTE->PDDR |= MASK(OUT1) | MASK(OUT2);

  // Turn off outputs
  PTE->PCOR = MASK(OUT1) | MASK(OUT2);
  // end of configuration code
}

/*----------------------------------------------------------------------------
 * nextRand: get next random number 
 *   Based on https://en.wikipedia.org/wiki/Linear_congruential_generator
 * --------------------------------------------------------------------------- */
uint32_t seed = 0x12345678 ;

// Returns a 32 bit number which is too long for us
uint32_t nextRand(void) {
  seed = (1103515245 * seed + 12345) ; 
  return seed ; 
}

// Generate random in range 0 to 900
//    - take top 10 bits - max is 1023
//    - reject if > 900 (about 10% probability)
uint32_t rand900(uint32_t r) {
  uint32_t r900 = (r & 0xFFC00000) >> 22 ; // top 10 bits
  while (r900 > 900) r900 = (nextRand() & 0xFFC00000) >> 22 ;
  return r900 ;
}

/*----------------------------------------------------------------------------
  Variables for communication
*----------------------------------------------------------------------------*/
volatile bool pressedB5_ev ;  // set by interrupt handler
                              //   Cleared by the task
/*----------------------------------------------------------------------------
 * Interrupt Handler GPIO E
 *    - Clear the pending request
 *    - Test the bit to see if it generated the interrupt 
  ---------------------------------------------------------------------------- */
void PORTE_IRQHandler(void) {  
    NVIC_ClearPendingIRQ(PORTE_IRQn);
    if ((PORTE->ISFR & B5)) {
        // Add code to respond to interupt here
        pressedB5_ev = true ;
    }
		
		
    // Clear status flags 
    PORTE->ISFR = B5 ; 
}

/*----------------------------------------------------------------------------
  task1LEDs

  * Flash RED and GREEN LEDS, 1 second each
  * Turns on BLUE LED for random cycle count between 305 and 50 cycles
*----------------------------------------------------------------------------*/
#define RED (0)
#define GREEN (1)
#define REDBLUE (2)
#define GREENBLUE (3)
#define FLASHTIME (100)

#define READY (4)
#define RANDOMWAIT (5)
#define TIMING (6)
#define SUCCESSON (7)
#define SUCCESSOFF (9)
#define ERRORON (10)
#define ERROROFF (11)

int stateTask1 ;  // this variable holds the current state
uint32_t counter1;    // counter for periodic flash
volatile uint32_t recordedReactionTime = 0;      // Recorded reaction time


/*----------------------------------------------------------------------------
  inittask1LEDs

  * Initialize Task1LEDs state and LEDs
*----------------------------------------------------------------------------*/
void initTask1LEDs() {
    stateTask1 = READY;     // initialise the state 
    setRGB(RED, RGB_OFF) ;    // turn the red LED on
    setRGB(BLUE, RGB_OFF) ;  // turn the LED off
    setRGB(GREEN, RGB_OFF) ; // turn the green LED off
    counter1 = FLASHTIME ; // set the flash time
}

void task1LEDs() {
    if (counter1 > 0) counter1-- ;  // counter for periodic flash
	
    switch (stateTask1) {
			case READY:
				setRGB(RED, RGB_ON);
				if (pressedB5_ev) {
					pressedB5_ev = false ;
					setRGB(RED, RGB_OFF);
					uint32_t r = nextRand();
          				counter1 = rand900(r)+ 100; // Set random wait
					stateTask1 = RANDOMWAIT;
				}
				break;
			case RANDOMWAIT:
				if (counter1 == 0) {
					setRGB(GREEN, RGB_ON);
					setTimeZero(); // Reset reaction time
					stateTask1 = TIMING;
				}
				else if(pressedB5_ev){
					pressedB5_ev = false;
					setRGB(RED, RGB_ON); // Indicate error
					counter1 = FLASHTIME;
					stateTask1 = ERRORON;
				}
				break;
				
			case ERRORON:
				if (counter1 == 0){
				  	setRGB(RED, RGB_OFF);
					counter1 = FLASHTIME;
					stateTask1 = ERROROFF;
				}
				break;
			case ERROROFF:
				if(counter1 == 0){
					setRGB(RED, RGB_ON);
					counter1 = FLASHTIME;
					stateTask1 = ERRORON;
				}
				break;
				
			case TIMING:
				if (pressedB5_ev) {
					pressedB5_ev = false;
	        			recordedReactionTime = getTime(); // Record time
	        			setRGB(GREEN, RGB_OFF);
					counter1 = FLASHTIME;
	        			stateTask1 = SUCCESSOFF;
					
				}
				break;
			case SUCCESSOFF:
				if (counter1 == 0){
				  	setRGB(GREEN, RGB_ON);
					counter1 = FLASHTIME;
					stateTask1 = SUCCESSON;
				}
				break;
			case SUCCESSON:
				if(counter1 == 0){
				  	setRGB(GREEN, RGB_OFF);
					stateTask1 = SUCCESSOFF;
					counter1 = FLASHTIME;
				}
				break;
		}
}


/*----------------------------------------------------------------------------
  MAIN function
 *----------------------------------------------------------------------------*/
int main (void) {
    configureRGB() ;                 // configure RGB using GPIO
    configureButtons(B5, true) ;     // configure button B5 (with an interrupt)
    configureOUT() ;                 // configure additional outputs
    initTask1LEDs() ;                // initialise task1 state
    Init_SysTick(1000) ;             // initialse SysTick every 1ms
    waitSysTickCounter(10) ;
    while (1) {                   // this runs for ever

        // Set OUT2 at start of task
        PTE->PSOR = MASK(OUT2) ;
        task1LEDs() ;
        // Clear OUT2 at end of task
        PTE->PCOR = MASK(OUT2) ;

        // toggle OUT1 every cycle
        PTE->PTOR = MASK(OUT1) ;
        
        // delay
        waitSysTickCounter(10) ;  // cycle every 10 ms
    }
}
