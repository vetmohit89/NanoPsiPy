import pandas as pd
from scipy.stats import chi2_contingency

def analyze(data):
    # Load the data
    # data = pd.read_csv('merged.csv')

    # Drop rows where control_misC is less than 0.10
    data = data[data['control_misC'] >= 0.10]

    # Filter rows where the ratio of control_C/control_T to treatment_C/treatment_T is greater than 0
    data = data[(data['control_C_reads'] / (data['control_C_reads'] + data['control_T_reads'])) - (data['treatment_C_reads'] / (data['treatment_C_reads'] + data['treatment_T_reads'])) > 0]

    # Function to calculate p-value
    def calculate_pvalue(row):
        # Create contingency table
        contingency_table = [[row['control_C_reads'], row['control_T_reads']],
                             [row['treatment_C_reads'], row['treatment_T_reads']]]

        # Perform Chi-square test with no Yates' correction
        chi2, p, dof, expected = chi2_contingency(contingency_table, correction=True)

        # Limit p-value to 6 decimal places
        p = float(format(p, '.6f'))
        return p

    # Apply the function to each row
    data['p_value'] = data.apply(calculate_pvalue, axis=1)

    # Add 'p_below_1' column
    data['p_below_1'] = data['p_value'].apply(lambda p: 'Yes' if p <= 0.01 else 'No')

    # Multiply 'control_misC' and 'treatment_misC' columns by 100
    data[['control_misC', 'treatment_misC']] *= 100

    # Save the updated data
    data.to_csv('control_vs_treatment_result.csv', index=False)

