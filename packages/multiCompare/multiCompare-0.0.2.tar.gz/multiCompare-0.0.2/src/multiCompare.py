import pandas as pd
import scipy.stats as stats
import statsmodels.stats.multicomp as mc

def cert_kruskal(df):
    treatment_data = df.drop('EX', axis=1)

    kruskal_result = stats.kruskal(*[df[EX] for EX in treatment_data])
    return kruskal_result

def compare_mulitiple(df, kruskal_result):
    if kruskal_result.pvalue < 0.05:
        long_df = pd.melt(df, id_vars=['EX'], var_name='Treatment', value_name='Value')

        comp = mc.MultiComparison(long_df['Value'], long_df['Treatment'])
        posthoc_res = comp.allpairtest(stats.ranksums, method='Holm')
        return posthoc_res[0]

def main():
    kruskal_result = cert_kruskal()
    score = compare_mulitiple(kruskal_result)
    return score

if __name__ == "__main__":
    main()