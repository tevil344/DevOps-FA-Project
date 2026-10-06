# CropLeaf viva - ready answers

## 1. Where is the login functionality in the backend?

The JSON login endpoint is registered in `backend/app/urls.py` as `/api/auth/login/` and implemented in `backend/app/views.py` in `api_login`. The regular Django form login is `login_view` in that same file. The React login screen is `frontend/src/components/UserAuth.jsx`.

Show this small, accurate snippet from `api_login`:

```python
username = data.get('username', '').strip()
password = data.get('password', '')
user = authenticate(request, username=username, password=password)

if user is not None:
    auth_login(request, user)
    request.session.set_expiry(timedelta(days=3))
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')
return HttpResponse('{"error": "Invalid username or password"}', status=401)
```

Explanation: `authenticate` verifies the supplied password against Django's stored password hash. It never compares a plaintext password in our code. `auth_login` creates the server-side session and the session cookie identifies the user on later requests. CSRF protection is enabled; the browser first receives a CSRF cookie from `/api/csrf/` and sends it on state-changing requests.

## 2. What are the benefits of Docker, Terraform, and Ansible?

| Tool | What it does here | Main benefit |
|---|---|---|
| Docker | Packages the React/Nginx frontend, Django backend and PostgreSQL services | Reproducible runtime: the stack behaves the same on laptop and EC2 |
| Terraform | Declares EC2, its security group and disk settings | Repeatable Infrastructure as Code; plan changes before applying them and destroy cleanly later |
| Ansible | Installs Docker, pulls a declared Git revision, writes protected configuration and starts Compose | Repeatable, idempotent server configuration without manually SSH-ing through steps |

One-line memory aid: **Terraform creates, Ansible configures, Docker runs.**

The end-to-end flow is:

```text
Source code -> Terraform -> EC2 -> Ansible -> Docker Compose -> CropLeaf -> browser
```

## 3. Which security measures and encryption are used?

Say only what the project actually implements or requires:

- Passwords use Django's password-hashing framework. Django 5 uses PBKDF2 with SHA-256 by default; the app calls `set_password` on registration and `authenticate` at login. Passwords are not stored as plaintext.
- CSRF middleware is enabled. The React client retrieves a CSRF cookie and returns it in `X-CSRFToken` before login, registration, and prediction POSTs.
- Secrets such as `SECRET_KEY`, database password and model URLs are environment variables in `.env`; `.env`, PEM keys and Terraform state are excluded by `.gitignore`. Ansible writes the server file with `0600` permissions and its real variable file should be encrypted using Ansible Vault.
- CORS is an explicit allow-list, rather than `*` with credentials. Debug is disabled in the deployment environment.
- On AWS, the Terraform root EBS volume is encrypted (`encrypted = true`) and EC2 requires IMDSv2 tokens. SSH ingress is restricted to the administrator CIDR; only HTTP is public for the demo.
- Docker exposes only Nginx port 80. The Django and PostgreSQL services remain on the internal Compose network. The Django container runs as the unprivileged `cropleaf` user.
- For a real public deployment, terminate **HTTPS/TLS** at a load balancer or Nginx and set `SECURE_SSL_REDIRECT=true`, `SESSION_COOKIE_SECURE=true`, and `CSRF_COOKIE_SECURE=true`. This protects traffic in transit. The supplied assessment stack uses HTTP to keep the EC2 demo simple.

Do not claim AES application-level encryption: the current code does not encrypt individual database fields. EBS encryption protects the EC2 disk at rest, and TLS is the correct transport encryption when enabled.

## 4. Four members: who contributed what?

Use your actual names in `TEAM_CONTRIBUTIONS.md`; a defensible division is:

1. Application and authentication - Django views, routes, forms and login demo.
2. Docker - Dockerfiles, Compose services, Nginx reverse proxy and local verification.
3. Terraform - AWS provider, EC2, security group, encrypted volume and outputs.
4. Ansible and QA - inventory, Docker installation, deployment playbook, health-check and documentation.

Each member should explain one artifact and show an output. Keep commits, command output and screenshots as evidence.

## Quick commands to remember

```bash
# local
docker compose up --build -d
curl http://localhost/api/health/

# provisioning
cd terraform && terraform init && terraform validate && terraform plan && terraform apply

# configuration + deployment
ansible -i ansible/inventory.ini cropleaf -m ping
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-vault-pass

# cleanup after assessment
cd terraform && terraform destroy
```
