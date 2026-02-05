import streamlit as st
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from streamlit_option_menu import option_menu
import time

def scrape_fk(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        products = []

        for product in driver.find_elements(By.CLASS_NAME, '_13oc-S'):
            name = product.find_element(By.CLASS_NAME, 's1Q9rs').text.strip()
            price = product.find_element(By.CLASS_NAME, '_30jeq3').text.strip()
            price = float(''.join(c for c in price if c.isdigit() or c == '.'))
            site = "Flipkart"
            product_url = product.find_element(By.CLASS_NAME, 's1Q9rs').get_attribute('href')
            # image waala add karna hai lekin hard hai, iska ho gaya
            # image_url = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
            products.append({'name': name, 'price': price, 'site': site, 'link': product_url})

        sorted_products = sorted(products, key=lambda x: x['price'])
        return sorted_products

    finally:
        driver.quit()

def scrape_ny(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        products = []

        names=driver.find_elements(By.CLASS_NAME, 'css-xrzmfa')
        prices=driver.find_elements(By.CLASS_NAME, 'css-111z9ua')
        wraps=driver.find_elements(By.CLASS_NAME, 'css-qlopj4')
        # image waala add karna hai lekin hard hai, iska ho gaya
        # images=driver.find_elements(By.TAG_NAME, 'img')

        for name, price, urls in zip(names, prices, wraps):
            temp_name = name.text.strip()
            temp_price = float(''.join(c for c in price.text.strip() if c.isdigit() or c == '.'))
            site = "Nykaa"
            product_url = urls.get_attribute('href')
            # image_url = img.get_attribute('src')
            products.append({'name': temp_name, 'price': temp_price, 'site': site, 'link': product_url})

        sorted_products = sorted(products, key=lambda x: x['price'])
        return sorted_products

    finally:
        driver.quit()

def scrape_pg(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        products = []

        names=driver.find_elements(By.CLASS_NAME, 'snize-title')
        prices=driver.find_elements(By.CLASS_NAME, 'snize-price')
        wraps=driver.find_elements(By.CLASS_NAME, 'snize-view-link')
        # image waala add karna hai lekin hard hai, nope
        # images=driver.find_elements(By.CLASS_NAME, 'snize-item-image')

        for name, price, urls in zip(names, prices, wraps):
            temp_name = name.text
            temp_price=float(price.text.replace("Rs. ",""))
            site = "Pilgrim Beauty"
            product_url = urls.get_attribute('href')
            # image_url = img.get_attribute('src')
            products.append({'name': temp_name, 'price': temp_price, 'site': site, 'link': product_url})

        sorted_products = sorted(products, key=lambda x: x['price'])
        return sorted_products

    finally:
        driver.quit()

def scrape_tira(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        products = []

        names=driver.find_elements(By.CLASS_NAME, 'product-name')
        prices=driver.find_elements(By.CLASS_NAME, 'discount-price')
        wraps=driver.find_elements(By.CLASS_NAME, 'product-wrap')
        # image waala add karna hai lekin hard hai, nope
        # images=driver.find_elements(By.CLASS_NAME, 'fy__img image')

        for name, price, urls in zip(names, prices, wraps):
            temp_name = name.text
            temporary='-'
            if price.text!='' and temporary not in price.text:
                temp_price=(price.text.replace('₹', ''))
                temp_price2=(temp_price.replace(',', ''))
                temp_price_final=float(temp_price2)
            site = "Tira Beauty"
            product_url = urls.get_attribute('href')
            # image_url = img.get_attribute('src')
            products.append({'name': temp_name, 'price': temp_price_final, 'site': site, 'link': product_url})

        sorted_products = sorted(products, key=lambda x: x['price'])
        return sorted_products

    finally:
        driver.quit()

def scrape_kl(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        products = []

        names=driver.find_elements(By.CLASS_NAME, 'product-title')
        prices=driver.find_elements(By.CLASS_NAME, 'bk-price')
        # image waala add karna hai lekin hard hai, yeh toh bohot fucked hai --> come later
        # images=driver.find_elements(By.CLASS_NAME, 'ty-pict     cm-image ')

        for name, price in zip(names, prices):
            temp_name = name.text
            if price.text!='':
                temp_price=(price.text.replace('₹', ''))
                temp_price2=(temp_price.replace(',', ''))
                temp_price_final=float(temp_price2)
            site = "Kindlife"
            temp_url=name.get_attribute('href')
            # image_url = img.get_attribute('src')
            products.append({'name': temp_name, 'price': temp_price_final, 'site': site, 'link': temp_url})

        sorted_products = sorted(products, key=lambda x: x['price'])
        return sorted_products

    finally:
        driver.quit()

def scrape_and_display_data(user_input):
    # spinner added, come later --> might need few fixes --> not required
    fk_url = 'https://www.flipkart.com/search?q=' + user_input + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    siteflip = ["Flipkart"]
    for site in siteflip:
        with st.spinner(f"Trying to get data from {site}..."):
            time.sleep(3)
            st.success(f"Request to {site} sent successfully!")
    fk_products = scrape_fk(fk_url)

    ny_url = 'https://www.nykaa.com/search/result/?q=' + user_input + '&root=search&searchType=Manual&sourcepage=home'
    sitenykaa= ["Nykaa"]
    for site in sitenykaa:
        with st.spinner(f"Trying to get data from {site}..."):
            time.sleep(1)
            st.success(f"Request to {site} sent successfully!")
    ny_products = scrape_ny(ny_url)

    pg_url = 'https://discoverpilgrim.com/pages/search-results-page?q=' + user_input
    sitepilgrim= ["Pilgrim"]
    for site in sitepilgrim:
        with st.spinner(f"Trying to get data from {site}..."):
            time.sleep(1)
            st.success(f"Request to {site} sent successfully!")
    pg_products = scrape_pg(pg_url)

    tira_url = 'https://www.tirabeauty.com/products/?q=' + user_input
    sitetira= ["Tira Beauty"]
    for site in sitetira:
        with st.spinner(f"Trying to get data from {site}..."):
            time.sleep(1)
            st.success(f"Request to {site} sent successfully!")
    tira_products = scrape_tira(tira_url)

    kl_url = 'https://www.kindlife.in/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q='+ user_input + '&dispatch=products.search'
    sitekindlife= ["Kindlife"]
    for site in sitekindlife:
        with st.spinner(f"Trying to get data from {site}..."):
            time.sleep(1)
            st.success(f"Request to {site} sent successfully!")
    kl_products = scrape_kl(kl_url)
    # be careful here, marking for future reference
    all_products = fk_products + ny_products + pg_products + tira_products + kl_products
    all_products = sorted(all_products, key=lambda x: x['price'])

    return all_products

# tried radio and selectbox --> i think importing option_menu should be the best option here, come back later --> done
st.sidebar.image('pricify.PNG',caption='Pricify',use_column_width=True)
st.sidebar.title("Navigation Menu")
with st.sidebar: 
        app_mode = option_menu("", ["Home", "About"])
if app_mode=="Home":
    st.title("Pricify - Making Every Penny Count")
    user_input = st.text_input("Enter the product you're looking for:")
    if st.button("Search"):
        all_products = scrape_and_display_data(user_input)
        df = pd.DataFrame(all_products)
        df['name'] = df.apply(lambda row: f"<a href='{row['link']}' style='text-decoration: underline;' target='_blank'>{row['name']}</a>", axis=1)
        df['price'] = df['price'].apply(lambda x: f'Rs. {x:.2f}')
        # df['image'] = df.apply(lambda row: f"<img src='{row['image']}' style='max-width:100px;'>", axis=1)
        df = df[['name', 'price', 'site']]
        st.write("Results:")
        # st.markdown(df[['image', 'name', 'price', 'site']].rename(columns={'name': 'Name', 'price': 'Price', 'site': 'Site'}).reset_index(drop=True).to_html(escape=False), unsafe_allow_html=True)
        st.markdown(df.rename(columns={'name': 'Name', 'price': 'Price', 'site': 'Site'}).reset_index(drop=True).to_html(escape=False), unsafe_allow_html=True)
        # st.table(df.rename(columns={'name': 'Name', 'price': 'Price', 'site': 'Site'}).reset_index(drop=True).rename_axis(index=1).style.set_table_styles([{'selector': 'thead tr th', 'props': 'text-align: center;'}]))
        # printing mein issue ho sakta hai be careful come later --> done ig
        csv_file_path = 'products.csv'
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['Name', 'Price', 'Site']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for product in all_products:
                writer.writerow({'Name': product['name'], 'Price': "Rs. " + str(product['price']), 'Site': product['site']})

        st.success(f"Data written to CSV file: {csv_file_path}")

# kuch likhna hai about mein neeche come later --> done
elif app_mode == "About":
        st.title("About Pricify")
        about_text = """
        Welcome to Pricify! Discover and compare makeup products effortlessly.
        Enter the product name, click 'Search', and explore prices from popular online retailers.
        Our user-friendly python-based web application allows you to effortlessly compare makeup products.

        ## Features

        - **Sortable Results:** Compare prices and details in a sortable table.
        - **CSV Export:** Save results to a CSV file for future reference.

        ## Developers

        Built with ❤️ by Anushka (E23CSEU0142) and Ayuj (E23CSEU0142).

        ## Project Information

        - **Project Type:** First-year Python project
        - **Web Scraping Library:** Selenium
        - **Data Analysis:** Pandas
        - **Web Framework:** Streamlit
        - **Version Control:** Git
        - **IDE:** VSCode


        Thank you for using Pricify!
        """
        st.markdown(about_text)