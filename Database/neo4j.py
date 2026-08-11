import os
from typing import List

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )
)


def create_constraints():

    with driver.session() as session:

        session.run("""
        CREATE CONSTRAINT patient_name IF NOT EXISTS
        FOR (p:Patient)
        REQUIRE p.name IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT diagnosis_name IF NOT EXISTS
        FOR (d:Diagnosis)
        REQUIRE d.name IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT medication_name IF NOT EXISTS
        FOR (m:Medication)
        REQUIRE m.name IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT test_name IF NOT EXISTS
        FOR (t:LabTest)
        REQUIRE t.name IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT hospital_name IF NOT EXISTS
        FOR (h:Hospital)
        REQUIRE h.name IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT doctor_name IF NOT EXISTS
        FOR (d:Doctor)
        REQUIRE d.name IS UNIQUE
        """)


def create_patient(name: str):

    if not name:
        return

    with driver.session() as session:

        session.run(
            """
            MERGE (:Patient {name:$name})
            """,
            name=name
        )


def create_hospital(patient: str, hospital: str):

    if not hospital:
        return

    with driver.session() as session:

        session.run(
            """
            MERGE (p:Patient {name:$patient})
            MERGE (h:Hospital {name:$hospital})
            MERGE (p)-[:VISITED]->(h)
            """,
            patient=patient,
            hospital=hospital
        )


def create_doctor(patient: str, doctor: str):

    if not doctor:
        return

    with driver.session() as session:

        session.run(
            """
            MERGE (p:Patient {name:$patient})
            MERGE (d:Doctor {name:$doctor})
            MERGE (p)-[:TREATED_BY]->(d)
            """,
            patient=patient,
            doctor=doctor
        )


def create_document(patient: str, document_type: str):

    with driver.session() as session:

        session.run(
            """
            MERGE (p:Patient {name:$patient})

            CREATE (d:Document{
                type:$document_type
            })

            MERGE (p)-[:HAS_DOCUMENT]->(d)
            """,
            patient=patient,
            document_type=document_type
        )


def create_diagnosis(patient: str, diagnoses: List[str]):

    with driver.session() as session:

        for diagnosis in diagnoses:

            session.run(
                """
                MERGE (p:Patient {name:$patient})
                MERGE (d:Diagnosis {name:$diagnosis})

                MERGE (p)-[:HAS_DIAGNOSIS]->(d)
                """,
                patient=patient,
                diagnosis=diagnosis
            )


def create_medications(patient: str, medications: List[dict]):

    with driver.session() as session:

        for medicine in medications:

            name = medicine.get("name")

            if not name:
                continue

            session.run(
                """
                MERGE (p:Patient {name:$patient})
                MERGE (m:Medication {name:$medicine})

                MERGE (p)-[:TAKES]->(m)
                """,
                patient=patient,
                medicine=name
            )


def create_lab_tests(patient: str, tests: List[dict]):

    with driver.session() as session:

        for test in tests:

            name = test.get("test")

            if not name:
                continue

            session.run(
                """
                MERGE (p:Patient {name:$patient})
                MERGE (t:LabTest {name:$test})

                MERGE (p)-[:HAS_TEST]->(t)
                """,
                patient=patient,
                test=name
            )


def get_patient_context(patient: str) -> str:

    with driver.session() as session:

        result = session.run(
            """
            MATCH (p:Patient {name:$patient})-[r]->(n)

            RETURN
                type(r) AS relationship,
                labels(n)[0] AS label,
                n.name AS value
            """,
            patient=patient
        )

        context = []

        for record in result:

            context.append(
                f"{record['relationship']} -> {record['label']} : {record['value']}"
            )

        return "\n".join(context)


def close_connection():

    driver.close()