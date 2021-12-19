class Query:
    def __init__(self):
        pass

    def init_company_info(self):
        return '''
            CREATE TABLE IF NOT EXISTS company_info
            (
                id          varchar(20) not null primary key,
                name        varchar(40) null,
                last_update date        null
            )
        '''

    def init_daily_price(self):
        return '''
            CREATE TABLE IF NOT EXISTS daily_price
            (
                company_id varchar(20) not null,
                date       date        not null,
                open       bigint      null,
                high       bigint      null,
                low        bigint      null,
                close      bigint      null,
                primary key (company_id, date)
            )
        '''

    def init_daily_volume(self):
        return '''
            CREATE TABLE IF NOT EXISTS daily_volume
            (
                company_id varchar(20) not null,
                date       date        not null,
                volume     bigint      null,
                primary key (company_id, date)
            )
        '''

    def select_company_info(self):
        return 'SELECT * FROM company_info'

    def get_last_update_date(self):
        return 'SELECT max(last_update) FROM company_info'

    def insert_company_info(self, id, name, last_update):
        return f'''
            INSERT INTO company_info
            (id, name, last_update)
            VALUES
            ('{id}', '{name}', '{last_update}')
            ON DUPLICATE KEY UPDATE id='{id}', last_update='{last_update}'
        '''

    def replace_into_daily_price(self, id, date, open, high, low, close):
        return f'''
            REPLACE INTO daily_price
            VALUES
            ('{id}', '{date}', {open}, {high}, {low}, {close})
        '''

    def replace_into_daily_volume(self, id, date, volume):
        return f'''
            REPLACE INTO daily_volume
            VALUES
            ('{id}', '{date}', {volume})
        '''
