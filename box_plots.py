import matplotlib.pyplot as plt
import streamlit as st

from datetime import datetime

def box_plot(chosen_molecule, data, labels):
    plt.rcParams['font.size'] = 11
    plt.rcParams.update({'mathtext.default': 'regular'})

    fig, ax = plt.subplots(figsize=(2.5, 4))
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
    now = datetime.now()  # current date and time
    date_time = now.strftime("_%m_%d_%Y_%H_%M_%S")
    path = str(chosen_molecule)+"_"+str(labels)+date_time+".svg"
    out_fig=fig.savefig(path, bbox_inches="tight",format="svg")
    # st.download_button('Download SVG', out_fig, file_name=path , mime='image/svg+xml')
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

def draw_box_plot_3more(sub_dfs,test_df, groups):
    molecules = st.selectbox(
        "Select a molecule for box plot",  # Label for the widget
        test_df.index,  # The initial list of options
        index=None,  # Start with no option selected
        placeholder="Choose an option...",  # Placeholder text
        accept_new_options=False  # Enable text input
    )

    if molecules != None:
        data = sub_dfs
        if st.button("Draw boxplot"):
            # for molecule in molecules:
            box_plot(molecules, data, groups)