import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#print(sys.argv[1])

def decom(file,tar=-1,pc1=1,pc2=2):

  df = pd.read_csv(file)
  df = df.dropna(how='any')

  for _ in df.columns:
    if "id" in _ :
      df = df.drop(_, axis=1)
    elif "ID" in _:
      df = df.drop(_, axis=1)
  
  y = df[df.columns[tar]]
  data = df.drop(df.columns[tar], axis=1)
  
  # データの正規化
  data_std = (data - data.mean()) / data.std(ddof=0)

  # 共分散行列の計算
  cov = np.cov(data_std.T)

  # 固有値と固有ベクトルの計算
  cov_ang = np.linalg.eig(cov)
  cov_ang_ = []
  for i in range(len(cov_ang[0])):
    cov_ang_.append([cov_ang[0][i],cov_ang[1][i]])

  # 固有値の大きさ順にソートする
  cov_ang_.sort(reverse=True)

  # 主成分選択（２次元）及びデータの投影
  result = []
  print(f"Number of components : {len(cov_ang_)}")
  for i in range(len(cov_ang_)):
    result.append(np.dot(cov_ang_[i][1],data_std.T))

  # 可視化
  points = [[],[],[],[]]
  for i in range(len(result[0])):
    points[0].append([result[pc1-1][i],result[pc2-1][i],y[i]])
    
  x0 = []

  for _ in list(y.unique()):
    x0.append([[],[]])

  for _ in points[0]:
    for i in range(len(list(y.unique()))):
      if _[2] == list(y.unique())[i]:
        x0[i][0].append(_[0])
        x0[i][1].append(_[1])
        break


  fig = plt.figure()
  fig.subplots_adjust(left=0.1,
                      bottom=0.1,
                      right=0.9,
                      top=0.9,
                      wspace=0.4,
                      hspace=0.4)
  ax1 = fig.add_subplot(1, 1, 1)
  ax1.set_xlabel(f"PComponent-{pc1}")
  ax1.set_ylabel(f"PComponent-{pc2}")
  for i in range(len(list(y.unique()))):
    ax1.scatter(x0[i][0],x0[i][1],label=list(y.unique())[i])
#  plt.show()
  return fig

def main():
  fig = decom(sys.argv[1],
              -1 if sys.argv[2] == "-1" else int(sys.argv[2]),
              int(sys.argv[3]) if len(sys.argv) == 5 else 1,
              int(sys.argv[4]) if len(sys.argv) == 5 else 2)
  fig.savefig('result.png')
  plt.show()
  
if __name__ == "__main__":
  main()

  



# decom(sys.argv[1],
#       -1 if sys.argv[2] == "-1" else int(sys.argv[2]),
#       int(sys.argv[3]) if len(sys.argv) == 5 else 1,
#       int(sys.argv[4]) if len(sys.argv) == 5 else 2)
