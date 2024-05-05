
%GSE communication protocol
%--------------------------

%Preamble
ID_SEND = 150;            %First byte in a send packet
PL_SEND = 66;             %(Packet length) Second byte in a send packet
MSG_ID_SEND = 201;        %Third byte in a send packet
ID_RECEIVE = 160;           %First byte in a received packet
PL_RECEIVE = 67;           %(Packet length) Second byte in a send packet
MSG_ID_RECEIVE = 200;       %Third byte in a received packet

%Card slots
CARD_IO1_SLOT = 5;    
CARD_IO2_SLOT = 6;             %Filling valves control
CARD_IO3_SLOT = 7;             %Releasing valves control
CARD_CURRENT_LOOP_SLOT = 2;    %Sensors
CARD_THERMISTOR_SLOT = 4;
CARD_LOAD_CELL_SLOT = 1;

%Card IDs
CARDID_EMPTY = 0;
CARDID_IO = 1;
CARDID_CURRENT_LOOP = 2;
CARDID_THERMISTOR = 4;
CARDID_LOAD_CELL = 8;
CARDID_STRAIN_ROSETTE = 16;
CARDID_CAPACITANCE = 32;
 
%IO card message order
H0_bridge_state_ind = 20; % (0 - Hard start, 127 - Middle, 255 - Hard end)
H1_bridge_state_ind = 21; % (0 - Hard start, 127 - Middle, 255 - Hard end)
H2_bridge_state_ind = 22; % (0 - Hard start, 127 - Middle, 255 - Hard end)
H0_bridge_fault_state_ind = 17; % (0 - OK, 255 - Fault)
H1_bridge_fault_state_ind = 18; % (0 - OK, 255 - Fault)
H2_bridge_fault_state_ind = 19; % (0 - OK, 255 - Fault)
Servo_0_state_ind = 3;    % in degrees (0 - 90)
Servo_1_state_ind = 4;    % in degrees (0 - 90)

%Current loop message order
Low_p_ind = 1;
High_p_ind = 2;
GSE_oxidiser_p_ind = 3; 
GSE_Pressurizer_p_ind = 4;
N2O_fuel_level_ind = 5;

%Cimrman communication protocol
%------------------------------
FC_ID = 100;
FC_PACKET_LENGTH = 33;
FC_SERVO_OP = 2;        %Open
FC_SERVO_CL = 1;        %Close
FC_SERVO_PULSE = 3;     %Pulse
FC_SERVO_IGNORE = 0;
FC_GND_MSG_SERVO_CTRL = 71;

%IO card supported commands
%--------------------------
H_Bridge_0_open = 16;
H_Bridge_0_close = 17;
H_Bridge_0_nudge_open = 18;
H_Bridge_0_nudge_close = 19;
H_Bridge_1_open = 20;
H_Bridge_1_close = 21;
H_Bridge_1_nudge_open = 22;
H_Bridge_1_nudge_close = 23;
H_Bridge_2_open = 24;
H_Bridge_2_close = 25;
H_Bridge_2_nudge_open = 26;
H_Bridge_2_nudge_close = 27;
H_Bridge_0_stop = 28;
H_Bridge_1_stop = 29;
H_Bridge_2_stop = 30;
H_Bridge_0_turn_forward = 70;
H_Bridge_1_turn_forward = 73;
H_Bridge_2_turn_forward = 76;
H_Bridge_0_turn_backward = 71;
H_Bridge_1_turn_backward = 74;
H_Bridge_2_turn_backward = 77;
H_Bridge_0_stop = 72;
H_Bridge_1_stop = 75;
H_Bridge_2_stop = 78;
Set_power_output_0_high = 44;
Set_power_output_1_high = 45;
Set_power_output_2_high = 46;
Set_power_output_3_high = 47;
Set_power_output_0_low = 60;
Set_power_output_1_low = 61;
Set_power_output_2_low = 62;
Set_power_output_3_low = 63;
Toggle_power_output_0_state = 92;
Toggle_power_output_1_state = 93;
Toggle_power_output_2_state = 94;
Toggle_power_output_3_state = 95;
Open_digital_servo_0 = 64;
Close_digital_servo_0 = 65;
Pulse_digital_servo_0 = 66;
Open_digital_servo_1 = 67;
Close_digital_servo_1 = 68;
Pulse_digital_servo_1 = 69;

%Sensor calibration
%------------------
PT5302_GAIN = 0.05;     %100 bar Pressure sensor gain
PT5302_OFFSET = -25;    %100 bar Pressure sensor offset
PT5500_GAIN = 0.2;       %300 bar Pressure sensor gain
PT5500_OFFSET = -100;   %300 bar Pressure sensor offset
TA3145_GAIN = 12.5;     %Temperature sensor gain 
TA3145_OFFSET = -100;   %Temperature sensor offset

% StateFlow constants
%--------------------

Acceptable_press_offset = 5; %bar
Press_Transition_time_const = 3; %s
Desired_pressure_in_pressure_section1 = 150; %bar
Desired_pressure_in_pressure_section2 = 180; %bar
Number_of_decisive_time_cycles = 5;
Large_State_transition_time_const = 5; %s
Small_State_transition_time_const = 2; %s
Desired_pressure_in_oxidiser_tank = 40; %bar
Oxidiser_fueling_exit = 1000;  %IF CHANGED, CHANGE IT ALSO IN COMBO BOX

%Pressure drop indication constants
%----------------------------------

Pressure_drop_const = 100; %bar (drop of 30 bars will resolve in pressure drop indication)

%UDP blocks settings (GSE)
%-------------------------

UDP_GSE_send_to_IP = '127.0.0.1'; 
UDP_GSE_send_to_PORT = 10003;
UDP_GSE_IO_send_sample_time = 0.05; %s
UDP_GSE_send_packet_length = 68;

UDP_GSE_receive_local_IP = '127.0.0.2'; 
UDP_GSE_receive_local_PORT = 10005;
UDP_GSE_receive_receive_width = 69;
UDP_GSE_Curr_loop_receive_sample_time = 0.01; %s
UDP_GSE_IO_receive_sample_time = 0.05;%


%If servos in rocket are controlled via GSE then parametres below should
%be equal to those for GSE

UDP_FC_send_to_IP = '127.0.0.1';
UDP_FC_send_to_PORT = 10003;
UDP_FC_send_sample_time = 0.05; 
UDP_FC_send_packet_length = 68;

%PWM
%---

GSE_PWM_period = 2;
FC_PWM_period = 2;

%For the purpose of the artificial model
%-----------------------------------

IO_card_2_port = 10003;
IO_card_3_port = 10004;

%Valve state constants
%---------------------

H_bridge_open_num = 255;
H_bridge_close_num = 0;
H_bridge_mid_num = 127;
Servo_open_limit = 20;
H_bridge_fault_state_num = 255;


%Valve control messages
%----------------------

%Cimrman messages have the following format:
%[FC_ID, FC_PACKET_LENGTH, FC_MSG_ID, HIGH_SERVO_STATE, LOW_SERVO_STATE, TIME(if pulse option is set), 0]
%Section sizes:
%[byte, byte, byte, byte, byte, byte[4], byte[24]] 

%GSE messages have the following format
%[ID_SEND, PL_SEND, MSG_ID_SEND, CARD_SLOT, Command]
%Section sizes:
%[byte, byte, byte, byte, byte[64]]

N2_fill_valve_open = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, H_Bridge_1_open, zeros(1,63)]);
N2_fill_valve_close = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, H_Bridge_1_close, zeros(1,63)]);

N2_release_valve_open = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO3_SLOT, H_Bridge_1_open, zeros(1,63)]);
N2_release_valve_close = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO3_SLOT, H_Bridge_1_close, zeros(1,63)]);

%GSE controlled
High_servo_open = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, Open_digital_servo_0, zeros(1,63)]);
High_servo_close = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, Close_digital_servo_0, zeros(1,63)]);

%Cimrman controlled
%High_servo_open = uint8([FC_ID, FC_PACKET_LENGTH, FC_GND_MSG_SERVO_CTRL, FC_SERVO_OP, FC_SERVO_IGNORE, zeros(1,28)]);
%High_servo_close = uint8([FC_ID, FC_PACKET_LENGTH, FC_GND_MSG_SERVO_CTRL, FC_SERVO_CL, FC_SERVO_IGNORE, zeros(1,28)]);

%GSE controlled
Low_servo_open = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, Open_digital_servo_1, zeros(1,63)]);
Low_servo_close = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, Close_digital_servo_1, zeros(1,63)]);

%Cimrman controlled
%Low_servo_open = uint8([FC_ID, FC_PACKET_LENGTH, FC_GND_MSG_SERVO_CTRL, FC_SERVO_IGNORE, FC_SERVO_OP, zeros(1,28)]);
%Low_servo_close = uint8([FC_ID, FC_PACKET_LENGTH, FC_GND_MSG_SERVO_CTRL, FC_SERVO_IGNORE, FC_SERVO_CL, zeros(1,28)]);

N2O_fill_valve_open = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, H_Bridge_2_open, zeros(1,63)]);
N2O_fill_valve_close = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO2_SLOT, H_Bridge_2_close, zeros(1,63)]);

N2O_release_valve_open = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO3_SLOT, H_Bridge_2_open, zeros(1,63)]);
N2O_release_valve_close = uint8([ID_SEND, PL_SEND, MSG_ID_SEND, CARD_IO3_SLOT, H_Bridge_2_close, zeros(1,63)]);

%Initial constant values
set_param('StateFlow_varB/Subsystem6/Constant', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant6', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant2', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant5', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant3', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant1', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant9', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant10', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant11', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant12', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant7', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant4', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant13', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem10/Constant14', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem/Constant2', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem/Constant3', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Constant1', 'Value', '0');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant8', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant9', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant10', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant11', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant12', 'Value', '1');
set_param('StateFlow_varB/Subsystem6/Subsystem3/Constant12', 'Value', '1');

%I expect that prev_states are set to 1 if H_bridges are open
%při posílání 201 (3. byte)
%při přijímání 200 (3. byte)
% první byte bude 150 (číslo zařízení)
% %délka je od 3 bytu dál


% Bus set up
%-----------

s = struct;
s.ID_SEND = ID_SEND;
s.PL_SEND = PL_SEND;
s.ID_RECEIVE = ID_RECEIVE;
s.PL_RECEIVE = PL_RECEIVE;
s.MSG_ID_RECEIVE = MSG_ID_RECEIVE;
s.CARD_IO1_SLOT = CARD_IO1_SLOT;    
s.CARD_IO2_SLOT = CARD_IO2_SLOT;
s.CARD_IO3_SLOT = CARD_IO3_SLOT;
s.CARD_CURRENT_LOOP_SLOT = CARD_CURRENT_LOOP_SLOT;
s.CARD_THERMISTOR_SLOT = CARD_THERMISTOR_SLOT;
s.CARD_LOAD_CELL_SLOT = CARD_LOAD_CELL_SLOT;
s.CARDID_EMPTY = CARDID_EMPTY;
s.CARDID_IO = CARDID_IO;
s.CARDID_CURRENT_LOOP = CARDID_CURRENT_LOOP;
s.CARDID_THERMISTOR = CARDID_THERMISTOR;
s.CARDID_LOAD_CELL = CARDID_LOAD_CELL;
s.CARDID_STRAIN_ROSETTE = CARDID_STRAIN_ROSETTE;
s.CARDID_CAPACITANCE = CARDID_CAPACITANCE;
s.H0_bridge_state_ind = H0_bridge_state_ind;
s.H1_bridge_state_ind = H1_bridge_state_ind;
s.H2_bridge_state_ind = H2_bridge_state_ind;
s.H0_bridge_fault_state_ind = H0_bridge_fault_state_ind;
s.H1_bridge_fault_state_ind = H1_bridge_fault_state_ind;
s.H2_bridge_fault_state_ind = H2_bridge_fault_state_ind; 
s.Servo_0_state_ind = Servo_0_state_ind;   
s.Servo_1_state_ind = Servo_1_state_ind;   
s.Low_p_ind = Low_p_ind;
s.High_p_ind = High_p_ind;
s.GSE_oxidiser_p_ind = GSE_oxidiser_p_ind; 
s.GSE_Pressurizer_p_ind = GSE_Pressurizer_p_ind;
s.N2O_fuel_level_ind = N2O_fuel_level_ind;
s.PT5302_GAIN = PT5302_GAIN;     
s.PT5302_OFFSET = PT5302_OFFSET;    
s.PT5500_GAIN = PT5500_GAIN;       
s.PT5500_OFFSET = PT5500_OFFSET;   
s.TA3145_GAIN = TA3145_GAIN;     
s.TA3145_OFFSET = TA3145_OFFSET;   
s.Acceptable_press_offset = Acceptable_press_offset; 
s.Press_Transition_time_const = Press_Transition_time_const;
s.Desired_pressure_in_pressure_section1 = Desired_pressure_in_pressure_section1;
s.Desired_pressure_in_pressure_section2 = Desired_pressure_in_pressure_section2;
s.Number_of_decisive_time_cycles = Number_of_decisive_time_cycles;
s.Large_State_transition_time_const = Large_State_transition_time_const; 
s.Small_State_transition_time_const = Small_State_transition_time_const; 
s.Desired_pressure_in_oxidiser_tank = Desired_pressure_in_oxidiser_tank; 
s.Oxidiser_fueling_exit = Oxidiser_fueling_exit;  
s.Pressure_drop_const = Pressure_drop_const; 
s.UDP_GSE_send_to_PORT = UDP_GSE_send_to_PORT;
s.UDP_GSE_IO_send_sample_time = UDP_GSE_IO_send_sample_time;
s.UDP_GSE_Curr_loop_receive_sample_time = UDP_GSE_Curr_loop_receive_sample_time;
s.UDP_GSE_send_packet_length = UDP_GSE_send_packet_length;
s.UDP_GSE_receive_local_PORT = UDP_GSE_receive_local_PORT;
s.UDP_GSE_receive_receive_width = UDP_GSE_receive_receive_width;
s.UDP_GSE_IO_receive_sample_time = UDP_GSE_IO_receive_sample_time; 
s.UDP_FC_send_to_PORT = UDP_FC_send_to_PORT;
s.UDP_FC_send_sample_time = UDP_FC_send_sample_time; 
s.UDP_FC_send_packet_length = UDP_FC_send_packet_length;
s.N2_fill_valve_open = N2_fill_valve_open;
s.N2_fill_valve_close = N2_fill_valve_close;
s.N2_release_valve_open = N2_release_valve_open;
s.N2_release_valve_close = N2_release_valve_close;
s.High_servo_open = High_servo_open;
s.High_servo_close = High_servo_close;
s.Low_servo_open = Low_servo_open;
s.Low_servo_close = Low_servo_close;
s.N2O_fill_valve_open = N2O_fill_valve_open;
s.N2O_fill_valve_close = N2O_fill_valve_close;
s.N2O_release_valve_open = N2O_release_valve_open;
s.N2O_release_valve_close = N2O_release_valve_close;
s.FC_ID = FC_ID;
s.FC_PACKET_LENGTH = FC_PACKET_LENGTH;
s.FC_SERVO_OP = FC_SERVO_OP;        
s.FC_SERVO_CL = FC_SERVO_CL;        
s.FC_SERVO_PULSE = FC_SERVO_PULSE;     
s.FC_SERVO_IGNORE = FC_SERVO_IGNORE;
s.FC_GND_MSG_SERVO_CTRL = FC_GND_MSG_SERVO_CTRL;
s.H_Bridge_0_open = H_Bridge_0_open;
s.H_Bridge_0_close = H_Bridge_0_close;
s.H_Bridge_0_nudge_open = H_Bridge_0_nudge_open;
s.H_Bridge_0_nudge_close = H_Bridge_0_nudge_close;
s.H_Bridge_1_open = H_Bridge_1_open;
s.H_Bridge_1_close = H_Bridge_1_close;
s.H_Bridge_1_nudge_open = H_Bridge_1_nudge_open;
s.H_Bridge_1_nudge_close = H_Bridge_1_nudge_close;
s.H_Bridge_2_open = H_Bridge_2_open;
s.H_Bridge_2_close = H_Bridge_2_close;
s.H_Bridge_2_nudge_open = H_Bridge_2_nudge_open;
s.H_Bridge_2_nudge_close = H_Bridge_2_nudge_close;
s.H_Bridge_0_stop = H_Bridge_0_stop;
s.H_Bridge_1_stop = H_Bridge_1_stop;
s.H_Bridge_2_stop = H_Bridge_2_stop;
s.H_Bridge_0_turn_forward = H_Bridge_0_turn_forward;
s.H_Bridge_1_turn_forward = H_Bridge_1_turn_forward;
s.H_Bridge_2_turn_forward = H_Bridge_2_turn_forward;
s.H_Bridge_0_turn_backward = H_Bridge_0_turn_backward;
s.H_Bridge_1_turn_backward = H_Bridge_1_turn_backward;
s.H_Bridge_2_turn_backward = H_Bridge_2_turn_backward;
s.H_Bridge_0_stop = H_Bridge_0_stop;
s.H_Bridge_1_stop = H_Bridge_1_stop;
s.H_Bridge_2_stop = H_Bridge_2_stop;
s.Set_power_output_0_high = Set_power_output_0_high;
s.Set_power_output_1_high = Set_power_output_1_high;
s.Set_power_output_2_high = Set_power_output_2_high;
s.Set_power_output_3_high = Set_power_output_3_high;
s.Set_power_output_0_low = Set_power_output_0_low;
s.Set_power_output_1_low = Set_power_output_1_low;
s.Set_power_output_2_low = Set_power_output_2_low;
s.Set_power_output_3_low = Set_power_output_3_low;
s.Toggle_power_output_0_state = Toggle_power_output_0_state;
s.Toggle_power_output_1_state = Toggle_power_output_1_state;
s.Toggle_power_output_2_state = Toggle_power_output_2_state;
s.Toggle_power_output_3_state = Toggle_power_output_3_state;
s.Open_digital_servo_0 = Open_digital_servo_0;
s.Close_digital_servo_0 = Close_digital_servo_0;
s.Pulse_digital_servo_0 = Pulse_digital_servo_0;
s.Open_digital_servo_1 = Open_digital_servo_1;
s.Close_digital_servo_1 = Close_digital_servo_1;
s.Pulse_digital_servo_1 = Pulse_digital_servo_1;
s.GSE_PWM_period = GSE_PWM_period;
s.FC_PWM_period = FC_PWM_period;
s.H_bridge_open_num = H_bridge_open_num;
s.H_bridge_close_num = H_bridge_close_num;
s.H_bridge_mid_num = H_bridge_mid_num;
s.Servo_open_limit = Servo_open_limit;
s.H_bridge_fault_state_num = H_bridge_fault_state_num;


s_bus_info = Simulink.Bus.createObject(s);
s_bus = evalin('base', s_bus_info.busName);