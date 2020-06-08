from elasticsearch_dsl import Search, Q, A

class Requestor:
    '''
        Class to request and parse relevant information to response json
    '''
    def get_matches(self, data):
        country = data['address']['country']

        query = self._build_query(data)

        search = Search(using=country, index='productos-'+country)

        search = search.query(query)
        
        resQ = search.execute()
        
        response = self._post_process(resQ.to_dict())
        
        return response

    # Build query with required fields, optional fields and filter by distance
    def _build_query(self, data):
        matches_query = Q('bool', should=self._build_matches(data['term']))
        
        # distance to be configurable
        filter = Q('geo_distance', distance=data['distance'], storeLocation=data['address']['location'])

        if 'preferences' in data:
            return Q('bool', must=matches_query, should=self._build_matches(' '.join(data['preferences'])), filter=filter)

        return Q('bool', must=matches_query, filter=filter)

    # Query to search with synonym and fuzzy over all the searchable fields
    def _build_matches(self, term):
        return [Q('match', name=term),Q('match', fuzzy_name=term),
                Q('match', description=term),Q('match', fuzzy_description=term),
                Q('match', brand=term),Q('match', fuzzy_brand=term),
                Q('match', type=term),Q('match', fuzzy_type=term),
                Q('match', store=term),Q('match', fuzzy_store=term),]


    # return a dictionary with stores as keys and products as list within
    def _post_process(self, es_resp):
        response = {'Products found': es_resp['hits']['total']['value']}
        if response['Products found'] == 0:
            return response
        
        hits = es_resp['hits']['hits']

        for hit in hits:
            store = hit['_source']['store']
            if store not in response:
                response[store] = []
            response[store].append(hit['_source'])
        
        return response

        


