from flask import Flask, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

uri = "bolt://localhost:7687"
user = "neo4j"
password = "novasenha"
driver = GraphDatabase.driver(uri, auth=(user, password))

@app.route('/aluno/<cpf>', methods=['GET'])
def get_aluno_treinos(cpf):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Aluno {CPF: $cpf})-[:REALIZADO_POR]-(t:Treino)
            RETURN t.codTreino AS codTreino, t.duracao AS duracao, t.foco AS foco
        """, cpf=cpf)
        treinos = [{"codTreino": record["codTreino"], "duracao": record["duracao"], "foco": record["foco"]} for record in result]
        return jsonify(treinos)

@app.route('/instrutor/<cpf>', methods=['GET'])
def get_instrutor_treinos(cpf):
    with driver.session() as session:
        result = session.run("""
            MATCH (i:Instrutor {CPF: $cpf})-[:ORIENTADO_POR]-(t:Treino)
            RETURN t.codTreino AS codTreino, t.duracao AS duracao, t.foco AS foco
        """, cpf=cpf)
        treinos = [{"codTreino": record["codTreino"], "duracao": record["duracao"], "foco": record["foco"]} for record in result]
        return jsonify(treinos)

@app.route('/plano/<codPlano>', methods=['GET'])
def get_plano(codPlano):
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Plano {codPlano: $codPlano})
            RETURN p.codPlano AS codPlano, p.categoria AS categoria, p.preço AS preco
        """, codPlano=codPlano)
        plano = result.single()
        return jsonify({"codPlano": plano["codPlano"], "categoria": plano["categoria"], "preco": plano["preco"]})

@app.route('/exercicio/<codExerc>', methods=['GET'])
def get_exercicio(codExerc):
    with driver.session() as session:
        result = session.run("""
            MATCH (e:Exercicio {codExerc: $codExerc})-[:USA]->(eq:Equipamento)
            RETURN e.codExerc AS codExerc, e.nome AS nome, eq.codEquip AS codEquip, eq.nome AS equipNome, eq.quantidade AS quantidade
        """, codExerc=codExerc)
        exercicios = [{"codExerc": record["codExerc"], "nome": record["nome"], "codEquip": record["codEquip"], "equipNome": record["equipNome"], "quantidade": record["quantidade"]} for record in result]
        return jsonify(exercicios)

if __name__ == '__main__':
    app.run(debug=True)
