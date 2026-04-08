from matplotlib_venn import venn3_unweighted
from matplotlib_venn import venn2_unweighted
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st

def venn(significant_metabolites):
    if len(significant_metabolites)==1:
        return 0
    # st.session_state.step = 3
    # print("significant_metabolites",significant_metabolites)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    # plt.figure(figsize=(4, 4))
    test_names = (x[0] for x in significant_metabolites)
    metabs = [set(x[1]) for x in significant_metabolites]
    if len(significant_metabolites)==2:
        venn = venn2_unweighted(metabs, test_names)
    elif len(significant_metabolites)==3:
        venn = venn3_unweighted(metabs, test_names)

    plt.title("Sample Venn diagram")
    st.pyplot(fig)
    plt.savefig("Venn.svg", format="svg")