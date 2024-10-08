#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing neccesary libaries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


# Load the dataset
df = pd.read_csv(r"E:\Users\user\Downloads\marketing\ifood_df.csv")

# Display the first few rows of the dataset
df.head()


# In[4]:


#checking for missing values
df.info


# In[5]:


df.isnull().sum()


# ### Getting rid of duplicate

# In[6]:


df.duplicated().sum()      #checking for duplicate values....


# In[7]:


df.drop_duplicates(inplace=True)
df.shape


# In[8]:


df.dtypes


# In[10]:


# Save the cleaned dataset
df.to_csv(r"E:\Users\user\Downloads\marketing\cleaned_ifood_df.csv", index=False)


# In[11]:


# Basic Statistics
print(df.describe(include='all'))

# Campaign Performance Analysis
plt.figure(figsize=(16, 12))


# In[13]:


# Plot Spending Distribution
plt.figure(figsize=(12, 8))
sns.histplot(df['MntTotal'], kde=True, color='blue')
plt.title('Distribution of Total Spending')
plt.xlabel('Total Spending')
plt.ylabel('Frequency')
plt.savefig(r"E:\Users\user\Downloads\marketing\total_spending_distribution.png")
plt.show()


# In[22]:


# Spending by Category
plt.figure(figsize=(12, 8))
spending_long = df[['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].melt(var_name='Product', value_name='Spending')
sns.histplot(x='Product', y='Spending', data=spending_long, bins=30)
plt.xticks(rotation=45)
plt.title('Spending by Product Category')
plt.savefig(r"E:\Users\user\Downloads\marketing\spending_by_category.png")
plt.show()



# In[24]:


# Income Distribution
plt.figure(figsize=(12, 8))
sns.histplot(df['Income'], kde=True, color='green')
plt.xlabel('Income')
plt.ylabel('Frequency')
plt.title('Income Distribution')
plt.savefig(r"E:\Users\user\Downloads\marketing\income_distribution.png")
plt.show()


# In[25]:


# Campaign Acceptance Distribution
plt.figure(figsize=(12, 8))
sns.histplot(df['AcceptedCmpOverall'], kde=True, color='red')
plt.xlabel('Accepted Campaigns')
plt.ylabel('Frequency')
plt.title('Campaign Acceptance Distribution')
plt.savefig(r"E:\Users\user\Downloads\marketing\campaign_acceptance_distribution.png")
plt.show()


# # Demographic Analysis

# In[26]:


plt.figure(figsize=(16, 12))

# Total Number of Kids
age_columns = ['Kidhome', 'Teenhome']
df['TotalKids'] = df[age_columns].sum(axis=1)

plt.subplot(2, 2, 1)
sns.histplot(df['TotalKids'], kde=True, color='purple')
plt.xlabel('Total Number of Kids')
plt.ylabel('Frequency')
plt.title('Distribution of Number of Kids')
plt.savefig(r"E:\Users\user\Downloads\marketing\total_kids_distribution.png")
plt.show()


# # Marital Status Analysis

# In[27]:


# Marital Status Analysis
marital_columns = ['marital_Together', 'marital_Widow']
marital_long = df[marital_columns].melt(var_name='MaritalStatus', value_name='Count')

plt.figure(figsize=(12, 8))
sns.barplot(x='MaritalStatus', y='Count', data=marital_long)
plt.title('Marital Status Distribution')
plt.savefig(r"E:\Users\user\Downloads\marketing\marital_status_distribution.png")
plt.show()


# In[28]:


# Education Level Analysis
education_columns = ['education_2n Cycle', 'education_Basic', 'education_Graduation', 'education_Master', 'education_PhD']
education_long = df[education_columns].melt(var_name='Education', value_name='Count')

plt.figure(figsize=(12, 8))
sns.barplot(x='Education', y='Count', data=education_long)
plt.title('Education Level Distribution')
plt.savefig(r"E:\Users\user\Downloads\marketing\education_level_distribution.png")
plt.show()


# # Correlation Analysis

# In[32]:


# List of spending columns
spending_columns = [
    'MntWines', 
    'MntFruits', 
    'MntMeatProducts', 
    'MntFishProducts', 
    'MntSweetProducts', 
    'MntGoldProds', 
    'MntTotal',  # Including MntTotal as per your column list
    'Income', 
    'AcceptedCmpOverall'
]

# Create a correlation matrix with the specified columns
plt.figure(figsize=(12, 10))
correlation_matrix = df[spending_columns].corr()  # Ensure all columns are present in df
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.savefig(r"E:\Users\user\Downloads\marketing\correlation_matrix.png")
plt.show()


# In[34]:


plt.figure(figsize=(12, 8))

# Create the scatter plot
scatter_plot = sns.scatterplot(x='MntTotal', y='AcceptedCmpOverall', hue='AcceptedCmpOverall', palette='viridis', data=df)

# Set labels and title
plt.xlabel('Total Spending (MntTotal)')
plt.ylabel('Accepted Campaigns')
plt.title('Total Spending vs Campaign Acceptance')

# Save the plot
plt.savefig(r"E:\Users\user\Downloads\marketing\total_spending_vs_campaign_acceptance.png")

# Adjusting the legend
handles, labels = scatter_plot.get_legend_handles_labels()
scatter_plot.legend(handles=handles, labels=labels, title='Accepted Campaigns', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.show()


# In[36]:


# Create Spending Segments based on MntTotal
df['SpendingSegment'] = pd.cut(
    df['MntTotal'],  # Use MntTotal instead of TotalSpending
    bins=[0, 100, 500, 1000, 2000, df['MntTotal'].max()],
    labels=['Low', 'Medium', 'High', 'Very High', 'Extremely High']
)

# Plot Spending Segments
plt.figure(figsize=(12, 8))
spending_segment_counts = df['SpendingSegment'].value_counts()
plt.pie(spending_segment_counts, labels=spending_segment_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
plt.title('Customer Segmentation by Total Spending (MntTotal)')
plt.savefig(r"E:\Users\user\Downloads\marketing\customer_segmentation_by_spending.png")
plt.show()


# In[37]:


# Create Acceptance Segments
df['AcceptanceSegment'] = pd.cut(df['AcceptedCmpOverall'], bins=[-1, 1, 2, 3, 4, 5], labels=['0', '1', '2', '3', '4+'])

# Plot Acceptance Segments
plt.figure(figsize=(12, 8))
acceptance_segment_counts = df['AcceptanceSegment'].value_counts()
plt.bar(acceptance_segment_counts.index, acceptance_segment_counts.values, color='purple')
plt.title('Customer Segmentation by Campaign Acceptance')
plt.xlabel('Number of Accepted Campaigns')
plt.ylabel('Number of Customers')
plt.savefig(r":\Users\user\Downloads\marketing\customer_segmentation_by_acceptance.png")
plt.show()


# In[ ]:




