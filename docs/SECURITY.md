# PAA — Sécurité (MVP Étape 10)

1. Réseau & Accès
   - HTTPS interne (TLS), HSTS 1 an.
   - Allowlist IP sur /admin et /paa/adminpanel via ADMIN_IP_ALLOWLIST (.env).
2. Comptes & MFA
   - MFA requis pour SA/PP (django-otp posé, enrôlement à finaliser étapes 11–13).
3. Secrets & Chiffrement
   - Champs sensibles via EncryptedTextField (Fernet). Clé FERNET_KEY dans .env.
   - Backups PostgreSQL chiffrés (openssl AES-256) + test restauration (scripts ops/).
4. Journalisation & Audit
   - AuditLog append-only, redaction de champs sensibles, exportable.
5. Headers & Cookies
   - CSP strict, cookies Secure/HttpOnly/SameSite=Strict, X-Frame-Options DENY, NoSniff.
6. SAST
   - Bandit exécuté en CI. Corriger findings bloquants avant prod.
7. Procédures
   - Revue mensuelle des permissions (SA/PP/P/U).
   - Test restauration trimestriel (ops/restore_test.sh).
   - Rotation FERNET_KEY planifiée (procédure à documenter).

Check-list déploiement prod :
- [ ] ADMIN_IP_ALLOWLIST défini
- [ ] FERNET_KEY défini (32 bytes base64url)
- [ ] Certificats TLS valides installés (nginx)
- [ ] Scripts backups planifiés (cron)
- [ ] Tests Bandit pass OK (ou findings acceptés)
- [ ] MFA activée pour SA/PP (si politique interne)
