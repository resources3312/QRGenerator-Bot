from os import getenv
from dotenv import load_dotenv
from io import BytesIO
from qrcode import QRCode
from redis import Redis

load_dotenv()

class UserRequestsArchive:
    @staticmethod
    def createTable() -> None:
        try:
            with connect(getenv("SQLITE_URL")) as session:
                session.cursor().execute("""
                    CREATE TABLE IF NOT EXISTS requests(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        received TEXT DEFAULT (datetime('now')),
                        user_id TEXT NOT NULL CHECK(length(user_id) == 10),
                        username TEXT NOT NULL,
                        qr_data TEXT NOT NULL
                    );
                                         """)
                session.commit()

    except Error: pass

    @staticmethod
    def addRequestInfo(self, user_id: int, username: str, qr_data: str) -> None:
        try:
            with connect(getenv("SQLITE_URL")) as session:
                session.cursor().execute("INSERT INTO (user_id, username, qr_data) VALUES (?, ?, ?)", (user_id, username, qr_data))
                session.commit()

        except Error: pass

    @staticmethod
    def getRequestsByUserId(user_id: int, index=0) -> tuple | None:
        try:
            with connect(getenv("SQLITE_URL")) as session:
                requests = session.cursor().execute(f"SELECT received, user_id, username, qr_data FROM requests WHERE user_id={user_id}").fetchall()
                return requests if requests else None

        except Error: None

    @staticmethod
    def getRequestsByUsername(username: str, index=0) -> tuple | None:
        try:
            with connect(getenv("SQLITE_URL")) as session:
                requests = session.cursor().execute(f"SELECT received, user_id, username, qr_data FROM requests WHERE username={username}").fetchall()
                return requests if requests else None

        except Error: None

     @staticmethod
    def getUsersList() -> tuple[tuple] | None:
        try:
            with connect(getenv("SQLITE_URL")) as session:
                requests = session.cursor().execute(f"SELECT received, user_id, username FROM requests").fetchall()
                return requests if requests else None

        except Error: None


class QRManager:
    @staticmethod
    def getUserColor(user_id: int) -> str:
        try:
            color = Redis(host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True).get(user_id)
            return color if color else "#000000"
        
        except: return "#000000"

    @staticmethod
    def setUserColor(user_id: int, color: str) -> bool:
        try:
            r = Redis(host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True)
            return True if r.set(user_id, color) else False
        
        except: return None

    @staticmethod
    def generateQR(data: str, color="#000000") -> BytesIO:
        byte_qr = BytesIO()

        qr = QRCode(border=6)
        qr.add_data(data)
        qr.make(fit=True)
        qr.make_image(fill_color=color).save(byte_qr, format="PNG")

        byte_qr.seek(0)
        return byte_qr



