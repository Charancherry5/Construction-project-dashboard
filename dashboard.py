import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
project_data = pd.read_csv('data.csv')

# Convert 'Created' and 'Status Changed' columns to datetime
project_data['Created'] = pd.to_datetime(project_data['Created'])
project_data['Status Changed'] = pd.to_datetime(project_data['Status Changed'])

st.title("Construction Project Dashboard")

st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Select a view", (
    "Overview", "Project Progress", "Budget Status", "Schedule",
    "Resources", "Environmental Impact"
))

if option == "Overview":
    st.header("Overview of all projects")

    st.subheader("Project Status Overview")
    status_counts = project_data['Status'].value_counts()
    st.write(status_counts)

    st.subheader("Average Open Actions")
    st.write(project_data['Open Actions'].mean())

    st.subheader("Total Overdue Projects")
    st.write(len(project_data[project_data['OverDue'] > 0]))

    st.subheader("Total Projects by Type")
    type_counts = project_data['Type'].value_counts()
    st.write(type_counts)

    st.subheader("Top 5 Projects with Highest Total Actions")
    top_projects = project_data.nlargest(5, 'Total Actions')[['Ref', 'Name', 'Total Actions']]
    st.write(top_projects)

elif option == "Project Progress":
    st.header("Project Progress")
    if 'Created' in project_data and 'Status' in project_data:
        # Bar chart of project progress by status
        fig, ax = plt.subplots()
        status_counts = project_data['Status'].value_counts()
        cmap = plt.get_cmap('viridis')
        colors = [cmap(i / len(status_counts)) for i in range(len(status_counts))]
        bars = ax.bar(status_counts.index, status_counts.values, color=colors)
        ax.set_xlabel('Status')
        ax.set_ylabel('Count')
        ax.set_title('Project Progress Overview')

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')  # Rotate x-labels for better visibility
        st.pyplot(fig)

        # Line chart of project progress over time
        st.subheader("Project Progress Over Time")
        if 'Created' in project_data and 'Status' in project_data:
            fig, ax = plt.subplots()
            sns.lineplot(data=project_data, x='Created', y='Status', hue='Type', palette='Set2', ax=ax)
            ax.set_xlabel('Created Date')
            ax.set_ylabel('Status')
            ax.set_title('Project Progress Over Time by Type')
            st.pyplot(fig)

        # Pie chart of project distribution by type
        st.subheader("Project Distribution by Type")
        if 'Type' in project_data:
            type_counts = project_data['Type'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title('Project Distribution by Type')
            st.pyplot(fig)

        # Bar chart of average open actions by status
        st.subheader("Average Open Actions by Status")
        if 'Status' in project_data and 'Open Actions' in project_data:
            avg_open_actions = project_data.groupby('Status')['Open Actions'].mean()
            fig, ax = plt.subplots()
            avg_open_actions.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_xlabel('Status')
            ax.set_ylabel('Average Open Actions')
            ax.set_title('Average Open Actions by Status')
            st.pyplot(fig)

    else:
        st.write("No data available for Project Progress.")

elif option == "Budget Status":
    st.header("Budget Status")
    if 'Created' in project_data and 'Total Actions' in project_data:
        # Line chart of budget status over time
        st.subheader("Budget Status Over Time")
        fig, ax = plt.subplots()
        sns.lineplot(data=project_data, x='Created', y='Total Actions', hue='Type', palette='Set2', ax=ax)
        ax.set_xlabel('Created Date')
        ax.set_ylabel('Total Actions')
        ax.set_title('Budget Status Over Time by Type')
        st.pyplot(fig)

        # Stacked bar chart of budget status by type
        st.subheader("Budget Status by Type")
        budget_status_by_type = project_data.groupby('Type')['Total Actions'].sum()
        fig, ax = plt.subplots()
        budget_status_by_type.plot(kind='bar', stacked=True, ax=ax, color=['#FF5733', '#FFC300', '#DAF7A6'])
        ax.set_xlabel('Project Type')
        ax.set_ylabel('Total Actions')
        ax.set_title('Budget Status by Type')
        st.pyplot(fig)

        # Scatter plot of budget status and open actions
        st.subheader("Budget Status vs Open Actions")
        if 'Total Actions' in project_data and 'Open Actions' in project_data:
            fig, ax = plt.subplots()
            sns.scatterplot(data=project_data, x='Total Actions', y='Open Actions', hue='Type', palette='Set2', ax=ax)
            ax.set_xlabel('Total Actions')
            ax.set_ylabel('Open Actions')
            ax.set_title('Budget Status vs Open Actions')
            st.pyplot(fig)

    else:
        st.write("No data available for Budget Status.")

elif option == "Schedule":
    st.header("Schedule Status")
    if 'Created' in project_data and 'Status Changed' in project_data:
        # Line chart of schedule status over time
        st.subheader("Schedule Status Over Time")
        fig, ax = plt.subplots()
        sns.lineplot(data=project_data, x='Created', y='Status Changed', hue='Type', palette='Set2', ax=ax)
        ax.set_xlabel('Created Date')
        ax.set_ylabel('Status Changed')
        ax.set_title('Schedule Status Over Time by Type')
        st.pyplot(fig)

        # Box plot of schedule status by type
        st.subheader("Schedule Status by Type")
        if 'Type' in project_data and 'Status Changed' in project_data:
            fig, ax = plt.subplots()
            sns.boxplot(data=project_data, x='Type', y='Status Changed', palette='Set2', ax=ax)
            ax.set_xlabel('Project Type')
            ax.set_ylabel('Status Changed')
            ax.set_title('Schedule Status by Type')
            st.pyplot(fig)

    else:
        st.write("No data available for Schedule Status.")

elif option == "Resources":
    st.header("Resource Allocation")
    if 'Created' in project_data and 'Open Actions' in project_data:
        # Bar chart of resource allocation over time
        st.subheader("Resource Allocation Over Time")
        fig, ax = plt.subplots()
        sns.lineplot(data=project_data, x='Created', y='Open Actions', hue='Type', palette='Set2', ax=ax)
        ax.set_xlabel('Created Date')
        ax.set_ylabel('Open Actions')
        ax.set_title('Resource Allocation Over Time by Type')
        st.pyplot(fig)

        # Bar chart of total actions by type
        st.subheader("Total Actions by Type")
        if 'Total Actions' in project_data:
            total_actions_by_type = project_data.groupby('Type')['Total Actions'].sum()
            fig, ax = plt.subplots()
            total_actions_by_type.plot(kind='bar', ax=ax, color='green')
            ax.set_xlabel('Project Type')
            ax.set_ylabel('Total Actions')
            ax.set_title('Total Actions by Type')
            st.pyplot(fig)

    else:
        st.write("No data available for Resource Allocation.")

elif option == "Environmental Impact":
    st.header("Environmental Impact")
    if 'Created' in project_data and 'Comments' in project_data:
        # Histogram of environmental impact comments
        st.subheader("Environmental Impact Comments")
        fig, ax = plt.subplots()
        sns.histplot(data=project_data, x='Comments', kde=True, color='orange', bins=np.arange(0, 11, 1))
        ax.set_xlabel('Comments')
        ax.set_ylabel('Density')
        ax.set_title('Distribution of Environmental Impact Comments')
        st.pyplot(fig)

        # Box plot of environmental impact comments by type
        st.subheader("Environmental Impact Comments by Type")
        if 'Type' in project_data:
            fig, ax = plt.subplots()
            sns.boxplot(data=project_data, x='Type', y='Comments', palette='Set2', ax=ax)
            ax.set_xlabel('Project Type')
            ax.set_ylabel('Comments')
            ax.set_title('Environmental Impact Comments by Type')
            st.pyplot(fig)

    else:
        st.write("No data available for Environmental Impact.")

       
