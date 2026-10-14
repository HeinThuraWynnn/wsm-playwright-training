# Approval boundaries
Obtain explicit authorization for production deployment/database changes, destructive migrations,
out-of-scope deletion, overwriting user changes, real payments, live customer data, secret
transmission, major architecture changes, and significant external effects. Existing explicit
authorization remains valid within its scope; do not repeatedly request approval.

The runner blocks declared protected operations unless `--approve OPERATION` is passed by a
trusted operator. `--trust-config` authorizes execution of reviewed commands, not production
side effects. A mislabeled command can bypass these labels: use filesystem, network and account
permissions outside AGD for actual containment. The CLI does not authenticate the approver.
Pushes and deployments are never part of AGD's default verification configuration.
