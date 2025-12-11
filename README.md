# Plasma <!-- omit in toc -->

## Pico, Pico W and RP2350 powered APA102 and WS281X LED drivers <!-- omit in toc -->

This repository is home to the MicroPython firmware and examples for Plasma 2040, Plasma Stick (Pico W Aboard), Plasma 2350 (RP2350) and Plasma 2350 W (RP2350 and RM2).

:warning: Looking for Plasma on the Raspberry Pi or Picade? Go here: https://github.com/pimoroni/plasma-python

- [Get Plasma](#get-plasma)
- [Download Firmware](#download-firmware)
- [Installation](#installation)
  - [Plasma 2350 \& 2350 W](#plasma-2350--2350-w)
  - [Plasma Stick 2040 W](#plasma-stick-2040-w)
  - [Plasma 2040](#plasma-2040)
- [Useful Links](#useful-links)
- [Other Resources](#other-resources)


## Get Plasma

* Plasma 2350 W - https://shop.pimoroni.com/products/plasma-2350-w
* Plasma 2350 - https://shop.pimoroni.com/products/plasma-2350
* Plasma Stick 2040 W - :warning: EOL - https://shop.pimoroni.com/products/plasma-stick-2040-w
* Plasma 2040 - :warning: EOL - https://shop.pimoroni.com/products/plasma-2040

## Download Firmware

You can find the latest firmware releases at [https://github.com/pimoroni/plasma/releases/latest](https://github.com/pimoroni/plasma/releases/latest).

For each board there are two choices, a regular build that just updates the firmware and a "-with-filesystem" build which includes a selection of [examples](examples) depending upon your board.

:warning: If you've changed any of the code on your board then back up before flashing "-with-filesystem" - *your files will be erased!*

## Installation

### Plasma 2350 & 2350 W

1. Connect Plasma 2350 (W) to your computer with a USB-C cable.
2. Put your device into bootloader mode by holding down the BOOT button whilst tapping RST.
3. Drag and drop the downloaded .uf2 file to the "RP2350" drive that appears.
4. Your device should reset, and you should then be able to connect to it using Thonny.

### Plasma Stick 2040 W

1. Connect Plasma 2040 to your computer with a micro USB cable.
2. Put your device into bootloader mode by holding down the BOOT button whilst tapping RST.
3. Drag and drop the downloaded .uf2 file to the "RPI-RP2" drive that appears.
4. Your device should reset, and you should then be able to connect to it using Thonny.

### Plasma 2040

1. Connect Plasma 2040 to your computer with a USB-C cable.
2. Put your device into bootloader mode by holding down the BOOT button whilst tapping RST.
3. Drag and drop the downloaded .uf2 file to the "RPI-RP2" drive that appears.
4. Your device should reset, and you should then be able to connect to it using Thonny.

## Useful Links

* [Learn: Getting started with Plasma 2040](https://learn.pimoroni.com/article/plasma-2040)
* [Learn: Assembling Wireless Plasma Kit](https://learn.pimoroni.com/article/assembling-wireless-plasma-kit)
* [Plasma documentation](docs/plasma.md)

## Other Resources

Links to community projects and other resources that you might find helpful can be found below. Note that these code examples have not been written/tested by us and we're not able to offer support with them.

- [Plasma Stick Ambient Light Generator](https://github.com/ksaj/Plasma-Stick-Ambient-Light-Generator)
- [Plasma Stick Halloween Light Show](https://github.com/ksaj/Plasma-Stick-Halloween-Light-Show)
- [77 LED Strip Effects for Plasma 2350](https://github.com/mrglennjones/plasma_2350_fx77)
