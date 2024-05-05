import socket as sc
import math as m
import time 
import threading as th
import tkinter as tk
import copy

class Refueling(tk.Tk):
    def __init__(self) -> None:
        """
        Initializes the Refueling class.

        Args:
            None

        Returns:
            None
        """
    
        super().__init__()
        self.geometry('1200x500')
        
        #Buttons init
        self.button1 = tk.Button(self, text='MAN', padx=50, pady=20, command = lambda: self.setControlMode('MAN'))
        self.button2 = tk.Button(self, text='AUTO', padx=50, pady=20, command = lambda: self.setControlMode('AUTO'))
        self.button3 = tk.Button(self, text='OFF', padx=50, pady=20, command= lambda: self.setControlMode('OFF'))
        self.button4 = tk.Button(self, text='N2_fill_valve_OPEN', padx=100, pady=20, command=lambda: self.controlValves('N2_fill_valve', 1, duration=self.duration))
        self.button5 = tk.Button(self, text='N2_fill_valve_CLOSE', padx=100, pady=20, command=lambda: self.controlValves('N2_fill_valve', 0, duration=self.duration))
        self.button6 = tk.Button(self, text='N2O_fill_valve_OPEN', padx=100, pady=20, command=lambda: self.controlValves('N2O_fill_valve', 1, duration=self.duration))
        self.button7 = tk.Button(self, text='N2O_fill_valve_CLOSE', padx=100, pady=20, command=lambda: self.controlValves('N2O_fill_valve', 0, duration=self.duration))
        self.button8 = tk.Button(self, text='High_servo_OPEN', padx=100, pady=20, command=lambda: self.controlValves('High_servo', 1, duration=self.duration))
        self.button9 = tk.Button(self, text='High_servo_CLOSE', padx=100, pady=20, command=lambda: self.controlValves('High_servo', 0, duration=self.duration))
        self.button10 = tk.Button(self, text='Low_servo_OPEN', padx=100, pady=20, command=lambda: self.controlValves('Low_servo', 1, duration=self.duration))
        self.button11 = tk.Button(self, text='Low_servo_CLOSE', padx=100, pady=20, command=lambda: self.controlValves('Low_servo', 0, duration=self.duration))
        self.button12 = tk.Button(self, text='N2_release_valve_OPEN', padx=100, pady=20, command=lambda: self.controlValves('N2_release_valve', 1, duration=self.duration))
        self.button13 = tk.Button(self, text='N2_release_valve_CLOSE', padx=100, pady=20, command=lambda: self.controlValves('N2_release_valve', 0, duration=self.duration))
        self.button14 = tk.Button(self, text='N2O_release_valve_OPEN', padx=100, pady=20, command=lambda: self.controlValves('N2O_release_valve', 1, duration=self.duration))
        self.button15 = tk.Button(self, text='N2O_release_valve_CLOSE', padx=100, pady=20, command=lambda: self.controlValves('N2O_release_valve', 0, duration=self.duration))
        self.button16 = tk.Button(self, text='OX_FILL_FINISH', padx=100, pady=20, command=self.callBackOX_fill_end)
        self.button17 = tk.Button(self, text='END', padx=100, pady=20, command=lambda: self.setControlMode('END'))
        
        #Entry init
        self.entry = tk.Entry(self)
        
        #Buttons placement
        self.button1.grid(row=0, column=0, padx=10, pady=10)
        self.button2.grid(row=1, column=0, padx=10, pady=10)
        self.button3.grid(row=2, column=0, padx=10, pady=10)
        self.button4.grid(row=0, column=1, padx=10, pady=10)
        self.button5.grid(row=0, column=2, padx=10, pady=10)
        self.button6.grid(row=1, column=1, padx=10, pady=10)
        self.button7.grid(row=1, column=2, padx=10, pady=10)
        self.button8.grid(row=2, column=1, padx=10, pady=10)
        self.button9.grid(row=2, column=2, padx=10, pady=10)
        self.button10.grid(row=3, column=1, padx=10, pady=10)
        self.button11.grid(row=3, column=2, padx=10, pady=10)
        self.button12.grid(row=4, column=1, padx=10, pady=10)
        self.button13.grid(row=4, column=2, padx=10, pady=10)
        self.button14.grid(row=5, column=1, padx=10, pady=10)
        self.button15.grid(row=5, column=2, padx=10, pady=10)
        self.button16.grid(row=5, column=0, padx=10, pady=10)
        self.button17.grid(row=3, column=0, padx=10, pady=10)
        
        #Entry placement
        self.entry.grid(row=4, column=0, padx=10, pady=10)
        
        #Configurations and bindings
        self.button4.config(state='disabled')
        self.button5.config(state='disabled')
        self.button6.config(state='disabled')
        self.button7.config(state='disabled')
        self.button8.config(state='disabled')
        self.button9.config(state='disabled')
        self.button10.config(state='disabled')
        self.button11.config(state='disabled')
        self.button12.config(state='disabled')
        self.button13.config(state='disabled')
        self.button14.config(state='disabled')
        self.button15.config(state='disabled')
        self.button16.config(state='disabled')
        self.entry.bind('<Return>', self.handleEntryChange)
        
        #Class params init
        self.control_mode = "OFF"
        self.duration = 0
        self.ox_fill_exit = False
        self.info_print_constant = 5 #s
        self.autoDurationConst = 0.5 #s
        self.High_p_previous = None
        self.pressurizer_fill_variant = 1
        self.OxidiserPress_variant = 1
        self.GLOBAL_START_TIME = time.time()
        self.preamble_dict = {
            'ID_SEND': 150,
            'PL_SEND': 66,
            'MSG_ID_SEND': 201,
            'ID_RECEIVE': 160,
            'PL_RECEIVE': 67,
            'MSG_ID_RECEIVE': 200
        }
        self.card_slots = {
            'CARD_IO1_SLOT': 5,
            'CARD_IO2_SLOT': 6,
            'CARD_IO3_SLOT': 7,
            'CARD_CURRENT_LOOP_SLOT': 2,
            'CARD_THERMISTOR_SLOT': 4,
            'CARD_LOAD_CELL_SLOT': 0
        }
        self.card_ids = {
            'CARDID_EMPTY': 0,
            'CARDID_IO': 1,
            'CARDID_CURRENT_LOOP': 2,
            'CARDID_THERMISTOR': 4,
            'CARDID_LOAD_CELL': 8,
            'CARDID_STRAIN_ROSETTE': 16,
            'CARDID_CAPACITANCE': 32
        }
        self.IO_card_message_order = {
            'H0_bridge_state_ind': 19,          # (0 - Hard start, 127 - Middle, 255 - Hard end)
            'H1_bridge_state_ind': 20,
            'H2_bridge_state_ind': 21,
            'H0_bridge_fault_state_ind': 16,    # (0 - OK, 255 - Fault)
            'H1_bridge_fault_state_ind': 17,
            'H2_bridge_fault_state_ind': 18,
            'High_servo_state_ind': 2,             # in degrees (0 - 90)
            'Low_servo_state_ind': 3
        }
        self.Current_loop_message_order = {
            'Low_p_ind': 0,   #13,
            'High_p_ind': 1,    #11,
            'GSE_oxidiser_p_ind':  2, #8,
            'GSE_Pressurizer_p_ind': 3, #9,
            'N2O_fuel_level_ind': 4
        }
        self.Cimrman_communication_protocol = {
            'FC_ID': 100,
            'FC_PACKET_LENGTH': 33,
            'FC_SERVO_OP': 2,
            'FC_SERVO_CL': 1,
            'FC_SERVO_PULSE': 3,
            'FC_SERVO_IGNORE': 0,
            'FC_GND_MSG_SERVO_CTRL': 71
        }
        self.IO_card_supported_commands = {
            'H_Bridge_0_open': 16,
            'H_Bridge_0_close': 17,
            'H_Bridge_0_nudge_open': 18,
            'H_Bridge_0_nudge_close': 19,
            'H_Bridge_1_open': 20,
            'H_Bridge_1_close': 21,
            'H_Bridge_1_nudge_open': 22,
            'H_Bridge_1_nudge_close': 23,
            'H_Bridge_2_open': 24,
            'H_Bridge_2_close': 25,
            'H_Bridge_2_nudge_open': 26,
            'H_Bridge_2_nudge_close': 27,
            'H_Bridge_0_stop': 28,
            'H_Bridge_1_stop': 29,
            'H_Bridge_2_stop': 30,
            'H_Bridge_0_turn_forward': 70,
            'H_Bridge_1_turn_forward': 73,
            'H_Bridge_2_turn_forward': 76,
            'H_Bridge_0_turn_backward': 71,
            'H_Bridge_1_turn_backward': 74,
            'H_Bridge_2_turn_backward': 77,
            'H_Bridge_0_stop': 72,
            'H_Bridge_1_stop': 75,
            'H_Bridge_2_stop': 78,
            'Set_power_output_0_high': 44,
            'Set_power_output_1_high': 45,
            'Set_power_output_2_high': 46,
            'Set_power_output_3_high': 47,
            'Set_power_output_0_low': 60,
            'Set_power_output_1_low': 61,
            'Set_power_output_2_low': 62,
            'Set_power_output_3_low': 63,
            'Toggle_power_output_0_state': 92,
            'Toggle_power_output_1_state': 93,
            'Toggle_power_output_2_state': 94,
            'Toggle_power_output_3_state': 95,
            'Open_digital_servo_0': 64,
            'Close_digital_servo_0': 65,
            'Pulse_digital_servo_0': 66,
            'Open_digital_servo_1': 67,
            'Close_digital_servo_1': 68,
            'Pulse_digital_servo_1': 69
        }
        self.Sensor_calibration = {
            'PT5302_GAIN': 0.05,   #100 bar
            'PT5302_OFFSET': -25,
            'PT5500_GAIN': 0.2,    #300 bar
            'PT5500_OFFSET': -100,
            'TA3145_GAIN': 12.5,
            'TA3145_OFFSET': -100
        }
        self.StateFlow_constants = {
            'Acceptable_press_offset': 5, #bar   needs to be set to higher value if simple regulator is used
            'Press_Transition_time_const': 3, #s
            'Desired_pressure_in_pressure_section1': 150, #bar
            'Desired_pressure_in_pressure_section2': 180, #bar
            'Number_of_decisive_time_cycles': 5,
            'Large_State_transition_time_const': 5, #s
            'Small_State_transition_time_const': 2, #s
            'Desired_pressure_in_oxidiser_tank': 40, #bar
            'Oxidiser_fueling_exit': 1000,  #IF CHANGED, CHANGE IT ALSO IN COMBO BOX
        }
        self.Pressure_drop_indication_constants= {'Pressure_drop_const': 100} #bar (drop of 100 bars will resolve in pressure drop indication)
        self.UDP_ME2GSE = {
            'UDP_GSE_IP': '192.168.1.3',
            'UDP_GSE_IP_V': '127.0.0.1',#'192.168.1.3',
            'UDP_FC_IP': '192.168.1.4',
            'UDP_FC_PORT': 8000,
            'UDP_GSE_PORT': 10003,
            'UDP_GSE_PORT1':10003,
            'UDP_GSE_PORT_V': 10003,
            'UDP_GSE_PORT1_V':10004,
            'UDP_IO_sample_time': 0.05, #s
            'UDP_PL': 68,  #packets
        }
        self.UDP_GSE2ME = {
            'UDP_MY_IP': '127.0.0.2', #'192.168.1.8',
            'UDP_MY_PORT': 10004,#10003,
            'UDP_PL': 69,
            'UDP_CL_sample_time': 0.01, #s
            'UDP_IO_sample_time': 0.05
        }
        self.Control_const = {
            'Period': 2, #s
            'Step': 1 #s
        }
        self.Control_messages = {
            'N2_fill_valve_open' : bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                          self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                          self.IO_card_supported_commands['H_Bridge_1_open']] + [0 for _ in range(63)]),
            
            'N2_fill_valve_close' : bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                           self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                           self.IO_card_supported_commands['H_Bridge_1_close']] + [0 for _ in range(63)]),
            
            'N2_release_valve_open' : bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                             self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO3_SLOT'],
                             self.IO_card_supported_commands['H_Bridge_1_open']] + [0 for _ in range(63)]),
            
            'N2_release_valve_close' : bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                              self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO3_SLOT'],
                              self.IO_card_supported_commands['H_Bridge_1_close']] + [0 for _ in range(63)]),
            
            'High_servo_open_GSE': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                          self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                          self.IO_card_supported_commands['Open_digital_servo_0']] + [0 for _ in range(63)]),
            
            'High_servo_close_GSE': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                           self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                           self.IO_card_supported_commands['Close_digital_servo_0']] + [0 for _ in range(63)]),
            
            'Low_servo_open_GSE': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                         self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                         self.IO_card_supported_commands['Open_digital_servo_1']] + [0 for _ in range(63)]),
            
            'Low_servo_close_GSE': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                          self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                          self.IO_card_supported_commands['Close_digital_servo_1']] + [0 for _ in range(63)]),
            
            'High_servo_open_FC': bytes([self.Cimrman_communication_protocol['FC_ID'], self.Cimrman_communication_protocol['FC_PACKET_LENGTH'],
                         self.Cimrman_communication_protocol['FC_GND_MSG_SERVO_CTRL'], self.Cimrman_communication_protocol['FC_SERVO_OP'],
                         self.Cimrman_communication_protocol['FC_SERVO_IGNORE']] + [0 for _ in range(28)]),
            
            'High_servo_close_FC': bytes([self.Cimrman_communication_protocol['FC_ID'], self.Cimrman_communication_protocol['FC_PACKET_LENGTH'],
                          self.Cimrman_communication_protocol['FC_GND_MSG_SERVO_CTRL'], self.Cimrman_communication_protocol['FC_SERVO_CL'],
                          self.Cimrman_communication_protocol['FC_SERVO_IGNORE']] + [0 for _ in range(28)]),
            
            'Low_servo_open_FC': bytes([self.Cimrman_communication_protocol['FC_ID'], self.Cimrman_communication_protocol['FC_PACKET_LENGTH'],
                            self.Cimrman_communication_protocol['FC_GND_MSG_SERVO_CTRL'], self.Cimrman_communication_protocol['FC_SERVO_IGNORE'],
                            self.Cimrman_communication_protocol['FC_SERVO_OP']] + [0 for _ in range(28)]),
            
            'Low_servo_close_FC': bytes([self.Cimrman_communication_protocol['FC_ID'], self.Cimrman_communication_protocol['FC_PACKET_LENGTH'],
                         self.Cimrman_communication_protocol['FC_GND_MSG_SERVO_CTRL'], self.Cimrman_communication_protocol['FC_SERVO_IGNORE'],
                         self.Cimrman_communication_protocol['FC_SERVO_CL']] + [0 for _ in range(28)]),
            
            'N2O_fill_valve_open': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                          self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                          self.IO_card_supported_commands['H_Bridge_2_open']] + [0 for _ in range(63)]),
            
            'N2O_fill_valve_close': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                           self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO2_SLOT'],
                           self.IO_card_supported_commands['H_Bridge_2_close']] + [0 for _ in range(63)]),
            
            'N2O_release_valve_open': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                             self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO3_SLOT'],
                             self.IO_card_supported_commands['H_Bridge_2_open']] + [0 for _ in range(63)]),
            
            'N2O_release_valve_close': bytes([self.preamble_dict['ID_SEND'], self.preamble_dict['PL_SEND'], 
                              self.preamble_dict['MSG_ID_SEND'], self.card_slots['CARD_IO3_SLOT'],
                              self.IO_card_supported_commands['H_Bridge_2_close']] + [0 for _ in range(63)])
        }
        self.ServoStatesandValues = {
            'Low_p': 0,
            'High_p': 0,
            'GSE_oxidiser_p': 0,
            'GSE_Pressurizer_p': 0,
            'N2O_fuel_level': 0,
            'N2_fill_valve_state': 0,
            'N2_release_valve_state': 0,
            'High_servo_state': 0,
            'Low_servo_state': 0,
            'N2O_fill_valve_state': 0,
            'N2O_release_valve_state': 0
        }
        self.Valve_state_constants = {
            'H_bridge_open_num':  0,#0,
            'H_bridge_close_num': 255, #255,
            'H_bridge_mid_num': 127,
            'Servo_close': 0,
            'Servo_open': 90,
            'H_bridge_fault_state_num': 255
        }
        
        #Socket class params
        self.send_socket = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
        self.receive_socket = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
        self.receive_socket.bind((self.UDP_GSE2ME['UDP_MY_IP'], self.UDP_GSE2ME['UDP_MY_PORT']))
        
        #Threading class params
        self.mutex_lock = th.Lock()
        self.mutex_lock1 = th.Lock()
        self.listening_thread = th.Thread(target=self.listeningThreadFunction)
        self.listening_thread.start()
    
    def callBackOX_fill_end(self) -> None:
        """
        This function sets the `ox_fill_exit` attribute to True.

        Parameters:
            self: The object instance.

        Returns:
            None
        """
        self.ox_fill_exit = True
    
    def handleEntryChange(self, ev: tk.Event) -> None:
        """
        Handles the change event of the entry widget by updating the `duration` attribute.

        Args:
            ev (tk.Event): The event object representing the change event.

        Returns:
            None
        """
        self.duration = float(self.entry.get())
        print(self.duration)
    
    def setControlMode(self, mode:str) -> None:
        """
        Sets the control mode of the system.

        Parameters:
            mode (str): The control mode to set. Valid values are 'OFF', 'MAN', 'AUTO', and 'END'.

        Returns:
            None
            
        Raises:
            None
        """
        if(mode == 'OFF'):
            print()
            print("[INFO] Control mode: OFF")
            print()
            #Setting the control mode to OFF
            self.mutex_lock1.acquire()
            self.control_mode = 'OFF'
            self.mutex_lock1.release()
            
            #Disabling the unused buttons
            self.button4.config(state='disabled')
            self.button5.config(state='disabled')
            self.button6.config(state='disabled')
            self.button7.config(state='disabled')
            self.button8.config(state='disabled')
            self.button9.config(state='disabled')
            self.button10.config(state='disabled')
            self.button11.config(state='disabled')
            self.button12.config(state='disabled')
            self.button13.config(state='disabled')
            self.button14.config(state='disabled')
            self.button15.config(state='disabled')
            self.button16.config(state='disabled')
            
            #Closing all the valves
            self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
            time.sleep(2)               
            self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
            self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
            self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))               
            self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               

        elif(mode == 'MAN'):
            print()
            print('[INFO] Control mode: MAN')
            print()
            #Setting the control mode to MAN
            self.mutex_lock1.acquire()
            self.control_mode = 'MAN'
            self.mutex_lock1.release()
            
            #Enabling the buttons needed for manual control
            self.button4.config(state='normal')
            self.button5.config(state='normal')
            self.button6.config(state='normal')
            self.button7.config(state='normal')
            self.button8.config(state='normal')
            self.button9.config(state='normal')
            self.button10.config(state='normal')
            self.button11.config(state='normal')
            self.button12.config(state='normal')
            self.button13.config(state='normal')
            self.button14.config(state='normal')
            self.button15.config(state='normal')
            
            #Disabling the buttons not needed for manual control
            self.button16.config(state='disabled')
        elif(mode == 'AUTO'):
            print()
            print('[INFO] Control mode: AUTO')
            print()
            #Setting the control mode to AUTO
            self.mutex_lock1.acquire()
            self.control_mode = 'AUTO'
            self.mutex_lock1.release()
            
            #Disabling the buttons not needed for auto control
            self.button4.config(state='disabled')
            self.button5.config(state='disabled')
            self.button6.config(state='disabled')
            self.button7.config(state='disabled')
            self.button8.config(state='disabled')
            self.button9.config(state='disabled')
            self.button10.config(state='disabled')
            self.button11.config(state='disabled')
            self.button12.config(state='disabled')
            self.button13.config(state='disabled')
            self.button14.config(state='disabled')
            self.button15.config(state='disabled')
            self.button16.config(state='disabled')
            
            #Starting the auto thread
            autoThread = th.Thread(target=self.autoMode)
            autoThread.start()
        elif(mode == 'END'):
            print()
            print('[INFO] Control mode: END')
            print()
            
            #Setting the control mode to END
            self.mutex_lock1.acquire()
            self.control_mode = 'END'
            self.mutex_lock1.release()
            
            #Destroying the window
            self.destroy()
            
    
    def PressurizerFill(self, desired_pressure: float, mode:int) -> None:
        """
        Handles the initial pressurizer fill.

        Args:
            desired_pressure (float): The desired pressure for the pressurizer.
            mode (int): Used control option.

        Returns:
            None
        """
        #Simple controller for pressurizer fill
        if(self.pressurizer_fill_variant == 0):  
            start = time.time()
            #Cycling through the loop utill we stay on desired pressure level for a certain time 
            while((time.time() - start) < self.StateFlow_constants['Large_State_transition_time_const']):
                #Getting the current pressure in the high section
                self.mutex_lock.acquire()
                High_section_pressure = self.ServoStatesandValues['High_p']
                self.mutex_lock.release()
                
                #If the difference between desired pressure and current pressure is greater than the acceptable offset
                if(desired_pressure - High_section_pressure > self.StateFlow_constants['Acceptable_press_offset']):
                    #Opening the fill valve for a certain time specified by the autoDurationConst
                    self.controlValves('N2_fill_valve', 1, 'AUTO', self.autoDurationConst)
                    #Resetting the start time
                    start = time.time()
                #Checking if the control mode has been changed
                self.mutex_lock1.acquire()
                auto = self.control_mode
                self.mutex_lock1.release()
                time.sleep(2)
                if(auto != 'AUTO'):
                    break
        #Modified conroller for pressurizer fill
        elif(self.pressurizer_fill_variant == 1):  
            start = time.time()
            High_section_pressure = 0
            time_estimate = self.autoDurationConst
            
            #Cycling through the loop utill we stay on desired pressure level for a certain time 
            while((time.time() - start) < self.StateFlow_constants['Large_State_transition_time_const']):
                #Saving the previous pressure in the high section
                previous_pressure = High_section_pressure
                #Getting the current pressure in the high section
                self.mutex_lock.acquire()
                High_section_pressure = self.ServoStatesandValues['High_p']
                self.mutex_lock.release()
                
                #If the pressure crossed the desired pressure the time estimate is halved
                if((desired_pressure - previous_pressure)*(desired_pressure - High_section_pressure) < 0):
                    time_estimate = time_estimate/2
                    print(f"Time estimate: {time_estimate}")
                #If the difference between desired pressure and current pressure is greater than the acceptable offset
                if(abs(desired_pressure - High_section_pressure) > self.StateFlow_constants['Acceptable_press_offset']):
                    if(High_section_pressure < desired_pressure):
                        #Opening the fill valve for a certain time specified by the time_estimate
                        self.controlValves('N2_fill_valve', 1, 'AUTO', time_estimate)
                    else:
                        #Opening the release valve for a certain time specified by the time_estimate
                        self.controlValves('N2_release_valve', 1, 'AUTO', time_estimate)
                    #Resetting the start time
                    start = time.time()
                
                #Checking if the control mode has been changed
                self.mutex_lock1.acquire()
                auto = self.control_mode
                self.mutex_lock1.release()
                time.sleep(2)
                if(auto != 'AUTO'):
                    break
        
        N2_fill_s = 2
        N2_release_s = 2
        
        #Waiting for the fill and release valves to close
        while(N2_fill_s != 0 or N2_release_s != 0):
            self.mutex_lock.acquire()
            N2_fill_s = self.ServoStatesandValues['N2_fill_valve_state']
            N2_release_s = self.ServoStatesandValues['N2_release_valve_state']
            self.mutex_lock.release()
            time.sleep(2)
        
        return mode + 1
    
    def OxidiserPress(self, desired_pressure: float, mode:int) -> None:
        """
        Handles pressurization of the oxidiser tank.

        Args:
            desired_pressure (float): The desired pressure level for the oxidiser tank.
            mode (int): The current mode of operation.

        Returns:
            None
        """
        #Simple controller for oxidiser pressurization
        if(self.OxidiserPress_variant == 0):
            start = time.time()
            #Cycling through the loop utill we stay on desired pressure level for a certain time
            while((time.time() - start) < self.StateFlow_constants['Large_State_transition_time_const']):
                #Getting the current pressure in the low section
                self.mutex_lock.acquire()
                Low_section_pressure = self.ServoStatesandValues['Low_p']
                self.mutex_lock.release()
                
                #If the difference between desired pressure and current pressure is greater than the acceptable offset
                if(desired_pressure - Low_section_pressure > self.StateFlow_constants['Acceptable_press_offset']):
                    #Opening the high servo valve for a certain time specified by the autoDurationConst
                    self.controlValves('High_servo', 1, 'AUTO', self.autoDurationConst)
                    #Resetting the start time
                    start = time.time()
                
                #Checking if the control mode has been changed
                self.mutex_lock1.acquire()
                auto = self.control_mode
                self.mutex_lock1.release()
                time.sleep(2)
                if(auto != 'AUTO'):
                    break
                
        #Modified controller for oxidiser pressurization
        elif(self.OxidiserPress_variant == 1):  
            start = time.time()
            Low_section_pressure = 0
            time_estimate = self.autoDurationConst
            
            #Cycling through the loop utill we stay on desired pressure level for a certain time
            while((time.time() - start) < self.StateFlow_constants['Large_State_transition_time_const']):
                #Saving the previous pressure in the low section
                previous_pressure = Low_section_pressure
                #Getting the current pressure in the low section
                self.mutex_lock.acquire()
                Low_section_pressure = self.ServoStatesandValues['Low_p']
                self.mutex_lock.release()
                
                #If the pressure crossed the desired pressure the time estimate is halved
                if((desired_pressure - previous_pressure)*(desired_pressure - Low_section_pressure) < 0):
                    time_estimate = time_estimate/2
                
                #If the difference between desired pressure and current pressure is greater than the acceptable offset
                if(abs(desired_pressure - Low_section_pressure) > self.StateFlow_constants['Acceptable_press_offset']):
                    #If the pressure is lower than desired pressure the high servo valve is opened
                    if(Low_section_pressure < desired_pressure):
                        #Opening the high servo valve for a certain time specified by the time_estimate
                        self.controlValves('High_servo', 1, 'AUTO', time_estimate)
                    else:
                        #If the pressure is higher than desired pressure the low servo valve is opened
                        self.controlValves('Low_servo', 1, 'AUTO', time_estimate)
                    start = time.time()
                
                #Checking if the control mode has been changed
                self.mutex_lock1.acquire()
                auto = self.control_mode
                self.mutex_lock1.release()
                time.sleep(2)
                if(auto != 'AUTO'):
                    break
        
        High_servo_s = 2
        Low_servo_s = 2
        
        #Waiting for the high and low servo valves to close
        while(High_servo_s != 0 or Low_servo_s != 0):
            self.mutex_lock.acquire()
            High_servo_s = self.ServoStatesandValues['High_servo_state']
            Low_servo_s = self.ServoStatesandValues['Low_servo_state']
            self.mutex_lock.release()
            time.sleep(2)
        
        return mode + 1
    
    def endPhase(self, mode: int) -> int: 
        """
        Waits for all valve states to reach zero before returning the next mode.

        Args:
            mode (int): The current mode.

        Returns:
            int: The next mode.

        """
        N2_fill_s = 2
        N2_release_s = 2
        High_servo_s = 2
        Low_servo_s = 2
        N2O_fill_s = 2
        N2O_release_s = 2

        #Waiting for all valve states to reach zero
        while(N2_fill_s != 0 or N2_release_s != 0 or High_servo_s != 0 or Low_servo_s != 0 or N2O_fill_s != 0 or N2O_release_s != 0):
            #Getting the current valve states
            self.mutex_lock.acquire()
            N2_fill_s = self.ServoStatesandValues['N2_fill_valve_state']
            N2_release_s = self.ServoStatesandValues['N2_release_valve_state']
            High_servo_s = self.ServoStatesandValues['High_servo_state']
            Low_servo_s = self.ServoStatesandValues['Low_servo_state']
            N2O_fill_s = self.ServoStatesandValues['N2O_fill_valve_state']
            N2O_release_s = self.ServoStatesandValues['N2O_release_valve_state']
            self.mutex_lock.release()
            
            #Closing all the valves
            self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
            time.sleep(2)               
            self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
            self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
            self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
            time.sleep(2)
            self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))               
            self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               

            time.sleep(2)
        
        return mode + 1
    
    def autoMode(self) -> None:
        """
        Executes the automatic mode for refueling.

        This method runs a loop that performs different actions based on the current mode.
        The actions include pressurizer fill, oxidizer pressurization, oxidizer fill, pressurizer fill (2nd phase),
        and ending the phase. The loop continues until the control mode is set to something other than 'AUTO'.

        Returns:
            None
        """
        auto = 'AUTO'
        mode = 0
        
        #Running the loop until the control mode is set to something other than 'AUTO'
        while(auto == 'AUTO'):
            #Performing different actions based on the current mode
            if(mode == 0):
                #Pressurizer fill - 1. Phase
                print("[INFO] Automode: Pressurizer fill - 1. Phase")
                mode = self.PressurizerFill(self.StateFlow_constants['Desired_pressure_in_pressure_section1'], mode)
            elif(mode == 1):
                #Oxidiser pressurization
                print("[INFO] Automode: Oxidiser pressurization")
                mode = self.OxidiserPress(self.StateFlow_constants['Desired_pressure_in_oxidiser_tank'], mode)
            elif(mode == 2):
                #Oxidiser fill
                print("[INFO] Automode: Oxidiser fill")
                #Enabling the buttons needed for Oxidiser fill
                self.button6.config(state='normal')
                self.button7.config(state='normal')
                self.button10.config(state='normal')
                self.button11.config(state='normal')
                self.button14.config(state='normal')
                self.button15.config(state='normal')
                self.button16.config(state='normal')
                if(self.ox_fill_exit):
                    mode = mode + 1
            elif(mode == 3):
                #Pressurizer fill - 2. Phase
                print("[INFO] Automode: Pressurizer fill - 2. Phase")
                #Disabling the buttons not needed for Pressurizer fill - 2. Phase
                self.button6.config(state='disable')
                self.button7.config(state='disable')
                self.button10.config(state='disable')
                self.button11.config(state='disable')
                self.button14.config(state='disable')
                self.button15.config(state='disable')
                self.button16.config(state='disable')
                mode = self.PressurizerFill(self.StateFlow_constants['Desired_pressure_in_pressure_section2'], mode)
            elif(mode == 4):
                #End phase
                print("[INFO] Automode: End phase")
                mode = self.endPhase(mode)
            else:
                #Finish
                print("[INFO] Automode: Finish")
                break
            
            #Checking if the control mode has been changed
            self.mutex_lock1.acquire()
            auto = self.control_mode
            self.mutex_lock1.release()
            time.sleep(1)
            
    def durationValves(self, valve: str, duration: float) -> None:
        """
        Closes the specified valve after the specified duration.

        Args:
            valve (str): The name of the valve to close. Possible values are:
                - 'N2_fill_valve'
                - 'N2_release_valve'
                - 'N2O_fill_valve'
                - 'N2O_release_valve'
                - 'High_servo'
                - 'Low_servo'
            duration (float): The duration in seconds to wait before closing the valve.

        Returns:
            None
        """
        
        time.sleep(duration)
        # Closing valves after the specified duration
        if valve == 'N2_fill_valve':
            self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
        elif valve == 'N2_release_valve':
            self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
            self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))
        elif valve == 'N2O_fill_valve':
            self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
        elif valve == 'N2O_release_valve':
            self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
            self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))
        elif valve == 'High_servo':
            self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
            #self.send_socket.sendto(self.Control_messages['High_servo_close_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
        elif valve == 'Low_servo':
            self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
            self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
            """
            temp = self.Control_messages['Low_servo_close_FC']
            t = int.to_bytes(int(duration), 4, 'little')
            temp = temp[:5] + t + temp[9:]
            print("--dadada---",t)
            self.send_socket.sendto(temp, (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
            """
            #self.send_socket.sendto(self.Control_messages['Low_servo_close_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))

        
    def controlValves(self, valve: str, state: int, mode='MAN', duration=0) -> None:
        """
        Controls the valves based on the given parameters.

        Args:
            valve (str): The name of the valve to control.
            state (int): The state of the valve (1 for open, 0 for close).
            mode (str, optional): The mode of control ('MAN' for manual, 'AUTO' for automatic). Defaults to 'MAN'.
            duration (int, optional): The duration of valve opening in seconds. Defaults to 0.

        Returns:
            None
        """
        #Creating a thread for the duration of the valve opening
        durationThread = th.Thread(target= lambda: self.durationValves(valve, duration))
        if(valve == 'N2_fill_valve'):
            #Opening the N2 fill valve
            if(state == 1):
                #Sending the open command
                print((self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['N2_fill_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['N2_fill_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
                #Checking if the duration is set
                if(duration != 0):
                    #Checking the mode of control
                    if(mode == 'MAN'):
                        #Starting the duration thread
                        durationThread.start()
                    elif(mode == 'AUTO'):
                        #Waiting for the specified duration
                        time.sleep(duration)
                        self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))              
                        self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
            #Closing the N2 fill valve
            elif(state == 0):
                self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))               
                self.send_socket.sendto(self.Control_messages['N2_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               

        elif(valve == 'N2_release_valve'):
            #Opening the N2 release valve
            if(state == 1):
                #Sending the open command
                self.send_socket.sendto(self.Control_messages['N2_release_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
                self.send_socket.sendto(self.Control_messages['N2_release_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))

                #Checking if the duration is set
                if(duration != 0):
                    #Checking the mode of control
                    if(mode == 'MAN'):
                        #Starting the duration thread
                        durationThread.start()
                    elif(mode == 'AUTO'):
                        #Waiting for the specified duration
                        time.sleep(duration)
                        self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
                        self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))                              
            #Closing the N2 release valve
            elif(state == 0):
                self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
                self.send_socket.sendto(self.Control_messages['N2_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))                              
                              

        elif(valve == 'N2O_fill_valve'):
            #Opening the N2O fill valve
            if(state == 1):
                #Sending the open command
                self.send_socket.sendto(self.Control_messages['N2O_fill_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['N2O_fill_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
                #Checking if the duration is set
                if(duration != 0):
                    #Checking the mode of control
                    if(mode == 'MAN'):
                        #Starting the duration thread
                        durationThread.start()
                    elif(mode == 'AUTO'):
                        #Waiting for the specified duration
                        print("dajbdadba", duration)
                        time.sleep(duration)
                        self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT'])) 
                        self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
              
            #Closing the N2O fill valve
            elif(state == 0):
                self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))               
                self.send_socket.sendto(self.Control_messages['N2O_fill_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               

        elif(valve == 'N2O_release_valve'):
            #Opening the N2O release valve
            if(state == 1):
                #Sending the open command
                self.send_socket.sendto(self.Control_messages['N2O_release_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
                self.send_socket.sendto(self.Control_messages['N2O_release_valve_open'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))
                #Checking if the duration is set
                if(duration != 0):
                    #Checking the mode of control
                    if(mode == 'MAN'):
                        #Starting the duration thread
                        durationThread.start()
                    elif(mode == 'AUTO'):
                        #Waiting for the specified duration
                        print(duration)
                        time.sleep(duration)
                        self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
                        self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))               
            #Closing the N2O release valve
            elif(state == 0):
                 self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT1']))
                 self.send_socket.sendto(self.Control_messages['N2O_release_valve_close'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT1_V']))               

        elif(valve == 'High_servo'):
            #Opening the high servo valve
            if(state == 1):
                #Sending the open command
                self.send_socket.sendto(self.Control_messages['High_servo_open_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['High_servo_open_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))
                """
                temp = self.Control_messages['High_servo_open_FC']
                t = int.to_bytes(int(duration), 4, 'little')
                temp = temp[:5] + t + temp[9:]
                if duration != 0:
                    temp = temp[:3] + int.to_bytes(3, 1, 'little') + temp[5:]
                """
                #self.send_socket.sendto(temp, (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                #self.send_socket.sendto(self.Control_messages['High_servo_open_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                #Checking if the duration is set
                
                if(duration != 0):
                    #Checking the mode of control
                    if(mode == 'MAN'):
                        #Starting the duration thread
                        durationThread.start()
                    elif(mode == 'AUTO'):
                        #Waiting for the specified duration
                        time.sleep(duration)
                        self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                        self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))

                        #self.send_socket.sendto(self.Control_messages['High_servo_close_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))               
                
            #Closing the high servo valve
            elif(state == 0):
                self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['High_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))

                #self.send_socket.sendto(self.Control_messages['High_servo_close_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))               

        elif(valve == 'Low_servo'):
            #Opening the low servo valve
            if(state == 1):
                #Sending the open command
                self.send_socket.sendto(self.Control_messages['Low_servo_open_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['Low_servo_open_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))                
                """
                temp = self.Control_messages['Low_servo_open_FC']
                t = int.to_bytes(int(duration), 4, 'little')
                temp = temp[:5] + t + temp[9:]
                
                if duration != 0:
                    temp = temp[:4] + int.to_bytes(3, 1, 'little') + temp[6:]
                self.send_socket.sendto(temp, (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                """
                #self.send_socket.sendto(self.Control_messages['Low_servo_open_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                #Checking if the duration is set
                
                if(duration != 0):
                    #Checking the mode of control
                    if(mode == 'MAN'):
                        #Starting the duration thread
                        durationThread.start()
                    elif(mode == 'AUTO'):
                        #Waiting for the specified duration
                        time.sleep(duration)
                        """
                        temp = self.Control_messages['Low_servo_close_FC']
                        t = int.to_bytes(int(duration), 4, 'little')
                        temp = temp[:5] + t + temp[9:]
                        self.send_socket.sendto(temp, (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                        """
                        #self.send_socket.sendto(self.Control_messages['Low_servo_close_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                        self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                        self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))                
            #Closing the low servo valve
            elif(state == 0):
                #self.send_socket.sendto(self.Control_messages['Low_servo_close_FC'], (self.UDP_ME2GSE['UDP_FC_IP'], self.UDP_ME2GSE['UDP_FC_PORT']))
                self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP'], self.UDP_ME2GSE['UDP_GSE_PORT']))
                self.send_socket.sendto(self.Control_messages['Low_servo_close_GSE'], (self.UDP_ME2GSE['UDP_GSE_IP_V'], self.UDP_ME2GSE['UDP_GSE_PORT_V']))               
        
    def pressureDataConv(self, data: int, sensor='PT5500') -> float:
        """
        Converts the pressure data from the specified sensor to a calibrated value.

        Args:
            data (int): The raw pressure data to be converted.
            sensor (str, optional): The type of sensor used. Defaults to 'PT5500'.

        Returns:
            float: The calibrated pressure value.

        Raises:
            KeyError: If the specified sensor is not found in the Sensor_calibration dictionary.
        """
        #Converting the raw data to calibrated value
        if sensor == 'PT5500':
            return data * self.Sensor_calibration['PT5500_GAIN'] + self.Sensor_calibration['PT5500_OFFSET']
        elif sensor == 'PT5302':
            return data * self.Sensor_calibration['PT5302_GAIN'] + self.Sensor_calibration['PT5302_OFFSET']
    
    def valveStateEstimation(self, number: int, valve_type = 'Ball', acceptable_dif = 5) -> int:
        """
        Estimates the state of a valve based on the given number and valve type.

        Args:
            number (int): The number used to estimate the valve state.
            valve_type (str, optional): The type of valve. Defaults to 'Ball'.
            acceptable_dif (int, optional): The acceptable difference between the number and the valve state constants. Defaults to 5.

        Returns:
            int: The estimated valve state. Returns 2 for 'open', 0 for 'close', 1 for 'mid', and None if the valve type is not recognized.
        """
        def isInRange(num: int, num_border: int) -> bool:
            """
            Check if the absolute difference between `num` and `num_border` is within an acceptable range.
            
            Parameters:
                num (int): The number to be checked.
                num_border (int): The border number to compare against.
                
            Returns:
                bool: True if the absolute difference is within the acceptable range, False otherwise.
            """
            return abs(num - num_border) <= acceptable_dif
        
        if(valve_type == 'Ball'):
            #Estimating the state of a ball valve
            if(isInRange(number, self.Valve_state_constants['H_bridge_open_num'])):
                return 2 #open
            elif(isInRange(number, self.Valve_state_constants['H_bridge_close_num'])):
                return 0 #close
            elif(isInRange(number, self.Valve_state_constants['H_bridge_mid_num'])):
                return 1 #mid
            else:
                return None
            
        elif(valve_type == 'Servo'):
            #Estimating the state of a servo valve
            if(isInRange(number, self.Valve_state_constants['Servo_open'])):
                return 2 #open
            elif(isInRange(number, self.Valve_state_constants['Servo_close'])):
                return 0 #close
            else:
                return 1 #mid
    
    def infoPrint(self, info_dict: dict) -> None:
        """
        Prints the information stored in the given dictionary.

        Parameters:
            info_dict (dict): A dictionary containing the information to be printed.

        Returns:
            None
        """
        print(f'[INFO] Time {time.time() - self.GLOBAL_START_TIME}')
        print("----------------------------------")
        for i in info_dict:
            print(i,':', round(info_dict[i], 2))
    
    def writeIntoFile(self, info_dict: dict) -> None:
        """
        Writes the information from the given dictionary into a file.

        Parameters:
            info_dict (dict): A dictionary containing the information to be written into the file.

        Returns:
            None
        """
        print(time.time() - self.GLOBAL_START_TIME, end=';', file=self.infoFile)
        for i in info_dict:
            print(info_dict[i], end=';', file=self.infoFile)
        print(file=self.infoFile)
        
    def listeningThreadFunction(self) -> None:
        """
        This function is responsible for listening to incoming messages and updating the valve states and values accordingly.
        
        Returns:
            None
        """
        start = time.time()
        info_dict = copy.copy(self.ServoStatesandValues)
        self.infoFile = open('Values.csv', 'a')
        
        #Writing the header into the file
        print('Time',end = ';', file = self.infoFile)
        for i in info_dict:
            print(i, end=';', file = self.infoFile)
        print('\n',file = self.infoFile)
        
        #Checking the control mode
        self.mutex_lock.acquire()
        end = self.control_mode  
        self.mutex_lock.release()
        
        while(end != 'END'):
            #Receiving the message
            received = self.receive_socket.recv(1024)
            # print(received)
            #Decoding the message
            id = received[0]
            pl = received[1]
            msg_id = received[2]
            card_id = received[3]
            slot = received[4]
            message = received[5:]
            #Checking the card id
            if(card_id == self.card_ids['CARDID_CURRENT_LOOP']):
                if(slot == self.card_slots['CARD_CURRENT_LOOP_SLOT']):
                    #Extracting the message channels
                    message_channels = [int.from_bytes(message[4*i:4*i+4], 'little') for i in range(16)]  #is the little endian correct?
                    
                    info_dict['Low_p'] = self.pressureDataConv(message_channels[self.Current_loop_message_order['Low_p_ind']], 'PT5302')
                    info_dict['High_p'] = self.pressureDataConv(message_channels[self.Current_loop_message_order['High_p_ind']])
                    info_dict['GSE_oxidiser_p'] = self.pressureDataConv(message_channels[self.Current_loop_message_order['GSE_oxidiser_p_ind']], 'PT5302')
                    info_dict['GSE_Pressurizer_p'] = self.pressureDataConv(message_channels[self.Current_loop_message_order['GSE_Pressurizer_p_ind']])
                    info_dict['N2O_fuel_level'] = message_channels[self.Current_loop_message_order['N2O_fuel_level_ind']]
                    #Updating the valve states and values
                    self.mutex_lock.acquire()
                    self.ServoStatesandValues['Low_p'] = info_dict['Low_p']
                    self.High_p_previous = self.ServoStatesandValues['High_p'] 
                    self.ServoStatesandValues['High_p'] = info_dict['High_p']
                    self.ServoStatesandValues['GSE_oxidiser_p'] = info_dict['GSE_oxidiser_p']
                    self.ServoStatesandValues['GSE_Pressurizer_p'] = info_dict['GSE_Pressurizer_p']
                    self.ServoStatesandValues['N2O_fuel_level'] = info_dict['N2O_fuel_level']
                    
                    self.mutex_lock.release()
            
            #Checking the card id
            elif(card_id == self.card_ids['CARDID_IO']):
                if(slot == self.card_slots['CARD_IO2_SLOT']):
                    #Extracting the message channels
                    message_channels = [x for x in message]
                    
                    #Estimating the valve states
                    info_dict['N2_fill_valve_state'] = self.valveStateEstimation(message_channels[self.IO_card_message_order['H1_bridge_state_ind']])
                    info_dict['High_servo_state'] = self.valveStateEstimation(message_channels[self.IO_card_message_order['High_servo_state_ind']], 'Servo')
                    info_dict['Low_servo_state'] = self.valveStateEstimation(message_channels[self.IO_card_message_order['Low_servo_state_ind']], 'Servo')
                    info_dict['N2O_fill_valve_state'] = self.valveStateEstimation(message_channels[self.IO_card_message_order['H2_bridge_state_ind']])    
                    
                    #Updating the valve states and values
                    self.mutex_lock.acquire()
                    self.ServoStatesandValues['N2_fill_valve_state'] = info_dict['N2_fill_valve_state']
                    self.ServoStatesandValues['High_servo_state'] = info_dict['High_servo_state']
                    self.ServoStatesandValues['Low_servo_state'] = info_dict['Low_servo_state']
                    self.ServoStatesandValues['N2O_fill_valve_state'] = info_dict['N2O_fill_valve_state']
                    self.mutex_lock.release()
                
                #Checking the card id
                elif(slot == self.card_slots['CARD_IO3_SLOT']):
                    #Extracting the message channels
                    message_channels = [x for x in message]
                    
                    #Estimating the valve states
                    info_dict['N2_release_valve_state'] = self.valveStateEstimation(message_channels[self.IO_card_message_order['H1_bridge_state_ind']])
                    info_dict['N2O_release_valve_state'] = self.valveStateEstimation(message_channels[self.IO_card_message_order['H2_bridge_state_ind']])
                    
                    #Updating the valve states and values
                    self.mutex_lock.acquire()
                    self.ServoStatesandValues['N2_release_valve_state'] = info_dict['N2_release_valve_state']
                    self.ServoStatesandValues['N2O_release_valve_state'] = info_dict['N2_release_valve_state']
                    self.mutex_lock.release()
                #Writing the information into the file
                self.writeIntoFile(info_dict)
                
            current_time = time.time()
            #Printing the information every 5 seconds
            if((current_time - start) > 5):
                self.infoPrint(info_dict)
                print()
                start = current_time
            
            #Checking the control mode
            self.mutex_lock.acquire()
            end = self.control_mode  
            self.mutex_lock.release()
        #Closing the file
        print(file = self.infoFile)
        self.infoFile.close()
                

a = Refueling()

a.mainloop()
