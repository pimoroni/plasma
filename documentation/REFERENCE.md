# Plasma: Reference <!-- omit in toc -->

- [Installing](#installing)
  - [Raspberry Pi / Linux](#raspberry-pi--linux)

## Introduction

Plasma is a multi-device LED control library originally intended to animate patterns across the arcade button illumination kits of the same name.

Plasma now supports a variety of LED types: APA102, WS281X (WS2811, WS2812, SK6812), USB/Serial (Plasma USB) and can drive them simultaneously configured as a single continuous strip.

You can use a command-line argument to specify a particular type and configuration of output device, or a .yml config file to specify any permutation.

## Installing

### Raspberry Pi / Linux

Plasma *requires* Python 3, so you should ensure it is installed first:

```
sudo apt install python3 python3-pip
```

You can then install the Python library with pip3:

```
sudo pip3 install plasmalights
```

## Configuring

Plasma can be configured either via a single command-line argument understood by the `auto` constructor.

This argument can either be a device type followed by configuration options, or a path to a `config.yml` file describing multiple devices.

### Available Options

All devices have *required* options which are positional and do not need to be named.

For example the APA102 output requires a data and clock pin like so: `APA102:14:15`

And the Serial output requires a port: `SERIAL:/dev/ttyAMA0`

#### APA102

```
APA102:<gpio_data>:<gpio_clock>
```

* `gpio_data` - BCM pin for data (first argument)
* `gpio_clock` - BCM pin for clock (second argument)
* `gpio_cs` - BCM pin for chip-select (third argument)

#### WS2812

```
WS281X:<strip_type>:<gpio_pin>
```

* `gpio_pin` - The BCM pin that the LEDs are connected to
* `strip_type` - A supported strip type, most of the time this will be `WS2812`
* `channel` - For PWM this will be either channel 0 or 1 depending on the pin used, Plasma will try to guess the right channel when it's not supplied
* `brightness` - Global brightness scale (0-255)
* `freq_hz` - Output signal frequency (usually 800khz)
* `dma` - DMA channel
* `invert` - Invert output signal for NPN-transistor based (inverting) level shifters

Available strip types (note, setting the white element of LEDs is currently not supported):

* `WS2812`
* `SK6812`
* `SK6812W`
* `SK6812_RGBW`
* `SK6812_RBGW`
* `SK6812_GRBW`
* `SK6812_GBRW`
* `SK6812_BRGW`
* `SK6812_BGRW`
* `WS2811_RGB`
* `WS2811_RBG`
* `WS2811_GRB`
* `WS2811_GBR`
* `WS2811_BRG`
* `WS2811_BGR`

#### Serial

### Configuring via the command-line

Supplying a device configuration via the command line is simple. You need to know three things:

1. What device you want to use
2. What port/pin(s) it's connected to
3. How many LEDs it's responsible for

For example, to drive 20 APA102 LEDs connected to pins 14 and 15 you would run an example like so:

```
./rainbow.py APA102:14:15:pixel_count=20
```

And to drive 20 WS281X LEDs connected to pin 18 you would use:

```
./rainbow.py WS281X:18:WS2812:pixel_count=20
```


### Configuring using a config file