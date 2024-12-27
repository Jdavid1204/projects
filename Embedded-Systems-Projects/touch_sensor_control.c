
/*----------------------------------------------------------------------------
    Touch Pad and LED Control

    Functionality:
    - Reads touch pad input periodically and displays touch position (distance).
    - Responds to specific touch positions by controlling LED brightness and state.
    - Implements two threads:
        1. t_touch: Periodically reads the touch pad and writes the distance to the terminal.
        2. t_controlLED: Adjusts LED brightness and state based on touch events.
 *---------------------------------------------------------------------------*/
 
#include "cmsis_os2.h"
#include <MKL28Z7.h>
#include <stdbool.h>
#include "./inc/rgb.h"
#include "./inc/serialPort.h"
#include "./inc/TSI.h"

#include "./inc/clock.h"
#include "./inc/TPMPWM.h"
#include "./inc/triColorLedPWM.h"

#define pos20Flag (1) // masks, so use powers of 2: 1, 2, 4, 8 etc
#define leftout (2) // masks, so use powers of 2: 1, 2, 4, 8 etc
#define inleft (4) // masks, so use powers of 2: 1, 2, 4, 8 etc
#define outright (8) // masks, so use powers of 2: 1, 2, 4, 8 etc
#define inright (16) // masks, so use powers of 2: 1, 2, 4, 8 etc
osEventFlagsId_t touchEvtFlags ;          // event flags


/*--------------------------------------------------------------
 *   Thread: t_touch
 *   Purpose: Read touch position periodically.
 *   - Polls the touch pad every 2 seconds.
 *   - Outputs the touch distance to the serial terminal.
 *   - Signals the t_controlLED thread based on specific touch positions.
 *--------------------------------------------------------------*/
osThreadId_t t_touch;      /* id of thread to read touch pad periodically */

// convert unsigned 8-bit to XXX
void uToString(uint8_t a, char* s) {  

    // array of digits
    int digit[3] ;  // [0] least significant
    uint8_t a_dash ;

    // digits
    int ix;
    for (ix = 0 ; ix < 3; ix++) {
        a_dash = a / 10 ;   // 234 --> 23 
        digit[2-ix] = a - (10 * a_dash) ;  // 234 - 230 --> 4
        a = a_dash ;    // 23
    }
    
    // skip leading zero
    ix = 0 ;
    while ( (ix < 2) && (digit[ix] == 0) ) {
        s[ix] = ' ' ;
        ix++ ;
    }
    
    // characters
    while (ix < 3) {
        s[ix] = digit[ix] + '0' ;
        ix++ ;
    }
}

char distStr[] = "dist = XXX" ;
//                01234567890

#define None (2)
#define LeftOut (3)
#define LeftIn (4)
#define RightOut (5)
#define RightIn (6)


void touchThread(void *arg) {
    uint8_t tsiPos ; 
    int softkey = None;

    while(1) {
        osDelay(25) ;
        tsiPos = readTSIDistance() ;
        
        // write distance
        uToString(tsiPos, &distStr[7]) ;
        sendMsg(distStr, CRLF) ;   

	    		  // Determine touch region and set corresponding event flags
			  switch (softkey) {
					case None:
						  if (tsiPos > 3 && tsiPos < 9) {
							    softkey = LeftOut;
							    osEventFlagsSet(touchEvtFlags, leftout);

							}
							if (tsiPos > 13 && tsiPos < 19) {
							    softkey = LeftIn;
								  osEventFlagsSet(touchEvtFlags, inleft);
							}
							if (tsiPos > 33) {
							    softkey = RightOut;
								  osEventFlagsSet(touchEvtFlags, outright);
							}
							if (tsiPos > 23 && tsiPos < 29) {
								  softkey = RightIn;
								  osEventFlagsSet(touchEvtFlags, inright);
								  
							}
						  break;
					
					case LeftOut:
						  if (tsiPos < 3 || tsiPos > 9) {
							    softkey = None;
							}
					    break;
					
					case LeftIn:
						  if (tsiPos < 13 || tsiPos > 19) {
							    softkey = None;
							}							
						  break;
					
					case RightOut:
						  if (tsiPos < 33) {
							    softkey = None;
							}				
					    break;
					
					case RightIn:
						  if (tsiPos < 23 || tsiPos > 29) {
							    softkey = None;
							}
						  break;
				}
    }
}


/*--------------------------------------------------------------
 *   Thread: t_controlLED
 *   Purpose: Lights blue or red LED based on touch events.
 *   - Adjusts brightness of the blue and red LEDs.
 *   - Clears the event flags after processing.
 *--------------------------------------------------------------*/

osThreadId_t t_controlLED;        /* id of thread to flash red led */

// colour brightness
unsigned int r;
unsigned int b;
unsigned int currentbBrightness = 0;
unsigned int currentrBrightness = 0;
enum LED currentLed;
bool isLeftOutPressed = false;
bool isInLeftPressed = false;
bool isOutRightPressed = false;
bool isInRightPressed = false;

//#define BLUEON (0)
//#define BLUEOFF (1)

void controlLEDThread (void *arg) {
    uint32_t flags ;	// returned by osEventFlagWait	
    while (1) {
        // Wait for any touch event flag to be set
        flags = osEventFlagsWait(touchEvtFlags, leftout | inleft | outright | inright, osFlagsWaitAny, osWaitForever);

       
        if (flags & leftout) {
            sendMsg("Outer Left Key Pressed", CRLF);
            if (currentLed == Blue && currentbBrightness < MAXBRIGHTNESS) {
                currentbBrightness++;
                setLEDBrightness(currentLed, currentbBrightness);
            } else if (currentLed == Red && currentrBrightness < MAXBRIGHTNESS) {
                currentrBrightness++;
                setLEDBrightness(currentLed, currentrBrightness);
            }
            osEventFlagsClear(touchEvtFlags, leftout);
        }

        
        if (flags & inleft) {
            sendMsg("Inner Left Key Pressed", CRLF);
            currentLed = Red;
            osEventFlagsClear(touchEvtFlags, inleft);
        }

       
        if (flags & outright) {
            sendMsg("Outer Right Key Pressed", CRLF);
            if (currentLed == Blue && currentbBrightness > 0) {
                currentbBrightness--;
                setLEDBrightness(currentLed, currentbBrightness);
            } else if (currentLed == Red && currentrBrightness > 0) {
                currentrBrightness--;
                setLEDBrightness(currentLed, currentrBrightness);
            }
            osEventFlagsClear(touchEvtFlags, outright);
        }

       
        if (flags & inright) {
            sendMsg("Inner Right Key Pressed", CRLF);
            currentLed = Blue;
            osEventFlagsClear(touchEvtFlags, inright);
        }
    }
}

/*----------------------------------------------------------------------------
 * Application main
 *   Initialise I/O
 *   Initialise kernel
 *   Create threads
 *   Start kernel
 *---------------------------------------------------------------------------*/

int main (void) { 
    
    // System Initialization
    SystemCoreClockUpdate();
  
    // Initialise RGB LEDs 
    configureRGB() ;

		// enable the peripheralclock
    enablePeripheralClock() ;
	

    // Configure TPM
    configureTPMClock() ;    // clocks to all TPM modules
    configureTPM0forPWM() ;  // configure PWM on TPM0 (all LEDs)
	
    setLEDBrightness(Red, 0) ;
    setLEDBrightness(Blue, 0) ;
    setLEDBrightness(Green, 0);
	


    // Configure pin multiplexing
    configureLEDforPWM() ;            // Configure LEDs for PWM control
    //configureGPIOinput();
    init_UART0(115200) ;

    // Initialize CMSIS-RTOS
    osKernelInitialize();
    
    // initialise serial port 
    initSerialPort() ;

    // initialise touch sensor
    TSI_init() ;

    // Create event flags
    touchEvtFlags = osEventFlagsNew(NULL);
    
    // Create threads
    t_touch = osThreadNew(touchThread, NULL, NULL); 
    t_controlLED = osThreadNew(controlLEDThread, NULL, NULL); 
 
    osKernelStart();    // Start thread execution - DOES NOT RETURN
    for (;;) {}         // Only executed when an error occurs
}
