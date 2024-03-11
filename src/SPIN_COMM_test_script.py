"""
Copyright (c) 2021-2024 LAAS-CNRS

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 2.1 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: LGLPV2.1
"""

"""
@brief  This is a class for the factory test of Twitst 1.4.1

@author Luiz Villa <luiz.villa@laas.fr>
@author Guillaume Arthaud <thomas.walter@laas.fr>
"""

import serial,  find_devices
from Twist_Class import Twist_Device

twist_vid = 0x2fe3
twist_pid = 0x0100

Twist_ports = find_devices.find_twist_device_ports(twist_vid, twist_pid)
print(Twist_ports)

Twist = Twist_Device(twist_port= Twist_ports[0])


message = Twist.sendCommand("IDLE")
print(message)
message = Twist.sendCommand("POWER_ON")
print(message)
message = Twist.sendCommand("POWER_OFF")
print(message)
message = Twist.sendCommand("DUTY", "LEG1", 0.01)
print(message)
message = Twist.sendCommand("CAPA", "LEG1", "ON")
print(message)
message = Twist.sendCommand( "BUCK", "LEG2", "ON")
print(message)
message = Twist.sendCommand( "BOOST", "LEG1", "ON")
print(message)
message = Twist.sendCommand("LEG","LEG2","ON")
print(message)
message = Twist.sendCommand("DRIVER","LEG2","ON")
print(message)



#---------------REFERENCE TEST------------------------------------
leg_to_test = "LEG1"
reference_names = ["V1","V2","VH","I1","I2","IH"]
reference_values = [1, 2, 3, 4, 5, 6]

message1 = Twist.sendCommand("IDLE")
print(message1)

message1 = Twist.sendCommand("DRIVER",leg_to_test,"ON")
print(message1)



for reference, reference_values in zip(reference_names, reference_values):
    message1 = Twist.sendCommand("POWER_OFF")
    print(message1)
    message1 = Twist.sendCommand("REFERENCE",leg_to_test,reference,reference_values)
    print(message1)
    message1 = Twist.sendCommand("POWER_ON")
    print(message1)


message1 = Twist.sendCommand("IDLE")
print(message1)
