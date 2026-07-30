# claude-workspace 폴더 구조

이 폴더는 Claude Code 작업 환경입니다. `CLAUDE.md`(활성화 시)를 Claude Code가 자동으로 읽어 아래 규칙과 구조를 따릅니다.

```
claude-workspace/
├── CLAUDE.md              ⚠️ 아직 없음 — CLAUDE_템플릿.md의 빈칸을 채워 이 이름으로 저장해야 활성화됨
├── CLAUDE_템플릿.md        Claude Code 지침 템플릿 (원본, 빈칸 [ ] 포함)
├── SECURITY.md            🚨 키 노출 등 비상시 대응 매뉴얼
├── README.md              지금 보고 있는 이 문서
├── .gitignore             .env, 키/자격 증명 파일 등을 git 추적에서 제외
├── .env                   ⚠️ 아직 없음 — API 키 등 환경변수 저장용 (git add 금지, .gitignore 처리됨)
├── weather.txt            강남구 날씨 기록 (scripts/gangnam_weather.py 실행 이력, append-only)
│
├── docs/                  문서 · 샘플 데이터
│   ├── resume.pdf
│   └── sample_sales.csv
│
├── portfolio/             포트폴리오 사이트
│   └── index.html
│
├── scripts/               자동화 스크립트
│   └── gangnam_weather.py   강남구 날씨/미세먼지 조회 → weather.txt에 기록
│
└── tasks/                 작업 관리
    ├── todo.md            오늘 할 일 / 진행 중인 작업 계획 (체크리스트)
    └── progress.md        작업 이력 (append-only 로그)
```

---

## 파일별 역할

| 파일 | 역할 |
|---|---|
| `CLAUDE.md` | Claude Code가 매 세션 자동으로 읽는 행동 지침서. 보안 규칙, 소통 방식, 작업 원칙 등을 정의 |
| `SECURITY.md` | 키/비밀번호 노출 의심 시 따르는 대응 절차 (확인→폐기→이력확인→재발급→교체) |
| `.gitignore` | `.env`, 키/인증서 파일, OS·에디터·캐시 파일 등을 git에서 제외 |
| `docs/` | 이력서, 샘플 데이터 등 참고 문서 |
| `portfolio/` | 포트폴리오 웹페이지 |
| `scripts/` | 반복 실행용 자동화 스크립트 |
| `tasks/todo.md` | 3단계 이상 걸리는 작업의 계획을 실행 전에 적어두는 곳 |
| `tasks/progress.md` | 완료한 작업을 시간순으로 기록하는 곳 (수정 없이 계속 추가만) |
| `.env` | 실제 API 키·비밀번호 저장 (아직 생성 안 됨, 절대 공유·커밋 금지) |

---

## 아직 안 된 것 (Next Steps)

1. **`CLAUDE.md` 활성화** — `CLAUDE_템플릿.md`의 빈칸(이름/역할 등)을 채운 뒤 `CLAUDE.md`로 저장해야 Claude Code가 규칙을 자동 인식함.
2. **`.env` 생성** — OpenRouter, WordPress 등에서 쓸 키를 저장할 파일. `SECURITY.md`의 빈칸(콘솔 주소 등)도 이 시점에 함께 채우는 게 좋음.
3. **`.ssh/oracle-server.key`, `~/.ssh/config`의 `oracle-server` 별칭** — Oracle 서버 접속용 SSH 설정 (claude-workspace 바깥, 홈 디렉토리 기준).

---

*이 문서는 폴더 구조가 바뀔 때마다 갱신하세요.*
