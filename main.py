import pandas as pd
from pywebio.input import *
from pywebio.output import *

data = pd.read_csv(r"C://Users//AMAR//Downloads//archive (1)//dataset.csv")
data.fillna(value='missing', inplace=True)
d1=pd.read_csv(r"C://Users//AMAR//Downloads//archive (1)//symptom_Description.csv")
symptoms=set()
for j in range(1,18):
  for i in data["Symptom_"+str(j)]:
    symptoms.add(i)
uniquesymptoms=list(symptoms)

dis=set()
for i in data["Disease"]:
  dis.add(i)
uniquediseases=list(dis)

dicfreq={}
for i in uniquediseases:
  dicfreq[i]=0
for p in data["Disease"]:
  dicfreq[p]+=1

dic={}
for u in uniquediseases:
  dic[u]=[]
for i in dic.keys():
  for j in range(4920):
    if data["Disease"][j]==i:
      dic[i].append(j)

dicf={}
for u in uniquediseases:
  dicf[u]=[]
for i in dicf.keys():
  lst=dic[i]
  for p in uniquesymptoms:
    c=0
    if c==1:
      break
    else:
      for y in lst:
        if c==1:
          break
        else:
          for e in range(1,18):
            if data["Symptom_"+str(e)][y]==p:
              c+=1
              break
    if c==0:
      dicf[i].append(0)
    else:
      dicf[i].append(1)

dif1={"Disease":uniquediseases}
for i in uniquesymptoms:
  dif1[i.replace(" ","")]=[]

for j in range(len(uniquesymptoms)):
  for p in dicf.keys():
    if dicf[p][j]==1:
      dif1[uniquesymptoms[j].replace(" ","")].append(1)
    else:
      dif1[uniquesymptoms[j].replace(" ","")].append(0)

df = pd.DataFrame(dif1)

import math
total=0
for i in dicfreq.values():
  total+=i
ent=0
for j in dicfreq.keys():
  x=dicfreq[j]/total
  ent+=(-x)*math.log(x,2)

def entropy(lst):
  dicfr={}
  for i in lst:
    dicfr[i]=0
  for j in lst:
    dicfr[j]+=1
  l=len(lst)
  ans=0
  for p in dicfr.keys():
    x=dicfr[p]/l
    ans+=(-x)*math.log(x,2)
  return ans


def info(df):
    lstd = []
    for i in df["Disease"]:
        lstd.append(i)
    ent = entropy(lstd)

    lstc = []
    for u in df.columns:
        if u != 'Disease':
            lstc.append(u)
    dicig = {}
    uniquesymptoms = lstc
    for i in uniquesymptoms:
        dfp = df[df[i] == 1]
        lstone = []
        for y in dfp["Disease"]:
            lstone.append(y)
        dfn = df[df[i] == 0]
        lstzero = []
        for y in dfn["Disease"]:
            lstzero.append(y)
        l = len(lstone) + len(lstzero)
        a = ((len(lstone) / l) * entropy(lstone))
        b = ((len(lstzero) / l) * entropy(lstzero))
        ig = ent - a - b
        dicig[i.replace(" ", "")] = ig

    lstig = []
    for p in dicig.keys():
        lstig.append((p, dicig[p]))
    lstig.sort(key=lambda y: y[1])
    lstig = lstig[::-1]
    return (lstig[0][0])

dicig={}
for p in uniquesymptoms:
  dicig[p.replace(" ","")]=0
for i in uniquesymptoms:
  lstone=[]
  lstzero=[]
  for j in range(41):
    if df[i.replace(" ","")][j]==1:
      lstone.append(df["Disease"][j])
    else:
      lstzero.append(df["Disease"][j])
  a=((len(lstone)/41)*entropy(lstone))
  b=((len(lstzero)/41)*entropy(lstzero))
  ig=ent-a-  b
  dicig[i.replace(" ","")]=ig

lstig=[]
for p in dicig.keys():
  lstig.append((p,dicig[p]))
lstig.sort(key=lambda y: y[1])
lstig=lstig[::-1]

for i in range(len(uniquesymptoms)):
  uniquesymptoms[i]=uniquesymptoms[i].replace(" ","")

data = pd.read_csv(r"C://Users//AMAR//Downloads//archive (1)//symptom_precaution.csv")

put_text("Enter the symptoms you are facing, separated by a space..\n")
df1 = df
lst = list(map(str, input().split()))
d = 0
for i in lst:
    if i not in uniquesymptoms:
        d += 1
        break
if d > 0:
    put_text("Sorry!! We can't tell about your disease. Please consult a doctor...")
else:
    dicind = {}
    for i in lst:
        dicind[i] = -1
    for u in lst:
        for p in range(len(lstig)):
            if lstig[p][0] == u:
                dicind[u] = p
                break
    lst1 = []
    for u in dicind.keys():
        lst1.append((u, dicind[u]))
    lst1.sort(key=lambda y: y[1])
    lst2 = []
    for p in lst1:
        lst2.append(p[0])

    ind1 = lst1[-1][1]

    for i in lst2:
        df1 = df1[df1[i] == 1]
        df1 = df1.drop(i, axis=1)

    may = []
    for r in df1["Disease"]:
        may.append(r)
    if may == []:
        put_text("CONGRATS!! according to our data, you don't have any disease...")
    else:
        if len(may) == 1:
            put_text("You are diagnosed with " + may[0] + " disease..")
            dis = may[0]
            lstp = []
            for y in d1["Disease"]:
                lstp.append(y.replace(" ", ""))
            w = lstp.index(dis.replace(" ", ""))
            put_text(d1["Description"][w])
            put_text("Thanks for using this app. Wish you a very good health!!")
        else:
            ci = 1
            put_text("You may have the following diseases: \n")
            for p in may:
                put_text(str(ci) + ". " + p)
                ci += 1

    if len(may) > 1:
        ans1 = input("Do you want to know the exact disease which you may have? (if yes, press 1, else, press 0)\n")
        if ans1 == '1':
            symp = lstig[int(ind1) + 1][0]
            c = 0

            while c == 0:
                ans = input("Do you experience " + str(symp) + "? if yes, enter 1, else, enter 0\n")
                if df1.shape[0] == 1:
                    c += 1
                    lst1 = []
                    for r in df1["Disease"]:
                        lst1.append(r)
                    dis = lst1[0]
                    put_text("You are diagnosed with the disease " + lst1[0] + "...")
                    lstp = []
                    for y in d1["Disease"]:
                        lstp.append(y.replace(" ", ""))
                    w = lstp.index(dis.replace(" ", ""))
                    put_text(d1["Description"][w])
                    ind = -1
                    for t in range(41):
                        if data["Disease"][t] == dis.replace(" ",""):
                            ind = t
                            break
                    prec = []
                    for u in range(1, 5):
                        prec.append(data["Precaution_" + str(u)][ind])
                    put_text("Some of the precautions of this disease are: ")
                    ci = 1
                    for y in range(len(prec)):

                        put_text(prec[y])
                    put_text()
                    put_text("Hope you recover from the disease at the earliest!!")
                    put_text("Thanks for using this app. Wish you a very good health!!")
                    break
                else:

                    if ans == '1':
                        df1 = df1[df1[symp] == 1]
                        df1 = df1.drop(symp, axis=1)
                        symp = info(df1)
                    else:
                        df1 = df1[df1[symp] == 0]
                        df1 = df1.drop(symp, axis=1)
                        symp = info(df1)
        else:
            put_text("Thanks for using this app. Wish you a very good health!!")