file "./build/sensorHubDen.elf"
target remote localhost:3333
monitor reset init
monitor halt
load
break main
continue
