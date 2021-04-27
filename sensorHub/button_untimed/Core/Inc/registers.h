/*
* registers.h
* Created on April 15, 2021
* Author: Morgan McCandless
*/

#ifndef REGISTERS_H_
#define REGISTERS_H_

// ---------- Register Definitions --------------------
/****************** GPIOS ****************************/
// Port A
#define GPIOA ((GPIO_TypeDef*)0x40020000)
#define GPIOA_MODER (GPIOA + GPIO_MODER_OFFSET)
#define GPIOA_OTYPER (GPIOA + GPIO_OTYPER_OFFSET)
#define GPIOA_OSPEEDR (GPIOA + GPIO_OSPEEDR_OFFSET)
#define GPIOA_PUPDR (GPIOA + GPIO_OSPEEDR_OFFSET)
#define GPIOA_IDR (GPIOA + GPIO_IDR_OFFSET)
#define GPIOA_ODR (GPIOA + GPIO_ODR_OFFSET)
#define GPIOA_BSRR (GPIOA + GPIO_BSRR_OFFSET)
#define GPIOA_LCKR (GPIOA + GPIO_LCKR_OFFSET)
#define GPIOA_AFRL (GPIOA + GPIO_AFRL_OFFSET)
#define GPIOA_AFRH (GPIOA + GPIO_AFRH_OFFSET)

// ------------- GPIO OFFSET MACROS -----------------
#define GPIO_MODER_OFFSET 0x00
#define GPIO_OTYPER_OFFSET 0x04
#define GPIO_OSPEEDR_OFFSET 0x08
#define GPIO_PUPDR_OFFSET 0x0C
#define GPIO_IDR_OFFSET 0x10
#define GPIO_ODR_OFFSET 0x14
#define GPIO_BSRR_OFFSET 0x18
#define GPIO_LCKR_OFFSET 0x1C
#define GPIO_AFRL_OFFSET 0x20
#define GPIO_ARFH_OFFSET 0x24


#endif // REGISTERS_H_
