import numpy as np
import rdflib
#from pyowm import OWM
g = rdflib.Graph()
g.parse("data/ontologie/onto.owl")

def chercher_produit_par_nom(name):
    print(name)
    print(type(name))
    name_query_1 = """
    SELECT DISTINCT ?p ?o ?produit
       WHERE {
         ?produit onto:appelation "xxx"^^xsd:string ;
                  ?p ?o.
       }""".replace("xxx", name)

    qres = g.query(name_query_1)
    dictionnaire =   {"id" : None,
                      "type" : None,
                      "appelation" : None,
                      "couleur" : None,
                      "materiaux" : None,
                      "marque" : None,
                      "montant" : None,
                      "nombre_reviews" : 0,
                      "note" : None,
                      "solde" : None,
                      "style" : None}
    first = True
    for row in qres:
        if first:
            dictionnaire["id"] = str(row["produit"])
            first = False
        else :
            dictionnaire[str(row["p"]).split('#')[-1]] = str(row["o"]).split('#')[-1]
    return dictionnaire

def chercher_produit_par_id(id):
    dictionnaire = None
    name_query_1 = """
    SELECT DISTINCT ?p ?o
    WHERE {
        onto:xxx ?p ?o.
    }""".replace("xxx", id)

    qres = g.query(name_query_1)
    dictionnaire = {"id" : "http://data.pariscite.fr/def/onto#" + str(id),
                      "type" : None,
                      "appelation" : None,
                      "couleur" : None,
                      "materiaux" : None,
                      "marque" : None,
                      "montant" : None,
                      "nombre_reviews" : 0,
                      "note" : None,
                      "solde" : None,
                      "style" : None}
    first = True
    for row in qres:        
        if first:
            first = False
        else :
            dictionnaire[str(row["p"]).split('#')[-1]] = str(row["o"]).split('#')[-1]
    return dictionnaire

def liste_produits_nom():
    name_query_2 = """
    SELECT DISTINCT ?name ?produit
       WHERE {
         ?produit onto:appelation ?name.
       }
       """

    qres = g.query(name_query_2)
    dictionnaire = []
    for row in qres:
        dictionnaire.append({"id" : str(row["produit"]).split('#')[-1],
                             "produit" : str(row["produit"]), 
                             "name" : str(row["name"])})
    return dictionnaire

def liste_produits_prix():
    name_query_5 = """
    SELECT DISTINCT ?prix ?produit
       WHERE {
         ?produit onto:montant ?prix ;
                  onto:appelation ?name.
       }
       ORDER BY (?prix)
       """

    qres = g.query(name_query_5)
    dictionnaire = []
    for row in qres:
        dictionnaire.append({"id" : str(row["produit"]).split('#')[-1],
                             "produit" : str(row["produit"]), 
                             "prix" : str(row["prix"])})
    return dictionnaire

def liste_produits_categorie(isCat1, categorie):
    if (isCat1) :
        name_query_5 = """
        SELECT DISTINCT ?name ?produit
          WHERE {
            ?produit rdf:type ?type ;
                     onto:appelation ?name.
            ?type rdfs:subClassOf onto:xxx.
          }
          """.replace("xxx", categorie)
        
    else :
        name_query_5 = """
        SELECT DISTINCT ?name ?produit
          WHERE {
            ?produit rdf:type onto:xxx ;
                     onto:appelation ?name.
          }""".replace("xxx", categorie)

    qres = g.query(name_query_5)
    dictionnaire = []
    for row in qres:
        dictionnaire.append({"id" : str(row["produit"]).split('#')[-1],
                             "produit" : str(row["produit"]), 
                             "catégorie" : categorie})
    return dictionnaire
    
def liste_produits_note():
    name_query_5 = """
    SELECT DISTINCT ?note ?nbr ?produit
       WHERE {
         ?produit onto:note ?note ;
                  onto:appelation ?name ;
                  onto:nombre_reviews ?nbr.
       }
       ORDER BY (?note)
       """
  
    dictionnaire = []
    qres = g.query(name_query_5)
    for row in qres:
        dictionnaire.append({"id" : str(row["produit"]).split('#')[-1],
                             "produit" : str(row["produit"]), 
                             "note" : str(row["note"]),
                             "nombre_reviews" : str(row["nbr"])})
    return dictionnaire

def liste_categories():
    name_query_3 = """SELECT ?subClass
                        WHERE { 
                          ?subClass rdfs:subClassOf onto:Produit .
                        }"""
    dictionnaire = []
    qres = g.query(name_query_3)
    for row in qres:
        dictionnaire.append({"id" : str(row["subClass"]),
                             "categorie" : str(row["subClass"]).split('#')[-1]})
        name_query_4 = """SELECT ?subClass
                            WHERE {
                              ?subClass rdfs:subClassOf onto:xxx .
                            }""".replace("xxx", str(row["subClass"]).split('#')[-1])
        qres1 = g.query(name_query_4)
        for row1 in qres1:
            dictionnaire.append({"id" : str(row1["subClass"]),
                                 "categorie" : str(row["subClass"]).split('#')[-1],
                                 "sous_categorie" : str(row1["subClass"]).split('#')[-1]})

    return dictionnaire, qres, qres1

def testisCat1(categorie, qres, qres1):
    isCat1 = None
    stop=0
    while(stop==0):
        for row in qres:
            if str(row[0].split('#')[-1]) == categorie:
                 stop=1
                 isCat1 = True
        for row in qres1:
            if str(row[0].split('#')[-1]) == categorie:
                 stop=1
                 isCat1 = False
        if(stop==0):
            print("Sélectionner une catégorie")
            categorie = input()
    return isCat1