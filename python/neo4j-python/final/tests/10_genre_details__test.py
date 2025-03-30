import pytest
from api.dao.genres import GenreDAO
from api.neo4j import get_driver


def test_return_list_of_genres(app):
    with app.app_context():
        name = "Action"

        # Get Neo4j Driver
        driver = get_driver()

        # Create DAO
        dao = GenreDAO(driver)

        # Get all genres
        output = dao.find(name)

        assert output["name"] == name

        print("Here is the answer to the quiz question on the lesson:")
        print("How many movies are in the Action genre?")
        print("Copy and paste the following answer into the text box: \n\n")

        print(output["movies"])
