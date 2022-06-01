# Ambulance_Location_Eval
Evaluating the existing ambulance location in the Municipality of Patras


## Requirements

Create environment with conda.

```
conda create --name Ambulance python=3.7
```

Activate environment and change directory:

```
conda activate Ambulance
cd anaconda3/envs/Ambulance
```

Use pip install to install the required packages: numpy, pymprog

pymprog is needed to define the model that sets the restrictions for the integer programming.

## The problem

USEMSA (United States Emergency Medical Services Act) sets these standards:

- In urban areas 95% of the incidents should be dealt with in **10 minutes**.
- In rural areas 95% of the incidents should be dealt with in **35 minutes**.

In case of **heart attack** the critical **response time** is **8 minutes** and every minute after that reduces the survival rates by 7-10%.

## The mathematical model

DSM (Double Standard Model) was first introduced by Gendreu in 1997 and uses two coverage standards: rt1 and rt2, where rt1 < rt2.

All the demand should be covered from the ambulances in time rt2 and lambda (%) in time rt1.

In order to solve this problem, we have to utilize graphs by defining a set of nodes that include:
- points of interest
- ambulance stations
- number of hospitals

There are also some more parameters for the problem that need to be defined.
- di: the density of emergency calls in region of interest i
- rt1 --> emergencies in 10 or 8 minutes and rt2 --> the response time that is needed for all the incidents to be dealt with.
- p: the upper limit of the vehicles (ambulances)
- pj: the upper limit of the vehicles in station j
- tji: the time that an ambulance needs to go from station i to region of interest j
- aij: binary variabe equal to 1 when tji <= rt1
- bij: binary variable equal to 1 when tji <= rt2
- lambda: the coverage percentage in time rt1

Finally, there are the variables of interest:
- xik: binary variable equal to 1 when region of interest i is covered k times from an ambulance in time rt1
- yj: the number of ambulances in station j (integer value)

So, we define the objective function:
Maximize(sum(di*xi^2)) where i =1, ..., n.

The objective function aims in maximizing the number of emergency calls that are covered 2 times in time rt1 in the region of interest i, while all the emergency calls are covered at least 1 time in time rt2.

We also set 7 restrictions that give the solution, along with some sign restrictions.

## Case study: Municipality of Patras

number of ambulances: 10
size: 125,4 km^2 
residents (2011): 170.896
density: 1.363 residents per km^2

![image](https://user-images.githubusercontent.com/24894934/171456625-e9ca7652-a194-4729-9b72-36f987fc2781.png)

Here are presented 12 regions of interest (black spots) and 4 stations/hospitals.

![image](https://user-images.githubusercontent.com/24894934/171456997-90195392-ed91-4cc8-b402-a5085e1a0f63.png)

I calculate the parameters needed for each region of interest and each station, while also setting a number of emergency calls in each region. The total number of calls and thus the maximum value of the objective function is 125.

I run the programm one time with 3 stations and one time with 4 stations (there was a recent station opening). Response time rt2 is set as the max of tji. In the first case rt2=18 minutes and in the second case rt2=16 minutes.

## Results

# First case (3 stations)

10 ambulances, rt1 = 10 minutes, rt2 = 18 minutes, emergency calls = 125

![Case 1 results](https://user-images.githubusercontent.com/24894934/171460688-f41a464b-d7ce-4b3f-8c96-09f1bcec116d.png)

minimum number of ambulances required to reach max value of the objective function: 5

max value of objective function: 111

The current system has an upper bound of 88.8% coverage of the emergency calls in response time rt1 = 10 minutes.

If we change rt1 to 8 minutes, the coverage drops to 42.4%.

![Case 1 results rt1_8](https://user-images.githubusercontent.com/24894934/171461877-28fb638c-45a0-41cd-b533-f2855c96fd62.png)

# Second case (4 stations)



