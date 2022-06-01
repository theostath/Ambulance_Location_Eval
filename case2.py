import numpy

# line 43-44: define rt1
# line 68: define lamda

#       ----- DATA BLOCK ------

################################################################
# region 1: Patra ( with 4 points of interest )
# region 2: Rio ( with 2 points of interest )
# region 3: Messatida ( with 3 points of interest )
# region 4: Paralia ( with 1 point of interest )
# region 5: Vraxnaiika ( with 2 points of interest )
################################################################
d = numpy.array([25, 25, 25, 25, 4, 4, 3, 3, 2, 6, 2, 1]) # density call (per region of interest)

P = 10+14 # upper boundary of ambulances
NumOfStations = 4
Pj = P-NumOfStations # upper boundary of ambulances per station
################################################################
#                           /     TIMES    /
# rows = stations
# station 1 = Hospital "Agios Antreas"
# station 2 = University Hospital
# station 3 = Port station
# station 4 = station of Pampeloponnisiako

# columns = points of interest
# points 1-4 = Patra
# points 5-7 = Messatida
# points 8-9 = Rio
# points 10-11 = Vraxnaiika
# points 12 = Paralia

# time from station to point of interest (in min)
time = numpy.array([[10, 7, 9, 5, 10, 10, 11, 14, 18, 15, 18, 11],
                    [11, 20, 18, 17, 22, 20, 19, 6, 11, 24, 25, 21],
                    [10, 10, 16, 3, 13, 13, 16, 14, 18, 14, 23, 11],
                    [13, 6, 8, 8, 9, 9, 9, 13, 17, 13, 16, 12]])

# Defince response times
# from station to spot
#rt1 = 10 # response time 1 = 8 min
rt1 = 8 # response time 1 = 8 min
# response time 2: choose the max from the minimum time from station to point of interest
rt2 = 0
for j in range(12):
    if min(time[i][j] for i in range(4))>rt2:
        rt2 = min(time[i][j] for i in range(4))

################################################################
#                     /     BINARY VALUES    /      
# if t_one <= rt1 then a = 1
a = numpy.zeros((4,12),'int')

for i in range(0,4):
    for j in range(0,12):
        if time[i][j]<=rt1:
            a[i][j]=1
# if t_one <= rt2 then b = 1
b = numpy.zeros((4,12),'int')

for i in range(0,4):
    for j in range(0,12):
        if time[i][j]<=rt2:
            b[i][j]=1
################################################################
lamda = 0.6 # percentage of points of interest covered in time rt1 (this is set as a requirement)

#        ---- MODEL BLOCK ----
from pymprog import model

# direct handling of the model
p = model('Ambulance Apodosh DSM')

p.verbose(True)  # be verbose

# VARIABLES
x1 = p.var('x1', 12, kind=int, bounds=(0,1)) # create 12 variables
x2 = p.var('x2', 12, kind=int, bounds=(0,1)) # create 12 variables
y = p.var('y', 4, kind=int, bounds=(1,Pj)) # create 4 variables

# OBJECTIVE FUNCTION
p.maximize(sum(d[i]*x2[i] for i in range(12)))

# CONSTRAINTS
# constraint no 1
for j in range(len(b[0])):
    R1=sum(y[i]*b[i][j] for i in range(4))>=1

# constraint no 2
R2=sum(d[i]*x1[i] for i in range(12))>=lamda*sum(d[i] for i in range(12))

# constraint no 3
for j in range(len(a[0])):
    R3=sum(y[i]*a[i][j] for i in range(4)) -x1[j] -x2[j] >=0

# constraint no 4
for i in range(12):
    R4=x1[i]>=x2[i]

# constraint no 5
R5=sum(y[i] for i in range(4))<=P
#R6=sum(y[i] for i in range(4))>=P # if i want to use all the ambulances, i also use this constraint

# constraints no 6 and 7 in bounds ^

#                        ---- REPORT BLOCK ----
#solver('intopt') #  for integer programming
p.solve() # solve the model

print("Response time for", lamda*100,"% double coverage in", rt1,"min.")
print("Maximum response time:", rt2,"min.")

print ("Value of objective function:", sum(d[i]*x2[i].primal for i in range(12)))

print ("Number of ambulances in Hospital 'Agios Antreas':", y[0].primal)
print ("Number of ambulances in University Hospital:", y[1].primal)
print ("Number of ambulances in Port station:", y[2].primal)
print ("Number of ambulances in station of Pampeloponnisiako:", y[3].primal)

p.end()