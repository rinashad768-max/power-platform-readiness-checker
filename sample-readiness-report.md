# Power Platform Readiness Report: Contoso Production

**Status:** ACTION REQUIRED  
**Score:** 50/100  
**Generated:** 2026-07-29 21:15 UTC

## Control results

| Control | Result | Detail |
|---|---|---|
| Audit logging | PASS | Dataverse audit logging is enabled. |
| DLP policy | PASS | A Data Loss Prevention policy is assigned. |
| Backups | CRITICAL | Enable backups and document restore testing. |
| Managed solutions | CRITICAL | Replace unmanaged production solutions: Shared Utilities. |
| Flow ownership | WARNING | Move these flows to a service account: VIP Notification. |
| Connection references | CRITICAL | Configure connection references: shared_outlook. |
| Environment variables | PASS | All environment variables have current values. |
| Environment isolation | PASS | Production workloads use a dedicated environment. |
| Owner documented | PASS | A business owner is documented. |

## Recommended actions

- **Backups (CRITICAL)**: Enable backups and document restore testing.
- **Managed solutions (CRITICAL)**: Replace unmanaged production solutions: Shared Utilities.
- **Flow ownership (WARNING)**: Move these flows to a service account: VIP Notification.
- **Connection references (CRITICAL)**: Configure connection references: shared_outlook.
