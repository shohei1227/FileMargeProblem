# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 21:00:41 2024

@author: Owner
"""

from gurobipy import *
import math
import numpy as np

i=5 #Incomeのレコード数
j=5 #Populationのレコードの数
I=range(0,5);
J=range(0,5);

N_i=[20,30,25,18,32];
N_j=[25,30,18,27,25];
G_i=np.array([10000,15500,20000,25000,15000]);
G_j=np.array([15000,15000,20000,25000,20000]);
M_i=np.array([3,2,5,4,3]);
M_j=np.array([4,2,1,2,4]);
combined_data_G=np.concatenate([G_i,G_j]);
combined_data_M=np.concatenate([M_i,M_j]);
s_G=np.var(combined_data_G);
s_M=np.var(combined_data_M);
num=0;

model=Model(); #モデルの宣言
x_ij={}; #変数x_itの宣言
for j in J:
    for i in I:
        x_ij[i,j]=model.addVar(vtype=GRB.INTEGER) #整数で定義

d_ij={}; #変数d_ijの宣言
for j in J: 
    for i in I:
        d_ij[i,j]=model.addVar(vtype=GRB.CONTINUOUS) #d_ijを連続変数で定義

model.update; #モデルのアップグレード

for i in I:
    model.addConstr(quicksum(x_ij[i,j] for j in J)-N_i[i]==0); #制約①

for j in J:
    model.addConstr(quicksum(x_ij[i,j] for i in I)-N_j[j]==0); #制約②

for j in J:
    for i in I:
        model.addConstr(x_ij[i,j]>=0); #制約③

for j in J:
    for i in I:
        model.addConstr(d_ij[i,j]==math.sqrt((G_i[i]-G_j[j])**2/s_G+(M_i[i]-M_j[j])**2/s_M)); #d_ijの計算

model.setObjective(quicksum(d_ij[i,j]*x_ij[i,j] for i in I for j in J),GRB.MINIMIZE); #目的関数の追加
model.optimize(); #最適化
print("Opt.value=",model.objval); #最適値の出力

for i in I: #最適解の出力
    for j in J:
        print("x_ij[",i,"][",j,"]=",x_ij[i,j].X);