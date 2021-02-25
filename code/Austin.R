# File:     Austin.R
# Project:  Decode Human Breath Microbiomes
# Reference source: Learning R taught by Dr. Poulson on Linked Learning 

# INSTALL AND LOAD PACKAGES ################################
library(xts)

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

# # Import CSV files into xts object
# 
# df3 <- df %>%
#   select(normalized_intensity1:normalized_intensity113
#   ) %>%
#   print(5)
# 
# xtsAustin <- as.matrix((df3), ncol=113)
# xtsAustin_data <- t(xtsAustin)
# 
# head(xtsAustin_data)


## Coerce data frame to array
## In here we unlist a data frame by rows, not columns by using the transpose method, t(dataframe)
Austin.array <- array(unlist(t(df3)), dim = c(113, 1, 1994))

print(ts1.array[,,1])

print(ts1.array[,,2])

typeof(ts1.array[,,2])

class(ts1.array[,,2])

is.vector(ts1.array[,,2])

# Create a daily time series in R from a numeric vector

ts.ts1 <- ts(ts1.array[,,1], start=1, frequency=7)

plot(ts.ts1)

ts.ts1.stl = stl(ts.ts1, s.window= 21)

plot(ts.ts1.stl)

is.vector(ts.ts1.stl$time.series[,2])


ts.ts2 <- ts(ts1.array[,,2], start=c(2003,2), end=c(2003,6), frequency=365)

plot(ts.ts2)

is.ts(ts.ts1)
## Create an xts object#

## for each time serie:
 ## convert it into a xts class 
 ## pass it into stl method
 ## I would have returns an object of class "stl" with components time.series
## a multiple time series with columns seasonal, trend and remainder
## extract the trend, put into into a result vector. Result vector would have 1994 elements.

austin_trend_result = rep(0,113)

for(i in 1:2){
  # Create a vector, size 113
  trend_v = rep(0,113)
  
  # Create a daily time series in R from a numeric vector
  
  Austin.ts <- ts(ts.array[,,i], start=1, frequency=7)
  
  ts.ts1.stl = stl(ts.ts1, s.window= 21)
  
  # Populate an array here
  
}
  

# CLEAN UP #################################################

# Clear environment
rm(list = ls()) 

# Clear packages
p_unload(pacman, negate=TRUE)  # Remove all add-ons

# Clear console
cat("\014")  # ctrl+L


