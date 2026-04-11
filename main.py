import matplotlib.pyplot as plt
import streamlit as st


from tests import *
from pca import *
from box_plots import *
from interface import *
from venn import *
from prepare_methods import *

options_list=[]
global bttn

statistics_list_1=["Shapiro", "Kolmogorov–Smirnov test"]
statistics_list_2=["Student's t-test ", "Kolmogorov–Smirnov test", "Mann–Whitney U test", "ANOVA"]
statistics_list_3=["ANOVA", "MANOVA", "PERMANOVA"]
uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=True, type="csv"
)

if 'normal' not in st.session_state:
    st.session_state.normal = 0



for uploaded_file in uploaded_files:
    # global normal
    # normal=0
    # global df
    df = pd.read_csv(uploaded_file,sep=';')
    if 'df' not in st.session_state:
        st.session_state.df = df
    if st.button("Load dataframe"):
        st.session_state.df = df
    number_of_groups = 0


    operations = ["Drop N/A columns",  "Fill N/A with median", "Remove outliers", "Z-normalization", "1-normalization"]
    perform_operations = st.multiselect(
        "Select operations",
        operations,
        max_selections=len(operations),
        accept_new_options=False,
        default = operations[:2]
    )
    if len(perform_operations) > 0:
        if st.button("Prepare dataframe"):
            st.session_state.df = prepare_df(st.session_state.df, perform_operations)
            st.write(st.session_state.df)
    if st.button("Show initial dataframe"):
        st.write(df)



    number_of_groups = st.radio(
        "Select number of groups",
        ["1", "2", "3 or more"],
        index=None
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
            index=0,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        gr2 = st.selectbox(
            "Select a second group",  # Label for the widget
            options_list,  # The initial list of options
            index=1,  # Start with no option selected
            placeholder="Choose an option...",  # Placeholder text
            accept_new_options=False  # Enable text input
        )
        # st.write(options_list)
        if gr1 != None and gr2 != None:
            labels = [gr1, gr2]
            sub_df1 = st.session_state.df.loc[st.session_state.df["Group"] == gr1]
            sub_df2 = st.session_state.df.loc[st.session_state.df["Group"] == gr2]
            test_df = pd.DataFrame(columns=['p-value'], index=sub_df1.columns[2:])
            if st.button("Show dataframes"):
                st.write("Full dataframe:")
                st.write(st.session_state.df)
                st.write("Dataframe, group", gr1)
                st.write(sub_df1)
                st.write("Dataframe, group", gr2)
                st.write(sub_df2)

            tests = st.multiselect(
                "Select two-group statistics",
                statistics_list_2,
                max_selections=len(statistics_list_2),
                accept_new_options=False,
                key="statistics"
            )

            if 'significant_metabolites' not in st.session_state:
                st.session_state.significant_metabolites = []

            # st.session_state.setdefault("step", 1)


            if st.button('Perform test', on_click=yes_callback):
                st.session_state.significant_metabolites = []
                for test in tests:
                    pair = perform_test(test,sub_df1,sub_df2,st.session_state.normal, test_df)
                    st.session_state.significant_metabolites.append(pair)
                    line(5)
            # if st.session_state.step == 2:
                venn(st.session_state.significant_metabolites)


            line(10)
            draw_box_plot(test_df, sub_df1, sub_df2, labels)

            if number_of_groups!="1" and len(sub_df1.columns[2:])>1:
                line(10)
                draw_pca(st.session_state.df, test_df.index)

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
        sub_dfs = []
        for label in groups:
            sub_dfs.append(st.session_state.df.loc[st.session_state.df["Group"] == label])

        line(10)
        test_df = pd.DataFrame(columns=['p-value'], index=st.session_state.df.columns[2:])
        draw_box_plot_3more(sub_dfs,test_df, groups)
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
            sub_df1 = st.session_state.df.loc[st.session_state.df["Group"] == gr1]
            if st.button("Show dataframe"):
                st.write("Dataframe:")
                st.write(sub_df1)
            test_df = pd.DataFrame(columns=['p-value'], index=sub_df1.columns[2:])

            test = st.selectbox(
                "Select one-group statistics",  # Label for the widget
                statistics_list_1,  # The initial list of options
                index=None,  # Start with no option selected
                placeholder="Choose an option...",  # Placeholder text
                accept_new_options=False  # Enable text input
            )
            if  test == "Shapiro":
                p_val, normal = Shapiro(sub_df1)
                normality(sub_df1,normal)
            elif test == "Kolmogorov–Smirnov test":
                p_val, normal=K_s_norm(sub_df1)
                normality(sub_df1,normal)






