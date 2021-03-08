from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn
#from conn import Connecteur
from cassandra import cluster

class Connecteur:
    @classmethod
    def connect(cls):
        cls.cluster = cluster.Cluster(['172.18.0.2', '172.18.0.3'], port=9042) #['172.18.0.2', '172.18.0.3'], port=9042
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


app = FastAPI()

@app.get('/api/get_infos_resto')
async def get_infos_resto(IDresto: int):
    result = Connecteur.get_restos(IDresto)
    return jsonable_encoder(result)

@app.get('/api/get_resto_type')
async def get_resto_type(cuisinetype: str):
    result = Connecteur.get_resto_type(cuisinetype)
    return jsonable_encoder(result)

@app.get('/api/nbr_inspec_resto')
async def nbr_inspec_resto(IDresto: int):
    result = Connecteur.nbr_inspec_resto(IDresto)
    return jsonable_encoder(result)

@app.get('/api/resto_grade')
async def resto_grade(grade: str):
    result = Connecteur.resto_grade(grade)
    return jsonable_encoder(result)

# if __name__ == '__main__':
#     uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)



