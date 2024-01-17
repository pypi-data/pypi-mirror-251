import numpy as np
import pandas as pd

from scipy.integrate import odeint
from scipy.optimize import minimize
import matplotlib.pyplot as plt
# %matplotlib inline

import sys
ini = sys.argv

def SEIR_model(v, t, beta, delta, gamma):
  dS=-beta*v[0]*v[2]
  dE=beta*v[0]*v[2]-delta*v[1]
  dI=delta*v[1]-gamma*v[2]
  dR=gamma*v[2]
  return [dS, dE, dI, dR]

#入力値
t_max = 500 # 処理回数
N=67450000 # 総人口
rday=75 # 免疫ができる日数(人の噂も七十五日)
x=100  # 1人が1日に感染させた人数(２４時間のインプレッション数、フォロワー数など)
cday=30 # 潜伏期間(見過ごす期間)

t_max = int(ini[1])
N = int(ini[2])
rday = int(ini[3])
x = int(ini[4])
cday = int(ini[5])

# 初期設定
dt = 1 # 間隔
E_0=1 # 炎上した人、燃料投下者
I_0=0 # 傍観者
S_0=N-I_0
R_0=0
ini_state = [S_0,E_0,I_0,R_0] #[S[0], E[0],I[0], R[0]]

beta_const = x/(N*E_0)
gamma_const = 1/rday
delta_const = 1/cday

times =np.arange(0,t_max, dt)
args  =(beta_const, delta_const, gamma_const)

result = odeint(SEIR_model, ini_state, times, args)
#plot
fig = plt.figure()
plt.plot(list(range(len(result))),result)
plt.legend(['knows nothing','fuel','bystander', 'bored with'])
plt.show()