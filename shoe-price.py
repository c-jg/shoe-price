import requests, smtplib
from bs4 import BeautifulSoup
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
email_addr = 'XXXXXXXXX@XXXXXXXXXX.COM'
# URL of shoes on Nike.com
url = 'https://www.nike.com/t/zoom-pegasus-turbo-mens-running-shoe-Z163c3/AJ4114-486'

req = requests.get(url)
site = req.text
html = BeautifulSoup(site, "html.parser")

price = html.findAll("div",{"class":"ncss-base ta-sm-r fs16-sm"})
shoe_price = price[1]
dollar_amt = price[1].get_text() 
discount = shoe_price.div.div["class"]
sale_price = shoe_price.div.div.get_text()

shoe = html.find("h1",{"data-test":"product-title"})
shoe_name = shoe.get_text()

if 'mb-1-sm' in discount:
    print(str(shoe_name) + ' is on sale for ' + str(sale_price))
    for name, email in zip(names, emails):
        conn = smtplib.SMTP('smtp.gmail.com', 587) # SMTP address and port
        conn.ehlo()
        conn.starttls()
        # Enter one-time Google account password below
        conn.login(email_addr, 'xxxxxxxxxxxxxxxxx')
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
