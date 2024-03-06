# Power Test Bench Communication Library

This repository contains a communication library for the power test bench of the Twist board converter developed by LAAS-CNRS.

## License

This library is distributed under the terms of the GNU Lesser General Public License (LGPL) version 2.1 or later. See the [LICENSE](LICENSE) file for details.

## Overview

The `comm_protocol.h` file serves as the main entry point of the OwnTech Power API. It provides communication protocols and data structures for interacting with the power test bench.

## Communication Protocol

The communication protocol consists of commands and messages exchanged between the test bench and external systems. These commands and messages are used to configure settings, send control signals, and receive measurements.

### Examples of Supported Commands

Here are a few examples of supported commands and their functionalities:

- **Setting Duty Cycle**:
  - Command: `_LEG1_d_0.5`
  - Description: Sets the duty cycle of LEG1 to 50%.

- **Setting Reference Value**:
  - Command: `_LEG2_r_3.0`
  - Description: Sets the reference value for LEG2 to 3.0.

- **Enabling Boolean Setting**:
  - Command: `_LEG1_l_on`
  - Description: Turns on a boolean setting for LEG1.

- **Setting Calibration Parameters**:
  - Command: `_VX_g_2.5_o_1.0`
  - Description: Sets the gain to 2.5 and offset to 1.0 for a tracking variable named "VX".

- **Changing Tester Mode**:
  - Command: `_i`
  - Description: Switches the tester to IDLE mode.
