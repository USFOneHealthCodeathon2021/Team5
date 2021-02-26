# File:     Austin.R
# Project:  Decode Human Breath Microbiomes
# Reference source: Learning R taught by Dr. Poulson on Linked Learning 

# INSTALL AND LOAD PACKAGES ################################
library(xts)
library(pacman)

# Install pacman ("package manager") if needed
# If there is an error, you can refer to this online material: https://stackoverflow.com/questions/42807247/installing-package-cannot-open-file-permission-denied
# if (!require("pacman")) install.packages("pacman")

# Load contributed packages with pacman
pacman::p_load(pacman, party, rio, tidyverse)
# pacman: for loading/unloading packages
# party: for decision trees
# rio: for importing data
# tidyverse: for so many reasons

# LOAD AND PREPARE DATA ############################################################################################################################################

# Save data to "df" (for "data frame")
# Rename outcome as "y" (if it helps)
# Specify outcome with df$y

# Import CSV files with readr::read_csv() from tidyverse
(df <- read_csv("data/Austin_data.csv"))
head(df)

# Create a reduce dataset containing only normalized least square variables only
df2 <- df %>%
  select(normalized_intensity1:normalized_intensity113
) %>%
  print(5)

# FLITER BY ONE VARIABLE ###################################

# Make a copy of df2
df3 <- df2 %>%
    print(1)

nTimeSeries = nrow(df3)

nObservations = ncol(df3)

#data.matrix <- matrix(df3, nrow = ncol(df3), ncol = nrow(df3) ,  byrow = TRUE)

#dim(data.matrix)

data.matrix[1,1]
## Coerce data frame to array
## In here we unlist a data frame by rows, not columns by using the transpose method, t(dataframe)
Austin.array <- array(unlist(t(df3)), dim = c(nObservations, 1, nTimeSeries))

trend_v = vector()
p1_v = vector()
p2_v = vector()

for(i in 1:nTimeSeries){
  
  # Create a daily time series in R from a numeric vector
  
  Austin.ts <- ts(Austin.array [,,i], start=1, frequency=7)
  
  Austin.ts.stl = stl(Austin.ts, s.window= 30)
  
  trend <- Austin.ts.stl$time.series[,2]

  # Step 2 ###########################################################
  N = 30
  dX = vector()
  for(j in (nObservations - N + 1): nObservations){
    dX[j - nObservations + N] = trend[j] - trend[j-1]
  }
  v = var(dX)/2
  v0 <- var(dX)/2
  #print(v0)
  dXbar <- mean(dX)
  #print(dXbar)
  
  posterior_mean <- v0/(1/(nObservations-1)+v0)*dXbar
  
  posterior_var <- 1/(1/v0 + N/v)
  
  #print(posterior_mean)
  #print(posterior_var)
  
  p1 <- pnorm(0, posterior_mean, sqrt(posterior_var), lower.tail = FALSE)
  p2 <- 1 - p1
  
  p1_v = c(p1_v, p1)
  p2_v = c(p2_v, p2)
  
}


# sort by p1 and p2
p1_order = order(p1_v, decreasing = TRUE)
p2_order = order(p2_v, decreasing = TRUE)
# print names of top 5 p1
names = df$taxa_string
Austin.ts <- tail(ts(Austin.array [,,p1_order[1]], start=1, frequency=7), 30)
plot(Austin.ts, ylab = "normalized intensity", xlab = "last 30 days", type = 'l', main = names[p1_order[1]])
Austin.ts <- tail(ts(Austin.array [,,p1_order[2]], start=1, frequency=7), 30)
plot(Austin.ts, ylab = "normalized intensity", xlab = "last 30 days", type = 'l', main = names[p1_order[2]])
Austin.ts <- tail(ts(Austin.array [,,p1_order[3]], start=1, frequency=7), 30)
plot(Austin.ts, ylab = "normalized intensity", xlab = "last 30 days", type = 'l', main = names[p1_order[3]])


# top 5 p2
Austin.ts <- tail(ts(Austin.array [,,p2_order[1]], start=1, frequency=7), 30)
plot(Austin.ts, ylab = "normalized intensity", xlab = "last 30 days", type = 'l', main = names[p2_order[1]])
Austin.ts <- tail(ts(Austin.array [,,p2_order[2]], start=1, frequency=7), 30)
plot(Austin.ts, ylab = "normalized intensity", xlab = "last 30 days", type = 'l', main = names[p2_order[2]])
Austin.ts <- tail(ts(Austin.array [,,p2_order[3]], start=1, frequency=7), 30)
plot(Austin.ts, ylab = "normalized intensity", xlab = "last 30 days", type = 'l', main = names[p2_order[3]])

names[p1_order[2]]
names[p1_order[3]]




# CLEAN UP #################################################

# Clear environment
rm(list = ls()) 

# Clear packages
p_unload(pacman, negate=TRUE)  # Remove all add-ons

# Clear console
cat("\030")  # ctrl+L


