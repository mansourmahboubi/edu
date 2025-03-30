# tag::import[]
# Import the neo4j dependency
import os

from neo4j import GraphDatabase

# end::import[]


uri = os.getenv("neo4j_uri")
username = os.getenv("neo4j_username")
password = os.getenv("neo4j_password")

"""
Example Authentication token.
You can pass the username and password as a tuple.
"""

# tag::auth[]
auth = (username, password)
# end::auth[]

# tag::driver[]
# Create a new Driver instance
driver = GraphDatabase.driver(
    uri,
    auth=(username, password),
    max_connection_lifetime=30 * 60,
    max_connection_pool_size=50,
    connection_acquisition_timeout=2 * 60,
)
# end::driver[]


"""
Here is the pseudocode for creating the Driver:

# tag::pseudo[]
driver = GraphDatabase.driver(
  connectionString, // <1>
  auth=(username, password), // <2>
  **configuration // <3>
)
# end::pseudo[]

The first argument is the connection string, it is constructed like so:

# tag::connection[]
  address of server
          ↓
neo4j://localhost:7687
  ↑                ↑
scheme        port number
# end::connection[]
"""

# tag::verifyConnectivity[]
# Verify the connection details
driver.verify_connectivity()
# end::verifyConnectivity[]


"""
# tag::sessionWithArgs[]
with driver.session(database="people") as session:
# end::sessionWithArgs[]
"""

# tag::importWithSession[]
# N/A
# end::importWithSession[]

# tag::driver.session[]
with driver.session() as session:
    # end::driver.session[]

    # tag::session.run[]
    session.run(
        "MATCH (p:Person {name: $name}) RETURN p",  # Query
        name="Tom Hanks",  # Named parameters referenced
    )  # in Cypher by prefixing with a $
    # end::session.run[]

    # tag::session.readTransaction[]
    # Define a Unit of work to run within a Transaction (`tx`)
    def get_movies(tx, title):
        result = tx.run(
            """
            MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
            WHERE m.title = $title // <1>
            RETURN p.name AS name
            LIMIT 10
        """,
            title=title,
        )
        return result.values()

    # Execute get_movies within a Read Transaction
    a = session.execute_read(get_movies, title="Arthur")  # <2>
    print(a)
    # end::session.readTransaction[]

    """
    # tag::session.writeTransaction[]
    # Call tx.run() to execute the query to create a Person node
    def create_person(tx, name):
        return tx.run(
            "CREATE (p:Person {name: $name})",
            name=name
        )


    # Execute the `create_person` "unit of work" within a write transaction
    session.execute_write(create_person, name="Michael")
    # end::session.writeTransaction[]
    """

    # tag::session.beginTransaction[]
    with session.begin_transaction() as tx:
        # Run queries by calling `tx.run()`
        # end::session.beginTransaction[]

        """
        # tag::session.beginTransaction.Try[]
        try:
            # Run a query
            tx.run(query, **params)

            # Commit the transaction
            tx.commit()
        except:
            # If something goes wrong in the try block,
            # then rollback the transaction
            tx.rollback()
        # end::session.beginTransaction.Try[]
        """

    session.close()


# tag::createPerson[]
def create_person_work(tx, name):
    return tx.run("CREATE (p:Person {name: $name}) RETURN p", name=name).single()


def create_person(name):
    # Create a Session for the `people` database
    session = driver.session(database="people")

    # Create a node within a write transaction
    record = session.execute_write(create_person_work, name=name)

    # Get the `p` value from the first record
    person = record["p"]

    # Close the session
    session.close()

    # Return the property from the node
    return person["name"]


# if __name__ == "__main__":
#     a = create_person("Mansour")
