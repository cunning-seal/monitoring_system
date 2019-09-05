import psycopg2
import sys
import signal

def main(argv):

    HOST = argv[0]
    DB_NAME = argv[1]
    USER = argv[2]
    PSWD = argv[3]



    try:
        # создание соединения с сервером базы данных
        def signal_handler(signal, frame):
            print("[E] SIGTERM IS CATCHED")
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)
        while True:
            try:
                main_conn = psycopg2.connect(host=HOST, user=USER, password=PSWD)
                main_cursor = main_conn.cursor()
                break
            except:
                print("[E] Ошибка создания основного соединения с сервером БД")
                continue
        print("[S] Основное соединение с сервером БД установлено")

        while True:
            try:
                main_cursor.execute("select datname from pg_database where datistemplate=false;")
                break
            except:
                continue
        db_names = main_cursor.fetchall()
        # main_cursor.close()

        cursors_set = []
        for dbtuple in db_names:
            while True:
                try:
                    conn = psycopg2.connect(host=HOST, database=dbtuple[0], user=USER, password=PSWD)
                    cursor = main_conn.cursor()
                    cursors_set.append(cursor)
                    break
                except:
                    print("[E] Ошибка создания соединения с базой данных {}".format(dbtuple[0]))
                    continue
            print("[S] Соединение с базой данных {} установлено".format(dbtuple[0]))

        try:
            # main_cursor.execute("select count(*) from pg_stat_activity;")
            # con_num = main_cursor.fetchone()
            # print(1)
            # print(con_num)

            # main_cursor.execute("show max_connections")
            # max_con_num = main_cursor.fetchone()
            # print(max_con_num)
            #

            # main_cursor.execute("select xact_rollback from pg_stat_database;")
            # res = main_cursor.fetchall()
            # print(res)

            main_cursor.execute("select xact_rollback from pg_stat_database;")
            rb_num = 0
            for db_tuple in main_cursor.fetchall():
                rb_num += db_tuple[0]
            main_cursor.execute("select xact_commit from pg_stat_database;")
            com_num = 0
            for db_tuple in main_cursor.fetchall():
                com_num += db_tuple[0]
            rback_perc = round(rb_num / com_num, 2)
            print(rback_perc)

            # print(len(cursors_set))
            # for c in cursors_set:
            #     c.execute("select datname, xact_rollback from pg_stat_database;")
            #     rb_num = c.fetchall()
            #     print(2)
            #     print(rb_num)
            #     c.execute("select datname, xact_commit from pg_stat_database;")
            #     com_num = c.fetchall()
            #     print(3)
            #     print(com_num)

        except:
            print("[E] Не удалось выполнить запрос к базе данных")
            e = sys.exc_info()[1]
            print("[E] " + str(e.args[0]))
            main_cursor.close()
            main_conn.close()
            for c in cursors_set:
                c.close()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main(sys.argv[1:])