from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests, smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


names, emails = get_contacts('contacts.txt')
message_template = read_template('body.txt')
 
to_file = open('contacts.txt','r')
to_text = to_file.read().strip()
to_file.close()
to = to_text

email_addr = 'xxxxxxxxxx@xxxxxxxxxx.com'    

n_url = 'https://www.nike.com/t/epic-react-flyknit-mens-running-shoe-mfm75M/AQ0067-102'

n_site = uReq(n_url)
n_page = n_site.read()
n_site.close()
page_soup = soup(n_page, "html.parser")

price = page_soup.findAll("div",{"class":"ncss-base ta-sm-r fs16-sm"})
shoe_price = price[1]
dollar_amt = price[1].get_text() 
discount = shoe_price.div.div["class"]
sale_price = shoe_price.div.div.get_text()

shoe = page_soup.find("h1",{"data-test":"product-title"})
shoe_name = shoe.get_text()

if 'mb-1-sm' in discount:
    print(str(shoe_name) + ' is on sale for ' + str(sale_price))
    for name, email in zip(names, emails):
        conn = smtplib.SMTP('smtp.gmail.com', 587) # SMTP address and port
        conn.ehlo()
        conn.starttls()
        conn.login(email_addr, 'xxxxxxxxxxxxxxxxxx')
        msg = MIMEMultipart()
        message = message_template.substitute(CONTACT_NAME=name.title(),SHOE=shoe_name,
        SP=sale_price)
            
        msg['From'] = email_addr
        msg['To'] = email
        msg['Subject'] = "Nike Shoe On Sale"

        msg.attach(MIMEText(message, 'plain'))
        conn.sendmail(email_addr, email, msg.as_string())
        print('Sent notification emails to the following recipient:\n')
        print(email)
    conn.quit()
else:
    print(str(shoe_name) + " is still " + str(dollar_amt))