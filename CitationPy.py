# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

#Add Dependencies
# %matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import pprint
from citipy import citipy
import gmaps
import gmaps.datasets
import scipy.stats as stats
from datetime import datetime
#import folium

# ## Importing CSV Data
#
#

#Import citation data from csv
citation_raw = pd.read_csv("Parking_Citations.csv")
citation_df = citation_raw


# +
#Name of columns 
#citation_df.columns.tolist()
# -

# ## Cleaning Columns from Dataset

# +
#Drop columns that are not needed
citation_df1 = citation_df.drop(["Meter Id","Marked Time","RP State Plate","Plate Expiry Date","VIN","Location","Route","Agency","Violation code","Body Style", "Violation Description", "Fine amount"], axis = 1)
citation_df1.head()

#Drop Lat and Lon = 99999
citation_df2 = citation_df1[(citation_df1["Latitude"] !=99999.000) & (citation_df1["Longitude"] !=99999.000)]
citation_df2.head()

# -

citation_df2.count()

#Take all rows where column values are not equal to zero
citation_df3 = citation_df2[(citation_df2[["Ticket number", "Issue Date","Issue time","Make","Color","Latitude","Longitude",]] != 0)]
citation_df3.head()


#Drop all rows with blank cells
citation_df4 = citation_df3.fillna("")


# +
#citation_df4.count()
# -

citation_df4["Make"].replace("", np.nan, inplace=True)
citation_df4.dropna(subset = ["Make"], inplace = True)

# +
#Sort values by make of car
#citation_df4.sort_values(["Make"],ascending=True)
# -


Sample_data = citation_df4.sample(frac=0.10, random_state = 1 )

Sample_data.head()

#Replace duplicates for all makes in top 30
citation_df4["Make"] = citation_df4["Make"].replace({'TOYT': 'TOYOTA', 'TOYO': 'TOYOTA'})
citation_df5 = citation_df4["Make"].value_counts()
citation_df6 = citation_df5.rename_axis('Make').reset_index(name='counts')
citation_df7 = citation_df6.head(25)


citation_df7.head()

# bar_order = citation_df7.sort_values("counts")


# +
#Bar plot for top 25 make of vehicles that got citations
fig = plt.gcf()
fig.set_size_inches(9.5, 10.5)
y_axis=np.arange(len(citation_df7["Make"]))
citation_df7.sort_values('counts',inplace=True)
plt.barh(y_axis,citation_df7["counts"], color="darkcyan", align="center",
         edgecolor="none",)

#Set labels
plt.ylabel('Make', fontsize=12, labelpad=15, weight="bold")
plt.xlabel('Counts', fontsize=12, labelpad=5, weight="bold")

#Edit ticks
plt.tick_params(axis="both", which="both", bottom="False", top="False", labelbottom="False", left="False", right="False", labelleft="True")
plt.yticks(y_axis, citation_df7["Make"], fontsize=9, rotation=360,)
plt.xticks(fontsize=10)

# get rid of the frame
for spine in plt.gca().spines.values():
    spine.set_visible(False)


plt.title('Top 25 Citations by Make of Cars ', fontsize=15)
fig.savefig("make_chart.png")
plt.show()
plt.clf()
plt.show()
# -

#Replace duplicates for all makes in top 30
citation_df8 = citation_df4["Color"].value_counts()
citation_df9 = citation_df8.rename_axis('Color').reset_index(name='Counts')
citation_df10 = citation_df9.head(10)


# +
#Bar plot for top 25 Color of vehicles that got citations
fig = plt.gcf()
fig.set_size_inches(15.5, 5.5)
x_axis=np.arange(len(citation_df10["Color"]))
plt.bar(x_axis,citation_df10["Counts"], color=('whitesmoke','black',"grey","silver","royalblue","red","green","rosybrown","maroon","gold","red","tan"))

#Set labels
plt.xlabel('Color', fontsize=18, labelpad=5, weight="bold")
plt.ylabel('Counts', fontsize=18, labelpad=5, weight="bold")

#Edit ticks
plt.xticks(x_axis, citation_df10["Color"], fontsize=12, rotation="horizontal")
plt.title('Top 10 Citations by Color of Cars', fontsize=18)

#plt.figure(figsize=(18,16))
plt.grid( which="major",linestyle="dotted", color="lemonchiffon")
plt.rcParams['axes.facecolor'] = 'burlywood'
fig.savefig("color_chart.png")

plt.show()
plt.clf()

# -

plt.clf()

# Sampling the models of four cars 
df1 = Sample_data[Sample_data.Make.isin(["BMW","FORD","VOLK","DODG"])]
df1.head()

# Group by make of the cars
df2 = df1.groupby("Make").Make.count()

Sample_data_large = citation_df4.sample(frac=0.50, random_state = 1 )

df3 = Sample_data_large[Sample_data_large.Make.isin(["BMW","FORD","VOLK","DODG"])]
df3.info()

df3 = df3.groupby("Make").Make.count()
df3

Observed = df2
Observed

Observed = pd.DataFrame(Observed)
Observed

Observed.columns.values[0]="Observed"
Observed

overall_ratio = (df3/len(df3)).round(0)
overall_ratio

Expected = overall_ratio * len(Observed)
Expected

Expected= pd.DataFrame(Expected)

Expected.columns.values[0] = "Expected"
Expected

Combined =  pd.concat([Observed, Expected], axis = 1)
Combined

#With four raws, the degree of freedom is 3
# with a p-value of 0.05, the CL is 1-0.05 = 0.95
Critcal_value = stats.chi2.ppf(q=0.95, df = 3)
Critcal_value

stats.chisquare(Combined["Observed"], Combined["Expected"])

# # DMV Data
#
#

#Import citation data from csv
dmv_raw = pd.read_csv("VehicleCount_070118.csv")
dmv_df = dmv_raw


# +
#Take needed columns only
dmv_df1=dmv_df[["Make", "Vehicles"]]

#Get total number of vehicles for each make
dmv_df2=dmv_df1.groupby(["Make"]).sum()

#Sort for top 25
dmv_df2 = dmv_df2.sort_values(["Vehicles"], ascending=False)

#Get top 25
dmv_df3 = dmv_df2.head(25).reset_index()
dmv_df3


# -

#Rename makes to tie DMV data to citation data
dmv_df3["Make"]=dmv_df3["Make"].replace({'HONDA': 'HOND', 'CHEVROLET': 'CHEV', 'NISSAN': 'NISS','DODGE': 'DODG',
                                 'MERCEDES-BENZ': 'MERZ','LEXUS': 'LEXS','MAZDA': 'MAZD','HYUNDAI': 'HYUN',
                                'SUBARU': 'SUBA','ACURA': 'ACUR','INFINITI': 'INFI',
                                'OTHER/UNK': 'OTHR','VOLVO': 'VOLV','MITSUBISHI': 'MITS',
                                'CHRYSLER': 'CHRY',
                                'VOLKSWAGEN': 'VOLK',
                                })
#dmv_df3

#Check for makes in top 25 in both DMV and Citation 
pd.merge(dmv_df3,citation_df7,how="inner")
