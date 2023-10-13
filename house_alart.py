import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
house={'Amsterdam':24,'Rotterdam':25,'Utretch':27}
msg=''
for key,value in house.items():
    url=f'https://holland2stay.com/residences.html?available_to_book=179,336&city={value}'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text,'html.parser')
    for i in soup.find_all('div',class_='regi-item'):
        price=i.find('div',class_='regularbold').get_text()
        price=int(price.split('.')[0].replace(',','').replace('€',''))
        if price<=1000:
            link=i.find('a')['href']
            content='\n'.join([line.get_text() for line in i.find_all('li')])
            msg+=f'{key}\n'
            msg+=f'{price} euro\n'
            msg+=f'{link}\n'
            msg+=f'{content}\n'
            msg+='\n'
        else:
            continue

my_email='mandy209520@yahoo.com.tw'
password='your password'
body = MIMEText(msg)
with smtplib.SMTP("smtp.mail.yahoo.com",port=587) as connection:
    # encrypt the content
    connection.starttls()
    connection.login(user=my_email,password=password)
    res=connection.sendmail(from_addr=my_email,
                        to_addrs='asiaopractice@myyahoo.com',
                        msg=f'Subject:House Available\n\n{body}.')
    if res=={}:
        print('Successfully send the message')
    else:
        print('Fail to send the message')