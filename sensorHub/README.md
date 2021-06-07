--- Introduction ---
README file for the sensor hub
Author: Morgan McCandless

----------------------------
sensorHub file organization:

--- int_hub_timed ---
Current build of the sensorHub. File organization of this directory is described later in this document. 

--- Tutorials ---
Contains internal tutorials used by the team on how to use the HAL library.
- button_untimed - tutorial on how to use GPIO input and output
- timerTutorial - tutorial on how to use timers and interrupts

--- Components ---
Holds smaller components of the sensorHub from before integration. 
Includes: 
- door_sensor - the code that is solely responsible for the door sensor
- sound_sensor - the code that is soleley responsible for the sound sensor (DEPRECATED, has inputs which are no longer used)
- integrated_hub - an integrated version of the sensorHub (DEPRECATED, has inputs which are no longer used, relies on an interrupt from the Raspberry Pi which ended up not working)

----------------------------
int_hub_timed file organization:
- Makefile - compiles the C code (only edit if you add files instead of just editing existing files)
- STM32F404VGTx_FLASH.ld - flash file, never directly interacted with by user (DO NOT EDIT)
- startup_stm32f407xx.s - assembly file for board startup, never directly interacted with by user (DO NOT EDIT)
- .mxproject - identifier for STM32CubeMX software (DO NOT EDIT)
- int_hub_timed.ioc - project file for STM32CubeMX software (DO NOT EDIT)
- .gdbinit - initializes gdb for arm cross compiler
- Middlewares - directory that contains files for the Middlewares (DO NOT EDIT ANY FILES IN THIS DIRECTORY)
- USB_HOST - directory that contains files for the USB hosting (DO NOT EDIT ANY FILES IN THIS DIRECTORY)
- Drivers - directory that contains driver information (DO NOT EDIT ANY FILES IN THIS DIRECTORY)

--- build ---
Contains results from running "make," re-generate by running "make clean" then make again." DO NOT EDIT ANY FILES IN THIS DIRECTORY
Relevant files: 
- int_hub_timed.bin - binary executable
- int_hub_timed.hex - hex executable
- int_hub_timed.elf - executable for running the debugger

--- Core ---
Contains all relevant .c and .h files for the user
-- Inc --
Contains all relevant header files to the user
- main.h - has all dependencies for main
- stm32f4xx_hal_conf.h - has all hal library imports and configuration (DO NOT EDIT)
- stm32f4xx_it.h - interrupt handler dependencies
-- Src --
Contains all relevant .c files for the user
- main.c - has the main function as well as all Inits (and user functions, if applicable)
- stm32f4xx_hal_msp.c - has all hal configuration (DO NOT EDIT)
- stm32f4xx_it.c - interrupt handlers
- system_stm32f4xx_it.c - system configuration (DO NOT EDIT)


----------------------------
Necessary software to compile, debug, and flash:
- arm_none_eabi: arm cross-compiler
- OpenOCD: open-source on-chip debugger
- Texane/STLink - flashing software

----------------------------
Important commands for debugging and flashing (execute all in int_hub_timed directory):

--- Debugging ---
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
Open another terminal, navigate to int_hub_timed directory
arm-none-eabi -tui

--- Flashing ---
Options:
st-flash -format ihex write ./build/*.hex
st-flash write ./build/*.bin 0x8000000

 
