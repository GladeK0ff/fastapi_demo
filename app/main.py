from fastapi import FastAPI
from .models import ListSchema
import psycopg2

app = FastAPI()

product = ListSchema

conn = psycopg2.connect(dbname="products", user = "postgres", password = "password", host="postgres", port = "5432")

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) not null,
        price FLOAT not null,
        amount SMALLINT not null);
''')

@app.get("/")
async def get_shop_list():
    cur.execute("SELECT * FROM products;")
    result = cur.fetchall()
    if result:
        return result
    return {"msg": "база пуста"}

@app.get("/one/{id}")
async def get_one(id: int):
    cur.execute(f"SELECT * FROM products where id = {id};")
    result = cur.fetchall()
    if result:
        return result
    return {"msg": f"нет такого продукта с id {id}"}

@app.post("/add")
async def add_product(product: ListSchema):
    cur.execute(f'''INSERT into products(name, price, amount)
                values ('{product.name}', '{product.price}', '{product.amount}');
                ''')
    conn.commit()
    return {"msg": "вы добавили в базу продукт!!!"}

@app.put("/change/{id}")
async def change_product(product: ListSchema, id: int):
    cur.execute(f"SELECT * FROM products where id = {id};")
    result = cur.fetchall()
    if result:
        cur.execute(f'''UPDATE products SET
                    name = '{product.name}',
                    price = '{product.price}',
                    amount = '{product.amount}'
                    where id = '{id}';''')
        conn.commit()
        return {"msg": f"Вы изменили продукт с id {id}"} 
    return {"msg": f"В базе нет продукта с id {id}"}
    

@app.delete("/delete/{id}")
async def delete_product(id: int):
    cur.execute(f"SELECT * FROM products where id = {id};")
    result = cur.fetchall()
    if result:
        cur.execute(f"DELETE from products where id = {id};")
        conn.commit()
        return {f"Вы удалили продукт из базы с id {id}"}
    return {"msg": f"В базе нет продукта с id {id}"}