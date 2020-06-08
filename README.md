# ES Client
simple Elasticsearch client for searching products

## Versions

  Python version being used ```3.6.9```
  Elasticsearch version being used ```7.7.1```

### Setting environment  
  Setting environment on the project (make sure you are in the backend folder) (for Windows users, replace bin for Scripts in venv folder)  

    virtualenv venv
    source venv/bin/activate
  
### Install requirements   

     pip install -r requirements.txt

### Run dev server  

    python manage.py runserver 0.0.0.0:8000

### ES Configuration

  Place the synonym file in Elasticsearch configuration folder under custom/products_synonyms.

  Run ES normally, and create the index with the "Index creation" request in the provided Postman collection. After index creation, "Bulk data" can be run and the data is going to be loaded in ES.

  The provided data contains different types and brands of dried pasta, brands are "Lucchetti", "Carozzi", "Acuenta", "Tottus", types are "Espirales", "Canutos", "Spagetti", "Corbatas", "Canelones". The supermarkets are "Lider", located at "-33.45, -70.6214", and "Tottus" located at "-33.442,-70.626". 

### Payload

	{
		"term":"fideos",
		"address":{
			"country":"cl",
			"location":"-33.46117,-70.618"
		},
		"preferences":["cocacola","cristal","carozzi"],
		"distance": "3km"
	}

  In this example "fideos" is not present in the data shared, but it is matched as a synonym. 
  Within "preferences", "carozzi" can be changed by "Lucchetti" and the order of the result is going to be changed. Also "acuenta" or "tottus" (which are a product brand specific from Lider and Tottus) can be used, and this brand is going to be put more relevance. Nevertheless, if Lider is not within the provided distance from the provided location, this preference is not going to alter the result. 

  "address" is the user address, and "location" is a string in the format "lat, lon", for the exercise purpose, it is the same that retrieved from google maps. For the provided location, "Tottus" and "Lider" are within 3KM, but only "Lider" is within 2km.

  "distance" is the distance range the store can be from the provided location (here location is assumed to be user location)