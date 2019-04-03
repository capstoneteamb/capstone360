class Model():
    def select(self):
        """
        Gets all recipe entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, title, author, ingredients, time, skill, description,image):
        """
        Inserts entry into database
        :param title: String
        :param author: String
        :param ingredients: String
        :param time: String
        :param skill: String
        :param description: String
        :param image: String
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass
