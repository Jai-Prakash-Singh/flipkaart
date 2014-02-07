from bs4 import BeautifulSoup
import urll_proxy
import time
import sys
import MySQLdb
import os
import shutil



def main():

    link = "http://www.flipkart.com/bags-wallets-belts/bags/hand-bags/pr?sid=reh%2Cihu%2Cm08"
    page = urll_proxy.main(link)
    soup = BeautifulSoup(page)
    tag_ul = soup.find_all("ul", attrs={"id":"brand"})

    f  = open("page1_bn_bl_bc.csv","a+")
    f2 = open("page1_brandname_brandlink", "a+")

    tag_a = tag_ul[0].find_all("a")
     
    pos = 1
    for l in tag_a:
        brand_link = "http://www.flipkart.com"+str(l.get("href")).strip()
	brand_name = str(l.span.get_text()).strip()
	brand_count = str(l.find("span", attrs={"class":"count"}).get_text()).strip("()")
	date = str(time.strftime("%d/%m/%Y"))
        print >>f, ','.join([date, str(pos), brand_name, brand_count, brand_link])
	print >>f2, ','.join([brand_name, brand_link])
        pos = pos+1
       

    f.close()
    f2.close()

    shutil.copy2("page1_bn_bl_bc.csv", "page1_bn_bl_bc_new.csv")
    os.remove("page1_bn_bl_bc.csv")
    



def addin_to_mysql():
    db = MySQLdb.connect("localhost","root","6Tresxcvbhy","flipkart")
    cursor = db.cursor()
    cursor.execute( "create table if not exists handbagbrands_info ( \
                    id int(11) not null auto_increment, date varchar(45), position varchar(20), \
                    brand_name varchar(200), brand_count varchar(20), brand_link varchar(255),PRIMARY KEY (id, brand_name));"
                  )

    f =  open("page1_bn_bl_bc_new.csv")
    for line in f:
        value = tuple(line.strip().split(","))
        sql = """insert into handbagbrands_info(date, position, brand_name, brand_count, brand_link) values ("%s", "%s", "%s", "%s", "%s")"""%(value)
        cursor.execute(sql)
        db.commit()

    f.close()
    
    cursor.execute(sql)
    db.close()




if __name__=="__main__":
    main() 
    addin_to_mysql()
