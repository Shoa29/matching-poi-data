from clean_data import cleanData
from calculation_confidencescore import CalculateConfidenceScore

if __name__ == '__main__':
    cleanerObj = cleanData()
    #cleaning dataframes
    osm_df = cleanerObj.csvToDataframe("osm_poi.csv")
    google_df = cleanerObj.csvToDataframe("google_poi.csv")
    match_results_df = cleanerObj.csvToDataframe("google_osm_poi_matching.csv")
    google_df = cleanerObj.cleanGmapDf(google_df)
    # obj for calculating confidence score class
    calcobj = CalculateConfidenceScore()
    geoDist = [] # will store distance between match and query geolocations
    string_scores = [] # stores the similarity score of match and query strings
    for row in range(len(match_results_df)):
        osmid = match_results_df.loc[row, 'osm_id']
        google_id = match_results_df.loc[row, 'internal_id']
        query = str(match_results_df.loc[row, 'query'])
        #gathering resultant and osm_poi longitude and latitude
        r_lat = google_df.loc[google_df['internal_id'] == google_id, 'latitude']
        r_long = google_df.loc[google_df['internal_id'] == google_id, 'longitude']
        o_lat = osm_df.loc[osm_df['osm_id'] == osmid, 'latitude']
        o_long = osm_df.loc[osm_df['osm_id'] == osmid, 'longitude']
        try:
            dist = calcobj.calcGeoDistance(float(o_lat), float(o_long), float(r_lat), float(r_long))#calculating distance between geolocations
            geoDist.append(dist)
        except:
            geoDist.append(10000)
        google_name = str(google_df.loc[google_df['internal_id'] == google_id, 'name'])
        google_address = str(google_df.loc[google_df['internal_id'] == google_id, 'address'])
        google_tags = str(google_df.loc[google_df['internal_id'] == google_id, 'tags'])
        google_string = google_name + google_address + google_tags
        if dist > 10:  # if distance between matched and query poi is small then dont check string similarity
            string_scores.append(calcobj.calcStringSimilarity(google_string, query))
        else:
            string_scores.append(1)
    geo_scores = list(map(lambda x: (1 / (1 + x)), geoDist))#calculating similarity score of distance calculated by inverting
    confidence_scores = C = [((a + b) / 2) for a, b in zip(geo_scores, string_scores)] #taking average of string and geolocations confidence score
    match_results_df['confidence_scores'] = confidence_scores
    match_results_df.to_csv("data/match_results.csv")


