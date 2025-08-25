import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_taxi_data():
    """
    Main function to load, process, and analyze local NYC taxi data.
    """
    # --- 1. Define File Paths ---
    # Dynamically find all .parquet files in the 'data' directory.
    data_folder = 'data'
    if not os.path.isdir(data_folder):
        print(f"Error: Directory not found at '{data_folder}'")
        print("Please create the 'data' directory and place your Parquet files inside.")
        return

    file_paths = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.parquet')]

    if not file_paths:
        print(f"Error: No Parquet files (.parquet) found in the '{data_folder}' directory.")
        return

    # --- 2. Load and Combine Data ---
    print("Loading and combining data from the following files:")
    for fp in file_paths:
        print(f" - {fp}")
    
    df = pd.concat([pd.read_parquet(fp) for fp in file_paths], ignore_index=True)

    # --- FIX: Standardize column names to lowercase ---
    df.columns = df.columns.str.lower()
    
    # --- 3. Data Cleaning and Preparation ---
    print("\nCleaning and preparing data...")
    # Convert to datetime objects
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # Calculate trip duration in minutes
    df['trip_duration_minutes'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60

    # Filter out invalid data points
    # - Positive duration, distance, and fare amount
    # - Realistic trip durations (e.g., > 1 minute and < 24 hours)
    # - Standard RateCodeIDs (1-6)
    initial_rows = len(df)
    # Use the new lowercase column name 'ratecodeid'
    df = df[
        (df['trip_duration_minutes'] > 1) &
        (df['trip_duration_minutes'] < 1440) &
        (df['trip_distance'] > 0) &
        (df['total_amount'] > 0) &
        (df['ratecodeid'].isin(range(1, 7)))
    ]
    print(f"Filtered out {initial_rows - len(df)} invalid rows.")

    # --- 4. Define and Calculate Unit-Economic Metrics ---
    print("Calculating unit-economic metrics...")
    # Metric 1: Cost per Minute (Primary)
    df['cost_per_minute'] = df['total_amount'] / df['trip_duration_minutes']

    # Metric 2: Cost per Mile (Secondary)
    df['cost_per_mile'] = df['total_amount'] / df['trip_distance']
    
    # Remove infinite values that might arise from edge cases
    df.replace([float('inf'), -float('inf')], pd.NA, inplace=True)
    df.dropna(subset=['cost_per_minute', 'cost_per_mile'], inplace=True)

    # --- 5. Analyze Metric by Rate Code ---
    print("Analyzing metrics by RateCodeID...")
    
    # Map RateCodeID to human-readable names
    rate_code_map = {
        1: 'Standard',
        2: 'JFK',
        3: 'Newark',
        4: 'Nassau/Westchester',
        5: 'Negotiated',
        6: 'Group Ride'
    }
    # Use the new lowercase column name 'ratecodeid'
    df['ratecodename'] = df['ratecodeid'].map(rate_code_map)

    # Generate a statistical summary table
    summary_table = df.groupby('ratecodename')['cost_per_minute'].describe()
    print("\n--- Summary: Cost per Minute by Rate Code ---")
    print(summary_table)

    # --- 6. Visualize the Results ---
    print("\nGenerating visualization...")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.boxplot(
        x='ratecodename',
        y='cost_per_minute',
        data=df,
        ax=ax,
        order=rate_code_map.values() # Ensure consistent order
    )
    
    # To make the plot readable, we'll limit the y-axis to a reasonable range
    # based on the data quantiles to exclude extreme outliers from the view.
    ax.set_ylim(0, df['cost_per_minute'].quantile(0.95))
    
    ax.set_title('Distribution of Cost per Minute by NYC Taxi Rate Code', fontsize=16)
    ax.set_xlabel('Rate Code', fontsize=12)
    ax.set_ylabel('Cost per Minute ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Save the figure
    output_path = 'cost_per_minute_by_rate_code.png'
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"\nChart saved to {output_path}")

if __name__ == '__main__':
    analyze_taxi_data()
