import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import re
from csv import reader,writer
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from twnews.soup import NewsSoup




def crawler(domain,url):
    print(domain)
    headers = {'User-Agent':'Mozilla/5.0'}
    result=[]
    try:
        r = requests.get(url=url,headers=headers)
        r.encoding = r.apparent_encoding

        if str(r.status_code) == '404':
            return '404'
    except:
        return "Error"
    

    #print(url)
    if domain=='www.cna.com.tw':
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            article_body = soup.find('div', attrs={'class': 'paragraph'}).find_all('p')

            for p in article_body:
                result.append(p.text)
            return result


        except Exception as e:
            print(e)
            return "Error"
        print ()


    elif domain == 'www.chinatimes.com':
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            article_body = soup.find('div', attrs={'class': 'article-body'}).find_all('p')

            for p in article_body:
                result.append(p.text)
            return result


        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain in ['news.ltn.com.tw', 'estate.ltn.com.tw']:
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            article_body = soup.find('div', attrs={'class': 'text boxTitle boxText'}).find_all('p')

            for p in article_body:
                # Ignore promo
                if p.get('class') is not None and 'appE1121' in p.get('class'):
                    continue

                # Ignore image caption
                if p.parent.get('class') is not None and 'photo' in p.parent.get('class'):
                    continue

                result.append(p.text)

            return result

        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain == 'ent.ltn.com.tw':
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            article_body = soup.find('div', attrs={'class': 'text'}).find_all('p')

            for p in article_body:
                # Ignore promo
                if p.get('class') is not None and 'appE1121' in p.get('class'):
                    continue

                # Ignore image caption
                if p.parent.get('class') is not None and 'photo' in p.parent.get('class'):
                    continue

                result.append(p.text)

            return result

        except Exception as e:
            print(e)
            return "Error"
        print ()



    elif domain == 'm.ltn.com.tw':
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            article_body = soup.find('div', attrs={'itemprop': 'articleBody'}).find_all('p')

            for p in article_body:
                # Ignore promo
                if (p.get('class') is not None
                    and ('appE1121' in p.get('class') or 'before_ir' in p.get('class'))):
                    continue

                result.append(str(p.text))

            return result

        except Exception as e:
            print(e)
            return "Error"
        print ()


    elif domain == 'www.setn.com':
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            article_body = soup.find('div', attrs={'id': 'Content1'}).find_all('p')

            for p in article_body:
                # Ignore image caption
                if p.get('style') is not None and 'text-align: center;' in p.get('style'):
                    continue

                result.append(str(p.text))


            return result

        except Exception as e:
            print(e)
            return "Error"
        print ()


    
    elif domain=="news.cnyes.com":#https://news.cnyes.com/news/id/4361945
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('p')
            for p in content[4:len(content)]:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()

    
    elif domain=="www.mirrormedia.mg":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            title=soup.find_all('title')
            content=soup.find_all('p')
            for p in title:
                result.append(p.text)        
            for p in content[4:len(content)-2]:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="m.ctee.com.tw":
    
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('p')
            for p in content[6:len(content)-2]:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="udn.com":
    
        try:

            soup = BeautifulSoup(r.text, 'html.parser')
            for noisy_content in soup.find_all('div', class_="article-content__paragraph"):
                for p in noisy_content.find_all('p'):
                    result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="news.mingpao.com":

        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('p')    
            for p in content[0:len(content)-1]:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()


    elif domain=="mops.twse.com.tw":


        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('div', {'id':'table01'})    
            for p in content:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()


    elif domain in ["technews.tw", "finance.technews.tw", "ccc.technews.tw"]:
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            for content in soup.find_all('div', class_="indent"):
                for p in content.find_all('p'):
                    result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="www.businesstoday.com.tw":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')        
            content=soup.find_all('div', {'itemprop':'articleBody'})    
            for p in content:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()

    

    elif domain=="www.ettoday.net":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')        
            content=soup.find_all('div', {'class':'content-container'})    
            for p in content:
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain=="house.ettoday.net":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')        
            content=soup.find('div', {'itemprop':'articleBody'})

            for strong in content.find_all('strong'):
                strong.replaceWith('')

            for p in content.find_all('p'):
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    if domain=="www.hk01.com":
        try:
            
            r = requests.get(url=url,headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')    
            content=soup.find('article', {'class':'sc-bwzfXH liBCIH sc-bdVaJa iMCZeY'})
            for p in content.find_all('p'):
                result.append(p.text)

            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()


    elif domain=="sina.com.hk":
        try:
            
            
            soup = BeautifulSoup(r.text, 'html.parser')    
            content=soup.find('div', {'id':'news-main-body'})
            for div in content.find_all("div", {'class':'news-keyword'}): 
                div.decompose()
            return content.text
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="news.tvbs.com.tw":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')    
            content=soup.find('div', {'id':'news_detail_div'})
            for div in content.find_all("strong"):
                div.replaceWith('')
            result.append(content.text)
            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    


    elif domain=="www.bnext.com.tw":  ##有少數新聞因為改版所以會抓錯，再手動抓
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content1=soup.find('div', {'class':'article_summary'})
            content2=soup.find('article', {'class':'main_content'})
            return (content1.text+content2.text)
        except Exception as e:
            print(e)
            return "Error"
        print ()
    
    elif domain=="hk.on.cc": 
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('div', {'class':'breakingNewsContent'})
            return content.text#.encode("latin1").decode("utf-8")
        except Exception as e:
            print(e)
            return "Error"
        print ()

        #text=soup.get_text().strip()
    


    elif domain=="www.cw.com.tw":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content1=soup.find('div', {'class':'preface'})
            content2=soup.find('div', {'class':'article__content py20'})
            for div in content2.find_all("span", {'class':'sans-serif'}): 
                div.replaceWith('')

            return (content1.text+content2.text)    
        except Exception as e:
            print(e)
            return "Error"
        print ()

    

    elif domain=="domestic.judicial.gov.tw":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('pre')
            return content.text
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="www.wealth.com.tw":
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('div', {'id':'cms-article'})
            return content.text
        except Exception as e:
            print(e)
            return "Error"
        print ()
    

    elif domain=="tw.news.yahoo.com":   #有吃到一些前文不包含的部分，懶得改
    
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('article')
            return content.text
        except Exception as e:
            print(e)
            return "Error"
        print ()
    


    elif domain=="www.coolloud.org.tw":   
        
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('p')
            for p in content:
                # result.append(p.text.encode("latin1").decode("utf-8"))
                result.append(p.text)
            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()
    
    

    elif domain=="www.managertoday.com.tw":   
        
        try:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('p')
            for p in content:
                result.append(p.text)
            return result
        except Exception as e:
            print(e)
            return "Error"
        print ()

    

    elif domain=="money.udn.com":
        
        try:
        
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('div', {'id':'article_body'})
            for div in content.find_all(["figcaption","a"]): 
                div.replaceWith('')
            for p in content.find_all('p'):
                result.append(p.text)
            return result

            
        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain=='fsc.gov.tw' or domain == 'www.fsc.gov.tw':

        try:
        
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find_all('div', {'class': 'page_content'})
            for div in content:
                for d in div.find_all('div'):
                    result.append(d.text)

            return result

            
        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain == 'www.hbrtaiwan.com' or domain == 'hbrtaiwan.com':
        try:
        
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('div', {'class': 'content-area--article artic-content column mainArticle'})
            for p in content.find_all('p'):
                result.append(p.text)

            return result

            
        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain == 'www.nextmag.com.tw':
        try:
        
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('div', {'class': 'article-content'})
            for div in content.find_all("strong"):
                div.replaceWith('')

            for div in content.find_all('span', {'style': 'color:#FF0000;'}):
                div.replaceWith('')

            for p in content.find_all('p'):
                result.append(p.text)

            return result

            
        except Exception as e:
            print(e)
            return "Error"
        print ()

    elif domain == 'ol.mingpao.com':
        try:
        
            soup = BeautifulSoup(r.text, 'html.parser')
            content=soup.find('div', {'class': 'article_content'})
            for p in content.find_all('p'):
                result.append(p.text)

            return result

            
        except Exception as e:
            print(e)
            return "Error"
        print ()

        





if __name__ == '__main__':

    #f = open("tbrain_train_final_0610.csv")
    f = open("tbrain_train_final_0610.csv", encoding='utf-8')
    lines = f.readlines()
    firstLine = lines.pop(0)


    r = reader(open('ESUN_news.csv', encoding='utf-8'))
    output_lines = list(r)

    open('failed.txt', 'w', encoding='utf-8').close()
    open('temp_output.txt', 'w', encoding='utf-8').close()

    for line in lines:
        line=line.strip()
        line=[line]
        for token in reader(line):
            ID=token[0]
            url=token[1]
            domain = urlparse(url).netloc
            #prev,back=token[2].split(" ### 省略內文 ### ") #前後文

            print("ID: ",ID)
            text=crawler(domain,url)
            if type(text) is list:
                text = ''.join(text)
            text=str(text).strip()
            #text=text.strip("\"[\'",'"')
            #text=text.strip("\']\"",'"')
            text=text.replace('\\n',' ')
            text = text.replace('\\t','')
            text = text.replace('\\xa0',' ')

            text= "".join(text.split())

            if text == 'Error' or text == 'None':
                with open('failed.txt', 'a', encoding='utf-8') as failed_urls:
                    failed_urls.write('{}, {}\n'.format(ID, text))
                    failed_urls.write(url + '\n')

            with open('temp_output.txt', 'a', encoding='utf-8') as temp_output:
                temp_output.write('{},{},{}\n'.format(ID, url, text))

            output_lines[int(ID)][2]='"'+text+'"'
            #print("Done.")
            print()
     
    writer = writer(open('ESUN_news_test.csv', 'w', encoding='utf-8'))
    writer.writerows(output_lines)
