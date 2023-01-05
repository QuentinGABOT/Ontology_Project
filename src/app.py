import base64
import json
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import sparql_rdf as rdf
from werkzeug.exceptions import abort

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/recherche")
def recherche():
    choix = request.args.get("choix", "")
    if choix == "nom":
        return redirect("/recherche/produits/nom")
    else:
        if choix == "id":
            return redirect("/recherche/produits/id")
    return (
        """<form action="" method="get">
                Pour effectuer une recherche sur un produit à partir de son nom, tapez "nom" ; à partir de son id, tapez "id": <input type="text" name="choix">
                <input type="submit" value="Valider le choix">
            </form>"""
    )

@app.route("/recherche/produits/nom")
def recherche_produits_nom():
    posts = rdf.liste_produits_nom()
    names = [j[1] for i in posts for j in i.items() if (j[0] == "name")]
    print(names)
    choix = request.args.get("choix", "")
    print(choix)
    print(str(choix) in names)
    if choix in names:
        print(choix)
        produit = rdf.chercher_produit_par_nom(choix)
        return redirect("/" + str(produit["id"].split('#')[-1]))
    return (
        """<form action="" method="get">
                Pour effectuer une recherche sur un produit à partir de son nom, tapez son nom : <input type="text" name="choix">
                <input type="submit" value="Valider le choix">
            </form>"""
    )

@app.route("/recherche/produits/id")
def recherche_produits_id():
    posts = rdf.liste_produits_nom()
    ids = [j[1] for i in posts for j in i.items() if (j[0] == "id")]
    choix = request.args.get("choix", "")
    if choix in ids:
        produit = rdf.chercher_produit_par_id(choix)
        return redirect("/" + str(produit["id"].split('#')[-1]))
    return (
        """<form action="" method="get">
                Pour effectuer une recherche sur un produit à partir de son id, tapez son id : <input type="text" name="choix">
                <input type="submit" value="Valider le choix">
            </form>"""
    )

@app.route("/liste")
def liste():
    choix = request.args.get("choix", "")
    if choix == "produits":
        return redirect("/liste/produits")
    else:
        if choix == "catégories":
            return redirect("liste/categories")
    return (
        """<form action="" method="get">
                Pour accéder à la liste de produits, tapez "produits" ; pour accéder à la liste des catégories, tapez "catégories": <input type="text" name="choix">
                <input type="submit" value="Valider le choix">
            </form>"""
    )

@app.route("/liste/produits")
def liste_produits():
    choix = request.args.get("choix", "")
    if choix == "nom":
        return redirect("/liste/produits/nom")
    else:
        if choix == "catégorie":
            return redirect("/liste/produits/categorie")
        else:
            if choix == "prix":
                return redirect("/liste/produits/prix")
            else:
                if choix == "note":
                    return redirect("/liste/produits/note")
    return (
        """<form action="" method="get">
                Pour accéder à la liste des produits en fonction du nom, tapez "nom" ; en fonction de la note, tapez "note" ; en fonction d'une catégorie, tapez "catégorie" ; en fonction du prix, tapez "prix": <input type="text" name="choix">
                <input type="submit" value="Valider le choix">                
            </form>"""
    )

@app.route("/liste/produits/categorie")
def liste_produits_categorie_choix():
    posts, qres, qres1 = rdf.liste_categories()
    categories = [j[1] for i in posts for j in i.items() if (j[0] == "categorie") or (j[0] == "sous_categorie")]
    choix = request.args.get("choix", "")
    if choix in categories:
        return redirect("/liste/produits/" + str(choix))
    return (
        """<form action="" method="get">
                Pour accéder à la liste des produits en fonction d'une catégorie, entrez une catégorie : <input type="text" name="choix">
                <input type="submit" value="Valider le choix">                
            </form>"""
    )

@app.route("/liste/produits/nom")
def liste_produits_nom():
    posts = rdf.liste_produits_nom()
    return render_template('nom.html', posts=posts)

@app.route("/liste/produits/prix")
def liste_produits_prix():
    posts = rdf.liste_produits_prix()
    return render_template('prix.html', posts=posts)

@app.route("/liste/produits/note")
def liste_produits_note():
    posts = rdf.liste_produits_note()
    return render_template('note.html', posts=posts)

@app.route("/liste/produits/<string:categorie>")
def liste_produits_categorie(categorie):
    dictionnaire, qres, qres1 = rdf.liste_categories()
    isCat1 = rdf.testisCat1(categorie, qres, qres1)
    posts = rdf.liste_produits_categorie(isCat1, categorie)
    return render_template('categorie.html', posts=posts)

@app.route("/liste/categories")
def liste_categories():
    posts, qres, qres1 = rdf.liste_categories()
    return render_template('liste_categorie.html', posts=posts)

@app.route("/<post_id>")
def post(post_id):
    post = get_prod_id(post_id)
    return render_template('post.html', post=post)

def get_prod_id(prod_id):
    post = rdf.chercher_produit_par_id(prod_id)
    if list(post.values()).count(None) == len(post) - 1: #car id ne sera jamais None
        abort(404)
    return post

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)