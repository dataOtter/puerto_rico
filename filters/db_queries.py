import mysql_query_fuctions as q
import constants as c


def get_db_city_agegroup():
    query1 = "SELECT SUM(EP2 < 30) AS 'in 20s', SUM(29 < EP2 AND EP2 < 40) AS 'in 30s', " \
            "SUM(39 < EP2 AND EP2 < 50) AS 'in 40s', SUM(49 < EP2) AS '50+', DM1 " \
            "FROM p1_screenings INNER JOIN p1_interviews ON p1_screenings.rds_id = p1_interviews.rds_id " \
            "GROUP BY DM1"
    result1 = q.execute_query_return_raw(query1)
    #print(result1)
    query2 = "SELECT SUM(P2FIAGE < 30) AS 'in 20s', SUM(29 < P2FIAGE AND P2FIAGE < 40) AS 'in 30s', " \
             "SUM(39 < P2FIAGE AND P2FIAGE < 50) AS 'in 40s', SUM(49 < P2FIAGE) AS '50+', P2FIDM1 " \
             "FROM p2_first_interviews GROUP BY P2FIDM1"
    result2 = q.execute_query_return_raw(query2)
    #print(result2)
    # get those cities recorded only in one of the interview phases
    p1_cities, p2_cities = [], []
    for label, city in c.CITY_LABELS_P1.items():
        p1_cities.append(city)
    for label, city in c.CITY_LABELS_P2.items():
        p2_cities.append(city)
    diff_cities = list(set(p1_cities).symmetric_difference(set(p2_cities)))

    data_list_dict = []

    for row1 in result1:
        city1 = c.CITY_LABELS_P1[row1[-1]]
        if city1 in diff_cities:  # if this city is only recorded in phase 1, add its values to the list of dictionaries
            #data_list_dict = add_dict_to_list(city1, data_list_dict,  row1)
            add_dict_to_list(city1, data_list_dict, row1)
            break

        for row2 in result2:
            city2 = c.CITY_LABELS_P2[row2[-1]]
            if city1 == city2:  # if this city is recorded in phase 1 and 2, add the values to the list of dictionaries
                #data_list_dict = add_dict_to_list(city1, data_list_dict, row1, row2)
                add_dict_to_list(city1, data_list_dict, row1, row2)
                break

    for row in result2:
        city = c.CITY_LABELS_P2[row[-1]]
        if city in diff_cities:  # if this city is only recorded in phase 2, add its values to the list of dictionaries
            #data_list_dict = add_dict_to_list(city, data_list_dict, row)
            add_dict_to_list(city, data_list_dict, row)

    return data_list_dict


def add_dict_to_list(city, list_dict, row1, row2=()):
    if len(row2) == 0:
        row2 = [0] * len(row1)
    temp_dict = {'City': city,
                 'freq': {'twenties': int(row1[0] + row2[0]),
                          'thirties': int(row1[1] + row2[1]),
                          'forties': int(row1[2] + row2[2]),
                          'fiftyplus': int(row1[3] + row2[3])}}
    list_dict.append(temp_dict)
    #return list_dict
