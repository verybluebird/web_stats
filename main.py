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




for uploaded_file in uploaded_files:
    global normal
    normal=0
    global df
    df = pd.read_csv(uploaded_file,sep=';')
    number_of_groups=0


    operations = ["Drop N/A columns",  "Fill N/A with meadian", "Remove outliers", "Z-normalization", "1-normalization"]
    perform_operations = st.multiselect(
        "Select groups",
        operations,
        max_selections=len(operations),
        accept_new_options=False,
        default = operations
    )
    if len(perform_operations) >0:
        if st.button("Prepare dataframe"):
            df = prepare_df(df, perform_operations)
            st.write(df)
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

            tests = st.multiselect(
                "Select two-group statistics",
                statistics_list_2,
                max_selections=len(statistics_list_2),
                accept_new_options=False,
                key="statistics"
            )
            global significant_metabolites
            significant_metabolites=[]

            # st.session_state.setdefault("step", 1)


            if st.button('Perform test', on_click=yes_callback):

                for test in tests:
                    pair = perform_test(test,sub_df1,sub_df2,normal, test_df)
                    significant_metabolites.append(pair)
                    line(5)
            # if st.session_state.step == 2:
                venn(significant_metabolites)


            line(10)
            draw_box_plot(test_df, sub_df1, sub_df2, labels)
            line(10)
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
                p_val=Shapiro(sub_df1, normal)
                normality(sub_df1, normal)
            elif test == "Kolmogorov–Smirnov test":
                p_val=K_s_norm(sub_df1, normal)
                normality(sub_df1, normal)






