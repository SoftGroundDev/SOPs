# SOP: Database Backup Verification

**Purpose:** Verify that database backups are completed successfully and can be restored
**Scope:** All production databases
**Owner:** Database Team
**Last Updated:** August 16, 2025

## Prerequisites
- [ ] Access to backup monitoring system
- [ ] Database admin credentials
- [ ] Test restoration environment available

## Steps

### Phase 1: Backup Status Check
1. Login to backup monitoring dashboard
2. Verify last backup completion time (should be within 24 hours)
3. Check backup file sizes against expected ranges
4. Review backup logs for any errors or warnings

### Phase 2: Integrity Verification
1. Run backup integrity check commands
2. Verify checksum validation passes
3. Document any integrity issues

### Phase 3: Test Restoration
1. Select a non-critical backup for testing
2. Restore to test environment
3. Verify data integrity and completeness
4. Document restoration time and any issues

## Success Criteria
- All backups completed within SLA timeframes
- No corruption detected in backup files
- Test restoration completes successfully
- All verification steps pass

## Troubleshooting
If backup verification fails:
1. Check disk space on backup storage
2. Review database server logs
3. Contact Database Team lead
4. Follow [[Incident Response Protocol]] if critical

## Related Documents
- [[Daily System Health Check]]
- [[Incident Response Protocol]]
