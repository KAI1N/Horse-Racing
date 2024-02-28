library(dslabs)
library(tidyverse)
library(caret)
library(dplyr)
library(readr)
#read.csvだとエラーが出たので、readrのread_csvを用いた
horse=read_csv('C:/Users/khata/OneDrive/デスクトップ/Horse Racing/2023_processed_data.csv')
nrow(horse)
top3=horse%>%
  filter(rank<=3)
ntop3=horse%>%
  filter(rank>3)
nrow(top3)
nrow(ntop3)

