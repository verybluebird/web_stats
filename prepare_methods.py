import pandas as pd
import numpy as np
import streamlit as st
global df

# Removing the outliers
def removeOutliers(data, col):
    # print('data col', data[col])

    Q3 = np.quantile(data[col], 0.75)
    Q1 = np.quantile(data[col], 0.25)
    IQR = Q3 - Q1

    print("IQR value for column %s is: %s" % (col, IQR))

    global filtered_data

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data.loc[data[col] > upper_bound, col] = upper_bound
    data.loc[data[col] < lower_bound, col] = lower_bound
    filtered_data = data

#z-normalization
def normalizeDf(z_scaled):
    for column in z_scaled.columns[2:]:
        z_scaled[column] = (z_scaled[column] - z_scaled[column].mean()) / z_scaled[column].std()
    return z_scaled
#min-max normalization
def normalizeDf_1(df_min_max_scaled):
    for column in df_min_max_scaled.columns[2:]:
        df_min_max_scaled[column] = (df_min_max_scaled[column] - df_min_max_scaled[column].min()) / (
                    df_min_max_scaled[column].max() - df_min_max_scaled[column].min())
    return df_min_max_scaled


def renameCols(z_scaled):
    # Prepare for Metaboanalyst
    z_scaled.rename(columns={"Replicate": "Sample"}, inplace=True)
    z_scaled.insert(1, 'Group', z_scaled["Sample"].str.split(' '))
    z_scaled['Group'] = z_scaled['Group'].map(lambda x: x[0])
    return z_scaled


def prepareDf(df, outputFile1, outputFile2):
    # Drop N/A columns
    df = df.dropna(axis=1, how='all')

    df = df.astype(str)

    # Delete unnecessary symbols
    for col in df.columns:
        df.rename(columns={col: col.removesuffix(' Min Quantification')}, inplace=True)

    # Delete unnecessary symbols
    for molecule in df:
        # print(molecule)
        if molecule != 'Replicate':
            df[molecule] = df[molecule].str.replace(',', '.')
            df[molecule] = df[molecule].map(lambda x: x.lstrip(r"NormalizedArea: "))
            df[molecule] = df[molecule].map(lambda x: x[:9])
        else:
            df[molecule] = df[molecule].map(lambda x: x.rstrip(r" (HILIC_MRM)"))
            df[molecule] = df[molecule].map(lambda x: x.rstrip(r" (RP_MRM)"))
            df[molecule] = df[molecule].map(lambda x: x.lstrip(r"#"))
            df[molecule] = df[molecule].map(lambda x: str(x).replace(r"-", r" ("))
            df[molecule] = df[molecule].map(lambda x: x + r")")

    # print("df", df.describe())
    # Удаление QC
    df = df.loc[df["Replicate"].str[:6] != 'LP (QC']
    df = df.loc[df["Replicate"].str[:5] != 'LP (1']

    # print("df", df.describe())
    # print("df1", df1.describe())

    # Заполнение N/A медианой
    for molecule in df:
        if molecule != 'Replicate':
            # print(molecule)
            df[molecule] = df[molecule].astype(float)
            # print(df[molecule].median())
            df[molecule] = df[molecule].fillna(df[molecule].median())

    print("Shape of data after outlier removal is: ", df.shape)

    # Удаление выбросов
    for i in df.columns[1:]:
        # print(i, 'original data', df[i])
        if i == df.columns[1]:
            removeOutliers(df, i)
        else:

            # print(i, 'filtered_data', filtered_data[i])
            if filtered_data[i].size != 0:
                removeOutliers(filtered_data, i)
            else:
                print('filtered_data[', i, '] size is 0')

    # Assigning filtered data back to our original variable
    df = filtered_data
    df = df.sort_values('Replicate')
    print("Shape of data after outlier removal is: ", df.shape)

    df.to_csv(outputFile1, sep=';')
    df_initial_non_norm = df
    z_scaled = df.copy()
    z_scaled = normalizeDf(z_scaled)
    z_scaled = renameCols(z_scaled)

    # Save to file
    z_scaled.to_csv(outputFile2, sep=';', index=False)


def selectTwoGroups(df, gr1_name, gr2_name):
    df1 = df.loc[df['Group'] == gr1_name]
    df2 = df.loc[df['Group'] == gr2_name]

    df_res = pd.concat([df1, df2])
    return df_res

def prepare_df(df,perform_operations):
    for op in perform_operations:
        if op == "Drop N/A columns":
            df = df.dropna(axis=1, how='all')
            df = df.astype(str)

        if op == "Delete unnecessary symbols":
            st.write("Deleting unnecessary symbols...")
            for molecule in df:
                # print(molecule)
                if molecule != 'Replicate':
                    df[molecule] = df[molecule].str.replace(',', '.')
                    df[molecule] = df[molecule].map(lambda x: x.lstrip(r"NormalizedArea: "))
                    df[molecule] = df[molecule].map(lambda x: x[:9])
                else:
                    df[molecule] = df[molecule].map(lambda x: x.rstrip(r" (HILIC_MRM)"))
                    df[molecule] = df[molecule].map(lambda x: x.rstrip(r" (RP_MRM)"))
                    df[molecule] = df[molecule].map(lambda x: x.lstrip(r"#"))
                    df[molecule] = df[molecule].map(lambda x: str(x).replace(r"-", r" ("))
                    df[molecule] = df[molecule].map(lambda x: x + r")")
        if op == "Fill N/A with meadian":
            st.write("Filling N/A with meadian...")
            for molecule in df:
                if molecule != 'Sample' and molecule != 'Group':
                    # st.write(molecule)
                    df[molecule] = df[molecule].astype(float)
                    # st.write(df[molecule].median())
                    df[molecule] = df[molecule].fillna(df[molecule].median())
            st.write("Done")
        if op== "Remove outliers":
            st.write("Removing outliers...")
            for i in df.columns[2:]:
                # print(i, 'original data', df[i])
                if i != 'Sample' and i != 'Group':
                    df[i] = df[i].astype(float)
                    if i == df.columns[2]:
                        removeOutliers(df, i)
                    else:

                        # print(i, 'filtered_data', filtered_data[i])
                        if filtered_data[i].size != 0:
                            removeOutliers(filtered_data, i)
                        else:
                            print('filtered_data[', i, '] size is 0')
            df = filtered_data
            df = df.sort_values('Group')
            st.write("Done")
        if op == "Z-normalization":
            st.write("Performing Z-normalization...")
            z_scaled = df.copy()
            z_scaled = normalizeDf(z_scaled)
            df = z_scaled
            st.write("Done")
        if op == "1-normalization":
            st.write("Performing 1-normalization...")
            df = normalizeDf_1(df)
            st.write("Done")

    df.to_csv("df_prepared.csv", sep=';', index=True)
    output_csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download CSV', output_csv, file_name="df_prepared.csv", mime='text/csv')
    return df

