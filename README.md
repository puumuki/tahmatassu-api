Tahmatassujen reseptikirja 2.0
==============================

+ 2 Pyyttonia
+ 1 Javascript
+ Ripaus HTML5
+ Ripaus CSS

Tahmatassujen reseptikirja on tarkoitettu jokapäiväiseen kotikäyttöön. Kaiken ikäisille ja kaiken karvaisille heeboille.

Kaikki reseptit jotka sivulta löytyvät on testattu ja hyväksi todettuja. Mitään reseptiä ei sivustolle lisätä ellei sitä ole meidän toimesta leivottu, paistettu tai kokattu. Ja tietysti maistettu. Reseptit ja lähdekoodit vapaasti omaan käyttöön.


Olen itse ajanut sovellusta Python 2.7 versiolla, Raspberry PI:lläni, jossa pyöritän sovellusta
screessä. En ole vielä raaskiutunut opistekemaan sen parempia hostaus mahdollisuuksia, tiedän
että Flask-sovelluksen saa pyörimään monessa sovelluspalvelinkehyksessä. Täytyisi varmaan tutustua aiheeseen :)

Asentaminen:

Mene projektin hakemistoon ja asenna tahmatassu-moduuli järjestelmään:

> python setup.py install

Asenna flask webserveri kirjasto

> pip install flask

Asenna markdown2 moduuli järjestelmään

> pip install markdown2

tai

> git clone https://github.com/trentm/python-markdown2

Siirry markdown2 kansioon

> python setup.py install

Käynnistät palvelimen oletuksena porttiin 8080:

python server/server.py 