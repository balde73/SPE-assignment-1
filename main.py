import matplotlib
matplotlib.use('Agg')

import datetime
import os
import argparse
import csv
import numpy as np
import scipy
from scipy.stats import norm
import matplotlib.pyplot as plt

# setting graphs
font = {'size'   : 14}
fontLeg = {'fontsize': 11}

matplotlib.rc('font', **font)
matplotlib.rc('legend', **fontLeg)

def split(data, index):
  # divide data for different values of index
  subsets = []
  value = "*_"
  num = -1
  for row in data:
    if(value!=row[index]):
      value = row[index]
      num = num + 1
      subsets.append([])
    subsets[num].append(row);
  return subsets

def column(data, index):
  # extract the values of column index from data (also convert in float)
  columnValues = []
  for row in data:
    columnValues.append(float(row[index]))
  return columnValues

def plot_di_max(data, i):
  width = 1/1.5
  setData = set(data)
  y = [data.count(x) for x in setData]
  x = [x for x in setData]
  plt.figure()
  plt.title("Web object "+str(i))
  plt.bar(x, y, width, color="blue")
  plt.xlabel("values (n)")
  plt.ylabel("quantity (m)")
  plt.savefig(directory+"/Web_object_"+str(i)+"_Dimax.pdf")
  if(not verbose):
    plt.close()

def plot_fitting(x, y, yFitted, i):
  plt.figure()
  plt.title("Web object "+str(i))
  plt.plot([xi/1000 for xi in x], [y_i/1000 for y_i in y], 'o', label='Original data', markersize=.4, color="gray")
  plt.plot([xi/1000 for xi in x], [y_i/1000 for y_i in yFitted], 'r', label='Fitted line', color="black")
  plt.xlabel("downloads (n x1000)")
  plt.ylabel("revenues (n x1000)")
  plt.legend()
  plt.savefig(directory+"/Web_object_"+str(i)+"_fitting.pdf")
  if(not verbose):
    plt.close()

def plot_all_revenues(xs, ys):
  if(len(xs) != len(ys)):
    print("[Error] plot_all_revenues: size of x and y does not match")
    return
  plt.figure()
  plt.title("Revenues/downloads for all object")
  lw = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  ls = ["-", "--", ":", "-", "--", ":", "-", "--", ":", "-"]
  m = ["x", "x", "x", "^", "^", "^", "o", "o", "o", "s"]
  for i, x in enumerate(xs):
    y = ys[i]
    plt.plot([x[0]/1000, x[-1]/1000], [y[0]/1000, y[-1]/1000], marker=m[i], linewidth=lw[i], ls=ls[i], label='Object'+str(i+1))
  plt.xlabel("downloads (n x1000)")
  plt.ylabel("revenues (n x1000)")
  plt.legend()
  plt.savefig(directory+"/all_revenues_downloads.pdf")
  if(not verbose):
    plt.close()

def plot_gaussian(data, bin, left, right):
  plt.figure()
  plt.hist(data, bins=bin, normed=True, alpha=0.6, color='gray')
  mu = np.mean(data)
  std = np.std(data)
  xmin, xmax = plt.xlim()
  x = np.linspace(xmin, xmax, 100)
  p = norm.pdf(x, mu, std)
  #plt.plot(x, p, 'k', linewidth=2)

  p1 = norm.pdf(x, 0, left)
  p2 = norm.pdf(x, 0, right)
  plt.plot(x, p1, 'k', linewidth=1)
  plt.plot(x, p2, 'k', linewidth=1)
  title = "Fitting: mu = %.2f,  std = [%.2f, %.2f]" % (mu, left, right)
  plt.xlabel("noise values (n)")
  plt.ylabel("probability (p)")
  plt.title(title)
  plt.savefig(directory+"/gaussian_noise.pdf")
  if(not verbose):
    plt.close()

# argumentparser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-vb', '--verbose',
          action='store_true',
          help="Print some graphs")
parser.add_argument('-vvb', '--vverbose',
          action='store_true',
          help="Print some graphs and save all graphs in /images")

config = parser.parse_args()

verbose = config.verbose
vverbose = config.vverbose

# prepare working space
now = datetime.datetime.now()
directory = os.path.join(os.getcwd(), "images", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

try:
  os.makedirs(directory)
except:
  print("impossible to create folder "+directory+" to store images. Using ./images")
  directory = './images'

with open('baldessari.csv', "r") as f:
  reader = csv.DictReader( f )
  subsets = split(reader, "i")

full_noise = []
clean_revenues_list = []
downloads_list = []
std_list = []
for i, subset in enumerate(subsets):
  # load esperimental parameters
  times     = column(subset, "t")
  downloads = column(subset, "x")
  revenues  = column(subset, "y")

  # compute D_MAX
  sortedDiffDownloads = np.sort(np.diff(downloads)).tolist()
  dMax = sortedDiffDownloads[-1]
  if(verbose and i==7 or vverbose):
    plot_di_max(sortedDiffDownloads, i)

  # compute ALPHA
  A = np.vstack([downloads, np.ones(len(downloads))]).T
  m, c = np.linalg.lstsq(A, revenues, rcond=-1)[0]
  clean_revenues = [v*m+c for v in downloads]
  downloads_list.append(downloads)
  clean_revenues_list.append(clean_revenues)

  print("Object: " + str(i) + " Dmax: " + str(dMax) + " alpha: " + str(m))

  if(verbose and i==7 or vverbose):
    plot_fitting(downloads, revenues, clean_revenues, i)

  noise = [a - b for a, b in zip(revenues, clean_revenues)]
  std_list.append(np.std(noise))
  full_noise = full_noise + noise

# compute std interval
print("----------------------------------")
left = scipy.stats.t.ppf(0.025, 14)

m = np.mean(std_list)
s = np.std(std_list)
print("confidence interval for sigma")

# compute sigma interval
confidence_level = [90, 95, 99]
for confidence in confidence_level:
  p = (-confidence + 100)/100
  n = len(std_list)

  t_p2 = scipy.stats.t.ppf(1-p/2, n-1)
  interval = t_p2*s/np.sqrt(n)

  interval_left = m - interval
  interval_right = m + interval

  print(confidence,'% [',interval_left,',',interval_right,']')

if(verbose or vverbose):
  plot_all_revenues(downloads_list, clean_revenues_list)
  plot_gaussian(full_noise, 30, interval_left, interval_right)

print("----------------------------------")
print("The graphs are saved as pdf inside \033[92m", directory, "\033[0m")
print("If you want to plot graphs in console comment line2 of ./main.py and remove plt.close()")
plt.show()
