---
type: reference
version: Phase-2
created: 2026-05-12
updated: 2026-05-12
status: active
tags: [homelab, edge-runtime, sovereign, hardware, deployment, self-hosted]
---

# PCA Homelab Reference Architecture

## Executive Summary

This document provides a **practical reference implementation** for running PCA as a sovereign, self-contained edge runtime — no cloud dependencies, complete local control, portable across hardware platforms.

A "homelab" PCA instance:

- ✅ Runs entirely on local hardware (GPU-accelerated)
- ✅ Requires no Anthropic API keys for inference (uses local Qwen2.5)
- ✅ Maintains Obsidian vault offline (true single-user control)
- ✅ Can be replicated to new hardware in ~2 hours
- ✅ Costs ~CAD $1,500 upfront, then $50-100/year electricity

This is the **Phase 2 target** — the point at which PCA becomes independent from cloud services.

---

## Hardware Reference

### Minimum Configuration (Phase 2)

| Component | Specification | Rationale | Cost |
|-----------|---------------|-----------|------|
| **GPU** | NVIDIA RTX 3090 24GB | Runs Qwen2.5-32B (20GB) + cache | CAD $800 |
| **CPU** | 8+ cores, 3.5+ GHz | Handles n8n, Neo4j, ChromaDB | $150-300 |
| **RAM** | 32GB DDR4+ | OS + containers + GPU offload | $150 |
| **Storage (OS)** | 500GB NVMe SSD | System partition | $50 |
| **Storage (Data)** | 2TB NVMe SSD | Obsidian vault, models, databases | $150 |
| **Power Supply** | 1000W Gold PSU | RTX 3090 peak 420W | $150 |
| **Cooling** | Quality air/liquid cooler | Sustained inference load | $80-200 |
| **Case** | Standard ATX + 3x 120mm fans | Airflow priority | $100 |
| **Networking** | Gigabit Ethernet | Wired preferred over WiFi | Onboard |
| **Motherboard** | PCIe 4.0, 2x M.2 slots | Storage speed, GPU support | $200 |

**Total Cost: ~CAD $1,900–2,300**

**Electricity Cost:**
- Idle: ~50W (fans, SSD)
- Inference: ~600W (GPU 420W + CPU 150W + rest 30W)
- Average usage: 4 hours/day inference, 20 idle
- Daily: (4 × 600W + 20 × 50W) / 24h ≈ 141W average
- Yearly: 141W × 24h × 365 days ÷ 1000 = 1,235 kWh
- Cost (assuming CAD $0.12/kWh): **CAD $150/year**

### Recommended Configuration (Future-Proof Phase 3)

| Component | Specification | Rationale | Cost |
|-----------|---------------|-----------|------|
| **GPU** | NVIDIA RTX 4090 24GB | Handles larger models (70B+) | CAD $2,000 |
| **CPU** | 12+ cores, 4.0+ GHz (e.g., Ryzen 5900X) | Enterprise workloads | $500 |
| **RAM** | 64GB DDR4 | Multi-user, concurrent inference | $300 |
| **Storage (OS)** | 1TB NVMe SSD | Fast boot + caching | $100 |
| **Storage (Data)** | 4TB NVMe RAID-1 | High availability, redundancy | $400 |
| **Power Supply** | 1200W Platinum PSU | RTX 4090 peak 575W | $200 |
| **Cooling** | Liquid cooler (280mm+) | Sustained high-load operation | $200 |
| **Case** | Full ATX with cable management | Professional build | $200 |
| **UPS** | 2000VA | Graceful shutdown on power loss | $300 |

**Total Cost: ~CAD $4,200–4,800**

---

## Network Architecture

### Local Network Topology

```
┌─────────────────────────────────────────────┐
│           Home Network (192.168.1.x)        │
│           WiFi 5GHz + Wired                  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │        Homelab PCA Server            │  │
│  │  (wired: 192.168.1.50 static IP)     │  │
│  │                                      │  │
│  │  Docker Containers:                  │  │
│  │  ├─ n8n (8080)                       │  │
│  │  ├─ Neo4j (7474/7687)               │  │
│  │  ├─ ChromaDB (8001)                  │  │
│  │  ├─ Ollama GPU (11434)              │  │
│  │  ├─ PostgreSQL (5432)               │  │
│  │  ├─ Redis (6379)                    │  │
│  │  ├─ Prometheus (9090)               │  │
│  │  └─ Grafana (3000)                  │  │
│  └──────────────────────────────────────┘  │
│           │           │           │         │
│      Access from:  Access from:  Access    │
│      • localhost     • other     internal   │
│      • 127.0.0.1     computers  only       │
│      • local only    on LAN      (Docker   │
│                                  bridge)   │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │      User Devices                    │  │
│  │  ├─ MacBook/Laptop (WiFi)           │  │
│  │  │  → Access: http://192.168.1.50   │  │
│  │  ├─ iPad (WiFi)                     │  │
│  │  │  → Access: http://192.168.1.50   │  │
│  │  └─ Phone (WiFi)                    │  │
│  │     → Access: http://192.168.1.50   │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
              │
         🔒 Firewall
              │
          Internet
         (Optional:
          GitHub
          backup
          only)
```

### Network Configuration

**Docker Network (Internal):**

```
Docker Bridge: 172.17.0.0/16
├─ n8n (172.17.0.2:8080)
├─ Neo4j (172.17.0.3:7687)
├─ ChromaDB (172.17.0.4:8001)
├─ Ollama (172.17.0.5:11434)
├─ PostgreSQL (172.17.0.6:5432)
├─ Redis (172.17.0.7:6379)
├─ Prometheus (172.17.0.8:9090)
└─ Grafana (172.17.0.9:3000)
```

**Port Mapping (Host → Container):**

| Service | Host Port | Container Port | Accessible From |
|---------|-----------|-----------------|-----------------|
| **n8n** | 8080 | 3000 | LAN + localhost |
| **Grafana** | 3000 | 3000 | LAN + localhost |
| **Neo4j Browser** | 7474 | 7474 | localhost only |
| **ChromaDB API** | 8001 | 8000 | Docker only |
| **Ollama API** | 11434 | 11434 | Docker + localhost |
| **PostgreSQL** | 5432 | 5432 | Docker only |
| **Redis** | 6379 | 6379 | Docker only |
| **Prometheus** | 9090 | 9090 | localhost only |

**Firewall Rules:**

```
Inbound:
├─ 8080/tcp → n8n (allow LAN + localhost)
├─ 3000/tcp → Grafana (allow LAN + localhost)
├─ 7474/tcp → Neo4j (localhost only)
└─ 11434/tcp → Ollama (allow LAN + localhost)

Outbound:
├─ 443/tcp → HTTPS (for GitHub backup, optional)
└─ All others: blocked
```

---

## Installation & Configuration

### Step 1: Hardware Assembly (1 hour)

1. **Prepare motherboard** — Mount to case, install CPU cooler
2. **Install RAM** — Two 16GB modules (or four 8GB)
3. **Install GPUs** — RTX 3090 in PCIe x16 slot 1
4. **Install storage** — Two NVMe SSDs (OS + Data)
5. **Install PSU** — Connect 24-pin + 8-pin connectors
6. **Cable management** — Route cables for airflow
7. **Connect cooling** — Secure pump/radiator, connect fans to mobo
8. **Final checks** — No loose screws, all connectors seated

### Step 2: OS Installation (30 minutes)

Choose one:

**Option A: Ubuntu 22.04 LTS (Recommended)**

```bash
# Download ISO
curl -O https://releases.ubuntu.com/22.04/ubuntu-22.04-live-server-amd64.iso

# Flash to USB (macOS)
diskutil list
diskutil unmountDisk /dev/diskN
sudo dd if=ubuntu-22.04-live-server-amd64.iso of=/dev/rdiskN bs=1m

# Boot from USB, select:
# - Manual partitioning
#   - /dev/nvme0n1: 500GB (OS partition)
#   - /dev/nvme1n1: 2TB (data partition) → Mount at /pca
# - Install NVIDIA drivers (during install or after)
# - SSH server enabled
# - Minimal packages (no GUI)
```

**Option B: Proxmox (Advanced)**

For running multiple VMs/containers simultaneously.

### Step 3: Docker & Dependencies (30 minutes)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install NVIDIA drivers
sudo apt install -y nvidia-driver-535 nvidia-utils

# Verify GPU
nvidia-smi
# Output should show: NVIDIA RTX 3090 (24GB)

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install NVIDIA Container Runtime
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-container-runtime

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

### Step 4: PCA Deployment (60 minutes)

```bash
# Create data directories
sudo mkdir -p /pca/{obsidian-vault,ollama-models,chroma-indexes,postgresql-data,neo4j-graph,prometheus-data,grafana-data}
sudo chown -R $USER:$USER /pca
chmod -R 755 /pca

# Clone PCA repository
cd /pca
git clone https://github.com/jjuniper-dev/personal-cognitive-architecture.git
cd personal-cognitive-architecture

# Create environment file
cat > .env << 'EOF'
N8N_USER=admin
N8N_PASSWORD=$(openssl rand -base64 12)
NEO4J_PASSWORD=$(openssl rand -base64 12)
POSTGRES_USER=pca_user
POSTGRES_PASSWORD=$(openssl rand -base64 12)
GRAFANA_PASSWORD=$(openssl rand -base64 12)
OBSIDIAN_VAULT_PATH=/pca/obsidian-vault
OLLAMA_MODELS_PATH=/pca/ollama-models
EOF

# Create Obsidian vault structure
mkdir -p /pca/obsidian-vault/{videos,assessments,knowledge-graph,config}

# Create Docker Compose override for GPU
cat > docker-compose.override.yml << 'EOF'
version: '3.8'

services:
  ollama:
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - CUDA_VISIBLE_DEVICES=0
EOF

# Start containers
docker-compose up -d

# Wait for services to be ready (~60 seconds)
sleep 60
docker-compose logs

# Initialize Neo4j schema
docker exec pca-neo4j cypher-shell -u neo4j -p $NEO4J_PASSWORD << 'EOF'
CREATE CONSTRAINT video_id IF NOT EXISTS FOR (v:VideoCapture) REQUIRE v.video_id IS UNIQUE;
CREATE CONSTRAINT agent_name IF NOT EXISTS FOR (a:Agent) REQUIRE a.name IS UNIQUE;
CREATE INDEX idx_validated IF NOT EXISTS FOR (v:VideoCapture) ON (v.validated);
EOF

# Pull Ollama models (first pull: ~25 minutes)
docker exec pca-ollama ollama pull qwen2.5:7b
docker exec pca-ollama ollama pull qwen2.5:32b
docker exec pca-ollama ollama pull bge-m3:latest

# Verify all services are healthy
docker-compose ps
# All should show "Up"

echo "✅ PCA homelab deployment complete!"
echo "Access at:"
echo "  n8n: http://localhost:8080"
echo "  Grafana: http://localhost:3000"
echo "  Ollama: http://localhost:11434/api/tags"
```

### Step 5: Network Configuration (20 minutes)

**Set Static IP (on Linux):**

```bash
# Find network interface
ip link show
# e.g., eth0 for wired, wlan0 for WiFi

# Edit netplan
sudo nano /etc/netplan/00-installer-config.yaml

# Configure static IP:
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.50/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]

# Apply
sudo netplan apply
ip addr show eth0
```

**Configure Firewall:**

```bash
# Enable UFW
sudo ufw enable

# Allow only necessary ports
sudo ufw allow 8080/tcp comment "n8n"
sudo ufw allow 3000/tcp comment "Grafana"
sudo ufw allow 11434/tcp comment "Ollama"
sudo ufw allow 22/tcp comment "SSH"

# Deny everything else by default
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Verify rules
sudo ufw status
```

**Set Up SSH Access (Optional):**

```bash
# Generate key on laptop
ssh-keygen -t ed25519 -f ~/.ssh/homelab

# Copy public key to server
ssh-copy-id -i ~/.ssh/homelab.pub user@192.168.1.50

# Now login without password
ssh -i ~/.ssh/homelab user@192.168.1.50

# Add to .ssh/config for convenience
cat >> ~/.ssh/config << 'EOF'
Host homelab
  HostName 192.168.1.50
  User pca_user
  IdentityFile ~/.ssh/homelab
  Port 22
EOF

# Access via: ssh homelab
```

---

## Configuration & Tuning

### Ollama Model Tuning

**For Qwen2.5-32B (best quality):**

```bash
# Create custom Modelfile for tuning
cat > ~/Modelfile.qwen32b << 'EOF'
FROM qwen2.5:32b

# Increase context window for better synthesis
PARAMETER num_ctx 8192

# Temperature for reasoning (slightly exploratory)
PARAMETER temperature 0.7

# Prompt template
TEMPLATE """
You are a cognitive system analyzing information. Respond with clear reasoning.

{{ .Prompt }}
"""
EOF

# Create custom model
docker exec pca-ollama ollama create qwen32b-tuned -f ~/Modelfile.qwen32b

# Update n8n to use qwen32b-tuned instead of qwen2.5:32b
```

**For Qwen2.5-7B (fast inference):**

```bash
cat > ~/Modelfile.qwen7b << 'EOF'
FROM qwen2.5:7b

# Fast context (less memory)
PARAMETER num_ctx 2048

# Temperature for consistency
PARAMETER temperature 0.3

# Streaming for real-time response
PARAMETER stream true
EOF

docker exec pca-ollama ollama create qwen7b-tuned -f ~/Modelfile.qwen7b
```

### GPU Memory Optimization

**Monitor GPU usage:**

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# Watch container memory
docker stats pca-ollama
```

**Reduce memory footprint (if OOM):**

```bash
# Quantize Qwen2.5-32B to 4-bit
# (Warning: slight quality loss)
docker exec pca-ollama ollama pull qwen2.5:32b-q4_0

# Update model reference in n8n to use q4_0 variant
```

### Performance Tuning

**Docker Compose resource limits:**

```yaml
services:
  ollama:
    deploy:
      resources:
        limits:
          cpus: '6'
          memory: 30G
        reservations:
          cpus: '4'
          memory: 24G
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

**PostgreSQL tuning:**

```sql
-- Connect to PostgreSQL
docker exec -it pca-postgres psql -U pca_user -d n8n

-- Increase shared buffers
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET effective_cache_size = '6GB';
ALTER SYSTEM SET work_mem = '50MB';

-- Reload configuration
SELECT pg_reload_conf();
```

---

## Maintenance & Monitoring

### Weekly Tasks

```bash
# Check disk usage
df -h /pca

# Check GPU health
nvidia-smi

# Check container status
docker-compose ps

# Check Docker logs for errors
docker-compose logs --tail 100 | grep ERROR
```

### Monthly Tasks

```bash
# Backup Obsidian vault to external drive
rsync -av /pca/obsidian-vault /mnt/backup/

# Backup Neo4j database
docker exec pca-neo4j neo4j-admin dump --database=neo4j --to=/backups/neo4j-$(date +%Y%m%d).dump

# Clean up Docker dangling images/volumes
docker image prune -a
docker volume prune

# Review Grafana dashboards for anomalies
# Login: http://localhost:3000
# Credentials: admin / $GRAFANA_PASSWORD
```

### Quarterly Tasks

```bash
# Update OS packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker-compose pull
docker-compose up -d --build

# Review logs for any warnings/errors
journalctl --since "3 months ago" | grep -i error

# Check hardware health (CPU temps, fan speeds)
sudo apt install lm-sensors
sensors
```

### Annual Tasks

```bash
# Full system backup (before major upgrades)
sudo rsync -av / /mnt/backup/full-backup-$(date +%Y%m%d)/ \
  --exclude=/proc --exclude=/sys --exclude=/dev --exclude=/mnt

# Test restoration from backup

# Clean up old PostgreSQL backups (>1 year)
find /pca/postgresql-backups -mtime +365 -delete

# Review and renew GitHub SSH keys (if using git backup)
```

---

## Troubleshooting

### GPU Not Detected

```bash
# Check NVIDIA driver
nvidia-smi

# Check NVIDIA Container Runtime
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi

# If container can't see GPU:
# 1. Verify nvidia-docker is installed
# 2. Add to docker daemon.json:
#    "runtimes": {
#      "nvidia": {
#        "path": "/usr/bin/nvidia-container-runtime",
#        "runtimeArgs": []
#      }
#    }
# 3. Restart Docker: sudo systemctl restart docker
```

### Ollama Out of Memory

```bash
# Reduce model size or number of concurrent requests
# In n8n: set max_concurrent_requests = 1

# Or switch to smaller model
docker exec pca-ollama ollama pull qwen2.5:7b
# Update n8n workflow to use qwen2.5:7b instead of 32b

# Monitor memory
docker stats pca-ollama --no-stream
```

### Neo4j Connection Issues

```bash
# Check Neo4j logs
docker logs pca-neo4j

# Verify port is accessible
netstat -an | grep 7687
# Should show LISTEN on 0.0.0.0:7687

# Try manual connection
docker exec pca-neo4j cypher-shell -u neo4j -p $NEO4J_PASSWORD
# Should get neo4j#  prompt
```

### Disk Space Running Low

```bash
# Check disk usage
du -sh /pca/* | sort -h

# Find large files
find /pca -type f -size +100M -exec ls -lh {} \;

# Common culprits:
# - Ollama models: /pca/ollama-models
# - PostgreSQL dumps: /pca/postgresql-data
# - Neo4j graph: /pca/neo4j-graph

# Clean up old PostgreSQL backups
find /pca/postgresql-data -name "*.backup" -mtime +30 -delete

# Clear Docker cache
docker system prune -a --volumes
```

---

## Backup & Disaster Recovery

### Backup Strategy

```bash
#!/bin/bash
# Automated daily backup script

BACKUP_DIR="/mnt/backup/pca-backups-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 1. Backup Obsidian vault
rsync -av /pca/obsidian-vault $BACKUP_DIR/

# 2. Backup Neo4j
docker exec pca-neo4j neo4j-admin dump --database=neo4j --to=/backups/neo4j.dump
cp /pca/neo4j-graph/neo4j.dump $BACKUP_DIR/

# 3. Backup PostgreSQL
docker exec pca-postgres pg_dump -U pca_user n8n > $BACKUP_DIR/n8n.sql

# 4. Backup .env file
cp /pca/personal-cognitive-architecture/.env $BACKUP_DIR/.env.backup

# 5. Compress
tar -czf $BACKUP_DIR/../pca-backup-$(date +%Y%m%d-%H%M%S).tar.gz $BACKUP_DIR

# 6. Optional: Upload to cloud
# aws s3 sync $BACKUP_DIR s3://pca-backups/

echo "✅ Backup complete: $BACKUP_DIR"
```

**Add to crontab:**

```bash
# Run daily at 3 AM
0 3 * * * /home/pca_user/backup-pca.sh

crontab -e
# Paste above line
```

### Disaster Recovery (Full System Restore)

```bash
# 1. Boot fresh Linux install on same/new hardware
# 2. Recreate /pca directories
sudo mkdir -p /pca
sudo chown -R pca_user:pca_user /pca

# 3. Restore from backup
tar -xzf pca-backup-20260512-030000.tar.gz -C /pca

# 4. Restore Obsidian vault
cp -r /pca/backup/obsidian-vault /pca/

# 5. Restore Neo4j
docker exec pca-neo4j neo4j-admin load --from=/backups/neo4j.dump --database=neo4j --overwrite-existing

# 6. Restore PostgreSQL
docker exec -i pca-postgres psql -U pca_user n8n < /pca/backup/n8n.sql

# 7. Verify all services
docker-compose up -d
docker-compose ps
```

---

## Cost Breakdown

### Initial Hardware Investment

```
GPU (RTX 3090):         CAD $800
CPU + Mobo + RAM:       $600
Storage (2TB NVMe):     $150
Cooling + Case + PSU:   $350
Misc (cables, fans):    $100
────────────────────────────────
Total Hardware:         CAD $2,000
```

### Operating Costs (Annual)

```
Electricity:            CAD $150
Replacement HDDs:       $100 (every 3 years)
Internet:               (included)
GitHub (private repo):  Free
────────────────────────────────
Total Annual:           ~CAD $150–250
```

### Total Cost of Ownership (5 years)

```
Initial:                CAD $2,000
5 years × $150:         $750
────────────────────────────────
Total 5-year TCO:       CAD $2,750
Cost per month:         ~$45
```

**vs. Cloud Inference (Anthropic API):**

```
Phase 1 (50 videos/day):  CAD $330/year
5 years:                  $1,650

But Phase 2 local inference cost difference:
(Cloud would be $3,000/year for similar workload)
Homelab saves ~$2,700/year in inference costs
Break-even: ~8 months (hardware pays for itself)
```

---

## Integration with PCA Layers

This homelab reference implements **Layer 9: Infrastructure** from the 9-layer architecture:

```
Layers 1-8 (Input through Output)
         ↓
Infrastructure Layer (this document)
├─ Compute (Ollama, n8n, Neo4j)
├─ Storage (Obsidian, PostgreSQL, ChromaDB)
├─ Networking (Docker, firewall, static IP)
├─ Monitoring (Prometheus, Grafana)
└─ Disaster recovery (backups, restore procedures)
         ↓
All PCA functionality enabled, owned, and controlled locally
```

---

## Roadmap: From Homelab to Enterprise

### Phase 2 → Phase 3 Upgrade Path

```
Homelab (Phase 2)
├─ Cost: CAD $2,000 upfront
├─ Capacity: 50 videos/day
├─ Control: 100% local
└─ Limitations: Single-user, single machine

Add Enterprise Gateway (Phase 3)
├─ Keep homelab for inference
├─ Add Azure cloud for:
│  ├─ Multi-user access (cloud portal)
│  ├─ Enterprise compliance (audit logs)
│  ├─ Backup & disaster recovery
│  └─ Burst capacity (cloud GPUs for large jobs)
└─ Hybrid: local-first, cloud-backup model
```

---

## Revision History

- **2026-05-12:** Initial version. Provided practical homelab reference with hardware specs, installation guide, tuning, maintenance, and cost analysis.

