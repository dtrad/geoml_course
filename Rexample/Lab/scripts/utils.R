set_time_unit <-
function(data, time_unit = "month", .fun = mean) {
    
    output <- data %>%
        mutate(Date = floor_date(Date, unit = time_unit)) %>%
        
        group_by(Date) %>%
        summarize(Value = .fun(Value)) %>%
        ungroup()
    
    return(output)
}
plot_splits <-
function(data, assess = "12 month") {

    data %>% 
        tk_time_series_cv_plan() %>%
        plot_time_series_cv_plan(Date, 
                                 Value, 
                                 .interactive = T, 
                                 .title = "WTI Oil Price (USD)",
                                 .color_lab = "Year",
                                 .plotly_slider = F)
    
}
fit_test <-
function(data, growth = "linear", seasonality = "additive", changepoint.range = 1) {
    
    model_prophet <- prophet_reg(mode = "regression",
                                 growth = growth,
                                 num_changepoints = 25,
                                 season = seasonality) %>%
        set_engine("prophet", weekly.seasonality = FALSE, changepoint.range = changepoint.range) %>%
        fit(Value ~ Date, training(data))
    
    return(model_prophet)
}
