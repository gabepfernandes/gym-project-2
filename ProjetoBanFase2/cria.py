from neo4j import GraphDatabase

def create_nodes_and_relationships(driver):
    with driver.session() as session:
        session.run("""
        // Criação de nós para Pessoas
        LOAD CSV WITH HEADERS FROM 'file:///pessoas.csv' AS row
        MERGE (p:Pessoa {CPF: row.CPF, nome: row.nome, telefone: row.telefone, sexo: row.sexo, dtNascimento: row.dtNascimento, email: row.email})

        // Criação de nós para Alunos
        LOAD CSV WITH HEADERS FROM 'file:///alunos.csv' AS row
        MERGE (a:Aluno {CPF: row.CPF, peso: row.peso, altura: row.altura})
        MERGE (p:Pessoa {CPF: row.CPF})
        MERGE (p)-[:É_ALUNO]->(a)

        // Criação de nós para Instrutores
        LOAD CSV WITH HEADERS FROM 'file:///instrutores.csv' AS row
        MERGE (i:Instrutor {CPF: row.CPF, nroContrato: row.nroContrato, salário: row.salário, CREF: row.CREF})
        MERGE (p:Pessoa {CPF: row.CPF})
        MERGE (p)-[:É_INSTRUTOR]->(i)

        // Criação de nós para Planos
        LOAD CSV WITH HEADERS FROM 'file:///planos.csv' AS row
        MERGE (pl:Plano {codPlano: row.codPlano, categoria: row.categoria, preço: row.preço})

        // Criação de nós para Treinos
        LOAD CSV WITH HEADERS FROM 'file:///treinos.csv' AS row
        MERGE (t:Treino {codTreino: row.codTreino, duracao: row.duracao, foco: row.foco})
        MERGE (i:Instrutor {CPF: row.cpf_instrutor})
        MERGE (t)-[:ORIENTADO_POR]->(i)

        // Criação de nós para Exercícios
        LOAD CSV WITH HEADERS FROM 'file:///exercicios.csv' AS row
        MERGE (e:Exercicio {codExerc: row.codExerc, nome: row.nome})

        // Criação de nós para Equipamentos
        LOAD CSV WITH HEADERS FROM 'file:///equipamentos.csv' AS row
        MERGE (eq:Equipamento {codEquip: row.codEquip, nome: row.nome, quantidade: row.quantidade})

        // Criação de atividades (Treino-Exercício)
        LOAD CSV WITH HEADERS FROM 'file:///atividades.csv' AS row
        MATCH (t:Treino {codTreino: row.codTreino}), (e:Exercicio {codExerc: row.codExerc})
        MERGE (t)-[:CONTÉM {nroSeries: row.nroSeries}]->(e)

        // Criação de participações (Treino-Aluno)
        LOAD CSV WITH HEADERS FROM 'file:///participacoes.csv' AS row
        MATCH (t:Treino {codTreino: row.codTreino}), (a:Aluno {CPF: row.cpf_aluno})
        MERGE (t)-[:REALIZADO_POR]->(a)

        // Criação de utilizações (Exercício-Equipamento)
        LOAD CSV WITH HEADERS FROM 'file:///utilizacoes.csv' AS row
        MATCH (e:Exercicio {codExerc: row.codExerc}), (eq:Equipamento {codEquip: row.codEquip})
        MERGE (e)-[:USA]->(eq)
        """)

uri = "bolt://localhost:7687"
user = "neo4j"
password = "novasenha"

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    create_nodes_and_relationships(driver)
    print("Banco de dados criado com sucesso")
except Exception as e:
    print(f"Erro ao conectar ao Neo4j: {e}")
finally:
    driver.close()