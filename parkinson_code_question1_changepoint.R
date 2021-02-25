# Description----
# John Parkinson's code for the 2021 Codathon -- Team 5 -- 2021-02-24
# Addressing Question 1: Is there a trend in the longitudinal data?
# Use the changepoint package to detect an inflection in a time series.
# In this case, I'm looking at a single random bacterium from the data set.
# I'm following the tutorial from https://rpubs.com/richkt/269908
#

# Set working directory and seed----
#setwd("Add/Your/Pathway/Here/")
set.seed(123)

# Load libraries----
suppressMessages(suppressWarnings(library('tidyverse')))
suppressMessages(suppressWarnings(library('changepoint')))
suppressMessages(suppressWarnings(library('tseries')))

# Define custom functions----
cptfn <- function(data, pen) { 
  ans <- cpt.mean(data, test.stat="Normal", method = "PELT", penalty = "Manual",
                  pen.value = pen)
  length(cpts(ans)) +1
} # I just copied this function from the tutorial


# Load and clean bacterial data----
y_anno <- read.csv("Austin_data.csv") %>%
  select(1:11) %>% # retain only annotation data
  slice(72) %>% # retain one random row (in this case, row 72)
  as_tibble() # convert to tibble

y_ts <- read.csv("Austin_data.csv") %>%
  select(125:237) %>% # retain only time series data
  slice(72) %>% # retain one random row (in this case, row 72)
  ts() # convert to time series
  
# Plot time series and evaluate penalty parameter----
pen.vals <- seq(0, 300,1) # values taken from tutorial--may need to adjust

elbowplotData <- unlist(lapply(pen.vals, function(p) 
  cptfn(data = as.numeric(y_ts), pen = p)))
  # create elbow plot to find appropriate PELT penalty value

plot.ts(as.numeric(y_ts),type='l',col='red',
        xlab = "time",
        ylab = " Y(t)",
        main = "Bacterial Time Series")

plot(pen.vals, elbowplotData, 
     xlab = "PELT penalty parameter",
     ylab = " ",
     main = " ")

# Set penalty, identify change point, and plot----
penalty.val <- 300 # this value is determined from elbow plots

y_ts_cptm <- cpt.mean(as.numeric(y_ts), 
                      penalty='Manual', pen.value = penalty.val, method='PELT') 

y_ts_cptm <- cpts(y_ts_cptm)

plot(y_ts_cptm,
     xlab = "time",
     ylab = " Y(t)",
     main = "Change in mean signal")

acf(as.numeric(y_ts), lag.max = length(y_ts),
    xlab = "lag #", ylab = 'ACF', main=' ')

# Check additional statistics----
Box.test(as.numeric(y_ts), lag = 300, type = "Ljung-Box")
adf.test(as.numeric(y_ts))
kpss.test(as.numeric(y_ts), null = "Trend")
