# SOP: Daily System Health Check

**Purpose:** Ensure all critical systems are operating normally and identify potential issues before they become problems
**Scope:** All production systems and services
**Owner:** Operations Team
**Last Updated:** August 16, 2025

## Prerequisites
- [ ] Access to monitoring dashboards
- [ ] VPN connection established
- [ ] Checklist template ready
- [ ] Incident response contact list available

## Steps

### Phase 1: System Monitoring
1. Open primary monitoring dashboard
2. Check CPU usage across all servers (should be < 80%)
3. Verify memory utilization (should be < 85%)
4. Review disk space usage (should be < 90%)
5. Check network connectivity status

### Phase 2: Service Health
1. Verify all critical services are running
2. Test application endpoints
3. Check database connectivity
4. Validate backup completion status
5. Review error logs for anomalies

### Phase 3: Performance Metrics
1. Check response times for key endpoints
2. Review transaction volumes
3. Validate cache hit ratios
4. Monitor queue lengths
5. Check SSL certificate expiry dates

## Verification
- [ ] All systems showing green status
- [ ] No critical alerts active
- [ ] Response times within acceptable ranges
- [ ] Daily checklist completed and filed
- [ ] Any issues escalated appropriately

## Troubleshooting

| Issue | Symptoms | Solution |
|-------|----------|----------|
| High CPU usage | CPU > 80% sustained | Check running processes, restart if needed, escalate if persistent |
| Disk space low | Disk > 90% full | Clean up logs, temporary files, or provision more space |
| Service down | Service unreachable | Restart service, check logs, follow [[Incident Response]] |
| Slow response | Response time > 2s | Check database queries, cache status, network latency |

## Related Procedures
- [[Incident Response]]
- [[System Restart Procedures]]
- [[Backup Verification]]
- [[Performance Monitoring]]

## Revision History
| Date | Changes | Author |
|------|---------|---------|
| 2025-08-16 | Initial version | Operations Team |

---

*Tags: #sop #operations #daily #monitoring #health-check*
