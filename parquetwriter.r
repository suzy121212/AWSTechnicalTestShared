#Parquet Writer

#Locally creates a Parquet file with some data in it. NB:Data is taken from Iris datset

#Note: Prior to running script ensure packages arrow and datasets are installed, using install.packages("arrow","datasets")

library(arrow)
library(datasets)

#Load Iris data set
data(iris)
iris<-iris[1:100,]

#Write Iris data set
write_parquet(iris, "irisdataset.parquet")
df<-read_parquet("irisdataset.parquet")


