# AWS-RDS-Instance-Scheduler
AWS-RDS-Instance-Scheduler 

# Architecture
![image](https://user-images.githubusercontent.com/43159901/166937171-eee393ca-f3af-4a12-9e29-d037fe07a472.png)


## 1. Create IAM Role For Lambda

![image](https://user-images.githubusercontent.com/43159901/166937754-b8d99fa0-0c5b-495b-8c48-e85942199d84.png)

![image](https://user-images.githubusercontent.com/43159901/166937972-e32dd6cd-7011-4dab-8315-8462263d11bb.png)


## 1-1. Create Inline Policy (see attachment "iam-policy.json" for details)
![image](https://user-images.githubusercontent.com/43159901/166938518-814d9ee4-806a-4aab-9932-033b559c5b94.png)

## 2. Create Lambda Functions

![image](https://user-images.githubusercontent.com/43159901/166939646-3519482c-9cc2-41fc-b691-c177cd964d36.png)

## 3. Create Amazon EventBridge Rules

## 3-1. Create RDS-Start-Rule with Custom Event pattern

![image](https://user-images.githubusercontent.com/43159901/166941405-7781e7d3-de81-4ccd-8182-ebcdca5b29b1.png)
![image](https://user-images.githubusercontent.com/43159901/166942049-888df8ae-19c0-43d2-bacf-276a94dbf3d7.png)
![image](https://user-images.githubusercontent.com/43159901/166942442-9ab0d43c-bbcd-4e1b-ac2b-f891c5d4250a.png)

## 3-2. RDS-Stop-Rule with Custom Event pattern
![image](https://user-images.githubusercontent.com/43159901/166942601-b94077e6-ddbd-4b51-b557-3341676b7ad2.png)
![image](https://user-images.githubusercontent.com/43159901/166942375-e14292d3-da4f-419f-80ba-4189983397a2.png)
![image](https://user-images.githubusercontent.com/43159901/166942445-df16882c-5ac6-4a9b-abe4-62a0579f9c98.png)


## 3-3. RDS-Schedule-Rule  with Cron Schedule
![image](https://user-images.githubusercontent.com/43159901/166942699-6a92ccfa-df0d-45c9-bb69-d72a5a370b9e.png)
![image](https://user-images.githubusercontent.com/43159901/166942916-c4954d0d-9392-4491-bd8e-03da8e24af51.png)
![image](https://user-images.githubusercontent.com/43159901/166942957-c7c754b9-61c1-40f7-9252-0308344314ad.png)


## PoC 

### Case 1. 


### Case 2.


### Case 3.

### Case 4.
