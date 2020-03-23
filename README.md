# Scimon

Two simple game modes for doing a fun rPi3/0 project with software and hardware

The hardware consists of 8 "Stations" spaced evenly in a circle (Every 45°). These buttons are wired back to the rPi. There must be enough conductors in the cable harness to support a SPST switch and an array of LEDs (henceforth "Station Light"). We could use 2 pairs of conductors (One pair for the Station Light and one pair for the SPST switch) or we could optimize and use a common ground (Switch would become Active Low with a pull-up resistor at configured on the input of the rPi)

The code in this project will be mostly/all in C to keep things really fast and closer to the metal. WiringPi will be used to gain access to ISRs on the inputs. While there might be use for other languages (Like porting to Rust eventually), we are going to start here and see where it goes.

Two different Game modes:
 - **Simple "instrument pad"**: This will be the first project to prove out all the I/O and get Audio working. Different sounds (Whether generated or looped files) will be attached to each Station. When the button is pressed, the sound will start. When the button is released, the sound will stop
 
 - **8 Person simon like game**: The classic 1978 Simon game will come to life in an 8 player mode! (Or one person running frantically around the circle trying to get all the beeps and boops.
