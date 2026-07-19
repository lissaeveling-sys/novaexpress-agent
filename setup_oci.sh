#!/bin/bash
# ─────────────────────────────────────────────────────────
# setup_oci.sh — Script de instalación para Oracle Cloud (OCI)
# Ejecutar una sola vez luego de conectarse por SSH a la VM
# Uso: bash setup_oci.sh
# ─────────────────────────────────────────────────────────

echo "🔄 Actualizando el sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🐍 Instalando Python y pip..."
sudo apt-get install -y python3 python3-pip git

echo "📦 Clonando el repositorio..."
# ⚠️  Reemplazá TU_USUARIO por tu nombre de usuario de GitHub
git clone https://github.com/TU_USUARIO/novaexpress-agent.git
cd novaexpress-agent

echo "📚 Instalando dependencias de Python..."
pip3 install -r requirements.txt

echo "🔑 Configurando API key de Cohere..."
# ⚠️  Reemplazá TU_API_KEY por tu clave real de Cohere
export COHERE_API_KEY="TU_API_KEY"

# Para que la variable persista al reiniciar la VM:
echo 'export COHERE_API_KEY="TU_API_KEY"' >> ~/.bashrc

echo "🚀 Iniciando la aplicación en segundo plano..."
# nohup permite que la app siga corriendo aunque cierres la terminal SSH
nohup python3 app.py > output.log 2>&1 &

echo "✅ Aplicación iniciada. Accedé en: http://TU_IP_PUBLICA_OCI:7860"
echo "📋 Para ver los logs: tail -f output.log"
echo "🛑 Para detener la app: kill \$(lsof -t -i:7860)"
