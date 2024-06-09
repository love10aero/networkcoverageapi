# Backend developer technical test

<aside>
💡 papernest product team wants to start selling mobile phone contracts in our web app. In order to help users choose the best provider, we want to provide hints with the network coverage at home. We want to implement it on a separate web service.

</aside>

# **Goal**

---

Build a small api project that we can request with a textual address request and retrieve 2G/3G/4G network coverage for each operator (if available) in the response.

## **Example**

---

GET: `your_api/?q=42+rue+papernest+75011+Paris`

Response:

```json
{
	"orange": {"2G": true, "3G": true, "4G": false}, 
	"SFR": {"2G": true, "3G": true, "4G": true}
}
```

## **Data that you can use**

---

[2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/59567297-fab1-4299-8630-4b4ae9977983/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv)

The file above provides a list of network coverage measure. Each line have the provider (20801 = Orange, 20810 = SFR, 20815 = Free, 20820 = Bouygue, [source](https://fr.wikipedia.org/wiki/Mobile_Network_Code#Tableau_des_MNC_pour_la_France_m%C3%A9tropolitaine)), Lambert93 geographic coordinate (X, Y) and network coverage for 2G, 3G and 4G

https://adresse.data.gouv.fr/api  This API allow you to retrieve :

- address detail from a query address (the insee code, geographic coordinates, etc.)
- Do reverse geographic search (from longitude and latitude, retrieve an address).

# **Instructions**

---

- Use the language/framework/technology of your choice
- Provide the resulting source code **in a hosted git repository (public is allowed)**
- How you manage these data sources is up to you. Do as you want (you can use other data sources if you want).
- If you transform the csv file with some offline processing, please provide the source file.
- The goal is not to work on precise geographic match, a city-level precision is enough.
- The api interface (payload format) can be changed if you want.

https://docs.djangoproject.com/en/5.0/ref/contrib/gis/tutorial/#setting-up