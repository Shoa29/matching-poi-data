import csv
import pandas as pd

class cleanData:
    def csvToDataframe(self, filename):
        """
        Formatting CSV Files
        """
        with open("data/" + filename, encoding="utf8") as file:
            csvreader = csv.reader(file)
            rows = []
            for row in csvreader:
                new_row = ''.join([str(r) for r in row])
                rows.append(new_row)
        with open("data/" + filename, "w", encoding="utf8") as file:
            csvwriter = csv.writer(file)
            for row in rows:
                if row.find('"{') != -1: #handling wrong format in osm_poi
                    start = row.find('"{')
                    end = row.find('}"')
                    temp = row[start:end + 2]
                    jsonstr = temp.replace(';', '')
                    row = row.replace(temp, jsonstr)
                    row = row.replace('"','')
                csvwriter.writerow([row.replace('""', '')])
        df = pd.read_csv("data/" + filename, sep=";", error_bad_lines=False)
        df.to_csv("data/" + filename)
        return df

    def cleanGmapDf(self, google_df):
        """
        Formatting address and tags column for google_poi dataframe
        :param google_df:
        :return: google_df
        """
        google_df['address'].replace('{', '', inplace=True)
        google_df['address'].replace('}', '', inplace=True)
        google_df['tags'].replace('{', '', inplace=True)
        google_df['tags'].replace('}', '', inplace=True)
        return google_df

