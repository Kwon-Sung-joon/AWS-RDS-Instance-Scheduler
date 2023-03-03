# AWS-RDS-Instance-Schedule
- 지정된 시간 혹은 장기간 사용하지 않은 RDS를 중지하여 비용 절감
- 

# Architecture
![image](https://user-images.githubusercontent.com/43159901/166951503-89d1e272-dce9-4ede-b80c-37c4f19b8155.png)


## 1. Create IAM Role For Lambda

![image](https://user-images.githubusercontent.com/43159901/166937754-b8d99fa0-0c5b-495b-8c48-e85942199d84.png)

![image](https://user-images.githubusercontent.com/43159901/166937972-e32dd6cd-7011-4dab-8315-8462263d11bb.png)


## 1-1. Create Inline Policy (see attachment "iam-policy.json" for details)
![image](https://user-images.githubusercontent.com/43159901/166938518-814d9ee4-806a-4aab-9932-033b559c5b94.png)

## 2. Create Lambda Functions

![image](https://user-images.githubusercontent.com/43159901/166939646-3519482c-9cc2-41fc-b691-c177cd964d36.png)

## 2-1. Create Lambda Environment variables.

Keys : EVENT_RULE, RDS_IDENTIFIER	<br>
Values : RDS-Schedule-Rule (you can see on chapter 3-3.) , Your DB Identifer
![image](https://user-images.githubusercontent.com/43159901/166950866-86d01c1f-249d-4deb-a2e7-2acd78058e40.png)



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

### Case 1. RDS Instance Start on AWS Web Console.
![image](https://user-images.githubusercontent.com/43159901/166944689-4dccb7e3-9b04-4ba9-b61e-5b80784981d4.png)
![image](https://user-images.githubusercontent.com/43159901/166944940-360dc974-3f3b-473a-9e59-b1f7c89c9510.png)
#### RDS-Schedule-Rule -> 1시간 후로 스케줄 변경
#### 1시간 후에 Lambda가 실행되어 RDS 중지
![image](https://user-images.githubusercontent.com/43159901/166945373-b0426915-dd22-44d0-9cbf-d6aafdc54a03.png)
#### CloudWatch Loggroups에서 로그 확인 가능

### Case 2. RDS Instance Stop on AWS Web Console.
![image](https://user-images.githubusercontent.com/43159901/166946162-a6148fb5-9e2f-4402-ac71-f87e56fbafe6.png)
![image](https://user-images.githubusercontent.com/43159901/166946684-1b83b7b9-88f8-427b-a92c-35e63943d21b.png)
#### RDS-Schedule-Rule -> 7일 3시간 전으로 스케줄 변경
#### 7일 후 (3시간 전) Lambbda가 실행되어 RDS 시작
![image](https://user-images.githubusercontent.com/43159901/166946848-d3b6d3aa-c266-41b5-8363-b4770919b26c.png)
#### CloudWatch Loggroups에서 로그 확인 가능

