from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
from flask_ngrok import run_with_ngrok
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify,render_template
from datetime import date
import json
import pandas as pd
import numpy as np
import html
import requests

# input
regione="Lazio"
provincia= "Viterbo"
professione= "idraulico"

# link
link= "https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "p-1?mr=200&rk=1"
r = requests.get("https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "p-2?mr=200&rk=1")
content = r.text

# soup
soup = bs(content, "lxml")
results=soup.find("span", class_="results-info__numresults")
res = results.text.splitlines()
n_results = int(res[1].lstrip().rstrip())

counter_res=0
dat=pd.DataFrame(columns=['Name', 'Cathegory', 'Phone','Address'])
# ciclo inizializzato per un massimo di 6 pagine con 80 risultati l-una
try:

  for page in range(0,6):
      page=page+1
      # link generation
      link= "https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "/p-"+str(page)+"?mr=80&rk=1"
      # print(link)
      r = requests.get("https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "/p-"+str(page)+"?mr=80&rk=1")
#       print(link)
      content = r.text
      soup = bs(content, "lxml")
      # soup extraction
      name = soup.find_all("h2", {"class":"list-element__title text-medium ", "itemprop":"name"})
      addr_street = soup.find_all("span", {"itemprop":"streetAddress"})
      addr_loc = soup.find_all("span", {"itemprop":"addressLocality"})
      addr_sugg= soup.find_all("span",  { "itemprop":"address"})
      phone_sugg=soup.find_all("div", {"class":"btn__label"}) 
      phone = soup.find_all("div", {"class":"btn__label", "itemprop":"telephone"})
      categ = soup.find_all("div",{"class":"list-element__category text-medium color-gray-4 mb-10"})
      # result extraction

      for i in range(0,len(name)-1):
          
          counter_res+=1
         
          # deleting suggested result (paid)
          if  (name[i].find("a")) == (name[i].find("a", {"data-pag":"Grande Cliente/RGS"})) :
#               print('*****************************************Name suggested removed************************************ \n' )
              phone.insert(i,'000' )
              name.remove(name[i])

          if (name[i].find("a")) != (name[i].find("a", {"data-pag":"Grande Cliente/RGS"})) :
            # print(i)  
            try: 
#               print(name[i].find("a").text)
            except:
              name[i]='NaN'
#               print("No name")
            try:
#               print(categ[i].text.rstrip().lstrip())
            except:
              categ[i]='NaN'
#               print("No categories")
            try:
              print(phone[i].text)
            except:
              phone[i]='NaN'
#               print("No number")
            try: 
#                   print((addr_street[i].text) + ' '+ (addr_loc[i].text)+"\n")        
            except: 
                  addr_street[i]='NaN'
                  addr_loc[i]='Nan'
#                   print('No address info')
          try:  
            dat = dat.append([{'Name':name[i].find("a").text, 'Cathegory':categ[i].text.rstrip().lstrip(),'Phone':phone[i].text,
                             'Address':((addr_street[i].text) + ' '+ (addr_loc[i].text))  }], ignore_index=True)
          except Exception as e:
#             print(e)
      
except Exception as e


#   print(e)
            
#   print("\n Errore,","Risultati trovati", counter_res,"totale risultati",n_results,sep=' ')


# with open('dat.json', 'w') as f:
#   f.write(dat.to_json())


# print("\n Risultati", counter_res,"totale risultati",n_results, "Risultati omessi",n_results-counter_res ,sep=' ')
app=Flask(import_name=scraper.py,template_folder='templates',__name__)
run_with_ngrok(app)
# with open('/content/dat.json', 'r') as myfile:
#       data = myfile.read()


@app.route('/', methods=("POST", "GET"))
def html_table():

    return render_template('simple.html',  tables=[dat.to_html(classes='data')], header="true")

if __name__ == "__main__":
    app.run()