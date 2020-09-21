# Oil Price Forecast with the Facebook Prophet ----

# During this lab, we will go through the whole workflow to 
# perform WTI CRUDE Oil price forecasting using the 
# Facebook Prophet algorithm inside the `modeltime` library.

# 1.0 - Libraries ----

# API
library(Quandl)

# Time Series
library(lubridate)
library(timetk)

# Visualization
library(plotly)

# Core
library(tidyverse)
library(tidyquant)
library(data.table)

# Model
library(tidymodels)
library(modeltime)
library(prophet)


# 2.0 - Loading and Visualizing the Data ----

# My Quandl key. To obtain a Quandl key, register using
# the link https://www.quandl.com/
# Quandl.api_key("Add your key here")
Quandl.api_key(Sys.getenv("QUANDL_API_KEY"))

# Setting API key for the EIA WTI crude oil price
eia_code <- "EIA/PET_RWTC_D"

# Downloaging data
wti_prices <- Quandl(code = eia_code, 
                     start_date = "2005-01-01", 
                     end_date = today(), 
                     order = "asc") %>% as_tibble()

wti_prices %>% plot_time_series(Date, 
                                Value,
                                .smooth = T,
                                .smooth_size = 0.5,
                                .smooth_alpha = 0.7,
                                .smooth_degree = 2,
                                .smooth_period = "1 year",
                                .interactive = T, 
                                .title = "WTI Oil Price (USD)",
                                .color_lab = "Year",
                                .plotly_slider = T)


# Subset the data for previous 2020 (unpredictable pandemic?)
# wti_prices <- wti_prices %>% 
#     subset(Date < "2020-01-01")
# 
# wti_prices %>% plot_time_series(Date, 
#                                 Value,
#                                 .smooth = T,
#                                 .smooth_size = 0.5,
#                                 .smooth_alpha = 0.7,
#                                 .smooth_degree = 2,
#                                 .smooth_period = "1 year",
#                                 .interactive = T, 
#                                 .title = "WTI Oil Price (USD)",
#                                 .color_lab = "Year",
#                                 .plotly_slider = T)


# 3.0 - Traing/Test Splitting ----

splits <- wti_prices %>% 
    time_series_split(assess = "12 months", cumulative = TRUE)

splits %>%
    tk_time_series_cv_plan() %>%
    plot_time_series_cv_plan(Date, 
                             Value, 
                             .interactive = T, 
                             .title = "WTI Oil Price (USD)",
                             .x_lab = "Date",
                             .y_lab = "WTI Oil Price (USD)",
                             .plotly_slider = T)


# 4.0 - Modeling the Prophet Model with the modeltime Library ----

## 4.1 - Fit Prophet Model ----
model_prophet <- prophet_reg(mode = "regression",
                             growth = "linear",
                             num_changepoints = 25,
                             season = "additive") %>%
    set_engine("prophet", weekly.seasonality = FALSE, changepoint.range = 1) %>%
    fit(Value ~ Date, training(splits))

model_prophet

## 4.2 - Fit ARIMA Model ----
model_arima <- arima_reg(mode = "regression",
                         seasonal_period = "1 weeks") %>%
    set_engine("auto_arima") %>%
    fit(Value ~ Date, training(splits))

model_arima

# 5.0 - Calibrating the Models ----

models_table <- modeltime_table(
    model_prophet,
    model_arima
)

models_table

calibration_table <- models_table %>% 
    modeltime_calibrate(testing(splits))

calibration_table

# 6.0 Forecasting over Testing Set ----

calibration_table %>%
    modeltime_forecast(actual_data = wti_prices) %>%
    plot_modeltime_forecast(.interactive = TRUE)

calibration_table %>%
    modeltime_accuracy() %>%
    table_modeltime_accuracy(.interactive = FALSE)


# 7.0 Refit Model ----

calibration_table %>%
    # filter(.model_id != 2) %>%      # Removing ARIMA model
    modeltime_refit(wti_prices) %>%
    modeltime_forecast(h = "12 months", actual_data = wti_prices) %>%
    plot_modeltime_forecast(.interactive = TRUE,
                            .plotly_slider = TRUE)


# 8.0 Other Time Units ----

# The downloaded data provides the daily price of the crude oil.
# We can aggregate the data for different time units for different
# types of analysis. First, a function to automatize this process:

set_time_unit <- function(data, time_unit = "month", .fun = mean) {
    
    output <- data %>%
        mutate(Date = floor_date(Date, unit = time_unit)) %>%
        
        group_by(Date) %>%
        summarize(Value = .fun(Value)) %>%
        ungroup()
    
    return(output)
}

wti_new_time_unit <- wti_prices %>% 
    set_time_unit(time_unit = "month",
                  .fun = median)

wti_new_time_unit %>% 
    plot_time_series(Date, 
                     Value,
                     .smooth = FALSE,
                     .interactive = T, 
                     .title = "WTI Oil Price (USD)",
                     .color_lab = "Year",
                     .plotly_slider = T)


# Split the data

plot_splits <- function(data, assess = "12 month") {

    data %>% 
        tk_time_series_cv_plan() %>%
        plot_time_series_cv_plan(Date, 
                                 Value, 
                                 .interactive = T, 
                                 .title = "WTI Oil Price (USD)",
                                 .color_lab = "Year",
                                 .plotly_slider = F)
    
}

wti_prices %>% 
    set_time_unit() %>% 
    time_series_split(assess = "12 months", cumulative = TRUE) %>% 
    plot_splits()
    
splits <- wti_new_time_unit %>% 
    time_series_split(assess = "12 months", cumulative = TRUE)


# Fit Prophet Model
model_prophet <- prophet_reg(mode = "regression",
                             growth = "linear",
                             num_changepoints = 25,
                             season = "additive") %>%
    set_engine("prophet", weekly.seasonality = FALSE, changepoint.range = 1) %>%
    fit(Value ~ Date, training(splits))

model_prophet


# Fit ARIMA Model
model_arima <- arima_reg(mode = "regression",
                         seasonal_period = "1 weeks") %>%
    set_engine("auto_arima") %>%
    fit(Value ~ Date, training(splits))

model_arima


# Calibrating the Models

models_table <- modeltime_table(
    model_prophet,
    model_arima
)

models_table

calibration_table <- models_table %>% 
    modeltime_calibrate(testing(splits))

calibration_table


# Forecasting over Testing Set

calibration_table %>%
    modeltime_forecast(actual_data = wti_new_time_unit) %>%
    plot_modeltime_forecast(.interactive = TRUE)

calibration_table %>%
    modeltime_accuracy() %>%
    table_modeltime_accuracy(.interactive = FALSE)

## Function for training and testing prediction

fit_test <- function(data, growth = "linear", seasonality = "additive", changepoint.range = 1) {
    
    model_prophet <- prophet_reg(mode = "regression",
                                 growth = growth,
                                 num_changepoints = 25,
                                 season = seasonality) %>%
        set_engine("prophet", weekly.seasonality = FALSE, changepoint.range = changepoint.range) %>%
        fit(Value ~ Date, training(data))
    
    return(model_prophet)
}



splits %>% 
    fit_test(seasonality = "multiplicative") %>% 
    modeltime_calibrate(testing(splits)) %>% 
    modeltime_forecast(actual_data = wti_new_time_unit) %>%
    plot_modeltime_forecast(.interactive = TRUE)

splits %>% 
    fit_test(seasonality = "additive") %>% 
    modeltime_calibrate(testing(splits)) %>% 
    modeltime_forecast(actual_data = wti_new_time_unit) %>%
    plot_modeltime_forecast(.interactive = TRUE)




# Refit Model

calibration_table %>%
    # filter(.model_id != 2) %>%      # Removing ARIMA model
    modeltime_refit(wti_new_time_unit) %>%
    modeltime_forecast(h = "12 months", actual_data = wti_new_time_unit) %>%
    plot_modeltime_forecast(.interactive = TRUE,
                            .plotly_slider = TRUE)

# Saving Functions ----
dump(c("set_time_unit", "plot_splits", "fit_test"), file = "scripts/utils.R")
