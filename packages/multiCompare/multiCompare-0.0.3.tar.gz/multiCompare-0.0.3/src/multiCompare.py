import pandas as pd
import scipy.stats as stats
import statsmodels.stats.multicomp as mc

def kruskal(df):
    treatment_data = df.drop('EX', axis=1)

    kruskal_result = stats.kruskal(*[df[EX] for EX in treatment_data])
    return kruskal_result

def compare(df, kruskal_result):
    if kruskal_result.pvalue < 0.05:
        long_df = pd.melt(df, id_vars=['EX'], var_name='Treatment', value_name='Value')

        comp = mc.MultiComparison(long_df['Value'], long_df['Treatment'])
        posthoc_res = comp.allpairtest(stats.ranksums, method='Holm')
        return posthoc_res[0]