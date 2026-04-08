from scipy import stats as stats
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp
import streamlit as st
import streamlit.components.v1 as components
from interface import *


def stat_significant(test_df):
    t= test_df.loc[test_df['p-value'] <0.05]
    print ("t", t.index.values)
    return t.index.values

def perform_test(test, sub_df1,sub_df2,normal, test_df):
    if test == "Student's t-test ":

        st.markdown("*Performing Student's t-test.*")
        st.markdown("*Testing for normality.*")

        Shapiro(sub_df1, normal)
        Shapiro(sub_df2, normal)
        if normal == 0:
            st.write("The",
                     "assumption of normality is violated. Consider non - parametric tests (e.g., Wilcoxon",
                     "signed - rank, Mann - Whitney U) or data transformation.")
        test_df = T_Test(sub_df1, sub_df2, test_df)
        result(test_df)
        t1= ("Student's t-test ",stat_significant(test_df))
        print("t1",t1)
        return t1
    elif test == "Mann–Whitney U test":
        st.markdown("*Performing Mann–Whitney U test.*")
        test_df = Mann_Whitney(sub_df1, sub_df2, test_df)
        result(test_df)
        return ("Mann–Whitney U test",stat_significant(test_df))
    elif test == "Kolmogorov–Smirnov test":
        st.markdown("*Performing Kolmogorov–Smirnov test.*")
        test_df = Kolmogorov(sub_df1, sub_df2, test_df, normal)
        result(test_df)
        return ("Kolmogorov–Smirnov test",stat_significant(test_df))


def normality(sub_df1, normal):
    st.write("Testing for normality. ")

    if normal == 0:
        st.write("The",
                 "assumption of normality is violated. Consider non - parametric tests (e.g., Wilcoxon",
                 "signed - rank, Mann - Whitney U) or data transformation.")
    else:
        st.write("Data is normally distributed. ")

    st.write(sub_df1)




def T_Test(sub_df1, sub_df2, test_df):

    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]
        b_df = sub_df2[column]
        if not b_df.empty:
            a = a_df.to_numpy()
            b = b_df.to_numpy()
            p_val = stats.ttest_ind(a=a, b=b, equal_var=True).pvalue
            # st.write(column, '\t', "equal" if p_val > 0.05 else "not equal", '\t', p_val)
            test_df.loc[column] = p_val
    return test_df

def  Mann_Whitney_U(sub_df1, sub_df2, test_df):
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]
        b_df = sub_df2[column]
        if not b_df.empty:
            a = a_df.to_numpy()
            b = b_df.to_numpy()
            p_val = mannwhitneyu(a, b, method="exact").pvalue
            test_df.loc[column] = p_val
    return test_df

def Shapiro(sub_df1, normal):
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]

        if not a_df.empty:

            a = a_df.to_numpy()
            shapiro_test1 = stats.shapiro(a)
            p_val = shapiro_test1.pvalue


            if p_val < 0.05:
                normal=1
            else:
                normal=0



    return p_val

def K_s_norm(sub_df1, normal):
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]

        if not a_df.empty:

            a = a_df.to_numpy()
            p_val = stats.kstest(a,stats.norm.cdf).pvalue

            # st.write("df1 ", '\t', "is normally distributed" if p_val > 0.05 else "is not normally distributed", '\t',
            #          "p value", p_val)
            if p_val < 0.05:
                normal=1
            else:
                normal=0



    return p_val

def Mann_Whitney(sub_df1, sub_df2, test_df):
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]
        b_df = sub_df2[column]
        if not b_df.empty:
            a = a_df.to_numpy()
            b = b_df.to_numpy()
            _, p_val = mannwhitneyu(a, b, method="exact")
            # st.write(column, '\t', "equal" if p_val > 0.05 else "not equal", '\t', p_val)
            test_df.loc[column] = p_val
    return test_df
def Kolmogorov_normality(a):
    return stats.kstest(a,stats.norm.cdf).pvalue

def Kolmogorov(sub_df1, sub_df2, test_df, normal):
    normal = 1
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]
        b_df = sub_df2[column]
        if not b_df.empty:
            a = a_df.to_numpy()
            b = b_df.to_numpy()

            if Kolmogorov_normality(a) <0.05 or Kolmogorov_normality(b) <0.05:
                normal=0
            stats.kstest(b,stats.norm.cdf)
            p_val = ks_2samp(a, b).pvalue
            # st.write(column, '\t', "equal" if p_val > 0.05 else "not equal", '\t', p_val)
            test_df.loc[column] = p_val
    if normal == 0:
        st.write("The",
                 "assumption of normality is violated.")
    return test_df