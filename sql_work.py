import sqlite3



class MongoLite():
    def __init__(self, dbfn=""):
        self.connection = None
        self.cursor = None

        if len(dbfn) > 0:
            self.connect(dbfn)

    def connect(self, dbfn):
        self.connection = sqlite3.connect(dbfn)
        self.cursor = self.connection.cursor()

    async def update_suggestion_channel(self, guildid, channelid):
        self.cursor.execute("INSERT INTO CHANNELS_SETUP (guildid,suggestion_chnl) VALUES (" + str(guildid) + ", " + str(channelid) + ") ON CONFLICT(guildid) DO UPDATE SET suggestion_chnl = " + str(channelid))
        self.connection.commit()

    async def vlookup(self, table, value, condition_rowname, condition_value):
        cr = self.connection.execute(
            "SELECT " + str(value) + " FROM " + str(table) + " WHERE " + str(condition_rowname) + "=" + str(condition_value))
        cro = cr.fetchone()
        if cro is not None:
            return cro[0]
