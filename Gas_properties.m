%Pressure vector set up
%----------------------
P_vec1 = 1:1:9;
P_vec2 = 10:10:290;
P_vec3 = 300:20:1000;
P_vec4 = 0.1:0.1:0.9;
P = [0.00001,P_vec4, P_vec1, P_vec2, P_vec3];

%Temperature vector set up
%-------------------------
Temp_vec = 150 : 10 : 2000;
T = Temp_vec;

%Using nistdata() function
%-------------------------
data1 = nistdata("N2", T, P);

%Getting appropriate properties
%------------------------------

                            %     Output
                            %     data   : Struct with the following fields: 
                            %       Single values:
species = data1.species;    %         species : Chemical symbol (e.g. 'H2')
Tc = data1.Tc;              %         Tc      : Critical temperature (K)
Pc = data1.pc;              %         Pc      : Critical pressure (Pa)
Mw = data1.Mw;              %         Mw      : Molar mass (kg/kmol)
                            %       Arrays:
Rho = data1.Rho;            %         Rho     : Density (kmol/m3)
V = data1.V;                %         V       : Volume (m3/kmol)
U = data1.U;                %         U       : Internal energy (J/kmol)
H = data1.H;                %         H       : Enthalpy (J/kmol)
S = data1.S;                %         S       : Entropy (J/kmol/K)
Cv = data1.Cv;              %         Cv      : Heat capacity at constant volume (J/kmol/k)
Cp = data1.Cp;              %         Cp      : Heat capacity at constant pressure (J/kmol/k)
C = data1.C;                %         C       : Speed of sound (m/s)
JT = data1.JT;              %         JT      : Joule-Thompson coefficient (K/Pa)
mu = data1.mu;              %         mu      : Dynamic viscosity (Pa s)
k = data1.k;                %         k       : Thermal conductivity (W/m/K)

%Conversion to better units
%--------------------------

Rho = Rho*Mw;               % conversion to kg/m^3
Molar_V = V/1000;           % conversion to m^3/mol
Molar_U = U/1000;           % conversion to J/mol
H = H/(1000*Mw);            % conversion to kJ/kg
S = S/(1000*Mw);            % conversion to kJ/(kg*K)
Cp = Cp/(1000*Mw);          % conversion to kJ/(kg*K)
mu = mu*(1e6);              % conversion to uPa s
k = k*1000;                 % conversion to mW/(mK)

%Getting bulk modulus and isobaric thermal expansion coefficient values
%----------------------------------------------------------------------

bulk_modulus = zeros(length(T), length(P));
isobaric_thermal_expansion_coeff = zeros(length(T), length(P));

th = thermo('N2');  % Initialise thermo object
for i = 1:length(T)
    for j = 1:length(P)
        th.Tpcalc(T(i),P(j)*(1e5)); %Calculate thermodynamic state at T, p
        bulk_modulus(i,j) = -th.v*th.p_v;
        isobaric_thermal_expansion_coeff(i,j) = -th.f_Tv/th.f_vv/th.v;
    end
end