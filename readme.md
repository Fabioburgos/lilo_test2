# NYC Taxi Trip Analysis: Unit Economics

## Project Overview

This project analyzes the unit economics of New York City taxi trips using publicly available data. The goal is to develop a metric that accurately reflects the true cost and revenue dynamics of a taxi ride, going beyond simple fare calculations. The script processes raw trip data, calculates a key performance metric, and visualizes how this metric varies across different fare types (Rate Codes).

## How to Run

1.  **Prerequisites**: Make sure you have Python 3 and the following libraries installed:
    ```bash
    pip install pandas matplotlib seaborn pyarrow
    ```

2.  **Project Structure**: Create a folder named `data` in the same directory as the script and place all your NYC Taxi `.parquet` files inside it.

    ```
    .
    ├── data/
    │   ├── yellow_tripdata_2024-01.parquet
    │   └── yellow_tripdata_2024-02.parquet
    │   └── ... (any other parquet files)
    └── analyze_taxi_data.py  (or your script name)
    ```

3.  **Execute**: Run the script from your terminal. It will automatically find and process all Parquet files within the `data` folder.
    ```bash
    python analyze_taxi_data.py
    ```

4.  **Output**: The script will:
    * Print a statistical summary table to the console.
    * Save a boxplot chart named `cost_per_minute_by_rate_code.png` to the project directory.

## Analysis and Methodology

The chosen approach for this analysis is to define a primary unit-economic metric: **Cost per Minute**. This metric is calculated by dividing the `total_amount` of a trip by its total duration in minutes. This provides a standardized way to measure the revenue generated for every minute a taxi is occupied. After calculating this metric for all valid trips, the data is grouped by the trip's Rate Code (e.g., Standard, JFK, Newark) to compare their performance. The results are presented in both a summary table and a boxplot to clearly visualize the distribution and central tendency of the Cost per Minute for each fare type.

The **Cost per Minute** approach is effective because it provides a standardized measure of revenue efficiency that accounts for the time-based nature of taxi service, especially in a dense city with variable traffic. Its main advantage is its robustness compared to a "cost per mile" metric, which can be misleading for trips with low distance but long duration due to traffic. A limitation is that this metric is based on revenue (`total_amount`) and does not factor in operational costs (fuel, maintenance, insurance) or driver idle time between fares. For the next iteration, I would propose integrating these cost factors to develop a **Net Profit per Hour** metric. This would provide a far more comprehensive view of true profitability by analyzing not just revenue, but the complete economic picture of taxi operations.