# -*- coding: utf-8 -*-
"""
@author: Abdelrahman & Tarek & Abdullah & Ayman
"""
#----imprting modules----#
LANG="en_US.UTF-8"
import ahkab
import cmath
import math
#-----------------------------------------------------------------------------------------------------------#

ac_circuit = ahkab.Circuit("AC Circuit")             #create an ahkab circuit

File = open("Netlist.txt","r+")                      #open the net list
freq = float(File.readline())                          #setting the frecuency
print("frequence: ", freq)
Circuit = File.readlines()                           #read all the lines

#---------------intializations-----------------#
pi = math.pi
i=0

element_type = {}
node1={}
node2={}
value={}
phase={}
ns1={}
ns2={}
vsource={}
resistors = {}
voltage_sources = {}
current_sources = {}
vcvs = {}
vccs = {}
ccvs = {}
cccs = {}
nodes_voltages = {}
Voltage = {}
Vm = {}

ri=0
vi=0
ci=0
vcvsi=0
vccsi=0
ccvsi=0
cccsi=0
#----------------------------------------------#

for X,i in zip(Circuit,range(len(Circuit))):
    print(X.split(),i)
    Type = X.split(' ')[0]                       #reading the type of the component
    element_type[i] = Type
    Node1 = X.split(' ')[1]                      #reading the anode node of the component
    node1[i] = Node1
    Node2 = X.split(' ')[2]                      #reading the cathode node of the component
    node2[i]=Node2
    if (Type[0] == "H" or Type[0] == "F"):
        Value = X.split(' ')[3]                  #reading the value of the component
    else:
        Value = float(X.split(' ')[3])
    value[i]=Value
    if len(X.split(' ')) > 4:
        Phase = float(X.split(' ')[4])           #reading the of the component if exists   
        phase[i]=Phase
    else:
        Phase = 0        
    if len(X.split(' ')) > 5 and Type[0] == 'E': #Voltage controlled voltage source
        N1 = X.split(' ')[1]                     #reading the anode node of the vcvs
        node1[i] = N1
        N2 = X.split(' ')[2]                     #reading the cathode node of the vcvs
        node2[i] = N2
        NS1 = X.split(' ')[3]                    #getting the driving anode node of the vcvs
        ns1[i]=NS1
        NS2 = X.split(' ')[4]                    #getting the driving cathode node of the vcvs
        ns2[i]=NS2
        Value = float(X.split(' ')[5])           #reading the proportionality factor
        value[i]=Value
    if len(X.split(' ')) > 4 and Type[0] == 'H': #Current controlled voltage source
        N1 = X.split(' ')[1]                     #reading the anode node of the ccvs
        node1[i] = N1
        N2 = X.split(' ')[2]                     #reading the cathode node of the ccvs
        node2[i] = N2
        Vsource = X.split(' ')[3]                #getting the voltage source whose current controls the ccvs    
        vsource[i]=Vsource
        Value = float(X.split(' ')[4])                  #reading the proportionality factor
        value[i]=Value
    if len(X.split(' ')) > 5 and Type[0] == 'G': #Voltage controlled current source
        N1 = X.split(' ')[1]                     #getting the driving anode node of the vccs
        node1[i] = N1
        N2 = X.split(' ')[2]                     #getting the driving tathode node of the vccs
        node2[i] = N2
        NS1 = X.split(' ')[3]                    #getting the driving anode node of the vccs
        ns1[i]=NS1
        NS2 = X.split(' ')[4]                    #getting the driving cathode node of the vccs 
        ns2[i]=NS2
        Value = float(X.split(' ')[5])           #reading the proportionality factor
        value[i]=Value
    if len(X.split(' ')) > 4 and Type[0] == 'F': #Current controlled current source
        N1 = X.split(' ')[1]                     #getting the driving anode node of the cccs   
        node1[i] = N1
        N2 = X.split(' ')[2]                     #getting the driving cathode node of the cccs
        node2[i] = N2
        Vsource = X.split(' ')[3]                #getting the voltage source whose current controls the cccs
        vsource[i]=Vsource
        Value = float(X.split(' ')[4])           #reading the proportionality factor
        value[i]=Value
    if Type[0] == 'V':                           #--->Adding independent voltage source<---#
        ac_circuit.add_vsource(Type,Node1,Node2,dc_value = 0, ac_value = Value*(math.cos(math.radians(Phase))+math.sin(math.radians(Phase))*1j))
        voltage_sources[vi]=X.split()
        vi+=1
    else:
        if Type[0] == 'L':                                          #--->Adding inductor<---#
            ac_circuit.add_inductor(Type,Node1,Node2,Value)
        else:
            if Type[0] == 'C':                                      #--->Adding capacitor<---#
                ac_circuit.add_capacitor(Type,Node1,Node2,Value)
            else:
                if Type[0] == 'R':                                  #--->Adding resistor<---#
                    ac_circuit.add_resistor(Type,Node1,Node2,Value)
                    resistors[ri]=X.split()
                    ri+=1
                else:
                    if Type[0] == 'E':                              #--->Adding vcvs<---#
                        ac_circuit.add_vcvs(Type,N1,N2,NS1,NS2,Value)
                        vcvs[vcvsi]=X.split()
                        vcvsi+=1
                    else:
                        if Type[0] == 'H':                          #--->Adding ccvs<---#
                            ac_circuit.add_ccvs(Type,N1,N2,Vsource,Value)  
                            ccvs[ccvsi]=X.split()
                            ccvsi+=1
                        else:
                            if Type[0] == 'G':                      #--->Adding vccs<---#  
                                ac_circuit.add_vccs(Type,N1,N2,NS1,NS2,Value)
                                vccs[vccsi]=X.split()
                                vccsi+=1
                            else:
                                if Type[0] == 'F':                  #--->Adding cccs<---#
                                    ac_circuit.add_cccs(Type,N1,N2,Vsource,Value)
                                    cccs[cccsi]=X.split()
                                    cccsi+=1
                                else:
                                    if Type[0] == 'I':              #--->Adding independent current source<---# 
                                        ac_circuit.add_isource(Type,Node1,Node2,dc_value = 0,ac_value = Value*(math.cos(math.radians(Phase))+math.sin(math.radians(Phase))*1j))
                                        current_sources[ci]=X.split()
                                        ci+=1       
                                
ac = ahkab.new_ac(start = freq,stop = freq,points = 2,x0 = None)    #setting the analysis
res = ahkab.run(ac_circuit,ac)                                      #runnung the ac ciruit
array = res['ac'].values()                                          #getting the result's values 
print()
print("Values:")
print(array)
keys = res['ac'].keys()                                             #getting the result's keys
print()
print("Keys:")
print(keys)
print()

i=1
j=1
while j < len(keys):
    if(keys[i][0] != 'I'):
        print(keys[i])
        x=cmath.polar(array[i][0])             #converting the result to polar form  
        print(x)
        y=round(x[0],3)                        #rounding the amplitude 
        print(y)
        z=round(math.degrees(x[1]),2)          #converting the phase to degrees and rounding it
        print(z)
        print()
        print()
    j+=1  
    i+=1

print(element_type)
print(node1)
print(node2)
print(value)
print(phase)
print(ns1)
print(ns2)
print(vsource)
print(resistors)
print(voltage_sources)
print(current_sources)
print(vcvs)
print(vccs)
print(ccvs)
print(cccs)
print("[", ri, ",", vi, ",", ci, ",", vcvsi, ",", vccsi, ",", ccvsi, ",", cccsi, "]\n")

nodes_voltages[0] = 0
for x,i in zip(keys,range(len(keys))):
    if(x[0]=='V'):
        nodes_voltages[i] = res['ac'][x][0]
        print(i, "  ", nodes_voltages[i])

print()
print("nodes's voltages:")
print(nodes_voltages)
print()

with open("Output.txt", 'w') as filehandle:
    for i in range(len(Circuit)):
        
        Element = element_type[i]
        n1 = int(node1[i])
        n2 = int(node2[i])
        Voltage[i] = nodes_voltages[n1] - nodes_voltages[n2]
        Vm[i] = cmath.polar(Voltage[i])[0]
        
        if(Element[0]=='V'):
            vn = 1
            if(vi>1):
                Current_Index = "I(VS" + str(vn) + ")"
                vn+=1
            else:
                Current_Index = "I(VS)"
            Current = res['ac'][Current_Index][0] 
            Current = -1 * Current.real + Current.imag * 1j
            print(Current)
            Power = ((Voltage[i]*Current)/2)*-1
            RoundedPower = str(round(Power.real, 4)*-1 + round(Power.imag, 4)*1j)
            P = RoundedPower[1:len(RoundedPower)-1]
            print(P)
            Output = "Power(" + Element + ") ="
            filehandle.writelines("{0} {1} VA\n".format(Output, P))
        else:
            if(Element[0]=='I'):
                Current = value[i]*math.cos(math.radians(-1*phase[i])) + value[i]*math.sin(math.radians(-1*phase[i]))*1j
                Power = ((Voltage[i])*(Current))/2
                RoundedPower = str(round(Power.real, 4)*-1 + round(Power.imag, 4)*-1j)
                P = RoundedPower[1:len(RoundedPower)-1]
                print(P)
                Output = "Power(" + Element + ") ="
                filehandle.writelines("{0} {1} VA\n".format(Output, P))
            else:
                if(Element[0]=='R'):
                    Z = value[i]
                    Power = ((Vm[i])*(Vm[i]))/(2*Z)
                    RoundedPower = str(round(Power, 4))
                    print(RoundedPower)
                    P = RoundedPower[0:len(RoundedPower)]
                    Output = "Power(" + Element + ") ="
                    filehandle.writelines("{0} {1} Watt\n".format(Output, P))
                else:
                    if(Element[0]=='L'):
                        Z = value[i]*2*pi*freq*1j
                        Power = ((Vm[i])*(Vm[i]))/(2*Z)                
                        RoundedPower = str(round(Power.real, 4) + round(Power.imag, 4)*1j)
                        print(RoundedPower)
                        P = RoundedPower[0:len(RoundedPower)-1]
                        Output = "Power(" + Element + ") ="
                        filehandle.writelines("{0} {1} VAR\n".format(Output, P))
                    else:
                        if(Element[0]=='C'):
                            Z = 1/(value[i]*2*pi*freq*1j)
                            Power = ((Vm[i])*(Vm[i]))/(2*Z)
                            RoundedPower = str(round(Power.real, 4) + round(Power.imag, 4)*1j)
                            print(RoundedPower)
                            P = RoundedPower[0:len(RoundedPower)-1]
                            Output = "Power(" + Element + ") ="
                            filehandle.writelines("{0} {1} VAR\n".format(Output, P))
                        else:
                            if(Element[0]=='E'):
                                vcvsn = 1
                                if(vcvsi>1):
                                    Current_Index = "I(E" + str(vcvsn) + ")"
                                    vcvsn+=1
                                else:
                                    Current_Index = "I(E)"
                                Current = res['ac'][Current_Index][0] 
                                Current = -1 * Current.real + Current.imag * 1j
                                print(Current)
                                ns1 = int(ns1[i])
                                ns2 = int(ns2[i])
                                DepVoltage = nodes_voltages[ns1] - nodes_voltages[ns2]
                                E = value[i]*DepVoltage
                                Power = (E*Current)/2
                                RoundedPower = str(round(Power.real, 4) + round(Power.imag, 4)*1j)
                                P = RoundedPower[1:len(RoundedPower)-1]
                                print(P)
                                Output = "Power(" + Element + ") ="
                                filehandle.writelines("{0} {1} VA\n".format(Output, P))
                            else:
                                if(Element[0]=='H'):
                                    Ix_Index = "I(" + vsource[i] + ")"
                                    Ix = res['ac'][Ix_Index][0]
                                    Ix *= -1
                                    H = value[i]*Ix
                                    ccvsn = 1
                                    if(ccvsi>1):
                                        Current_Index = "I(H" + str(ccvsn) + ")"
                                        ccvsn+=1
                                    else:
                                        Current_Index = "I(H)"
                                    Current = res['ac'][Current_Index][0]
                                    Current = -1 * Current.real + Current.imag * 1j
                                    print(Current)
                                    Power = (H*Current)/2
                                    RoundedPower = str(round(Power.real, 4) + round(Power.imag, 4)*1j)
                                    P = RoundedPower[1:len(RoundedPower)-1]
                                    print(P)
                                    Output = "Power(" + Element + ") ="
                                    filehandle.writelines("{0} {1} VA\n".format(Output, P))
                                else:
                                    if(Element[0]=='G'):
                                        ns1 = float(ns1[i])
                                        ns2 = float(ns2[i])
                                        DepVoltage = nodes_voltages[ns1] - nodes_voltages[ns2]
                                        G = value[i]*DepVoltage
                                        Power = ((Voltage[i])*(G))/2
                                        RoundedPower = str(round(Power.real, 4) + round(Power.imag, 4)*1j)
                                        P = RoundedPower[1:len(RoundedPower)-1]
                                        print(P)
                                        Output = "Power(" + Element + ") ="
                                        filehandle.writelines("{0} {1} VA\n".format(Output, P))
                                    else:
                                        if(Element[0]=='F'):
                                            Ix_Index = "I(" + vsource[i] + ")"
                                            Ix = res['ac'][Ix_Index][0]
                                            Ix *= -1
                                            F = value[i]*Ix
                                            F = F.real + F.imag * -1j
                                            Power = ((Voltage[i])*(F))/2
                                            RoundedPower = str(round(Power.real, 4) + round(Power.imag, 4)*1j)
                                            P = RoundedPower[1:len(RoundedPower)-1]
                                            print(P)
                                            Output = "Power(" + Element + ") ="
                                            filehandle.writelines("{0} {1} VA\n".format(Output, P))
                                            
filehandle.close()                                                   #closing Output.txt file    
print()
print("Voltages:")
print(Voltage)
print("\nAnalysis complete, please open Output.txt to see the results.\n")