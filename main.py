from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.app_router import router as app_router
from fastapi.middleware.cors import CORSMiddleware
from app.domain.music.models.song import Base
from app.foundation.infrastructure.database.database import database
from sqlalchemy.schema import CreateTable
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 데이터베이스 테이블 생성
    engine = database.engine
    async with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            create_table_sql = CreateTable(table)
            try:
                await conn.execute(create_table_sql)
            except Exception as e:
                print(f"Info: {str(e)}")
    
    yield  # FastAPI 애플리케이션 실행
    
    # Shutdown: 데이터베이스 연결 종료
    await database.close()

# ✅ FastAPI 애플리케이션 생성
app = FastAPI(lifespan=lifespan)

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 모든 도메인에서 요청 허용 (보안상 필요하면 특정 도메인만 허용)
    allow_credentials=True,
    allow_methods=["*"],  # ✅ 모든 HTTP 메서드 허용 (POST, OPTIONS 등)
    allow_headers=["*"],  # ✅ 모든 헤더 허용
)

# ✅ 라우터 등록
app.include_router(app_router, prefix="/api")

def current_time():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get(path="/")
async def home():
    return HTMLResponse(content=f"""
<body>
<div style="width: 400px; margin: 50 auto;">
    <h1> 크롤러 서버 구동 중입니다.</h1>
    <h2>{current_time()}</h2>
</div>
</body>
""")

    
