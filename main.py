import pandas as pd
from scipy import stats as st
import numpy as np
import streamlit as st
from scipy import stats as stats
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp




def color_survived(val):
    color = 'green' if val > 0.05 else 'red'
    return f'background-color: {color}'

def result(test_df):
    st.dataframe(
        test_df.style.map(lambda x: f"background-color: {'green' if x >= 0.05 else 'red'}", subset='p-value'),
        column_config={
            "_index": st.column_config.Column(width="medium"),
            "p-value": st.column_config.Column(width="small")
        },
        width='content'  # Set to True to stretch table to container width

    )

def normality(sub_df1):
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

def Shapiro(sub_df1):
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]

        if not a_df.empty:

            a = a_df.to_numpy()
            shapiro_test1 = stats.shapiro(a)
            p_val = shapiro_test1.pvalue
            global normal
            # st.write("df1 ", '\t', "is normally distributed" if p_val > 0.05 else "is not normally distributed", '\t',
            #          "p value", p_val)
            if p_val < 0.05:
                normal=1
            else:
                normal=0



    return p_val

def K_s_norm(sub_df1):
    for column in sub_df1.columns[2:]:
        a_df = sub_df1[column]

        if not a_df.empty:

            a = a_df.to_numpy()
            p_val = stats.kstest(a,stats.norm.cdf).pvalue
            global normal
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

def Kolmogorov(sub_df1, sub_df2, test_df):
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
def click_button():
    bttn=1
options_list=[]
global bttn

statistics_list_1=["Shapiro", "Kolmogorov–Smirnov test"]
statistics_list_2=["Student's t-test ", "Kolmogorov–Smirnov test", "Mann–Whitney U test", "ANOVA"]
statistics_list_3=["ANOVA", "MANOVA", "PERMANOVA"]
uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=True, type="csv"
)






for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file,sep=';')
    number_of_groups=0
    number_of_groups = st.radio(
        "Select number of groups",
        ["1", "2", "3 or more"],
        index=None
    )

    options_list = df["Group"].unique()

    if number_of_groups == "2":
        bttn = 0
        gr1 = st.selectbox(
            "Select a first group",  # Label for the widget
            options_list,  # The initial list of options
            index=None,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        gr2 = st.selectbox(
            "Select a second group",  # Label for the widget
            options_list,  # The initial list of options
            index=None,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        # st.write(options_list)
        if gr1 != None and gr2 != None:
            sub_df1 = df.loc[df["Group"] == gr1]
            sub_df2 = df.loc[df["Group"] == gr2]
            test_df = pd.DataFrame(columns=['p-value'], index=sub_df1.columns[2:])
            test = st.selectbox(
                "Select two-group statistics",  # Label for the widget
                statistics_list_2,  # The initial list of options
                index=None,  # Start with no option selected
                placeholder="Choose an option...",  # Placeholder text
                accept_new_options=False  # Enable text input
            )
            st.write(df)
            st.write(sub_df1)
            st.write(sub_df2)

            if test == "Student's t-test " and st.button("Perform test", on_click=click_button):

                st.write("Testing for normality. ")

                Shapiro(sub_df1)
                Shapiro(sub_df2)
                if normal == 0:
                    st.write("The",
                             "assumption of normality is violated. Consider non - parametric tests (e.g., Wilcoxon",
                             "signed - rank, Mann - Whitney U) or data transformation.")
                test_df = T_Test(sub_df1, sub_df2, test_df)
                result(test_df)
            elif test == "Mann–Whitney U test" and st.button("Perform test", on_click=click_button):
                test_df = Mann_Whitney(sub_df1, sub_df2, test_df)
                result(test_df)
            elif test == "Kolmogorov–Smirnov test" and st.button("Perform test", on_click=click_button):
                test_df = Kolmogorov(sub_df1, sub_df2, test_df)
                result(test_df)
    elif number_of_groups == "3 or more":
        bttn = 0
        groups = st.multiselect(
            "Select groups",
            options_list,
            max_selections=len(options_list),
            accept_new_options=False,
        )
        if len(groups) > 1:
            test = st.selectbox(
                "Select statistics",  # Label for the widget
                statistics_list_3,  # The initial list of options
                index=None,  # Start with no option selected
                placeholder="Choose an option...",  # Placeholder text
                accept_new_options=False  # Enable text input
            )
    elif number_of_groups == "1":
        bttn = 0
        gr1 = st.selectbox(
            "Select a group",  # Label for the widget
            options_list,  # The initial list of options
            index=None,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        if gr1 != None:
            sub_df1 = df.loc[df["Group"] == gr1]

            test_df = pd.DataFrame(columns=['p-value'], index=sub_df1.columns[2:])
            test = st.selectbox(
                "Select one-group statistics",  # Label for the widget
                statistics_list_1,  # The initial list of options
                index=None,  # Start with no option selected
                placeholder="Choose an option...",  # Placeholder text
                accept_new_options=False  # Enable text input
            )
            if  test == "Shapiro":
                p_val=Shapiro(sub_df1)
                normality(sub_df1)
            elif test == "Kolmogorov–Smirnov test":
                p_val=K_s_norm(sub_df1)
                normality(sub_df1)






