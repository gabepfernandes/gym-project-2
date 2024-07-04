from neo4j import GraphDatabase

def create_nodes_and_relationships(driver):
    with driver.session() as session:
        session.run("""
        // Criação de nós para Pessoas
        LOAD CSV WITH HEADERS FROM 'file:///pessoas.csv' AS pessoaRow
        MERGE (pessoa:Pessoa {CPF: pessoaRow.CPF, nome: pessoaRow.nome, telefone: pessoaRow.telefone, sexo: pessoaRow.sexo, dtNascimento: pessoaRow.dtNascimento, email: pessoaRow.email})
        WITH pessoaRow

        // Criação de nós para Alunos
        LOAD CSV WITH HEADERS FROM 'file:///alunos.csv' AS alunoRow
        MERGE (aluno:Aluno {CPF: alunoRow.CPF, peso: alunoRow.peso, altura: alunoRow.altura})
        WITH alunoRow
        MATCH (pessoaAluno:Pessoa {CPF: alunoRow.CPF})
        MERGE (pessoaAluno)-[:É_ALUNO]->(aluno)
        WITH alunoRow

        // Criação de nós para Instrutores
        LOAD CSV WITH HEADERS FROM 'file:///instrutores.csv' AS instrutorRow
        MERGE (instrutor:Instrutor {CPF: instrutorRow.CPF, nroContrato: instrutorRow.nroContrato, salário: instrutorRow.salário})
        WITH instrutorRow
        MATCH (pessoaInstrutor:Pessoa {CPF: instrutorRow.CPF})
        MERGE (pessoaInstrutor)-[:É_INSTRUTOR]->(instrutor)
        WITH instrutorRow

        // Criação de nós para Planos
        LOAD CSV WITH HEADERS FROM 'file:///planos.csv' AS planoRow
        MERGE (plano:Plano {codPlano: planoRow.codPlano, categoria: planoRow.categoria, preço: planoRow.preço})
        WITH planoRow

        // Criação de nós para Treinos
        LOAD CSV WITH HEADERS FROM 'file:///treinos.csv' AS treinoRow
        MERGE (treino:Treino {codTreino: treinoRow.codTreino, duracao: treinoRow.duracao, foco: treinoRow.foco})
        WITH treinoRow
        MATCH (instrutorTreino:Instrutor {CPF: treinoRow.cpf_instrutor})
        MERGE (treino)-[:ORIENTADO_POR]->(instrutorTreino)
        WITH treinoRow

        // Criação de nós para Exercícios
        LOAD CSV WITH HEADERS FROM 'file:///exercicios.csv' AS exercicioRow
        MERGE (exercicio:Exercicio {codExerc: exercicioRow.codExerc, nome: exercicioRow.nome})
        WITH exercicioRow

        // Criação de nós para Equipamentos
        LOAD CSV WITH HEADERS FROM 'file:///equipamentos.csv' AS equipamentoRow
        MERGE (equipamento:Equipamento {codEquip: equipamentoRow.codEquip, nome: equipamentoRow.nome})
        WITH equipamentoRow

        // Criação de atividades (Treino-Exercício)
        LOAD CSV WITH HEADERS FROM 'file:///atividades.csv' AS atividadeRow
        MATCH (treinoAtividade:Treino {codTreino: atividadeRow.codTreino}), (exercicioAtividade:Exercicio {codExerc: atividadeRow.codExerc})
        MERGE (treinoAtividade)-[:CONTÉM {nroSeries: atividadeRow.nroSeries}]->(exercicioAtividade)
        WITH atividadeRow

        // Criação de participações (Treino-Aluno)
        LOAD CSV WITH HEADERS FROM 'file:///participacoes.csv' AS participacaoRow
        MATCH (treinoParticipacao:Treino {codTreino: participacaoRow.codTreino}), (alunoParticipacao:Aluno {CPF: participacaoRow.cpf_aluno})
        MERGE (treinoParticipacao)-[:REALIZADO_POR]->(alunoParticipacao)
        WITH participacaoRow

        // Criação de utilizações (Exercício-Equipamento)
        LOAD CSV WITH HEADERS FROM 'file:///utiliza.csv' AS utilizacaoRow
        MATCH (exercicioUtilizacao:Exercicio {codExerc: utilizacaoRow.codExerc}), (equipamentoUtilizacao:Equipamento {codEquip: utilizacaoRow.codEquip})
        MERGE (exercicioUtilizacao)-[:USA]->(equipamentoUtilizacao)
        """)

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    create_nodes_and_relationships(driver)
    print("Banco de dados criado com sucesso")
except Exception as e:
    print(f"Erro ao conectar ao Neo4j: {e}")
finally:
    driver.close()
