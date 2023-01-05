import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from lxml import html
from tqdm import tqdm
import numpy as np

def find_category_1(m):
    if "Furniture" in m :
        return "Meuble"
    else :
        if "Rugs" in m:
            return "Tapis"
        else :
            if "Decor" in m:
                return "Décoration"
            else :
                if "bedding" in m:
                    return "Literie"
                else :
                    if "Home-Improvement" in m:
                        return "Aménagement_Intérieur"
                    else :
                        if "Lighting" in m:
                            return "Luminaire"
                        else :
                            return None

def find_category_2(m, category_1):
    if category_1 == "Meuble":
        if "Living" in m :
            return "Meuble_Salon"
        else :
            if "Dining" in m :
                return "Meuble_Salle_à_manger"
            else :
                if "Bedroom" in m :
                    return "Meuble_Chambre"
                else :
                    if "Kitchen" in m :
                        return "Meuble_Cuisine"
                    else :
                        if "Patio" in m :
                            return "Meuble_Terasse"
                        else :
                            if "Office" in m :
                                return "Meuble_Bureau"
                            else :
                                return None
    else :
        if category_1 == "Tapis":
            if "Handmade" in m :
                return "Tapis_Artisanal"
            else :
                if "Bath" in m :
                    return "Tapis_Bain"
                else :
                    if "Kitchen" in m :
                        return "Tapis_Cuisine"
                    else :
                        if "Persian" in m :
                            return "Tapis_Persan"
                        else :
                            if "Outdoor" in m :
                                return "Tapis_Extérieur"
                            else :
                                if "Area" in m :
                                    return "Tapis_Sol"
                                else :
                                    return None
        else :
            if category_1 == "Décoration":
                if "Christmas" in m :
                    return "Décoration_Noël"
                else :
                    if "Wall" in m :
                        return "Décoration_Mur"
                    else :
                        if "Mirrors" in m :
                            return "Mirroir"
                        else :
                            if "Art" in m :
                                return "Art"
                            else :
                                if "Window" in m :
                                    return "Rideaux"
                                else :
                                    if "Accessories" in m :
                                        return "Accessoires"
                                    else :
                                        return None
            else :
                if category_1 == "Literie":
                    if "Pillows" in m :
                        return "Oreiller"
                    else :
                        if "bedding-sets" in m :
                            return "Ensemble_Literie"
                        else :
                            if "comforters" in m :
                                return "Couette"
                            else :
                                if "quilts" in m :
                                    return "Édredon"
                                else :
                                    if "mattress" in m :
                                        return "Matelas"
                                    else :
                                        if "covers" in m :
                                            return "Couverture"
                                        else :
                                            return None
                else :
                    if category_1 == "Aménagement_Intérieur":
                        if "Bathroom" in m :
                            return "Salle_de_bain"
                        else :
                            if "Vacuums" in m :
                                return "Aspirateur"
                            else :
                                if "Flooring" in m :
                                    return "Sol_Mur"
                                else :
                                    if "Appliances" in m :
                                        return "Cuisine"
                                    else :
                                        if "Storage" in m :
                                            return "Rangement"
                                        else :
                                            return None
                    else :
                        if category_1 == "Luminaire":
                            if "Lamps" in m :
                                return "Lampe"
                            else :
                                if "Kitchen" in m :
                                    return "Luminaire_Cuisine"
                                else :
                                    if "Outdoor" in m :
                                        return "Luminaire_Exterieur"
                                    else :
                                        if "Ceiling" in m :
                                            return "Luminaire_Plafond"
                                        else :
                                            return None
                        else :
                            return None

def find_index(tag, tree, body):
    index = 1
    colonne = 1
    test = False
    while (test == False):
        subtree = tree.xpath('//*[@id="' + body + '"]/div/div[2]/div/div[1]/table[1]/tbody/tr[' + str(index) + ']/td[' + str(colonne) + ']/text()')
        if (tag.lower() in subtree[0].lower()):
            colonne = 2
            subtree = tree.xpath('//*[@id="' + body + '"]/div/div[2]/div/div[1]/table[1]/tbody/tr[' + str(index) + ']/td[' + str(colonne) + ']/text()')
            return subtree[0]
        index = index + 1
    
def set_id(df):
    return "prod_" + str(len(df.index))

def set_name(soup):
    found = None
    try :
        res = soup.find(id = "productTitle")
        m = re.search('<h1>(.+?)</h1>', str(res))
        found = None
        if m:
            found = m.group(1)
    except :
        pass
    return found

def set_marque(soup):
    found = None
    try :
        res = soup.find(id = "brand-name")
        m = re.search('<>a/<(.+?)>"', str(res)[::-1])
        found = None
        if m: 
            found = m.group(1)
            found = found[::-1]
    except :
        pass
    return found

def set_note(soup):
    res = None
    try :
        res = float(soup.find(class_ = "background-star-container add-to-cart-rating-stars")['data-rating'])
    except :
        pass
    return res

def set_number_reviews(soup):
    found = None
    try :
        res = soup.find(class_ = "product-info-review-count")
        m = re.search('">(.+?) Reviews</p>', str(res))
        found = None
        if m: 
            found = m.group(1)
    except :
        pass
    return found

def set_montant(soup):
    res = None
    try :
        res = float(soup.find(class_ = "monetary-price-value")['content'])
    except :
        pass
    return res

def set_solde(soup):
    solde = None
    try :
        if soup.find(class_ = "price onSale"):
            solde = True
        elif soup.find(class_ = "price notOnSale"):
            solde = False
    except :
        pass
    return solde

def set_chara(src):
    tree = html.fromstring(src)

    ## Caractéristiques Générales

    list_tags_more = ["Style", "Matière", "Couleur", "Country of Origin"]

    style = None
    try :
        style = find_index(list_tags_more[0], tree, "more")
        style = re.sub(r"(?:[;\n']|\s{2,})",r'',style)
    except :
        pass

    matériaux = None
    try :
        matériaux = find_index(list_tags_more[1], tree, "more")
        matériaux = re.sub(r"(?:[;\n']|\s{2,})",r'',matériaux)
    except :
        pass

    couleur = None
    try :
        couleur = find_index(list_tags_more[2], tree, "more")
        couleur = re.sub(r"(?:[;\n']|\s{2,})",r'',couleur)
    except :
        pass
    
    return style, matériaux, couleur

def parse_products(cat1, cat2, src, df):
    soup = BeautifulSoup(src, 'lxml')
    id = set_id(df)
    name = set_name(soup)
    marque = set_marque(soup)
    montant = set_montant(soup)
    note = set_note(soup)
    number_reviews = set_number_reviews(soup)
    style, matériaux, couleur = set_chara(src)
    solde = set_solde(soup)
    df.loc[len(df.index)] = [id, marque, matériaux, montant, style, couleur, solde, note, number_reviews, name, cat1, cat2]

def scrapping():
    df = pd.DataFrame([], columns=["id", "marque", "matériaux", "montant", "style", "couleur", "solde", "note", "number_reviews", "name", "cat1", "cat2"])           
    res = requests.get('https://www.overstock.com/', headers={"User-Agent": "Requests"}).text

    soup = BeautifulSoup(res, 'lxml')
    #res1 = soup.find_all(class_="TopNav_linksContainer_03")
    res = soup.find_all(class_="TopNav_hoverState_fd")
    #brands = soup.find_all(class_="list-items")
    for cats in tqdm(res, desc="Cats"):
        m = re.search('href="/(.+?)">', str(cats))
        found1 = None
        if m:
            found1 = m.group(1)
        category_1 = find_category_1(found1)
        if category_1:
            res1 = requests.get('https://www.overstock.com/' + str(found1), headers={"User-Agent": "Requests"}).text   
            soup = BeautifulSoup(res1, 'lxml')
            res1 = soup.find_all(class_="leftNav_tierOneLeftnavLi__Ipkyq")
            for sub_cats in tqdm(res1, desc="Sub-cats"):
                m = re.search('href="/(.+?)">', str(sub_cats))
                found2 = None
                if m:
                    found2 = m.group(1)
                category_2 = find_category_2(found2, category_1)
                if category_2 :
                    for page in tqdm(range(0,5), desc="Page"): #il y a 84 pages pour chaque catégorie : nous limitons la recherche à 5 pages
                        res2 = requests.get('https:/' + str(found2) + "?page=" +str(page), headers={"User-Agent": "Requests"}).text
                        soup = BeautifulSoup(res2, 'lxml')
                        res2 = soup.find_all(class_="productCardLink")
                        for product in tqdm(res2, desc="Articles"):
                            m = re.search('href="(.+?)" rel', str(product))
                            found3 = None
                            if m:
                                found3 = m.group(1)
                            res3 = requests.get(str(found3), headers={"User-Agent": "Requests"}).text
                            parse_products(category_1, category_2, res3, df)

    indexes = df[["name", "marque"]].drop_duplicates(subset=None, keep="first", inplace=False).index
    df = df.loc[indexes].to_csv("outputs/products.csv", index= False, sep =";", encoding='utf-8')
    
    df = pd.read_csv("outputs/products.csv", sep=";", encoding="utf-8")
    print(df.head())
    df.replace('', np.nan, inplace=True)
    df.dropna(subset=list(df.columns), inplace=True)
    df = df.rename(columns = {"matériaux": "materiaux"})
    df.marque = df.marque.str.replace("and", "&")
    df.name = df.name.str.replace("and", "&")

    df.montant = df.montant.astype(float)
    df.note = df.note.astype(float)
    df.number_reviews = df.number_reviews.astype(int)
    df.solde = df.solde.astype(bool)

    print(df.dtypes)

    for name in df.cat2.drop_duplicates():
        df.loc[df.cat2 == name].to_excel("outputs/categories/" + str(name) + ".xlsx", index= False, encoding='utf-8')