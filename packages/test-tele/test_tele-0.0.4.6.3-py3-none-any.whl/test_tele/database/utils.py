import aiosqlite


class Database:
    def __init__(self):
        self.sqlpath = 'ttele.db'

    async def connect(self):
        self.con = await aiosqlite.connect(self.sqlpath, uri=True)
        self.cursor = await self.con.cursor()


    async def close(self):
        await self.cursor.close()
        await self.con.close()


    async def execute(self, query, values=None):
        await self.connect()
        await self.cursor.execute(query, values)
        await self.con.commit()


    async def fetch_all(self):
        return await self.cursor.fetchall()


    async def create_tables(self):
        # subscriber != donator : 0 False 1 True
        # full_subscriber : 0 False 1 True (will join group)
        await self.execute('''CREATE TABLE IF NOT EXISTS users(
                            user_id integer primary key,
                            chat_id integer null,
                            username text null,
                            firstname text null,
                            is_subscriber integer null,
                            is_full_subscriber integer null
                        )''')
        
        # no_caption : 0 False 1 True
        # no_keyboard : 0 False 1 True
        # def_inline : gelbooru | konachan | realbooru | aibooru
        # lang : id | en | ru | zh
        await self.execute('''CREATE TABLE IF NOT EXISTS settings(
                            sett_id integer primary key autoincrement,
                            lang text null,
                            def_inline text null,
                            no_caption integer null,
                            no_keyboard integer null,
                            id_user integer null
                        )''')
        
        # safe username of public channel
        # will grab any username inserted, became my own database
        await self.execute('''CREATE TABLE IF NOT EXISTS public_channels(
                            pchannel_id integer primary key autoincrement,
                            username text null,
                            notes text null
                        )''')
        
        # safe sticker links
        await self.execute('''CREATE TABLE IF NOT EXISTS stickers(
                            sticker_id integer primary key autoincrement,
                            link text null,
                            notes text null
                        )''')
        
        # safe messages
        await self.execute('''CREATE TABLE IF NOT EXISTS messages(
                            msg_id integer primary key autoincrement,
                            id integer null,
                            entity text null,
                            link text null,
                            type text null
                        )''')
        
        await self.close()


    # Hapus table
    async def drop_table(self, table_name):
        await self.execute(f"DROP TABLE IF EXISTS {table_name}")
        await self.close()
        

