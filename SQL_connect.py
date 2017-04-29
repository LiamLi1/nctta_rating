from sqlalchemy import create_engine
import pandas as pd


class DatabaseConnect(object):

    def __init__(self, username, password, host, dbname):
        self.DB_CON_STR = 'mysql+pymysql://' + username + ':' \
                          + password + '@' + host + '/' + dbname + '?charset=utf8'
        self.engine = create_engine(self.DB_CON_STR, echo=False)

    def read(self, sql):
        return pd.read_sql(sql, con=self.engine)

    def write(self, df, table):
        if type(df) != bool:
            df.to_sql(table, self.engine, if_exists='append')

    def write_crawler(self, crawler, table):
        if len(crawler.idrange) == 1:
            id_list = range(1, crawler.idrange)
        else:
            id_list = crawler.idrange
        for i in id_list:
            if i % 100 == 0:
                print(i)
            try:
                df = crawler.getPageItem(i)
                self.write(df, table)
            except Exception as e:
                print('TypeErrror:', e)
                print(i)