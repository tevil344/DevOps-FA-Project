# FA2 CI/CD implementation

## Pipeline design

```text
Developer push / pull request
          |
          v
GitHub Actions CI: Python syntax -> React build -> Compose validation -> IaC scan
          |
          v
Manual, protected production approval
          |
          v
GitHub Actions CD -> Ansible -> EC2 Docker Compose -> health check and metrics
```

The CI workflow is `.github/workflows/ci.yml`. It runs on every pull request and push to `main`. A failing build, invalid Compose file, or high/critical Infrastructure-as-Code finding fails the job before deployment.

The CD workflow is `.github/workflows/deploy.yml`. It is intentionally manual (`workflow_dispatch`) and uses a GitHub **production environment** so a reviewer can approve the deployment. It calls the same Ansible playbook used in the local demonstration, avoiding deployment drift. The playbook polls `/api/health/` after Compose starts, so the CD job fails rather than reporting success when the deployed backend is not ready.

## GitHub configuration required before using CD

1. Push this FA-ready repository to your group's GitHub repository.
2. In GitHub, create the `production` environment and require a reviewer if your rubric expects approval gates.
3. Add these repository/environment secrets. Never add them to a workflow file:

| Secret | Contents |
|---|---|
| `SSH_PRIVATE_KEY` | EC2 private key contents |
| `ANSIBLE_INVENTORY` | The private inventory line for the EC2 host |
| `ANSIBLE_VAULT_PASSWORD` | Password used to encrypt `ansible/group_vars/all.yml` |

4. Encrypt the real `ansible/group_vars/all.yml` with Ansible Vault, commit the encrypted file, and start **CD - Deploy CropLeaf** from the Actions tab with a tested Git commit or tag.

For faculty, show one successful CI run, one pending/approved deployment gate, and the Ansible task output. Do not trigger CD against an untested commit.
