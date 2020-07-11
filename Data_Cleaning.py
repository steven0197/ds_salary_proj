# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 21:43:25 2020

@author: Steven
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carga de datos
df = pd.read_csv('Data/glassdoor_jobs.csv')

#Retirar Elementos -1 de los estimativos de salario
df = df[df['Salary Estimate'] != '-1']
df.reset_index(drop = True, inplace = True)
# Salary Parsing
df['Hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in  x.lower() else 0)
df['Employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'Employer Provided Salary:' in  x.lower() else 0)


salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minusk = salary.apply(lambda x: x.replace('K' , '').replace('$' , ''))
clean = minusk.apply(lambda x: x.lower().replace('per hour' , '').replace('employer provided salary:' , '') )
                        
df['min_sal'] = clean.apply(lambda x: x.split('-')[0]).astype(int)  
df['max_sal'] = clean.apply(lambda x: x.split('-')[1]).astype(int)     

df['sal_prom'] = df[['min_sal' , 'max_sal']].mean(axis = 1)                 

# Company Name

df['Company Name'] = df['Company Name'].apply(lambda x: x.split('\n')[0])

#State 

df['State'] = df.Location.str.split(',').str[1]

df.State.apply(lambda x: x.replace('Los Angeles' , 'CA'))

# Is the work in the Headquarters

df['IN_HEADQUARTERS']  = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0 , axis= 1)

#Company AGE

df['COMPANY_AGE'] = df.Founded.apply(lambda x: 0 if x < 0 else 2020 - x )

#Parsing on job description (python, etc...)

#python

df['PYTHON_YN'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.PYTHON_YN.value_counts()

#R

df['R_YN'] = df['Job Description'].apply(lambda x: 1 if ' r ' in x.lower() or 'r studio' in x.lower() else 0)
df.R_YN.value_counts()

#spark

df['SPARK_YN'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.SPARK_YN.value_counts()

#aws 

df['AWS_YN'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.AWS_YN.value_counts()

#Excel

df['EXCEL_YN'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.EXCEL_YN.value_counts()

#Terminando

df.columns
df_out = df.drop(['Unnamed: 0'], axis = 1)

df_out.to_csv("SALARY_DATA_CLEANED.CSV", index = False)

df2 = pd.read_csv("SALARY_DATA_CLEANED.CSV")
