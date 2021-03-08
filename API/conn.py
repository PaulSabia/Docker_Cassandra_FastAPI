from cassandra import cluster

class Connecteur:
    @classmethod
    def connect(cls):
        cls.cluster = cluster.Cluster() #['172.18.0.2', '172.18.0.3'], port=9042
        cls.session = cls.cluster.connect('resto', wait_for_all_pools=True)
        cls.session.execute('USE resto')
    @classmethod
    def disconnect(cls):
        cls.cluster.shutdown()

    @classmethod
    def get_restos(cls, IDresto):
        cls.connect()
        rows = cls.session.execute(f'SELECT * FROM restaurant WHERE id={IDresto}')
        for (id, borough, buildingnum, cuisinetype, name, phone, street, zipcode) in rows:
            dic = {
                'id': id,
                'borough': borough,
                'buildingnum': buildingnum,
                'cuisinetype': cuisinetype,
                'name': name, 
                'phone': phone,
                'street': street,
                'zipcode': zipcode
            }
        cls.disconnect()
        return dic

    @classmethod
    def get_resto_type(cls, cuisinetype):
        cls.connect()
        rows = cls.session.execute(f"SELECT name FROM restaurant WHERE cuisinetype='{cuisinetype}'")
        result = []
        for elem in rows[:10]:
            result.append(elem[0])
        cls.disconnect()
        return result

    @classmethod
    def nbr_inspec_resto(cls, IDresto):
        cls.connect()
        rows = cls.session.execute(f"SELECT COUNT(*) FROM inspection WHERE idrestaurant={IDresto}")
        result = []
        for elem in rows:
            result.append(elem[0])
        cls.disconnect()
        return result

    @classmethod
    def resto_grade(cls, grade):
        cls.connect()
        rows = cls.session.execute(f"SELECT idrestaurant FROM inspection WHERE grade='{grade}' GROUP BY idrestaurant limit 10")
        result = []
        for elem in rows:
            resto_name = cls.session.execute(f"SELECT name FROM restaurant WHERE id={elem[0]}")
            for name in resto_name:
                result.append(name[0])
        cls.disconnect()
        return result

#test = Connecteur.get_restos('50041578')
#print(test)

# test_2 = Connecteur.get_resto_type('American')
# print(test_2)

# test_3 = Connecteur.nbr_inspec_resto('41553467')
# print(test_3)

# test_4 = Connecteur.resto_grade('A')
# print(test_4)