from neo4j import GraphDatabase



def create_merge_dados(driver):
    with driver.session() as session:
        session.run("""
        
        MERGE (n:Aluno {CPF: "12345678900"})
        ON CREATE SET n.nome = "Vinicius", 
                      n.telefone = "99213141241", 
                      n.sexo = "M", 
                      n.dtNascimento = "19/12/1998", 
                      n.email = "vini@gmail.com",
                      n.peso = 70,
                      n.altura = 1.83,
                      n.codPlano = "P001"
        ON MATCH SET n.nome = "Vinicius", 
                     n.telefone = "99213141241", 
                     n.sexo = "M", 
                     n.dtNascimento = "19/12/1998", 
                     n.email = "vini@gmail.com",
                     n.peso = 70,
                     n.altura = 1.83,
                     n.codPlano = "P001"
                    

        MERGE (p:Aluno {CPF: "11212543292"})
        ON CREATE SET p.nome = "Gabriela", 
                      p.telefone = "99213141241", 
                      p.sexo = "F", 
                      p.dtNascimento = "20/01/2000", 
                      p.email = "gabi@gmail.com",
                      p.peso = 62,
                      p.altura = 1.60,
                      p.codPlano = "P002"
        ON MATCH SET p.nome = "Gabriela", 
                     p.telefone = "9903583201", 
                     p.sexo = "F", 
                     p.dtNascimento = "19/12/1998", 
                     p.email = "gabi@gmail.com",
                     p.peso = 62,
                     p.altura = 1.60,
                     p.codPlano = "P002"
                    
        MERGE (i:Instrutor {CPF: "892123951923"})
        ON CREATE SET i.nome = "Lucas",
                      i.telefone = "8922102931",
                      i.sexo = "M",
                      i.dtNascimento = "03/04/1999",
                      i.email = "luc@gmail.com",
                      i.peso = 80,
                      i.altura = 1.79,
                      i.nroContrato = 1223,
                      i.salario = 2500.00
        ON MATCH SET i.nome = "Lucas",
                      i.telefone = "8922102931",
                      i.sexo = "M",
                      i.dtNascimento = "03/04/1999",
                      i.email = "luc@gmail.com",
                      i.peso = 80,
                      i.altura = 1.79,
                      i.nroContrato = 1223,
                      i.salario = 2500.00

        MERGE (w:Instrutor {CPF: "09878213202"})
        ON CREATE SET w.nome = "Wanessa",
                      w.telefone = "998448135",
                      w.sexo = "F",
                      w.dtNascimento = "13/12/1985",
                      w.email = "wan@gmail.com",
                      w.peso = 55,
                      w.altura = 1.59,
                      w.nroContrato = 1113,
                      w.salario = 4500.00
        ON MATCH SET i.nome = "Wanessa",
                      w.telefone = "998448135",
                      w.sexo = "F",
                      w.dtNascimento = "13/12/1985",
                      w.email = "wan@gmail.com",
                      w.peso = 55,
                      w.altura = 1.59,
                      w.nroContrato = 1113,
                      w.salario = 4500.00
                    
        MERGE (pl:Plano {codPlano: "P001"})
        ON CREATE SET pl.categoria = "Basic", 
                      pl.preco = 100
        ON MATCH SET pl.categoria = "Basic", 
                     pl.preco = 100
                     
        MERGE (pm:Plano {codPlano: "P002"})
        ON CREATE SET pm.categoria = "Premium", 
                      pm.preco = 200
        ON MATCH SET pm.categoria = "Premium", 
                     pm.preco = 200

        MERGE (tr1:Treino {codTreino: "T001"})
        ON CREATE SET tr1.duracao = 60, 
                      tr1.foco = "Inferiores", 
                      tr1.cpf_instrutor = "892123951923"
        ON MATCH SET tr1.duracao = 60, 
                     tr1.foco = "Inferiores", 
                     tr1.cpf_instrutor = "892123951923"

        MERGE (tr2:Treino {codTreino: "T002"})
        ON CREATE SET tr2.duracao = 45, 
                      tr2.foco = "Superiores", 
                      tr2.cpf_instrutor = "09878213202"
        ON MATCH SET tr2.duracao = 45, 
                     tr2.foco = "Superiores", 
                     tr2.cpf_instrutor = "09878213202"

        MERGE (ex1:Exercicio {codExerc: "E001"})
        ON CREATE SET ex1.nome = "Supino Reto"
        ON MATCH SET ex1.nome = "Supino Reto"

        MERGE (ex2:Exercicio {codExerc: "E002"})
        ON CREATE SET ex2.nome = "Triceps Testa"
        ON MATCH SET ex2.nome = "Triceps Testa"     

        MERGE (ex3:Exercicio {codExerc: "E003"})
        ON CREATE SET ex3.nome = "Agachamento"
        ON MATCH SET ex3.nome = "Agachamento"

        MERGE (ex4:Exercicio {codExerc: "E004"})
        ON CREATE SET ex4.nome = "Leg Press"
        ON MATCH SET ex4.nome = "Leg Press"  
        
        MERGE (eq1:Equipamento {codEquip: "EQ001"})
        ON CREATE SET eq1.nome = "Halter"
        ON MATCH SET eq1.nome = "Halter"
                    
        MERGE (eq2:Equipamento {codEquip: "EQ002"})
        ON CREATE SET eq2.nome = "Polia"
        ON MATCH SET eq2.nome = "Polia"
                    
        MERGE (eq3:Equipamento {codEquip: "EQ003"})
        ON CREATE SET eq3.nome = "Barra Livre"
        ON MATCH SET eq3.nome = "Barra Livre"

        WITH n, p, pl, pm
        MATCH (a:Aluno), (plano:Plano)
        WHERE a.codPlano = plano.codPlano
        MERGE (a)-[:ASSINA]->(plano)
                    
        WITH n, p
        MATCH (n:Aluno {CPF: "12345678900"}), (tr1:Treino {codTreino: "T001"})
        MATCH (p:Aluno {CPF: "11212543292"}), (tr2:Treino {codTreino: "T002"})
        MERGE (n)-[:POSSUI]->(tr1)
        MERGE (p)-[:POSSUI]->(tr2)

        WITH tr1, tr2
        MATCH (i:Instrutor {CPF: "892123951923"}), (tr1:Treino {codTreino: "T001"})
        MATCH (w: Instrutor {CPF: "09878213202"}), (tr2:Treino {codTreino: "T002"})
        MERGE (i)-[:MONTA]->(tr1)
        MERGE (w)-[:MONTA]->(tr2)
                    
        WITH tr1, tr2
        MATCH (tr1:Treino {codTreino: "T001"}), (ex3: Exercicio{codExerc: "E003"})
        MATCH (tr1:Treino {codTreino: "T001"}), (ex4: Exercicio{codExerc: "E004"})
        MATCH (tr2:Treino {codTreino: "T002"}), (ex1: Exercicio{codExerc: "E001"})
        MATCH (tr2:Treino {codTreino: "T002"}), (ex2: Exercicio{codExerc: "E002"})
        MERGE (tr1)-[:ATIVIDADE]->(ex3)
        MERGE (tr1)-[:ATIVIDADE]->(ex4)
        MERGE (tr2)-[:ATIVIDADE]->(ex1)
        MERGE (tr2)-[:ATIVIDADE]->(ex2)

                    
        WITH tr1, tr2
        MATCH (tr1:Treino {codTreino: "T001"}), (ex3: Exercicio{codExerc: "E003"})
        MATCH (tr1:Treino {codTreino: "T001"}), (ex4: Exercicio{codExerc: "E004"})
        MATCH (tr2:Treino {codTreino: "T002"}), (ex1: Exercicio{codExerc: "E001"})
        MATCH (tr2:Treino {codTreino: "T002"}), (ex2: Exercicio{codExerc: "E002"})
        MERGE (tr1)-[:ATIVIDADE]->(ex3)
        MERGE (tr1)-[:ATIVIDADE]->(ex4)
        MERGE (tr2)-[:ATIVIDADE]->(ex1)
        MERGE (tr2)-[:ATIVIDADE]->(ex2)
                    
        WITH ex3, ex2, ex1
        MATCH (ex3: Exercicio{codExerc: "E003"}), (eq3: Equipamento{codEquip: "EQ003"})
        MATCH (ex1: Exercicio{codExerc: "E001"}), (eq1: Equipamento{codEquip: "EQ001"})
        MATCH (ex2: Exercicio{codExerc: "E002"}), (eq2: Equipamento{codEquip: "EQ002"})
        MERGE (ex3)-[:INCLUI]->(eq3)
        MERGE (ex1)-[:INCLUI]->(eq1)
        MERGE (ex2)-[:INCLUI]->(eq2)

        """)

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    # create_unique_constraint(driver)  # Create the constraint
    create_merge_dados(driver)  # Create or update the Pessoa node
    print("Pessoa node created or updated successfully with CPF as unique identifier")
except Exception as e:
    print(f"Erro ao conectar ao Neo4j: {e}")
finally:
    driver.close()
