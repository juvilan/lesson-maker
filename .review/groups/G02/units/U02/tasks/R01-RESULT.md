# R01 리뷰 결과

카테고리: security
발견된 이슈: 5개
완료 시각: 2026-03-24T21:42:27.325Z

## 발견된 이슈

### F001 [HIGH]
- file: `_shared/tools/tex_renderer.py`
- line: 339
- severity: high
- category: security
- message: subprocess.run으로 xelatex 실행 시 입력 JSON 데이터가 LaTeX 소스에 삽입된다. tex_escape가 일반 텍스트 특수문자는 처리하지만, LaTeX 명령어 인젝션(\input, \write18 등)을 완전히 차단하지 못한다. 악의적 JSON 입력에 \input{/etc/passwd}나 \immediate\write18{cmd} 같은 페이로드가 포함되면 파일 읽기 또는 (shell-escape 활성 시) 임의 명령 실행이 가능하다.
- suggestion: (1) xelatex 실행 시 -no-shell-escape 플래그를 명시적으로 추가하여 \write18 계열 명령 실행을 차단. (2) tex_escape에서 백슬래시를 \textbackslash{}로 변환하고 있으나, $...$ 수식 구간 내부는 이스케이프하지 않으므로 수식 내 \input 등의 명령이 통과할 수 있음. 수식 구간에서도 위험 명령어(\input, \include, \write, \openout, \catcode)를 필터링하는 deny-list 검증 추가 필요.
- fixable: true

### F002 [MEDIUM]
- file: `_shared/tools/tex_renderer.py`
- line: 335
- severity: medium
- category: security
- message: xelatex 컴파일 실패 시 로그 파일 마지막 3000자를 에러 메시지에 포함하여 raise한다. 로그에는 서버 파일 경로, 시스템 정보, 임시 디렉토리 구조 등 민감 정보가 포함될 수 있으며, 이 에러가 상위 호출자를 통해 사용자에게 노출되면 정보 유출로 이어진다.
- suggestion: 에러 메시지에 로그 전체를 포함하지 말고, "LaTeX 컴파일 실패" 같은 일반 메시지만 반환. 상세 로그는 파일로 저장하거나 로깅 프레임워크로 기록.
- fixable: true

### F003 [MEDIUM]
- file: `_shared/tools/tex_renderer.py`
- line: 119
- severity: medium
- category: security
- message: load_template에서 사용자가 --template 인자로 지정한 임의 경로의 JSON 파일을 읽는다. 경로 검증 없이 os.path.exists + open을 수행하므로, 경로 순회(path traversal)를 통해 시스템 내 임의 JSON 파일을 읽을 수 있다. CLI 도구 특성상 위험도는 제한적이나, 웹 서비스로 래핑될 경우 심각해진다.
- suggestion: 허용 디렉토리 기준으로 realpath를 검증하거나, 템플릿 경로를 특정 디렉토리 내로 제한.
- fixable: true

### F004 [LOW]
- file: `_shared/tools/tests/test_pdf_renderer.py`
- line: 10
- severity: low
- category: security
- message: sys.path.insert(0, ...)로 상위 디렉토리를 모듈 검색 경로에 추가한다. 테스트 코드이므로 실질적 위험은 낮으나, 해당 경로에 악성 모듈이 존재하면 의도치 않은 코드가 임포트될 수 있다(dependency confusion 유사 패턴).
- suggestion: 테스트 실행 시 conftest.py나 pyproject.toml의 [tool.pytest.ini_options] pythonpath 설정으로 관리하는 것이 더 안전.
- fixable: true

### F005 [LOW]
- file: `_shared/tools/tex_renderer.py`
- line: 328
- severity: low
- category: security
- message: compile_tex에서 subprocess.run 호출 시 cmd가 리스트 형태라 shell injection은 불가하나, capture_output=True로 stdout/stderr를 메모리에 저장한다. 극단적으로 큰 LaTeX 로그가 생성되면 메모리 소모 가능성이 있다(DoS 벡터).
- suggestion: subprocess.run에 timeout 파라미터를 추가하여 무한 컴파일 방지 (예: timeout=120).
- fixable: true

## 원본 출력

# Security Review Report

**Scope:** `test_pdf_renderer.py`, `test_rename_output.py`, `tex_renderer.py`
**Risk Level:** MEDIUM

## Summary
- Critical Issues: 0
- High Issues: 1
- Medium Issues: 2
- Low Issues: 2

---

```
[FINDING]
file: _shared/tools/tex_renderer.py
line: 339
severity: high
category: security
message: subprocess.run으로 xelatex 실행 시 입력 JSON 데이터가 LaTeX 소스에 삽입된다. tex_escape가 일반 텍스트 특수문자는 처리하지만, LaTeX 명령어 인젝션(\input, \write18 등)을 완전히 차단하지 못한다. 악의적 JSON 입력에 \input{/etc/passwd}나 \immediate\write18{cmd} 같은 페이로드가 포함되면 파일 읽기 또는 (shell-escape 활성 시) 임의 명령 실행이 가능하다.
suggestion: (1) xelatex 실행 시 -no-shell-escape 플래그를 명시적으로 추가하여 \write18 계열 명령 실행을 차단. (2) tex_escape에서 백슬래시를 \textbackslash{}로 변환하고 있으나, $...$ 수식 구간 내부는 이스케이프하지 않으므로 수식 내 \input 등의 명령이 통과할 수 있음. 수식 구간에서도 위험 명령어(\input, \include, \write, \openout, \catcode)를 필터링하는 deny-list 검증 추가 필요.
fixable: true
```

```
[FINDING]
file: _shared/tools/tex_renderer.py
line: 335-336
severity: medium
category: security
message: xelatex 컴파일 실패 시 로그 파일 마지막 3000자를 에러 메시지에 포함하여 raise한다. 로그에는 서버 파일 경로, 시스템 정보, 임시 디렉토리 구조 등 민감 정보가 포함될 수 있으며, 이 에러가 상위 호출자를 통해 사용자에게 노출되면 정보 유출로 이어진다.
suggestion: 에러 메시지에 로그 전체를 포함하지 말고, "LaTeX 컴파일 실패" 같은 일반 메시지만 반환. 상세 로그는 파일로 저장하거나 로깅 프레임워크로 기록.
fixable: true
```

```
[FINDING]
file: _shared/tools/tex_renderer.py
line: 119-122
severity: medium
category: security
message: load_template에서 사용자가 --template 인자로 지정한 임의 경로의 JSON 파일을 읽는다. 경로 검증 없이 os.path.exists + open을 수행하므로, 경로 순회(path traversal)를 통해 시스템 내 임의 JSON 파일을 읽을 수 있다. CLI 도구 특성상 위험도는 제한적이나, 웹 서비스로 래핑될 경우 심각해진다.
suggestion: 허용 디렉토리 기준으로 realpath를 검증하거나, 템플릿 경로를 특정 디렉토리 내로 제한.
fixable: true
```

```
[FINDING]
file: _shared/tools/tests/test_pdf_renderer.py
line: 10
severity: low
category: security
message: sys.path.insert(0, ...)로 상위 디렉토리를 모듈 검색 경로에 추가한다. 테스트 코드이므로 실질적 위험은 낮으나, 해당 경로에 악성 모듈이 존재하면 의도치 않은 코드가 임포트될 수 있다(dependency confusion 유사 패턴).
suggestion: 테스트 실행 시 conftest.py나 pyproject.toml의 [tool.pytest.ini_options] pythonpath 설정으로 관리하는 것이 더 안전.
fixable: true
```

```
[FINDING]
file: _shared/tools/tex_renderer.py
line: 328
severity: low
category: security
message: compile_tex에서 subprocess.run 호출 시 cmd가 리스트 형태라 shell injection은 불가하나, capture_output=True로 stdout/stderr를 메모리에 저장한다. 극단적으로 큰 LaTeX 로그가 생성되면 메모리 소모 가능성이 있다(DoS 벡터).
suggestion: subprocess.run에 timeout 파라미터를 추가하여 무한 컴파일 방지 (예: timeout=120).
fixable: true
```

---

## Security Checklist

- [x] No hardcoded secrets — API 키, 패스워드, 토큰 없음
- [x] SQL injection — 해당 없음 (DB 미사용)
- [ ] Command injection — xelatex `-no-shell-escape` 미지정 (HIGH)
- [ ] Input validation — LaTeX 수식 구간 내 위험 명령어 필터링 부재
- [x] Dependencies — 외부 패키지(fpdf2, pytest) 자체는 안전
- [ ] Error information disclosure — 에러 메시지에 로그 과다 노출

**가장 우선 조치 사항:** `tex_renderer.py`의 xelatex 실행 시 `-no-shell-escape` 플래그 추가 및 수식 구간 내 위험 명령어 필터링.
