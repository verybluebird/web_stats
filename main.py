import pandas as pd

import matplotlib.pyplot as plt
import streamlit as st
from scipy import stats as stats
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp


from pca import *


def draw_pca(df,features):
    # if st.button("Draw PCA"):

        features=features.tolist()

        pca(df,features)


def box_plot(chosen_molecule, data, labels):
    plt.rcParams['font.size'] = 11
    plt.rcParams.update({'mathtext.default': 'regular'})

    fig, ax = plt.subplots(figsize=(5.5, 4))
    # print(labels)
    mol_data=data
    # hardness = ax.boxplot(data, tick_labels=labels[0], sym="", widths=0.4, medianprops={'alpha': 1})
    for i in range(len(data)):
        # st.write(data[i])
        mol_data[i] = mol_data[i][chosen_molecule]


    plt.boxplot(mol_data, labels=labels)
    ax.set_ylabel(chosen_molecule)
    st.pyplot(fig)
    # if st.button("Save figure"):
    path = str(chosen_molecule)+"_"+str(labels)+".svg"
    fig.savefig(path, bbox_inches="tight")
        # st.write("Your figure has been saved to ",path)




def draw_box_plot(test_df, sub_df1, sub_df2,labels):
    molecules = st.selectbox(
        "Select a molecule for box plot",  # Label for the widget
        test_df.index,  # The initial list of options
        index=None,  # Start with no option selected
        placeholder="Choose an option...",  # Placeholder text
        accept_new_options=False  # Enable text input
    )

    # molecules = st.multiselect(
    #     "Select molecules for box plot",
    #     test_df.index,
    #     max_selections=len(test_df.index),
    #     accept_new_options=False,
    # )
    # if len(molecules) > 0:
    if molecules != None:
        data=[sub_df1, sub_df2]
        if st.button("Draw boxplot"):
            # for molecule in molecules:
            box_plot(molecules, data, labels)


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
        index=1
    )


    options_list = df["Group"].unique()
    print(options_list)
    if number_of_groups is None:
        st.write()
    elif number_of_groups == "2":
        bttn = 0
        gr1 = st.selectbox(
            "Select a first group",  # Label for the widget
            options_list,  # The initial list of options
            index=1,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        gr2 = st.selectbox(
            "Select a second group",  # Label for the widget
            options_list,  # The initial list of options
            index=2,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        # st.write(options_list)
        if gr1 != None and gr2 != None:
            labels = [gr1, gr2]
            sub_df1 = df.loc[df["Group"] == gr1]
            sub_df2 = df.loc[df["Group"] == gr2]
            test_df = pd.DataFrame(columns=['p-value'], index=sub_df1.columns[2:])
            if st.button("Show dataframes"):
                st.write("Initial dataframe:")
                st.write(df)
                st.write("Dataframe, group", gr1)
                st.write(sub_df1)
                st.write("Dataframe, group", gr2)
                st.write(sub_df2)
            test = st.selectbox(
                "Select two-group statistics",  # Label for the widget
                statistics_list_2,  # The initial list of options
                index=None,  # Start with no option selected
                placeholder="Choose an option...",  # Placeholder text
                accept_new_options=False  # Enable text input
            )


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



            draw_box_plot(test_df, sub_df1, sub_df2, labels)
            draw_pca(df, test_df.index)
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






