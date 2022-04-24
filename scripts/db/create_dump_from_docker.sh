docker-compose -f /root/family_budget_bot/docker-compose.yaml exec postgres pg_dump -U postgres family_budget > /root/family_budget_bot/dump.sql
