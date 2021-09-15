

$pip install beautifulsoup4
$pip install requests
$pip install lxml
import requests

#geographical search
regione="Lazio"
provincia= "Viterbo"
professione= "idraulico"

#building link
from bs4 import BeautifulSoup as bs
link= "https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "p-1?mr=200&rk=1"
r = requests.get("https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "p-2?mr=200&rk=1")
content = r.text
soup = bs(content, "lxml")
link

#number of results
results=soup.find("span", class_="results-info__numresults")
res = results.text.splitlines()
n_results = int(res[1].lstrip().rstrip())
n_results

#contatore risultati
counter_res=0
# ciclo inizializzato per un massimo di 6 pagine con 80 risultati l-una
try:
  for page in range(0,6):
      page=page+1
      # link generation
      link= "https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "/p-"+str(page)+"?mr=80&rk=1"
      # print(link)
      r = requests.get("https://www.paginegialle.it/ricerca/" + professione + "/" + provincia + "/p-"+str(page)+"?mr=80&rk=1")
      print(link)
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
              print('*****************************************Name suggested removed************************************ \n' )
              phone.insert(i,'000' )
              name.remove(name[i])

          if (name[i].find("a")) != (name[i].find("a", {"data-pag":"Grande Cliente/RGS"})) :
            # print(i)  
            try:   
              print(name[i].find("a").text)
            except:
              print("No name")
            try:
              print(categ[i].text.rstrip().lstrip())
            except:
              print("No categories")
            try:
              print(phone[i].text)
            except:
              print("No number")
            try: 
                  print((addr_street[i].text) + ' '+ (addr_loc[i].text)+"\n")        
            except: 
                  print('No address info')
                #  <div class="list-element__label list-element__label--sugg">suggerito</div>

          # if  (name[i].find("a")) == (name[i].find("a", {"data-pag":"Grande Cliente/RGS"})) :
          #     phone.insert(i,'000' )
          #     # i=i+2
except:
  print("\n Errore,","Risultati trovati", counter_res,"totale risultati",n_results,sep=' ')


print("\n Risultati", counter_res,"totale risultati",n_results, "Risultati omessi",n_results-counter_res ,sep=' ')

