import sqlite3

import numpy as np

domains = ['smartphone_tablet', 'laptop', 'camera']
dbs = {}

for domain in domains:
    db = 'db/{}-dbase.db'.format(domain)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    dbs[domain] = c

def oneHotVector(num, domain, vector):
    """Return number of available entities for particular domain."""
    number_of_options = 6
    if domain != 'train':
        idx = domains.index(domain)
        if num == 0:
            vector[idx * 6: idx * 6 + 6] = np.array([1, 0, 0, 0, 0,0])
        elif num == 1:
            vector[idx * 6: idx * 6 + 6] = np.array([0, 1, 0, 0, 0, 0])
        elif num == 2:
            vector[idx * 6: idx * 6 + 6] = np.array([0, 0, 1, 0, 0, 0])
        elif num == 3:
            vector[idx * 6: idx * 6 + 6] = np.array([0, 0, 0, 1, 0, 0])
        elif num == 4:
            vector[idx * 6: idx * 6 + 6] = np.array([0, 0, 0, 0, 1, 0])
        elif num >= 5:
            vector[idx * 6: idx * 6 + 6] = np.array([0, 0, 0, 0, 0, 1])

    return vector

def queryResult(domain, agent_metadata):
    """Returns the list of entities for a given domain
    based on the annotation of the belief state"""
    # query the db
    sql_query = "select * from {}".format(domain)

    flag = True
    #print turn['metadata'][domain]['semi']
    for key, val in agent_metadata[domain].items():
        if val == "Not mentioned":
            pass
        else:
            if flag:
                # sql_query += " where "
                val2 = val
                # val2 = val.replace("'", "''")
                #val2 = normalize(val2)
                # change query for trains
                if key == 'cost':
                    flag = False
                    if domain == 'smartphone_tablet':
                        sql_query += " where " + r" " + "approx_price_EUR" + " < " + r"'" + val2 + r"'"
                    elif domain == 'laptop':
                        sql_query += " where " + r" " + "discount_price" + " < " + r"'" + val2 + r"'"
                    elif domain == 'camera':
                        sql_query += " where " + r" " + "Price" + " < " + r"'" + val2 + r"'"
                    # sql_query += r" " + key + " < " + r"'" + val2 + r"'"
                elif key == 'camera':
                    flag = False
                    sql_query += " where " + r" " + "P_Camera" + " > " + r"'" + val2 + r"'"
                elif key == 'ram' and domain == 'smartphone_tablet':
                    flag = False
                    sql_query += " where " + r" " + "RAM" + " > " + r"'" + val2 + r"'"
                elif key == 'battery' and domain == 'smartphone_tablet':
                    flag = False
                    sql_query += " where " + r" " + "Battery" + " > " + r"'" + val2 + r"'"
                elif key == 'model' and domain == 'smartphone_tablet':
                    flag = False
                    sql_query += " where " + r" " + "model" + "=" + r"'" + val2 + r"'"
                elif key == 'color' and domain == 'smartphone_tablet':
                    flag = False
                    sql_query += " where " + r" " + "Color" + "=" + r"'" + val2 + r"'"
                elif key == 'brand':
                    flag = False
                    if domain == 'smartphone_tablet':
                        sql_query += " where " + r" " + "brand" + "=" + r"'" + val2 + r"'"
                    elif domain == 'laptop':
                        sql_query += " where " + r" " + "brand" + "=" + r"'" + val2 + r"'"
                    elif domain == 'camera':
                        sql_query += " where " + r" " + "Model" + "=" + r"'" + val2 + r"'"
            else:
                val2 = val
                # val2 = val.replace("'", "''")
                #val2 = normalize(val2)
                if key == 'cost':
                    if domain == 'smartphone_tablet':
                        sql_query += r" and " + "approx_price_EUR" + " < " + r"'" + val2 + r"'"
                    elif domain == 'laptop':
                        sql_query += r" and " + "discount_price" + " < " + r"'" + val2 + r"'"
                    elif domain == 'camera':
                        sql_query += r" and " + "Price" + " < " + r"'" + val2 + r"'"
                    # sql_query += r" " + key + " < " + r"'" + val2 + r"'"
                elif key == 'camera':
                    sql_query += r" and " + "P_Camera" + " > " + r"'" + val2 + r"'"
                elif key == 'ram' and domain == 'smartphone_tablet':
                    sql_query += r" and " + "RAM" + " > " + r"'" + val2 + r"'"
                elif key == 'battery' and domain == 'smartphone_tablet':
                    sql_query += r" and " + "Battery" + " > " + r"'" + val2 + r"'"
                elif key == 'model' and domain == 'smartphone_tablet':
                    sql_query += r" and " + "model" + "=" + r"'" + val2 + r"'"
                elif key == 'color' and domain == 'smartphone_tablet':
                    sql_query += r" and " + "Color" + "=" + r"'" + val2 + r"'"
                elif key == 'brand':
                    if domain == 'smartphone_tablet':
                        sql_query += r" and " + "brand" + "=" + r"'" + val2 + r"'"
                    elif domain == 'laptop':
                        sql_query += r" and " + "brand" + "=" + r"'" + val2 + r"'"
                    elif domain == 'camera':
                        sql_query += r" and " + "Model" + "=" + r"'" + val2 + r"'"

    #try:  # "select * from attraction  where name = 'queens college'"
    # print(sql_query)
    #print domain
    if flag == False:
        num_entities = len(dbs[domain].execute(sql_query).fetchall())
    else:
        num_entities = 2000
    return num_entities