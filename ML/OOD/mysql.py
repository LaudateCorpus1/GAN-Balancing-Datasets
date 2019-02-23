#!/usr/bin/env python3
# Matt Stillwell
import pymysql.cursors


class SQLConnector(object):

    def __init__(self):
        """ Constructor """
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                port=3306,
                user='ldeng',
                password='cs*titanML',
                db='results',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

    def _create_hyper(self):
        """ Creates the hypers table """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        create table hypers (
                            id int, 
                            iteration int, 
                            layers varchar(255), 
                            attack int, 
                            accuracy float(20)
                        );
                    """
                cursor.execute(sql)
            self.connection.commit()
        finally:
            pass

    def write_hyper(self, theid, layersstr, attack, acc):
        """ Writes to the hypers table """
        try:
            with self.connection.cursor() as cursor:
                sql1 = """
                            select max(iteration) 
                            from hypers 
                            where id = %s;
                        """
                sql2 = """ 
                            insert into hypers (id, iteration, layers, attack, accuracy) 
                            values (%s, %s, %s, %s, %s); 
                        """

                cursor.execute(sql1, (str(theid)))
                dicti = cursor.fetchall()[0]
                maxnum = dicti.get('max(iteration)')
                if maxnum is None:
                    maxnum = 0
                maxnum += 1
                cursor.execute(sql2, (str(theid), str(maxnum), str(layersstr), str(attack), str(acc)))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

        finally:
            pass

    def sort_hyper(self):
        """ Reorders the hypers table based off of id """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        alter table hypers 
                        order by id asc;
                    """
                cursor.execute(sql)
            self.connection.commit()
        finally:
            pass

    def read_hyper(self, acc=0):
        """ Reads from the hypers table dependent on accuracy """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        select * from hypers 
                        where accuracy > %s;
                    """
                cursor.execute(sql, (str(acc)))
                result = cursor.fetchall()
                return result
        finally:
            pass

    #=====================================================

    def _create_gens(self):
        """ Creates the gen table """
        try:
            with self.connection.cursor() as cursor:
                sql = """ 
                        create table gens (
                            id int, 
                            modelnum int, 
                            iteration int, 
                            duration int, 
                            protocol_type varchar(10), 
                            service varchar(50), 
                            flag varchar(100), 
                            src_bytes int, 
                            dst_bytes int, 
                            land int, 
                            wrong_fragment int, 
                            urgent int, 
                            hot int, 
                            num_failed_logins int, 
                            logged_in int, 
                            num_compromised int, 
                            root_shell int, 
                            su_attempted int, 
                            num_root int, 
                            num_file_creations int, 
                            num_shells int, 
                            num_access_files int, 
                            num_outbound_cmds int, 
                            is_host_login int, 
                            is_guest_login int, 
                            count int, 
                            srv_count int, 
                            serror_rate int, 
                            srv_serror_rate int, 
                            rerror_rate int, 
                            srv_rerror_rate int, 
                            same_srv_rate int, 
                            diff_srv_rate int, 
                            srv_diff_host_rate int, 
                            dst_host_count int, 
                            dst_host_srv_count int, 
                            dst_host_same_srv_rate int, 
                            dst_host_diff_srv_rate float(20), 
                            dst_host_same_src_port_rate float(20), 
                            dst_host_srv_diff_host_rate int, 
                            dst_host_serror_rate int, 
                            dst_host_srv_serror_rate int, 
                            dst_host_rerror_rate int, 
                            dst_host_srv_rerror_rate int, 
                            attack_type int
                        );
                    """
                cursor.execute(sql)
            self.connection.commit()
        finally:
            pass

    def write_gens(self, theid, modelnum, iteration, duration, protocol_type, service, flag,
            src_bytes, dst_bytes, land, wrong_fragment, urgent, hot, num_failed_logins, logged_in,
            num_compromised, root_shell, su_attempted, num_root, num_file_creations, num_shells,
            num_access_files, num_outbound_cmds, is_host_login, is_guest_login, count, srv_count,
            serror_rate, srv_serror_rate, rerror_rate, srv_rerror_rate, same_srv_rate,
            diff_srv_rate, srv_diff_host_rate, dst_host_count, dst_host_srv_count,
            dst_host_same_srv_rate, dst_host_diff_srv_rate, dst_host_same_src_port_rate,
            dst_host_srv_diff_host_rate, dst_host_serror_rate, dst_host_srv_serror_rate,
            dst_host_rerror_rate, dst_host_srv_rerror_rate, attack_type):
        """ Writes to the gens table """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        insert into gens (
                            id, 
                            modelnum, 
                            iteration, 
                            duration, 
                            protocol_type, 
                            service, 
                            flag, 
                            src_bytes, 
                            dst_bytes, 
                            land, 
                            wrong_fragment, 
                            urgent, 
                            hot, 
                            num_failed_logins, 
                            logged_in, 
                            num_compromised, 
                            root_shell, 
                            su_attempted, 
                            num_root, 
                            num_file_creations, 
                            num_shells, 
                            num_access_files, 
                            num_outbound_cmds, 
                            is_host_login, 
                            is_guest_login, 
                            count, 
                            srv_count, 
                            serror_rate, 
                            srv_serror_rate, 
                            rerror_rate, 
                            srv_rerror_rate, 
                            same_srv_rate, 
                            diff_srv_rate, 
                            srv_diff_host_rate, 
                            dst_host_count, 
                            dst_host_srv_count, 
                            dst_host_same_srv_rate, 
                            dst_host_diff_srv_rate, 
                            dst_host_same_src_port_rate, 
                            dst_host_srv_diff_host_rate, 
                            dst_host_serror_rate, 
                            dst_host_srv_serror_rate, 
                            dst_host_rerror_rate, 
                            dst_host_srv_rerror_rate, 
                            attack_type
                        ) values (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s
                        );
                    """

                cursor.execute(sql, (str(theid), str(modelnum), str(iteration), str(duration),
                    str(protocol_type), str(service), str(flag), str(src_bytes),
                    str(dst_bytes), str(land), str(wrong_fragment), str(urgent),
                    str(hot), str(num_failed_logins), str(logged_in),
                    str(num_compromised), str(root_shell), str(su_attempted),
                    str(num_root), str(num_file_creations), str(num_shells),
                    str(num_access_files), str(num_outbound_cmds),
                    str(is_host_login), str(is_guest_login), str(count),
                    str(srv_count), str(serror_rate), str(srv_serror_rate),
                    str(rerror_rate), str(srv_rerror_rate), str(same_srv_rate),
                    str(diff_srv_rate), str(srv_diff_host_rate),
                    str(dst_host_count), str(dst_host_srv_count),
                    str(dst_host_same_srv_rate), str(dst_host_diff_srv_rate),
                    str(dst_host_same_src_port_rate),
                    str(dst_host_srv_diff_host_rate), str(dst_host_serror_rate),
                    str(dst_host_srv_serror_rate), str(dst_host_rerror_rate),
                    str(dst_host_srv_rerror_rate), str(attack_type)))

                # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

        finally:
            pass

    def read_gens(self, acc=0):
        """ Reads from the gens table dependent on accuracy """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        select id, modelnum, iteration, attack_type 
                        from gens;
                    """
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            pass

    #=============================================

    def read_specific_joined(self, theid, theiter):
        """ Reads the joined table at a specific id and iteration """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        select gens.id, modelnum, gens.iteration, layers, attack_type, name, accuracy 
                        from gens, hypers, attacks
                        where gens.modelnum = hypers.id 
                        and gens.iteration = hypers.iteration
                        and hypers.attack = attacks.id
                        and gens.id = %s 
                        and gens.iteration = %s;
                    """
                cursor.execute(sql, (str(theid), str(theiter)))
                result = cursor.fetchall()
                return result
        finally:
            pass

    def read_joined(self, acc=0):
        """ Reads the joined table dependent on the accuracy """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        select gens.id, modelnum, gens.iteration, layers, attack_type, name, accuracy 
                        from gens, hypers, attacks 
                        where gens.modelnum = hypers.id 
                        and gens.iteration = hypers.iteration 
                        and hypers.attack = attacks.id 
                        and accuracy > %s;
                    """
                cursor.execute(sql, (str(acc)))
                result = cursor.fetchall()
                return result
        finally:
            pass


    def pull_attack(self, attack):
        """ Reads the joined table at a specific id and iteration """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        select * 
                        from hypers, attacks
                        where hypers.attack = attacks.id 
                        and name = %s
                        and accuracy = (
                            select max(accuracy)
                            from hypers
                        );
                    """
                cursor.execute(sql, (str(attack)))
                result = cursor.fetchall()
                return result
        finally:
            pass


    def pull_heavy_attack(self, attack):
        """ Reads the joined table at a specific id and iteration """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        select * 
                        from gens, hypers, attacks
                        where gens.modelnum = hypers.id 
                        and gens.iteration = hypers.iteration
                        and hypers.attack = attacks.id 
                        and name = %s  
                        and accuracy = (
                            select max(accuracy)
                        );
                    """
                cursor.execute(sql, (str(attack)))
                result = cursor.fetchall()
                return result
        finally:
            pass

    #====================================================

    def _create_attacks(self):
        """ Creates the hypers table """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        create table attacks (
                            id int, 
                            name varchar(255)
                        );
                    """
                cursor.execute(sql)
            self.connection.commit()
        finally:
            pass


    def _write_attacks(self, theid, attack):
        """ Writes to the attacks table """
        try:
            with self.connection.cursor() as cursor:
                sql = """
                        insert into attacks (id, name)
                        values (%s, %s);
                    """
                cursor.execute(sql, (str(theid), str(attack)))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            pass

    def _fill_attacks(self):
        self.write_attacks(1, "normal")
        self.write_attacks(2, "buffer_overflow")
        self.write_attacks(3, "loadmodule")
        self.write_attacks(4, "perl")
        self.write_attacks(5, "neptune")
        self.write_attacks(6, "smurf")
        self.write_attacks(7, "guess_passwd")
        self.write_attacks(8, "pod")
        self.write_attacks(9, "teardrop")
        self.write_attacks(10, "portsweep")
        self.write_attacks(11, "ipsweep")
        self.write_attacks(12, "land")
        self.write_attacks(13, "ftp_write")
        self.write_attacks(14, "back")
        self.write_attacks(15, "imap")
        self.write_attacks(16, "satan")
        self.write_attacks(17, "phf")
        self.write_attacks(18, "nmap")
        self.write_attacks(19, "multihop")
        self.write_attacks(20, "warezmaster")
        self.write_attacks(21, "warezclient")
        self.write_attacks(22, "spy")
        self.write_attacks(23, "rootkit")


    def read_attacks(self, num=1):
        """ Reads from the attack table dependent on num """
        try:
            with self.connection.cursor() as cursor:
                sql = "select id, name from attacks;"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            pass

    #====================================================

    def output_to_csv(self, dictionaryarray, filename = "stats.csv"):
        """ Writes a csv file output from a given dictionary """

        string = ""
        for dictionary in dictionaryarray:  # just i in resiults?
            count = 0
            for _, value in dictionary.items():
                string += str(value)
                count = count + 1
                if count < len(dictionary.items()):
                    string += ","
            string += "\n"

        f = open(filename, "w")
        f.write(string)

    def close(self):
        self.connection.close()



def main():
    """ Auto run main method """
    conn = SQLConnector()

    # print(conn.pull_attack("neptune"))
    print(conn.pull_heavy_attack("neptune"))

    #print(conn.read_joined())
    #print(conn.read_specific_joined(1,1))

    #conn._create_gens()
    #conn._create_hyper()

    #conn._create_attacks()
    #conn._fill_attacks()


    #conn.write_hyper(1, "2,3,4", 5, 80.3)
    #conn.write_gens(1, 1, 1, 0, "tcp", "ftp_data", "REJ", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0.00, 171, 62, 0.27, 0.02, 0.01, 0.03, 0.01, 0, 0.29, 0.02, 10)

    #print(conn.read_gens())
    #print(conn.read_hyper())

    #conn.sort_hyper()

    #print(conn.read_specific_joined(1, 1))
    #print(conn.read_joined(20))
    #conn.output_to_csv(conn.read_joined(20))

if __name__ == "__main__":
    main()
