### Scimon

Two simple game modes for doing a fun rPi3/0 project with software and hardware

The hardware consists of 8 "Stations" spaced evenly in a circle (Every 45°). These buttons are wired back to the rPi. There must be enough conductors in the cable harness to support a SPST switch and an array of LEDs (henceforth "Station Light"). We could use 2 pairs of conductors (One pair for the Station Light and one pair for the SPST switch) or we could optimize and use a common VDD (We cannot use a common ground because the FET is after the load) (Switch would become Active High with a pull-down resistor at configured on the input of the rPi)

The code in this project will be mostly/all in C to keep things really fast and closer to the metal. WiringPi (Thank you Gordon!!!!) will be used to code ISRs on the inputs to track button presses without polling. While there might be use for other languages (Like porting to Rust eventually), we are going to start here and see where it goes.

Two different Game modes:
 - **Simple "instrument pad"**: This will be the first project to prove out all the I/O and get Audio working. Different sounds (Whether generated or looped files) will be attached to each Station. When the button is pressed, the sound will start. When the button is released, the sound will stop
 
 - **8 Person simon like game**: The classic 1978 Simon game will come to life in an 8 player mode! (Or one person running frantically around the circle trying to get all the beeps and boops.


#The Station Circuit:
Each station will be made up of a "Button" for the player/user to press, and a "Light" that will illuminate when the User/Player presses the button (Or any other logic). A small protecton circuit will be constructed to block ESD and ringing induced from the "long" cable and human factors. While there shouldn't be an opportunity for ESD during normal operation (Because the button is in a plastic housing electrically isolated from the rPi input), we will practice safe static. The small handful of components should also offer us a "hardware debounce" and nice clean signal (TBD: gunna have to put a scope on it).

The rPi will be in a central hub enclosure save from the elements (This is meant to run outside on battery power). Each Station will have a CAT5 cable run to it to supply power/signal for the lighting and a path for the Button to switch too.

# rPi Input:
The capabilities of the rPi inputs can be read about here: [gpio-pin-electrical-specifications](http://www.mosaic-industries.com/embedded-systems/microcontroller-projects/raspberry-pi/gpio-pin-electrical-specifications)

![GPIO Pins](/circuits/raspberry-pi-circuit-gpio-input-pins.png)

Some example protection circuits can be found here: [Protecting Inputs](https://www.digikey.com/en/articles/techzone/2012/apr/protecting-inputs-in-digital-electronics)
8 inputs on the rPi will be select as INPUTs to monitor the 8 station buttons. The WiringPi library will be utilized to register "Interrupt Service Routines" (ISR) so that we do not have to set up a tight polling loop to monitor the buttons. This frees the processor(s) to go and do fun things like play sounds and yell at players for screwing up. Each Input will have an external protection circuit to help remove/minimize ringing/ESD from the button. The rPi chipset offers a programable pullup/pulldown resistor, so we will not needs to add this to the circuit.

We will be using this RC protection circuit:

![RC-circuit](/circuits/input-protection-rc.jpeg)

The SPST Button in the station will utilize the VDD wire from the LEDs. This effectively makes our switch "Active High", so we will need to configure the input at the rPi with a pull-down resistor. When configuring an ISR for a pin in wiringPi, we can select from watching the rising-edge, falling-edge, or both. We are going to subscribe to both since our Music instrument mode needs both (To turn sound on and off)

# Button Lighting Circuit:
Each button at a station will have an LED array inside it to light the button up. The lighting of the button itself is software controlled (The lighting of the button is not wired to the button switch). 8 I/O pins configured as outputs need to be selected from the rPi. rPi output pins can only source 16mA, so these is useless to drive an LED array. So instead, we'll connect each output pin to a MOSFET which will be directly driving the lighting. The following FET (SOT23) was selected for the rPi output to control
[SOT23 FET for driving Button LEDs](https://www.digikey.com/products/en?keywords=DMN2041L-7DICT-ND)
This FET's gate is fully saturated at the 3.3V output logic level. So turning the rPi's output "ON" will turn the FET Completely ON and then drive the lights in the button.


# rPi Pin Selection:
//TODO: