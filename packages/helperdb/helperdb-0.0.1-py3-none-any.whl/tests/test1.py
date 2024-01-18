import unittest
import asyncio
from helperdb.helperdb import Database

class TestDatabaseMethods(unittest.TestCase):
    async def setUp(self):
        # Setup: Create a Database instance and connect to an in-memory database
        self.db = Database(":memory:")
        await self.db.connect()

    async def tearDown(self):
        # Teardown: Close the database connection
        await self.db.close()

    async def test_execute_fetch(self):
        # Test execute and fetch methods

        # Define a sample table creation query
        create_table_query = """
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """

        # Execute the query
        await self.db.execute(create_table_query)

        # Insert some data
        insert_data_query = "INSERT INTO test_table (name) VALUES (?)"
        await self.db.execute(insert_data_query, "John Doe")

        # Fetch the data
        result = await self.db.fetch("SELECT * FROM test_table")

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John Doe")

    async def test_fetchone(self):
        # Test fetchone method

        # Insert some data
        insert_data_query = "INSERT INTO test_table (name) VALUES (?)"
        await self.db.execute(insert_data_query, "Jane Doe")

        # Fetch one row
        result = await self.db.fetchone("SELECT * FROM test_table WHERE name=?", "Jane Doe")

        # Assertion
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Jane Doe")

if __name__ == '__main__':
    # Run the tests
    unittest.main()
