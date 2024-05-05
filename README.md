To perform SIL, the following steps must be taken:

1) Download the whole repository in .zip or clone it.
2) Open the folder with downloaded files in MATLAB.
3) Open both .slx files: Rocket_model_Stateflow_testing.slx, StateFlow_varB.slx.
4) Run MATLAB files: Rocket_gas_model_setting.m, Gas_properties.m, State_Flow_varB_setting.m.
5) Run both files from 3).
6) Go to the StateFlow_varB.slx file and open the Control panel.
7) Turn the knob setting the OMA modes (OFF, MAN, AUTO) to MAN, and wait 5 seconds.
8) Turn the knob setting the OMA modes to AUTO.
9) If the Pressure section fill control light starts blinking -> SIL is running.

The Refueling.py file was used during the second COLD-FLOW attempt, it is not appropriately set to perform SIL.
