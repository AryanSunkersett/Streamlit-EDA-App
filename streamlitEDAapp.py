import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# streamlit run /Users/aryan/Desktop/DATA-APP/stats21discussionproject.py

st.title('Stats 21 EDA Application')

st.sidebar.title('Dataset Options')

# uploader button
st.sidebar.subheader('File Upload')
uploaded_file = st.sidebar.file_uploader("Upload a CSV")


# display rest of the application and options when a file is uploaded
if uploaded_file is not None:

    # save the file to a pandas dataframe
    df = pd.read_csv(uploaded_file)
    

    # show dataframe info
    st.subheader('Basic Info:')
    st.write('There are ' + str(len(df.columns)) + ' columns in your dataset.')
    st.write('There are ' + str(len(df.index)) + ' rows in your dataset.')
    
    # display the number of different types of variables
    datatypes = df.dtypes.value_counts() 
    for i in datatypes.index:
        st.write('The number of ', i, ' objects is ', datatypes[i])
    st.divider()


    



    # display dataframe for user to view on the main page, optional slider for displayed rows
    display_df = st.sidebar.checkbox('Preview Dataframe', key = 'disabled')
    if display_df:
        st.subheader(uploaded_file.name[0:-4] + ' Dataframe:')
        displayed_rows = st.sidebar.slider('How many rows do you want to see?', 1, len(df.index))
        st.dataframe(df.head(displayed_rows))
        st.divider()
    





    # set up column selection
    st.sidebar.divider()
    st.sidebar.subheader('Column Selection')
    col_type = st.sidebar.selectbox('Column Type', ('Numeric', 'Categorical'))



    # numeric column case + graph and five number summary
    if col_type == "Numeric":
        numeric_col = st.sidebar.selectbox('Column Name', df.select_dtypes(include = ['int64', 'float64']).columns)
        st.subheader(numeric_col + ' Info:')
        # five number summary
        df[numeric_col].describe().loc[['min', '25%', '50%', '75%', 'max']]

        st.divider()


        # histogram
        st.sidebar.divider()
        st.subheader('Histogram:')
        fig = plt.figure(figsize = (9, 7))

        # customize histogram options
        st.sidebar.subheader('Graph Options')
        hist_title = st.sidebar.text_input('Set Title', ('Histogram of ' + numeric_col))
        hist_xtitle = st.sidebar.text_input('Set X-Axis Title', numeric_col)
        hist_type = st.sidebar.selectbox('Type of histogram', ('count', 'frequency', 'density', 'probability', 'percent'))
        hist_kernel_density = st.sidebar.checkbox('Kernel Density Estimate')
        hist_bins = st.sidebar.slider('Number of Bins', min_value = 5, max_value = 100, value = 30)
        hist_color = st.sidebar.color_picker('Pick a color', '#4E99F1')
        hist_opacity = st.sidebar.slider('Bar Opacity', min_value = 0.0, max_value = 1.0, value = .5, step = .05)

        # create the histogram based on the specifications
        sns.histplot(data = df, x = numeric_col, stat = hist_type, color = hist_color, bins = hist_bins, alpha = hist_opacity, kde = hist_kernel_density)
        plt.title(hist_title)
        plt.xlabel(hist_xtitle)
        st.pyplot(fig)


        # saving the image
        filename = hist_title + '.png'
        fig.savefig(filename, dpi = 300)
        with open(filename, 'rb') as file:
            btn = st.download_button(
            label = 'Download Image',
            data = file,
            file_name = filename,
            mime = 'image/png'
            )


    # categorical column stuff and graph
    if col_type == "Categorical":
        cate_col = st.sidebar.selectbox('Select a column', df.select_dtypes(include = ['object']).columns)
        st.sidebar.divider()
        
        # make the proportion table
        st.subheader(cate_col + ' Info:')
        df[cate_col].value_counts() / len(df)
        st.divider()


        # barplot
        st.subheader('Graph:')
        fig = plt.figure(figsize = (9, 7))

        # customize barplot options
        st.sidebar.subheader('Graph Options')
        bar_y_axis = st.sidebar.selectbox('Y-Axis', df.select_dtypes(include = ['int64', 'float64']).columns)
        bar_title = st.sidebar.text_input('Set Title', ('Barplot of ' + cate_col))
        bar_xtitle = st.sidebar.text_input('Set X-Axis Title', cate_col)
        bar_ytitle = st.sidebar.text_input('Set Y-Axis Title', bar_y_axis)
        bar_opacity = st.sidebar.slider('Bar Opacity', min_value = 0.0, max_value = 1.0, value = 1.0, step = .05)
        countplot = st.sidebar.checkbox('Countplot')

        # create barplot using the specifications
        if not countplot:
            sns.barplot(data = df, x = cate_col, y = bar_y_axis, alpha = bar_opacity)
            plt.title(bar_title)
            plt.xlabel(bar_xtitle)
            plt.ylabel(bar_ytitle)
            st.pyplot(fig)
        else:
            sns.countplot(data=df, x = cate_col, alpha = bar_opacity)
            plt.title(bar_title)
            plt.xlabel(bar_xtitle)
            st.pyplot(fig)

        # saving the image
        filename = bar_title + '.png'
        fig.savefig(filename, dpi = 300)
        with open(filename, 'rb') as file:
            btn = st.download_button(
            label = 'Download Image',
            data = file,
            file_name = filename,
            mime = 'image/png'
            )



    
    # this is all commented out because for some reason streamlit's .map function was not displaying correctly
    # i checked the forums, but could not find a solution
    # this is possibly because mapbox's third party tos may have changed
    # if i find out how to fix it, make sure to reenable 'coordinates' as an option for column type


    # if col_type == "Coordinate":
    #     coor_col = st.sidebar.multiselect('Latitude and Logitude Columns', df.select_dtypes(include = ['int64', 'float64']).columns)
    #     st.sidebar.markdown('**You must put *latitude* first, and *longitude* second!**')
    #     st.sidebar.markdown('**Any non-coordinate columns will result in an error or faulty map!**')

    #     if coor_col:
    #         st.subheader('Point Map')
    #         map_df = df[[coor_col[0], coor_col[1]]].copy()
    #         map_df = map_df.dropna()
    #         st.map(map_df)
    