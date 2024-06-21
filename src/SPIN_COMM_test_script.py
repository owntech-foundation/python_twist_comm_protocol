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

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import xmlrpc.client as xml
import time
import matplotlib.pyplot as plt
import numpy as np


leg_to_test = "LEG1"
reference_names = ["V1","V2","VH","I1","I2","IH"]
reference_values = [10, 10, 30, 2, 2, 1]
meas_values = [0, 0, 0, 0, 0, 0]

plecs = xml.Server("http://localhost:1080/RPC2").plecs
model = 'PV_string_model'
plecs.set(model+'/Sun', 'Value', str(1))


count = np.linspace(0,22,10)
vmppt = 22
sign = -1
vmppt_step = 0.2
Pnow = 0
Pbefore = 0


ref_base_value =1
ref_step = 0.01
ref_max_value = 1.5
reference = ref_base_value # initializes the reference
# Create a figure and axis
fig, ax = plt.subplots()
line1, = ax.plot([], [], lw=2, label='I1')
line2, = ax.plot([], [], lw=2, label='I2')
line3, = ax.plot([], [], lw=2, label='VMPPT/10')
line4, = ax.plot([], [], lw=2, label='Power/10')

# Set the frame limit
frame_limit = 200

# Initialize empty lists for x and y data
xdata, ydata1, ydata2, ydata3, ydata4 = [], [], [], [], []
# Set up the plot parameters
ax.set_xlim(0, frame_limit)    # while count<6 :
      #   meas_values[count] = Twist.getMeasurement(reference_names[count])

      #   # message = Twist.getMeasurement('I1')
      #   # message = Twist.getMeasurement('I2')
      #   # message = Twist.getMeasurement('VH')
      #   # message = Twist.getMeasurement('IH')
      #   count = count + 1
      # ydata.append(meas_values)  # Simulate real-time data
ax.legend()
ax.set_ylim(-2, 7)
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Real-time Plot')

# Function to initialize the plot
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    line4.set_data([], [])
    return line1, line2, line3, line4

def reference_update():
  global reference
  reference = reference + ref_step
  if reference > ref_max_value : reference = ref_base_value

# Function to update the plot
def update(frame):
  global reference
  global vmppt
  global sign
  global vmppt_step
  global Pnow
  global Pbefore

  if frame == frame_limit:
      xdata.clear()
      ydata1.clear()
      ydata2.clear()
      ydata3.clear()
      ydata4.clear()
      ax.set_xlim(frame, frame + frame_limit)
  else:
    xdata.append(frame)

    Pnow = Twist.getMeasurement('V1')*Twist.getMeasurement('I1')
    if (Pnow<Pbefore) : sign = -sign
    vmppt = vmppt + sign * vmppt_step
    Pbefore = Pnow
    Twist.sendCommand("REFERENCE","LEG2","V2",vmppt)
    time.sleep(10e-3)
    v1_meas = Twist.getMeasurement('V1')

    plecs.set(model+'/Vref', 'Value', str(v1_meas))
    if frame == 30 : plecs.set(model+'/Sun', 'Value', str(0.8))
    if frame == 50 : plecs.set(model+'/Sun', 'Value', str(0.6))
    if frame == 75 : plecs.set(model+'/Sun', 'Value', str(0.4))
    if frame == 100 : plecs.set(model+'/Sun', 'Value', str(0.6))
    if frame == 125 : plecs.set(model+'/Sun', 'Value', str(0.8))
    if frame == 150 : plecs.set(model+'/Sun', 'Value', str(1))
    data = plecs.simulate(model)
    values1 = data['Values'][0]
    last_10_values1 = values1[-10:]
    average_values1 = sum(last_10_values1) / len(last_10_values1)
    Twist.sendCommand("REFERENCE","LEG1","I1",average_values1)

    # reference_update()
    y_value1 = Twist.getMeasurement('I1')  # Convert the string to a float

    ydata1.append(y_value1)  # Append the float value to ydata1

    ydata2.append(Twist.getMeasurement('I2'))  # Append the float value to ydata2

    ydata3.append(vmppt/10)  # Append the float value to ydata1
    ydata4.append(Pnow/10)  # Append the float value to ydata1
    line1.set_data(xdata, ydata1)
    line2.set_data(xdata, ydata2)
    line3.set_data(xdata, ydata3)
    line4.set_data(xdata, ydata4)


  return line1, line2, line3, line4

twist_vid = 0x2fe3
twist_pid = 0x0101

Twist_ports = find_devices.find_twist_device_ports(twist_vid, twist_pid)
print(Twist_ports)

Twist = Twist_Device(twist_port= Twist_ports[0])













# #---------------REFERENCE TEST------------------------------------

message1 = Twist.sendCommand("IDLE")
print(message1)

message = Twist.sendCommand( "BUCK", "LEG1", "ON")
print(message)
message = Twist.sendCommand( "BUCK", "LEG2", "ON")
print(message)

message = Twist.sendCommand("LEG","LEG1","ON")
print(message)
message = Twist.sendCommand("LEG","LEG2","ON")
print(message)

message1 = Twist.sendCommand("REFERENCE","LEG1","I1",0.5)

print(message1)

message = Twist.sendCommand("POWER_ON")
print(message)


# # message = Twist.sendCommand("POWER_OFF")
# print(Twist.getLine())
# for test in range(1) : print(Twist.getMeasurement('V1'))

# gen_value = '40'
# init_value = '30'
# for voltage_value in count :
#     plecs.set(model+'/Vref', 'Value', str(voltage_value))
#     # plecs.set(model+'/Constant','Value',init_value)
#     # g = plecs.get(model+'/Out1')

#     data = plecs.simulate(model)

#     # Extracting time and values
#     time = data['Time']
#     values1 = data['Values'][0]
#     # values2 = data['Values'][1]
#     # values3 = data['Values'][2]
#     # values4 = data['Values'][3]

#     # Extracting the last 10 values for values1 and values2
#     last_10_values1 = values1[-10:]
#     # last_10_values2 = values2[-10:]
#     # last_10_values3 = values3[-10:]
#     # last_10_values4 = values4[-10:]

#     # Calculating the average of the last 10 values
#     average_values1 = sum(last_10_values1) / len(last_10_values1)
#     # average_values2 = sum(last_10_values2) / len(last_10_values2)
#     # average_values3 = sum(last_10_values3) / len(last_10_values3)
#     # average_values4 = sum(last_10_values4) / len(last_10_values4)

#     print(f"Average of last 10 values for values1: {average_values1}")
#     # print(f"Average of last 10 values for values2: {average_values2}")
#     # print(f"Average of last 10 values for values3: {average_values3}")
#     # print(f"Average of last 10 values for values4: {average_values4}")

#     message1 = Twist.sendCommand("REFERENCE",leg_to_test,"I1",average_values1)
#     print(Twist.getMeasurement('I1'))

try:
  ani = animation.FuncAnimation(fig, update, frames=range(frame_limit), init_func=init, blit=True)
  plt.grid()
  plt.show()
finally:
  message1 = Twist.sendCommand("IDLE")
  print(message1)
