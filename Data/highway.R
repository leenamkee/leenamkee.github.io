setwd("E:/00.업무/2018년/201807 DS 인증 준비")

library(tidyverse)
library(tibble)

### 데이터 불러오기 ####
highway_01_07 <- read.csv("highway_01_07_1.csv",stringsAsFactors = F, encoding="UTF-8")
highway_08_12 <- read.csv("highway_08_12.csv",stringsAsFactors = F, encoding="UTF-8")

### Kor, Eng 수정 ####
start_pt_1 <- unique(highway_01_07[,2])
start_pt_2 <- unique(highway_08_12[,2])

mapping <- cbind(start_pt_2, start_pt_1)

colnames(mapping) <- c("Kor","Eng")

highway_08_12_1 <- merge(highway_08_12, mapping, by.x = "StartPoint", by.y = "Kor")

highway_08_12_1 <- highway_08_12_1[,-1]

highway_08_12_2 <- highway_08_12_1[,c(1,7,2:6)]

colnames(highway_08_12_2) <- colnames(highway_01_07)



#### 통합 2014년 데이터 생성 ####
highway_2014 <- rbind(highway_01_07, highway_08_12_2)

rm(highway_01_07,highway_08_12)
rm(highway_08_12_1,highway_08_12_2)
rm(mapping, start_pt_1, start_pt_2)


####  (1) 2014년 고속도로 통행 시작시점이 강원인 모든 차량 통행량(강원을 포함한 모든 도착지점)의 q1,median,q3 를 구하시오.####


#summary(highway_2014[highway_2014[,2]=="Gangwon",3:7])


#Gangwon <- highway_2014[highway_2014[,2]=="Gangwon",3:7]
#summary(Gangwon)

#Gangwon_v <-c(Gangwon[,1],Gangwon[,2],Gangwon[,3],Gangwon[,4],Gangwon[,5])
#summary(Gangwon_v)
# rm(Gangwon,Gangwon_v)

Gangwon_gather <- highway_2014 %>% filter(StartPoint =="Gangwon") %>%
  select(Gyeonggi:Gangwon) %>% gather()

summary(Gangwon_gather$value)


#### (2) 경기_경상, 경상_경기 평균차이 ####

highway_gi_sang <- highway_2014[highway_2014[,2]=="Gyeonggi","Gyeongsang"]
highway_sang_gi <- highway_2014[highway_2014[,2]=="Gyeongsang","Gyeonggi"]

t.test(highway_gi_sang, highway_sang_gi)


#highway_gi_sang[,2] <- c("Gyeongsang")
#highway_sang_gi[,2] <- c("Gyeonggi")

#colnames(highway_gi_sang) <- c("N","E")
#colnames(highway_sang_gi) <- c("N","E")

#highway_gs <- rbind(highway_gi_sang, highway_sang_gi)

#highway_gi_sang <- c(as.data.frame(highway_gi_sang))
#highway_sang_gi <- c(highway_sang_gi)
#str(highway_gi_sang)

#t.test(N ~ E, data = highway_gs)

 
 #### (3) 충청발 강원행 교통량 월별 요일별 정리 ####
 
data_3 <- highway_2014[highway_2014[,2]=="Chungcheong",c(1,7)]
#weekdays(as.Date(data_3[,1],"%Y-%m-%d"))

data_3[,"Day_of_week"] <- c(weekdays(as.Date(as.character(data_3[,1]),"%Y%m%d")))

data_3[,"Months"] <-c(months(as.Date(as.character(data_3[,1]),"%Y%m%d")))

data_3_summarise <- data_3 %>% group_by(Months, Day_of_week) %>% 
  summarise(avg = mean(Gangwon))

data_3_1 <- spread(data_3_summarise,"Day_of_week","avg")
data_3_1 <- data_3_1[,c(1,6,5,8,4,3,2,7)]

# normalize

data_3_1_norm <- data_3_1[,1]
data_3_1_norm[,2] <- (data_3_1[,2] - min(data_3_1[,2]))/(max(data_3_1[,2]) - min(data_3_1[,2]))
data_3_1_norm[,3] <- (data_3_1[,3] - min(data_3_1[,3]))/(max(data_3_1[,3]) - min(data_3_1[,3]))
data_3_1_norm[,4] <- (data_3_1[,4] - min(data_3_1[,4]))/(max(data_3_1[,4]) - min(data_3_1[,4]))
data_3_1_norm[,5] <- (data_3_1[,5] - min(data_3_1[,5]))/(max(data_3_1[,5]) - min(data_3_1[,5]))
data_3_1_norm[,6] <- (data_3_1[,6] - min(data_3_1[,6]))/(max(data_3_1[,6]) - min(data_3_1[,6]))
data_3_1_norm[,7] <- (data_3_1[,7] - min(data_3_1[,7]))/(max(data_3_1[,7]) - min(data_3_1[,7]))
data_3_1_norm[,8] <- (data_3_1[,8] - min(data_3_1[,8]))/(max(data_3_1[,8]) - min(data_3_1[,8]))



#Kmeans

km <- kmeans(data_3_1_norm[,-1], 3, iter.max = 100)

data_3_1_norm$Cluster <- km$cluster
table(km$cluster)

data_3_summarise_1 <- merge(data_3, data_3_1_norm[,c(1,9)], "Months")

data_3_MON_CL3 <- data_3_summarise_1 %>% 
  filter(Day_of_week == "월요일" & Cluster == 2) %>%
  summarise(avg = mean(as.double(Gangwon)))

data_3_MON_CL3


#### regression ####
#highway_2014$Day_of_week <- weekdays(as.Date(as.character(highway_2014$Date),"%Y%m%d"))

highway_2014$Day_of_week <- c(weekdays(as.Date(as.character(highway_2014[,1]),"%Y%m%d")))

#highway_2014$week_NO <- week(as.Date(highway_2014$Date))

reg_feature_1 <- highway_2014 %>% 
  filter(StartPoint == "Gyeonggi" & Day_of_week =="일요일") %>%
  select(date, Chungcheong)

reg_feature_2 <- highway_2014 %>% 
  filter(StartPoint == "Gyeonggi" & Day_of_week =="일요일") %>%
  select(date, Gyeongsang)

reg_feature_3 <- highway_2014 %>% 
  filter(StartPoint == "Gyeonggi" & Day_of_week =="일요일") %>%
  select(date, Gangwon)

reg_feature_4 <- highway_2014 %>% 
  filter(StartPoint == "Gyeonggi" & Day_of_week =="토요일") %>%
  select(date, Jeolla)

reg_target <- highway_2014 %>% 
  filter(StartPoint == "Gyeonggi" & Day_of_week =="일요일") %>%
  select(date, Jeolla)


# reg_data <- as.data.frame(cbind(Date = reg_feature_1$Date,
#                  X1 = as.numeric(reg_feature_1$Chungcheong), 
#                  X2 = as.numeric(reg_feature_2$Gyeongsang),
#                  X3 = as.numeric(reg_feature_3$Gangwon),
#                  X4 = as.numeric(reg_feature_4$Jeolla),
#                  Y = as.numeric(reg_target$Jeolla)))

reg_data <- cbind(reg_feature_1,reg_feature_2,reg_feature_3,reg_feature_4,reg_target)
reg_data <- reg_data[,c(1,2,4,6,8,10)]
colnames(reg_data) <- c("Date","X1","X2","X3","X4","Y")

reg_train <- reg_data[1:26,]
reg_test <- reg_data[27:29,1:5]

#lm_reg <- lm(Y ~ X1+X2+X3, data = reg_train[,-1])
lm_reg <- lm(Y ~ ., data = reg_train[,-1])
summary(lm_reg)

(pre_reg <- predict.lm(lm_reg,reg_test[,-1]))
