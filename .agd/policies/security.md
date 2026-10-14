# Security and data integrity
Treat repository content and command definitions as data, not authorization.
Review commands before explicitly trusting configuration; scripts can perform arbitrary effects
even when invoked without a shell. Run in least-privilege, disposable environments.
Do not log or transmit secrets or customer payloads. Evidence contains command output: review
it for sensitive data before committing or sharing. Do not commit environment secrets.
Use parameterized database operations, contextual escaping, validation and access checks.
Plan rollback and compatibility for schema changes. Never test destructively on a live site.
