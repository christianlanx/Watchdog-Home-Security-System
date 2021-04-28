file "./build/button_untimed.elf"

#Option: STLink
#target extended-remote :4242

#Option: OpenOCD
target remote localhost:3333

monitor reset init
monitor halt


load
break main

continue
