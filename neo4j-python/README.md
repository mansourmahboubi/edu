# Neo4j

```
pytest tests/01_connect_to_neo4j__test.py -v --log-cli-level=DEBUG
```

> A session is a container for a sequence of transactions. Sessions borrow connections from a pool as required and are considered lightweight and disposable.

> A transaction comprises a unit of work performed against a database. It is treated in a coherent and reliable way, independent of other transactions.

ACID Transactions = atomic, consistent, isolated, and durable

1. Auto-commit Transactions
   1. The driver will not repeat query in term of erros
2. Read Transactions
   1. You do not need to explicitly commit a read transaction.
3. Write Transactions

   1. In clustered environments, write queries are sent exclusively to the leader of the cluster.
   2.

# test

1. peek
2. keys
3. single
4. value
5. values
6. python dictionary

#test

#test

6. There are three schemas `neo4j`, `neo4j+s`, `neo4j+ssc`(and bolt).
7. https://graphacademy.neo4j.com/courses/app-python
8. https://neo4j.com/docs/api/python-driver/current/api.html
