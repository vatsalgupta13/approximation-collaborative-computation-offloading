# Cloud-MEC Optimal Collaborative Computation Offloading(CMOCO) solution -
# Approximation Collaborative Computation offloading algorithm (ACCO)
from __future__ import division
import sys
# N is the total number of MDs

N = int(input("enter the number of MDs: "))
if N==0:
    print("enter a value greater than or equal to 1")
    N = int(input("enter the number of MDs: "))
N_set=[]*N
for i in range(0,N):
    N_set.append(i)
# K is the maximum number of wireless channels availaible
K = int(input("enter the maximum number of wireless channels availaible: "))
if K==0:
    print("enter a value greater than or equal to 1")
    K = int(input("enter the maximum number of wireless channels availaible: "))
# array of tasks
t_max=[]*N # maximum permissible latency
m = []*N # size of computation input data
c = []*N # number of CPU cycles required
for i in range(0,N):
    x = float(input("enter the value of maximum permissible latency for MD %i: " %i))
    t_max.append(x)
    y = float(input("enter the value of computation input data %i: " %i))
    m.append(y)
    z = int(input("enter the number of maximum CPU cycles %i: " %i))
    c.append(z)
f_local = []*N # computing abilty of MD i per CPU cycle
y_local = []*N # consumed energy per CPU cycle
transmit_power = []*N # transmit power of MD i
r = []*N # uplink data rate of transmitting from MD i to the wireless BS via a wireless access
for i in range(0,N):
    x = float(input("enter the computing capability of MD %i: " %i))
    f_local.append(x)
    y = float(input("enter the consumed energy of MD %i: " %i))
    y_local.append(y)
    z = float(input("enter the transmit power of MD %i: " %i))
    transmit_power.append(z)
    v = float(input("enter the uplink data rate from MD %i to BS : " %i))
    r.append(v)
# computing ability of MEC
f_mec = float(input("enter the computing capability of MEC: "))
# uplink data rate of the optical fiber network
c_bs = float(input("enter the uplink data rate of the optical fiber network: "))
# uplink propogation delay (optical backbone network)
tau = float(input("enter the uplink propogation delay: "))
# number of optical amplifying from ONU BS to CCC
n = int(input("enter the number of optical amplifying: "))


# OUTPUT
# optimal computation offloading decision list S
S = []*N
# total minimum energy consumption
E_min = 0

# FUNCTIONS
# functions to calculate total processing time
def compute_local(ci,f_local):            # for local execution model
    return (ci/f_local)

def compute_mec(mi,ri,c_bs,ci,f_mec):     # for mobile-edge execution model
    a= mi/ri
    b=mi/c_bs
    g= ci/f_mec
    return(a+b+g)

def compute_ccc(mi,ri,n,c_bs,tau):        # for centralised cloud execution model
    a=mi/ri
    b=n*(mi/c_bs)
    return(a+b+tau)

# functions to calculate the total consumed energy
def energy_local(ci,y_local):             # for local execution model
    return (ci*y_local)
def energy_mec(pi,t_mec):                 # for mobile-edge execution model
    return(pi*t_mec)
def energy_ccc(pi,t_ccc):                 # for centralised cloud execution model
    return(pi*t_ccc)

# procedure to determine offloading decision
def offloading_decision_procedure(P):
    for p in P:
        e_mec = energy_mec(transmit_power[p],compute_mec(m[p],r[p],c_bs,c[p],f_mec))
        e_ccc = energy_ccc(transmit_power[p],compute_ccc(m[p],r[p],n,c_bs,tau))
        if e_mec <= e_ccc:
            S_mec.append(p)
        else:
            S_ccc.append(p)

# MAIN ALGORITHM
M = []*N
P = []*N
S_local = []*N
S_mec = []*N
S_ccc= []*N
for i in range(0,N):
    t_local=compute_local(c[i],f_local[i])
    t_mec=compute_mec(m[i],r[i],c_bs,c[i],f_mec)
    t_ccc=compute_ccc(m[i],r[i],n,c_bs,tau)
    if min(t_local,t_mec,t_ccc) > t_max[i]:
        N_set.remove(i)
if len(N_set)==0:
    sys.exit("No offloading scheme possible")
else:
    N=len(N_set)
    for j in N_set:
        t_local = compute_local(c[j],f_local[j])
        if t_local>t_max[j] and len(M)<K:
            N_set.remove(j)
            M.append(j)
            P.append(j)
            offloading_decision_procedure(P)
P = []
while len(N_set) != 0 :
    for l in N_set:
        N_set.remove(l)
        k = min(K, len(N_set) + len(M))
        e_local = energy_local(c[l], y_local[l])
        e_mec = energy_mec(transmit_power[l],compute_mec(m[l],r[l],c_bs,c[l],f_mec))
        e_ccc = energy_ccc(transmit_power[l],compute_ccc(m[l],r[l],n,c_bs,tau))
        if min(e_mec,e_ccc) <= e_local and len(M)<K:
            M.append(l)
            P.append(l)
        else:
            S_local.append(l)

offloading_decision_procedure(P) # for all tasks not carried out by MDs locally

# to calculate E_min and print the offloading decsion set

if len(S_local)!=0:
    print("These tasks have been performed on the MDs itself" )
    for f in S_local:
          E_min = E_min + energy_local(c[f],y_local[f])
          print("Task %i" %f)
    print("\n")
else:
    print("No tasks have been performed locally")


if len(S_mec)!= 0:
    print("these tasks have been offloaded and performed on the MEC server" )
    for g in S_mec:
          E_min = E_min + energy_mec(transmit_power[g],compute_mec(m[g],r[g],c_bs,c[g],f_mec))
          print("Task %i" %g)
    print("\n")
else:
    print("No tasks have been offloaded to the MEC server")


if len(S_ccc)!= 0:
    print("these tasks have been offloaded and performed on the centralised cloud server" )
    for h in S_ccc:
         E_min = E_min + energy_ccc(transmit_power[h],compute_ccc(m[h],r[h],n,c_bs,tau))
         print("Task %i" %h)
else:
    print("No tasks have been offloaded to the centralised cloud server")

print ("Minimum Energy Consumption is: ", E_min)









