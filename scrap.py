import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
import time

class Soup():
    def __init__(self,url):
        self.url=url
        self.data=[]
    #Returns the number of jobs with a specific position, language {h} and experience required {seniority} in specified city {city}
    def get_number(self,lang,city,seniority):
        if self.url == "www.pracuj.pl":
            
            self.data.append(lang.lower())
            if(lang.lower()=="c#"):
                lang='c%23'
            if(lang.lower()=="c++"):
                lang="c%2b%2b"
            if(lang.lower().__contains__(" ")):
                lang.replace(" ","%20")
            
            self.url+="/praca/"+lang.lower()+";kw/"
            self.url+=city.lower()+";wp?rd=0"
            page=requests.get(self.url)
            zupa=BeautifulSoup(page.content,'html.parser')
            span=zupa.find_all(class_="results-header__offer-count-text-number")
            self.data.append(city.lower())
            self.data.append(str(datetime.date(datetime.now())))
            self.data.append(span[0].text)

        elif self.url =="http://www.nofluffjobs.com":
            self.data.append(lang.lower())
            self.data.append(city.lower())
            self.data.append(str(datetime.date(datetime.now())))

            self.url+="/pl/jobs/"+lang.lower()+"?criteria=city%3D"+city.lower()+"%20seniority%3D"+seniority.lower()+"&page=1"
            page=requests.get(self.url)
            zupa=BeautifulSoup(page.content,'html.parser')
            span = zupa.find_all(class_="pr-lg-3 m-0")
            self.data.append(span.__len__())

        elif self.url == "http://www.bulldogjob.com":
            self.data.append(lang.lower())
            self.data.append(city.lower())
            self.data.append(str(datetime.date(datetime.now())))
            self.url+="/companies/jobs/s/city\,"+city.lower()+"/skills\,"+lang.lower()+"/experiance_level\,"+seniority.lower()
            print(self.url)
            page=requests.get(self.url)
            zupa=BeautifulSoup(page.content,'html.parser')
            span = zupa.find_all(class_="job-details")
            self.data.append(span.__len__())
            print(span.__len__())


    #Returns a list of job offers with a specific position, language {h} and experience required {seniority} in specified city {city} with maximum distance {km}(default 0)
    def get_jobs_pracuj(self,job,city,seniority,km=0):
        j=0
        results=[]
        self.data.append(job.lower())
        if(job.lower()=="c#"):
            job='c%23'
        if(job.lower()=="c++"):
            job="c%2b%2b"
        if(job.lower().__contains__(" ")):
            job.replace(" ","%20")     
        self.url+="/praca/"+job.lower()+"%20"+seniority.lower()+";kw/"
        self.url+=city.lower()+";wp?rd="+str(km)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        #print(self.url)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        
        r=driver.page_source
        
        zupa=BeautifulSoup(r,'html.parser')
        zupa.prettify()
        container=zupa.find(class_="results__list-container")
        spans=container.find_all(class_="results__list-container-item")
        while(zupa.find("li",class_="pagination_element pagination_element--next")!=None):
            #print("Mamy to")
            lapa=zupa.find("li",class_="pagination_element pagination_element--next")
            new_url=lapa.find("a",class_="pagination_trigger").get("href")
            #print(new_url)
            driver.get("https://www.pracuj.pl"+new_url)
            r=driver.page_source
            time.sleep(5)
            zupa=BeautifulSoup(r,'html.parser')
            con=zupa.find(class_="results__list-container")
            spans+=con.find_all(class_="results__list-container-item")
        

        for i in range(0,spans.__len__()):
            wyniki=[]
            #print(spans[i].contents)
            if(len(spans[i].contents)>=3):
                if(len(spans[i].contents[1].contents)>1):
                    wyniki.append(spans[i].find(class_="offer-details__title-link").contents[0])
                    
                    wyniki.append(spans[i].find(class_="offer-company__name").contents[0])
                    
                    wyniki.append(spans[i].find(class_="offer-labels__item offer-labels__item--location").contents[1])
                    wyniki.append(spans[i].find(class_="offer-actions__date").contents[2]+spans[i].find(class_="offer-actions__date").contents[4].replace("\n",""))
                    wyniki.append(spans[i].find(class_="offer__click-area").get("href"))
            
                    if spans[i].find(class_="offer-logo").contents[1].get('class')!=['offer-logo__empty']:
                        wyniki.append(spans[i].find(class_="offer-logo").contents[1].contents[0].get("src"))
                    else:
                        wyniki.append("brak logo")
                    
                    j+=1
                    results.append(wyniki)
                    
            elif i>10:
                if spans[i].find(class_="offer-details__title-link")!=None:
                    wyniki.append(spans[i].find(class_="offer-details__title-link").contents[0])
                    wyniki.append(spans[i].find(class_="offer-company__name").contents[0])
                    wyniki.append(spans[i].find(class_="offer-labels__item offer-labels__item--location").contents[1])
                    wyniki.append(spans[i].find(class_="offer-actions__date").contents[1]+spans[i].find(class_="offer-actions__date").contents[3].replace("\n",""))
                    wyniki.append(spans[i].find(class_="offer__click-area").get("href"))
                    if spans[i].find(class_="offer-logo").contents[0].find("span")==None:
                        wyniki.append(spans[i].find(class_="offer-logo").contents[0].contents[0].get("src"))
                    else:
                        wyniki.append("brak logo")
                    
                    j+=1
                    results.append(wyniki)
        #print(j)
        return results

