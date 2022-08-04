from hstest.outcomes.wrong_answer_outcome import WrongAnswer


class PostgreSQLConnector:

    @staticmethod
    def connect(connection_params: dict[str, any]):
        try:
            import psycopg2
        except ModuleNotFoundError:
            raise WrongAnswer(f"For the 'postgresql' dialect psycopg2 library should be installed")

        if 'host' not in connection_params:
            connection_params['host'] = 'localhost'
        if 'port' not in connection_params:
            connection_params['port'] = 5432

        try:
            return psycopg2.connect(**connection_params)
        except:
            raise WrongAnswer(f"Can't connect to the PostgreSQL database with the following parameters:\n"
                              f"{connection_params}")
