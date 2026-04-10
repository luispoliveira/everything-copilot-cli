# NestJS Backend Expert — Memory & Lessons Learned

> This file is automatically maintained by the NestJS Backend Expert agent.
> **Read at the start of every run. Update at the end of every run.**

---

## ⚠️ Known Pitfalls

<!-- Format:
### Pitfall: [Short title]
- **Context**: When/where does this happen?
- **What went wrong**: What was the mistake?
- **Fix/Avoid**: What to do instead
- **Project**: (optional) specific project where this occurred
- **Date**: YYYY-MM-DD
-->

### Pitfall: ExcelJS date parsing returns multiple formats

- **Context**: When reading date cells from Excel files using ExcelJS library
- **What went wrong**: Date validation using `instanceof Date` fails for dates stored as strings (DD/MM/YYYY) in Excel, causing valid dates to be skipped
- **Fix/Avoid**: Create a robust date parser that handles:
  - Date objects (already parsed)
  - DD/MM/YYYY string format (common in European/Portuguese Excel files)
  - ISO date strings
  - Excel serial numbers
  - Always validate the parsed date is a real calendar date
- **Project**: ext-arrabida-wms-back-nx (ProductsService.importValidities)
- **Date**: 2026-04-09

---

## ✅ Successful Patterns

<!-- Format:
### Pattern: [Short title]
- **Context**: When to apply this
- **Approach**: What worked well
- **Project**: (optional)
- **Date**: YYYY-MM-DD
-->

### Pattern: Multi-format date parsing helper

- **Context**: When importing data from Excel files where date formats can vary
- **Approach**: Create a private `parseValidityDate(value: unknown)` helper that:
  1. Checks if value is already a valid Date object
  2. Tries regex matching for DD/MM/YYYY format
  3. Validates the parsed date components match the actual date (e.g., prevents 31/02/2026)
  4. Falls back to standard Date constructor for ISO strings
  5. Handles Excel serial numbers
  6. Returns `null` for invalid inputs
- **Project**: ext-arrabida-wms-back-nx
- **Date**: 2026-04-09

---

## 📋 Project-Specific Notes

<!-- Specific observations about codebases encountered, e.g.:
- Project X uses a custom PrismaService wrapper — inject it differently
- Project Y has a monorepo (Turborepo) — adjust import paths accordingly
- Project Z uses better-auth with a custom session strategy
-->

### ext-arrabida-wms-back-nx

- **Type**: Nx monorepo with NestJS apps and libs
- **Structure**: Apps (api, cli, worker) + Libs (data-layer, auth, prisma, etc.)
- **ORM**: Prisma with PostgreSQL
- **Locations**: Portuguese farmacia (pharmacy) warehouse management system
- **Date formats**: Uses DD/MM/YYYY in Excel imports (European format)
- **Date**: 2026-04-09

---

## 📦 Package Version Compatibility

<!-- Track known version conflicts or compatibility issues. Format:
- `@nestjs/bullmq@X` requires `bullmq@Y` — do not upgrade independently
- `better-auth@X` session type requires explicit generic on `getSession<T>()`
-->

_No version notes yet._

---

## 🔒 Security Observations

<!-- Track security decisions made per project. Format:
- Project X: Rate limiting set to 60 req/min per IP on auth routes
- Project Y: CORS allow-list managed via ConfigService + Zod env var
-->

_No security notes yet._

---

## 🧪 Testing Patterns

<!-- Track effective test setup strategies. Format:
- Prisma mock: use `jest-mock-extended` + `mockDeep<PrismaClient>()` — works reliably
- BullMQ queue: mock `Queue` with `{ add: jest.fn() }` in unit tests
-->

_No testing notes yet._
