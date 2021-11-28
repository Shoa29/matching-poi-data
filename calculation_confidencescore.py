import math
import numpy as np
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class CalculateConfidenceScore:
    def calcGeoDistance(self, origin_lat, origin_long, res_lat, res_long):
        """
        :param origin_lat: original latitude in osm_poi
        :param origin_long: original longitude in osm_poi
        :param res_lat: matched latitude in google_poi
        :param res_long: matched longitude in google_poi
        :return: distance calculated in Km between original lat and longitude
        """
        o_lat= np.radians(origin_lat)
        o_long = np.radians(origin_long)
        r_lat= np.radians(res_lat)
        r_long = np.radians(res_long)
        dlong = r_long - o_long
        dlat = r_lat - o_lat
        a = math.sin(dlat / 2) ** 2 + math.cos(o_lat) * math.cos(r_lat) * math.sin(dlong / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6373.0
        distance = R * c
        return distance

    def clean_str(self, text):
        """

        :param text:
        :return: text with removed punctuations
        """
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        return text

    def cos_sim(self, vecs1, vecs2):
        """
        :param vecs1:vectorized first string
        :param vecs2: vectorized second string of query
        :return: cosine similarity score of both strings
        """
        vecs1 = vecs1.reshape(1, -1)
        vecs2 = vecs2.reshape(1, -1)
        return cosine_similarity(vecs1, vecs2)[0][0]

    def calcStringSimilarity(self, google_string, query):
        """
        Calculating string similarity to return confidence score
        :param google_string: name + tags + address
        :param query:
        :return: cosine similarity between match and query
        """
        str_arr = [google_string, query]
        new_str = list(map(self.clean_str, str_arr))
        vectorizer = CountVectorizer().fit_transform(new_str)
        str_vector = vectorizer.toarray()
        return self.cos_sim(str_vector[0], str_vector[1])


