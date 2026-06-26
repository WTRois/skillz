---
name: security-auditor
description: >
  Melakukan security audit menyeluruh pada codebase web menggunakan 6 framework keamanan
  sekaligus: OWASP Top 10 (2021), OWASP API Security Top 10 (2023), CWE/SANS Top 25 (2024),
  OWASP ASVS Level 1-2, Security Headers, dan Dependency/Supply Chain Security.
  Stack auto-detected untuk menerapkan pola vulnerability yang tepat per bahasa dan framework.
  Output: laporan terstruktur dengan severity rating, referensi CVE/CWE, kode vulnerable,
  kode fix, dan remediation roadmap berdasarkan prioritas risiko.
  Gunakan skill ini ketika: "audit keamanan project ini", "cek vulnerability", "security review",
  "ada celah keamanan apa", "apakah kode ini aman", "cek OWASP", "security audit",
  atau permintaan sejenis terkait keamanan kode.
---

# Security Auditor

Audit keamanan menyeluruh menggunakan **6 security framework** secara bersamaan.
Stack auto-detected untuk pola vulnerability yang akurat per bahasa dan framework.

---

## Framework yang Digunakan

| # | Framework | Fokus |
|---|-----------|-------|
| 1 | **OWASP Top 10 (2021)** | Risiko keamanan web paling kritis |
| 2 | **OWASP API Security Top 10 (2023)** | Risiko spesifik REST/GraphQL API |
| 3 | **CWE/SANS Top 25 (2024)** | Weakness paling berbahaya di software |
| 4 | **OWASP ASVS v4.0 Level 1–2** | Kontrol verifikasi keamanan aplikasi |
| 5 | **OWASP Secure Headers Project** | HTTP security headers |
| 6 | **Supply Chain Security (SLSA L1)** | Dependency & build integrity |

---

## Fase 0 — Stack Detection

Scan file berikut, isi STACK block sebelum lanjut.

### Detection Matrix

| Indikator | Nilai |
|-----------|-------|
| `go.mod` + `gin-gonic/gin` | `lang: go, backend: gin` |
| `go.mod` + `labstack/echo` | `lang: go, backend: echo` |
| `go.mod` + `gofiber/fiber` | `lang: go, backend: fiber` |
| `go.mod` + `go-chi/chi` | `lang: go, backend: chi` |
| `package.json` + `express` | `lang: node, backend: express` |
| `package.json` + `@nestjs/core` | `lang: node, backend: nestjs` |
| `package.json` + `fastify` | `lang: node, backend: fastify` |
| `package.json` + `hono` | `lang: node, backend: hono` |
| `requirements.txt` + `fastapi` | `lang: python, backend: fastapi` |
| `requirements.txt` + `django` | `lang: python, backend: django` |
| `requirements.txt` + `flask` | `lang: python, backend: flask` |
| `composer.json` + `laravel/framework` | `lang: php, backend: laravel` |
| `pom.xml` + `spring-boot` | `lang: java, backend: spring` |
| `nuxt.config.ts` ada | `frontend: nuxt` |
| `next.config.*` ada | `frontend: nextjs` |
| `package.json` + `vue` (no nuxt) | `frontend: vue` |
| `package.json` + `react` (no next) | `frontend: react` |
| `schema.prisma` ada | `orm: prisma` |
| `go.mod` + `gorm.io/gorm` | `orm: gorm` |
| `sqlc.yaml` ada | `orm: sqlc` |
| `package.json` + `typeorm` | `orm: typeorm` |
| `package.json` + `drizzle-orm` | `orm: drizzle` |
| Config/env mengandung `postgres` | `db: postgres` |
| Config/env mengandung `mysql` | `db: mysql` |
| Config/env mengandung `mongodb` | `db: mongodb` |
| Config/env mengandung `redis` | `cache: redis` |
| `Dockerfile` / `docker-compose.yml` ada | `infra: docker/compose` |
| `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `go.sum` ada | `lockfile: yes` |

```
[STACK]
lang:     <go | node | python | php | java | rust>
backend:  <gin | echo | fiber | chi | express | nestjs | fastify | hono | fastapi | django | flask | laravel | spring>
frontend: <nuxt | nextjs | vue | react | angular | svelte | none>
orm:      <gorm | sqlc | sqlx | prisma | typeorm | drizzle | sequelize | django-orm | eloquent | raw-sql | none>
db:       <postgres | mysql | sqlite | mongodb | none>
cache:    <redis | none>
infra:    <compose | docker | k8s | none>
lockfile: <yes | no>
has_auth: <yes | no | unknown>  ← deteksi dari: JWT, session, middleware auth
has_api:  <yes | no>            ← deteksi dari: routes/endpoints yang ditemukan
[/STACK]
```

---

## Fase 1 — Attack Surface Mapping

Identifikasi semua titik masuk potensial sebelum analisis dimulai.

### 1a. Entry Points

Scan dan catat semua:
- **HTTP Endpoints**: semua route yang terdefinisi (GET/POST/PUT/DELETE/PATCH)
- **Public vs Authenticated**: endpoint mana yang butuh auth, mana yang tidak
- **File Upload**: endpoint yang menerima file
- **External Calls**: HTTP client calls ke service lain (fetch, axios, http.Get, requests)
- **WebSocket**: koneksi real-time jika ada
- **Background Jobs / Cron**: proses yang berjalan di background
- **Admin Endpoints**: route dengan prefix `/admin`, `/internal`, `/dashboard`

### 1b. Data Flow

Untuk setiap entry point, trace:
```
User Input → Validation → Processing → Storage/Response
```
Tandai setiap titik di mana user input digunakan tanpa sanitasi.

### 1c. Sensitive Data Inventory

Identifikasi di mana data sensitif berada:
- Password / credential handling
- Token (JWT, API key, OAuth)
- PII (email, nama, alamat, nomor telepon)
- Payment data
- File yang di-upload user

### Output: SURFACE Block

```
[SURFACE]
total_endpoints:   N
public_endpoints:  [list path]
auth_endpoints:    [list path]
file_upload:       [list path, atau none]
external_calls:    [list service/domain, atau none]
sensitive_data:    [list tipe data sensitif ditemukan]
admin_routes:      [list path, atau none]
[/SURFACE]
```

---

## Fase 2 — Multi-Framework Security Analysis

Jalankan semua check berikut secara berurutan. Setiap temuan dicatat dengan format Finding di bawah.

### Format Finding

```
[FINDING]
id:         <KODE-NNN> (contoh: OWASP-001, CWE-003, ASVS-005)
severity:   <CRITICAL | HIGH | MEDIUM | LOW | INFO>
framework:  <nama framework + kode referensi>
title:      <judul singkat>
file:       <path:line jika bisa diidentifikasi>
description: <penjelasan masalah>
vulnerable_code: |
  <kode bermasalah>
fix_code: |
  <kode yang benar>
remediation: <langkah perbaikan konkret>
[/FINDING]
```

---

### Check 2.1 — OWASP Top 10 (2021)

#### A01: Broken Access Control

Cari pola berikut:

| `backend` | Pola Vulnerable |
|-----------|----------------|
| `gin` / `echo` / `fiber` | Route tanpa middleware auth, `c.Param("id")` langsung ke DB tanpa cek kepemilikan |
| `express` / `nestjs` | Endpoint tanpa `@UseGuards()` / `authMiddleware`, `req.params.id` ke DB tanpa ownership check |
| `fastapi` | Endpoint tanpa `Depends(get_current_user)`, `item_id` ke DB tanpa filter `user_id` |
| `django` | View tanpa `@login_required` / `permission_required`, queryset tanpa filter `user=request.user` |
| `laravel` | Route tanpa `auth` middleware, `Model::find($id)` tanpa `where('user_id', auth()->id())` |
| `spring` | Endpoint tanpa `@PreAuthorize`, repository method tanpa ownership filter |

**Checks spesifik:**
- [ ] Horizontal privilege escalation: user A bisa akses data user B via ID manipulation
- [ ] Vertical privilege escalation: user biasa bisa akses admin endpoint
- [ ] IDOR (Insecure Direct Object Reference): ID di URL/body langsung ke DB query
- [ ] Missing function-level access control: endpoint admin tidak diproteksi
- [ ] CORS misconfiguration: `Access-Control-Allow-Origin: *` pada endpoint auth/private

#### A02: Cryptographic Failures

| `lang` | Pola Vulnerable |
|--------|----------------|
| `go` | `md5.Sum`, `sha1.New` untuk password, `math/rand` untuk token, hardcoded key di source |
| `node` | `crypto.createHash('md5')` untuk password, `Math.random()` untuk token, secret di kode |
| `python` | `hashlib.md5/sha1` untuk password, `random.random()` untuk token, key di kode |
| `php` | `md5()`, `sha1()` untuk password, `rand()` untuk token, hardcoded key |
| `java` | `MessageDigest.getInstance("MD5/SHA1")` untuk password, `new Random()` untuk token |

**Checks spesifik:**
- [ ] Password disimpan plain text atau hash lemah (MD5/SHA1/SHA256 tanpa salt)
- [ ] Data sensitif ditransmisikan via HTTP (bukan HTTPS)
- [ ] Sensitive data (password, token, PII) muncul di log
- [ ] JWT menggunakan algoritma `alg: none` atau HS256 dengan secret lemah
- [ ] API key / secret hardcoded di source code atau committed ke git
- [ ] Database connection string dengan password exposed di config yang di-commit

#### A03: Injection

**SQL Injection** — cari per ORM/stack:

| `orm` | Pola Vulnerable |
|-------|----------------|
| `gorm` | `db.Raw("SELECT * FROM users WHERE email = '" + email + "'")` — string concat di Raw() |
| `sqlc` | Jarang — tapi cek jika ada custom raw query di luar sqlc |
| `sqlx` | `db.Query("SELECT ... WHERE id = " + id)` — concat langsung |
| `prisma` | `$queryRaw` dengan template literal: `` $queryRaw`SELECT * WHERE id = ${id}` `` |
| `typeorm` | `createQueryBuilder().where("user.id = " + id)` — bukan parameter binding |
| `drizzle` | `sql.raw("SELECT * WHERE id = " + id)` — raw string |
| `django-orm` | `User.objects.raw(f"SELECT * WHERE email = '{email}'")` — f-string di raw() |
| `eloquent` | `DB::select("SELECT * WHERE email = '$email'")` — variable langsung |
| `sequelize` | `sequelize.query("SELECT * WHERE id = " + id)` — concat |

**Command Injection:**

| `lang` | Pola Vulnerable |
|--------|----------------|
| `go` | `exec.Command("sh", "-c", userInput)` |
| `node` | `child_process.exec(userInput)`, `exec(\`ls ${userInput}\`)` |
| `python` | `subprocess.run(userInput, shell=True)`, `os.system(userInput)` |
| `php` | `exec($userInput)`, `shell_exec($userInput)`, `system($userInput)` |
| `java` | `Runtime.getRuntime().exec(userInput)` |

**XSS (Server-Side Rendering):**

| `backend`/`frontend` | Pola Vulnerable |
|---------------------|----------------|
| `django` | `mark_safe(user_input)`, `{% autoescape off %}` |
| `flask` | `Markup(user_input)`, `render_template_string(user_input)` |
| `laravel` | `{!! $userInput !!}` di Blade (unescaped) |
| `nuxt`/`vue` | `v-html="userInput"` dengan data dari user |
| `react`/`nextjs` | `dangerouslySetInnerHTML={{ __html: userInput }}` |

**NoSQL Injection (jika `db: mongodb`):**
- Cari `$where`, `$regex` dengan input langsung dari user
- `db.collection.find({ [userInput]: value })`

**Template Injection:**
- `flask`: `render_template_string(f"Hello {name}")` — user bisa inject `{{ 7*7 }}`
- `django`: `Template(user_input).render(context)`

**Path Traversal:**
- Cari `filepath.Join(baseDir, userInput)` tanpa validasi di Go
- `path.join(baseDir, req.params.file)` tanpa sanitasi di Node
- `open(f"{base_dir}/{user_filename}")` di Python

#### A04: Insecure Design

- [ ] Tidak ada rate limiting pada endpoint sensitif (login, register, forgot password, OTP)
- [ ] Tidak ada account lockout setelah failed login berulang
- [ ] Tidak ada pembatasan jumlah resource yang bisa dibuat per user (mass creation)
- [ ] Proses bisnis kritis tanpa konfirmasi ulang (transfer, delete, perubahan email)

#### A05: Security Misconfiguration

- [ ] Debug mode aktif di production (`DEBUG=True`, `gin.SetMode(gin.DebugMode)`)
- [ ] Stack trace / error detail terekspos ke user di production
- [ ] Default credential tidak diganti (admin/admin, root/root)
- [ ] Direktori listing aktif (index.html tidak ada tapi folder accessible)
- [ ] Unnecessary HTTP methods enabled (TRACE, TRACK)
- [ ] CORS `*` pada endpoint yang butuh auth

#### A06: Vulnerable and Outdated Components

- [ ] Cek versi dependency di `go.mod`, `package.json`, `requirements.txt`, `composer.json`
- [ ] Cari dependency yang tidak di-pin ke versi spesifik
- [ ] `package.json` menggunakan `^` atau `~` yang bisa auto-upgrade ke versi vulnerable

#### A07: Identification and Authentication Failures

| Area | Check |
|------|-------|
| Password Policy | Tidak ada validasi minimum panjang/kompleksitas |
| Brute Force | Login endpoint tanpa rate limiting / CAPTCHA |
| Session | Session ID tidak di-regenerate setelah login |
| JWT | Token tidak di-blacklist setelah logout, expiry terlalu panjang |
| "Remember Me" | Token persisten disimpan insecure |
| Password Reset | Token reset lemah atau tidak expire |

#### A08: Software and Data Integrity Failures

| `lang`/stack | Pola Vulnerable |
|--------------|----------------|
| `node` | `JSON.parse` dari sumber tidak trusted tanpa validasi, `npm install` tanpa lockfile |
| `python` | `pickle.loads(user_data)`, `yaml.load()` tanpa `Loader=yaml.SafeLoader` |
| `java` | `ObjectInputStream.readObject()` dari input tidak trusted |
| `php` | `unserialize($userInput)` |
| `go` | `encoding/gob` decode dari user input |

#### A09: Security Logging and Monitoring Failures

- [ ] Tidak ada logging untuk: failed login, permission denied, input validation failure
- [ ] Log mengandung data sensitif (password, token, credit card)
- [ ] Log hanya ke stdout tanpa persistent storage
- [ ] Tidak ada alerting untuk anomali (banyak failed login, dll)
- [ ] Error ditelan (`_` atau `pass`) tanpa logging

#### A10: Server-Side Request Forgery (SSRF)

Cari pola:

| `lang` | Pola Vulnerable |
|--------|----------------|
| `go` | `http.Get(userInput)`, `http.NewRequest("GET", userInput, nil)` |
| `node` | `axios.get(userInput)`, `fetch(userInput)`, `request(userInput)` |
| `python` | `requests.get(userInput)`, `urllib.request.urlopen(userInput)` |
| `php` | `file_get_contents($userInput)`, `curl_setopt($ch, CURLOPT_URL, $userInput)` |
| `java` | `new URL(userInput).openConnection()` |

Tidak ada whitelist domain yang diizinkan? → Temuan SSRF.

---

### Check 2.2 — OWASP API Security Top 10 (2023)

*Jalankan jika `has_api: yes`*

#### API1: Broken Object Level Authorization (BOLA/IDOR)

Untuk setiap endpoint yang menerima `{id}` atau `{uuid}`:
- Apakah ada pengecekan bahwa resource tersebut milik user yang sedang login?
- Apakah bisa akses `/api/users/2/orders` padahal user saat ini adalah user ID 1?

#### API2: Broken Authentication

- [ ] Token dikirim via URL query param (terekspos di log server)
- [ ] Token tidak expire (tidak ada `exp` claim di JWT)
- [ ] Basic auth digunakan pada API (bukan Bearer token)
- [ ] API key sama untuk semua environment (dev/staging/prod)

#### API3: Broken Object Property Level Authorization

- [ ] Mass assignment: semua field dari request body langsung disimpan ke DB
- [ ] Response mengekspos field yang tidak perlu (password_hash, internal_id, dll)

| ORM | Pola Vulnerable |
|-----|----------------|
| `gorm` | `db.Save(&user)` dari struct yang langsung di-bind dari `c.ShouldBindJSON` |
| `django-orm` | `User.objects.create(**request.data)` tanpa filter field |
| `eloquent` | `User::create($request->all())` tanpa `$fillable` |
| `typeorm` | `userRepo.save(req.body)` langsung |

#### API4: Unrestricted Resource Consumption

- [ ] Tidak ada pagination pada endpoint list (bisa return jutaan record)
- [ ] Tidak ada limit ukuran file upload
- [ ] Tidak ada rate limiting per user/IP
- [ ] Query parameter bisa manipulasi jumlah record: `?limit=999999`

#### API5: Broken Function Level Authorization

- [ ] Endpoint admin (`DELETE /api/users/:id`, `POST /api/admin/...`) tanpa role check
- [ ] HTTP method yang berbeda tidak dicek secara konsisten (GET aman tapi DELETE tidak)
- [ ] Dokumentasi endpoint vs implementasi tidak konsisten (hidden endpoint tanpa auth)

#### API6: Unrestricted Access to Sensitive Business Flows

- [ ] Proses checkout / booking / transfer tanpa idempotency check (bisa double submit)
- [ ] Voucher / promo code bisa digunakan unlimited tanpa tracking
- [ ] Endpoint scraping-prone tanpa proteksi (bulk export data)

#### API7: Server Side Request Forgery

*(sudah covered di A10 — catat jika ditemukan via webhook URL, URL preview, import from URL)*

#### API8: Security Misconfiguration

- [ ] CORS mengizinkan `*` pada API yang butuh auth
- [ ] HTTP methods tidak dibatasi per endpoint
- [ ] Error response mengandung stack trace / query detail
- [ ] API berjalan di HTTP bukan HTTPS

#### API9: Improper Inventory Management

- [ ] Ada endpoint versi lama (`/api/v1/`, `/api/legacy/`) yang masih aktif tanpa auth
- [ ] Endpoint debug / test masih aktif di production (`/api/test`, `/health` dengan detail)
- [ ] Tidak ada API versioning — breaking change langsung ke endpoint aktif

#### API10: Unsafe Consumption of APIs

- [ ] Response dari third-party API langsung di-forward ke user tanpa validasi
- [ ] Data dari webhook eksternal langsung diproses tanpa signature verification
- [ ] Tidak ada timeout pada outbound HTTP call ke service lain

---

### Check 2.3 — CWE/SANS Top 25 (2024)

Fokus pada CWE yang paling relevan untuk web dan belum covered di atas:

| CWE | Nama | Yang Dicari |
|-----|------|------------|
| **CWE-352** | CSRF | Form POST / state-changing endpoint tanpa CSRF token. Cek: middleware csrf aktif? SameSite cookie? |
| **CWE-434** | Unrestricted File Upload | Upload endpoint: validasi tipe file? Ekstensi? Magic bytes? File disimpan di web root yang accessible? |
| **CWE-611** | XML External Entity (XXE) | Parsing XML dari user input. Go: `encoding/xml`, Python: `xml.etree`, Java: `DocumentBuilder` — apakah external entity disabled? |
| **CWE-918** | SSRF | *(covered di A10)* |
| **CWE-798** | Hardcoded Credentials | Grep: `password =`, `secret =`, `api_key =`, `token =` dengan value literal (bukan env var) |
| **CWE-22** | Path Traversal | *(covered di A03)* |
| **CWE-502** | Deserialization | *(covered di A08)* |
| **CWE-269** | Improper Privilege Management | Service berjalan sebagai root? Docker container sebagai root? File permission terlalu luas? |
| **CWE-319** | Cleartext Transmission | HTTP endpoint untuk data sensitif? Cookie tanpa `Secure` flag? |
| **CWE-307** | Improper Restriction of Excessive Auth Attempts | Rate limiting pada login, OTP, forgot password |
| **CWE-601** | Open Redirect | `redirect(request.args.get('next'))` tanpa validasi domain. Cari: `redirect`, `302`, `Location` header dari user input |
| **CWE-918** | ReDoS | Regex kompleks pada input user. Cari pattern dengan nested quantifier: `(a+)+`, `([a-zA-Z]+)*` |

---

### Check 2.4 — OWASP ASVS v4.0 (Level 1 & 2)

Fokus pada area yang paling sering diabaikan:

#### V2: Authentication

- [ ] Password hashing: bcrypt (cost ≥ 10), argon2id, atau scrypt? *Bukan* SHA/MD5
- [ ] Forgot password: token random (≥ 32 bytes), expire ≤ 1 jam, single-use
- [ ] Login response tidak membedakan "user tidak ada" vs "password salah" (user enumeration)
- [ ] Multi-factor authentication tersedia untuk akun sensitif

#### V3: Session Management

- [ ] Session token: panjang ≥ 128 bit, random dari CSPRNG
- [ ] Session diinvalidasi setelah logout (server-side revocation)
- [ ] Cookie: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`
- [ ] JWT: `exp` claim ada dan wajar (≤ 24 jam untuk access token)
- [ ] Refresh token dirotasi setelah digunakan (rotation)

#### V4: Access Control

- [ ] Deny-by-default: middleware auth diterapkan global, bukan opt-in per route
- [ ] Resource ownership divalidasi di service/repository layer, bukan hanya middleware

#### V5: Validation, Sanitization, Encoding

- [ ] Semua input divalidasi: tipe, panjang, format, range
- [ ] Output di-encode sesuai konteks: HTML (escape), SQL (parameterized), command (avoid)
- [ ] File upload: validasi magic bytes (bukan hanya ekstensi), disimpan di luar web root

#### V6: Cryptography

- [ ] TLS 1.2+ saja — TLS 1.0/1.1 disabled
- [ ] Cipher suite modern: AES-GCM, ChaCha20-Poly1305
- [ ] Key management: secret di environment variable atau secret manager, bukan hardcoded

#### V7: Error Handling and Logging

- [ ] Error production: generic message ke user, detail ke log
- [ ] Log ada untuk: auth events, access denied, input validation failure, admin actions
- [ ] Log tidak mengandung credential, PII, atau token

#### V8: Data Protection

- [ ] PII di-encrypt at rest jika tersimpan di DB
- [ ] Data sensitif tidak di-cache di browser (Cache-Control: no-store)
- [ ] Backup dienkripsi

#### V14: Configuration

- [ ] Dependency up to date (periksa go.sum, package-lock.json, requirements.txt)
- [ ] Environment separation: config production berbeda dari development
- [ ] Tidak ada test / dev data di production environment

---

### Check 2.5 — Security Headers

*Jalankan jika `frontend` ≠ `none` atau project adalah web app*

Cari di: `nuxt.config.ts`, `next.config.ts`, nginx/caddy config, middleware, response header setup.

| Header | Status | Nilai yang Diharapkan |
|--------|--------|----------------------|
| `Content-Security-Policy` | Ada/Tidak | `default-src 'self'` + whitelist spesifik |
| `X-Content-Type-Options` | Ada/Tidak | `nosniff` |
| `X-Frame-Options` | Ada/Tidak | `DENY` atau `SAMEORIGIN` (atau CSP `frame-ancestors`) |
| `Strict-Transport-Security` | Ada/Tidak | `max-age=31536000; includeSubDomains` |
| `Referrer-Policy` | Ada/Tidak | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Ada/Tidak | Disable fitur tidak dipakai |
| `Cache-Control` | Sensitif | `no-store` untuk halaman auth/private |
| `Set-Cookie` | Ada auth cookie | `HttpOnly; Secure; SameSite=Lax` |

Nilai untuk check per framework:

| `frontend` | Tempat Set Header |
|-----------|------------------|
| `nuxt` | `nuxt.config.ts` → `routeRules` / `nitro.headers` / `@nuxtjs/security` module |
| `nextjs` | `next.config.ts` → `headers()` function |
| `express` | `helmet` middleware |
| `fastapi` | `from starlette.middleware.cors import CORSMiddleware`, custom middleware |
| `django` | `SECURE_*` settings, `django-csp` |
| `laravel` | `middleware/TrustProxies.php`, `config/security.php` |
| `gin`/`echo` | Custom middleware atau `secure` library |

---

### Check 2.6 — Supply Chain & Dependency Security

#### Lockfile Integrity

- [ ] `lockfile: yes` → lockfile di-commit ke repo? Tidak di-.gitignore?
- [ ] `lockfile: no` → risiko tinggi: build bisa mengambil versi berbeda setiap run

#### Dependency Pinning

| `lang` | Check |
|--------|-------|
| `node` | `package.json` menggunakan versi exact (`"express": "4.18.2"`) atau range (`^4.18.2`)? Range = risiko |
| `go` | `go.sum` ada dan di-commit? `replace` directive mencurigakan? |
| `python` | `requirements.txt` pin exact version (`django==4.2.1`) atau flexible (`django>=4`)? |
| `php` | `composer.lock` di-commit? |

#### Known Vulnerable Patterns

Grep untuk pattern ini terlepas dari versi:
- `node`: `node-serialize`, `serialize-javascript` (jika digunakan dengan untrusted input)
- `python`: `PyYAML` tanpa `Loader=yaml.SafeLoader`, `pickle` dengan untrusted data
- Semua: dependency yang tidak maintenance (cek last commit di repo jika perlu)

#### Secret Leakage in Git

- [ ] Grep di file config yang mungkin ter-commit: `.env`, `config.yaml`, `*.json`
- [ ] Cek `.gitignore` — apakah `.env`, `secrets.*`, `*.pem` ada di list?
- [ ] Cek apakah ada file `.env.example` dengan nilai real (bukan placeholder)

---

## Fase 3 — Risk Scoring & Prioritization

### Severity Matrix

| Severity | Kriteria | Contoh |
|----------|----------|--------|
| 🔴 **CRITICAL** | Exploitable langsung, RCE, auth bypass total, data breach massal | SQLi tanpa auth, hardcoded admin password, RCE via command injection |
| 🟠 **HIGH** | Exploitable dengan kondisi minimal, privilege escalation, IDOR massal | BOLA pada endpoint user data, JWT tanpa signature verify, SSRF |
| 🟡 **MEDIUM** | Butuh kondisi spesifik, dampak terbatas atau indirect | CSRF pada form biasa, missing rate limit, info disclosure via error |
| 🔵 **LOW** | Best practice, defense-in-depth, risiko minimal direct | Missing security header, log verbosity, minor misconfiguration |
| ℹ️ **INFO** | Observasi, peluang hardening | Dependency bisa diupdate, komentar berisi info sensitif |

### Skoring Tambahan

Untuk setiap temuan CRITICAL/HIGH, tambahkan:
- **Attack Vector**: Network (paling berbahaya) / Adjacent / Local
- **Privileges Required**: None (paling berbahaya) / Low / High
- **User Interaction**: None (paling berbahaya) / Required
- **Exploitability**: Mudah (public exploit ada) / Moderat / Sulit

---

## Fase 4 — Report Output

```markdown
# 🔒 Security Audit Report: [Nama Project]

**Audit Date:** [tanggal]
**Stack:** [dari STACK block]
**Frameworks Applied:** OWASP Top 10 (2021) · OWASP API Security Top 10 (2023) · CWE/SANS Top 25 · ASVS v4.0 · Security Headers · Supply Chain

---

## 📊 Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | N |
| 🟠 High | N |
| 🟡 Medium | N |
| 🔵 Low | N |
| ℹ️ Info | N |
| **Total** | **N** |

**Overall Risk Level:** [CRITICAL / HIGH / MEDIUM / LOW]

[2–3 kalimat ringkasan kondisi keamanan project secara keseluruhan]

---

## 🔴 Critical & High Findings

### [KODE-NNN] [Judul Temuan]

**Severity:** 🔴 Critical
**Framework:** OWASP A03 · CWE-89
**File:** `path/to/file.go:47`
**Attack Vector:** Network · No Privileges Required · No User Interaction

**Masalah:**
[Penjelasan teknis singkat mengapa ini berbahaya]

**Kode Vulnerable:**
```[lang]
// kode bermasalah
```

**Fix:**
```[lang]
// kode yang benar
```

**Remediation:** [Langkah konkret untuk perbaikan]

---

[Ulangi untuk setiap Critical dan High finding]

---

## 🟡 Medium Findings

[Format sama tapi lebih ringkas — judul + masalah + fix]

---

## 🔵 Low & Info Findings

[Tabel ringkas]

| ID | Judul | Framework | File |
|----|-------|-----------|------|
| ... | ... | ... | ... |

---

## ✅ Passed Checks

[List check penting yang LULUS — berikan kredit untuk yang sudah benar]

| Area | Status | Catatan |
|------|--------|---------|
| Password Hashing | ✅ | bcrypt cost=12 |
| ... | ... | ... |

---

## 🛡️ Security Headers Status

[Jika web app]

| Header | Status | Nilai Saat Ini | Rekomendasi |
|--------|--------|----------------|-------------|
| CSP | ❌ Missing | — | `default-src 'self'` |
| HSTS | ✅ | `max-age=31536000` | — |
| ... | ... | ... | ... |

---

## 📦 Dependency Security

| Status | Keterangan |
|--------|-----------|
| Lockfile | [✅ ada / ❌ tidak ada] |
| Pinning | [✅ exact / ⚠️ range / ❌ tidak ada] |
| .gitignore | [✅ `.env` excluded / ❌ tidak] |
| Hardcoded secrets | [✅ tidak ada / ❌ ditemukan di: path] |

---

## 🚀 Remediation Roadmap

Urutkan berdasarkan: **severity × effort** (critical + mudah diperbaiki = prioritas #1)

| Prioritas | Finding | Effort | Impact | Assignee |
|-----------|---------|--------|--------|----------|
| 🔴 1 | [judul] | 1 jam | Critical | Dev |
| 🔴 2 | [judul] | 2 jam | Critical | Dev |
| 🟠 3 | [judul] | 4 jam | High | Dev |
| ... | ... | ... | ... | ... |

### Quick Wins (< 1 jam, impact tinggi)

1. [Item paling cepat diperbaiki]
2. [Item kedua]
3. [Item ketiga]

---

## 📋 Catatan Auditor

[Konteks penting, asumsi yang dibuat, area yang tidak bisa diaudit (misal: runtime behavior),
rekomendasi untuk audit lanjutan (pentest, DAST, dll)]
```

---

## Aturan Output

- **Jangan** hanya list masalah tanpa kode fix — setiap finding harus ada contoh perbaikannya
- **Severity jujur** — jangan downgrade karena "mungkin tidak dieksploitasi"
- **File dan line number** — sertakan jika bisa diidentifikasi dari static analysis
- **False positive awareness** — jika tidak bisa konfirmasi 100%, tandai `[POSSIBLE]`
- **Passed checks wajib ada** — jangan hanya list masalah, apresiasi yang sudah benar
- **Quick wins harus ada** — minimal 3 hal yang bisa diperbaiki < 1 jam

---

## Checklist Kualitas

Verifikasi sebelum deliver:

- [ ] STACK block terisi (Fase 0 selesai)
- [ ] SURFACE block berisi semua entry points (Fase 1 selesai)
- [ ] Semua 6 framework check sudah dijalankan
- [ ] Setiap finding ada: severity, framework reference, file, kode vulnerable, kode fix
- [ ] Remediation roadmap diurutkan severity × effort
- [ ] Quick wins (< 1 jam) sudah diidentifikasi
- [ ] Passed checks ada (bukan hanya masalah)
- [ ] Security headers dicek jika ada frontend/web app
- [ ] Dependency / supply chain dicek
- [ ] Tidak ada finding tanpa rekomendasi konkret
