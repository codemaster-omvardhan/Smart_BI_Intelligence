def generate_insights(growth_metrics, correlations, anomalies):

    insights = []

    # Growth insights
    for metric, months in growth_metrics.items():

        for month, growth in months.items():

            if growth is None:
                continue

            if growth > 15:
                insights.append(
                    f"{metric} increased by {growth}% compared to the previous month."
                )

            elif growth < -15:
                insights.append(
                    f"{metric} decreased by {abs(growth)}% compared to the previous month."
                )

    # Correlation insights
    for corr in correlations:

        if abs(corr["correlation"]) > 0.75:

            insights.append(
                f"A strong correlation exists between {corr['metric_1']} and {corr['metric_2']} (r={corr['correlation']})."
            )

    # Anomaly insights
    for metric, points in anomalies.items():

        if len(points) > 0:

            insights.append(
                f"An unusual spike or drop was detected in {metric}."
            )

    return insights