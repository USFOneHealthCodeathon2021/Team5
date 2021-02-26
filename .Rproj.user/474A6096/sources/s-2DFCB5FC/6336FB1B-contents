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

for(i in 1:nTimeSeries){
  
  # Create a daily time series in R from a numeric vector
  
  Austin.ts <- ts(Austin.array [,,i], start=1, frequency=7)
  
  Austin.ts.stl = stl(Austin.ts, s.window= 21)
  
  trend_v <- c(trend_v, Austin.ts.stl$time.series[,2])
}

trend_matrix <- matrix(trend_v, nrow = nObservations, byrow = TRUE)

dim(trend_matrix)


# CLEAN UP #################################################

# Clear environment
rm(list = ls()) 

# Clear packages
p_unload(pacman, negate=TRUE)  # Remove all add-ons

# Clear console
cat("\014")  # ctrl+L


