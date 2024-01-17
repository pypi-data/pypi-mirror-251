import pandas as pd
import scipy.stats as stats
import statsmodels.stats.multicomp as mc

data = {
    "T1": [6.21, 6.13, 5.99, 6.11],
    "T2": [8.25, 8.21, 8.14, 8.34],
    "T3": [7.89, 7.99, 8.10, 7.97],
    "T4": [6.34, 6.52, 6.14, 6.32],
    "T5": [7.89, 7.86, 7.92, 7.80],
    "T6": [7.45, 7.52, 7.47, 7.49],
    "EX": [8.5, 8.5, 8.49, 8.48]
}

B_cinerea = pd.DataFrame(data)

def cert_kruskal():
    treatment_data = B_cinerea.drop('EX', axis=1)

    kruskal_result = stats.kruskal(*[B_cinerea[EX] for EX in treatment_data])
    return kruskal_result

def compare_mulitiple(kruskal_result):
    if kruskal_result.pvalue < 0.05:
        long_df = pd.melt(B_cinerea, id_vars=['EX'], var_name='Treatment', value_name='Value')

        comp = mc.MultiComparison(long_df['Value'], long_df['Treatment'])
        posthoc_res = comp.allpairtest(stats.ranksums, method='Holm')
        return posthoc_res[0]

def main():
    kruskal_result = cert_kruskal()
    score = compare_mulitiple(kruskal_result)
    return score

if __name__ == "__main__":
    main()