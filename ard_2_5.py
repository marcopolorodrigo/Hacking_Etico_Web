# Simulación de reglas personalizadas para detección de ataques a IA
# Estas reglas se añadirían al archivo de reglas de Suricata

ai_rules = """
# Regla para detectar inyección de prompts
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET AI_PROMPT_INJECTION Prompt Injection Attempt"; 
  flow:to_server,established; 
  content:"ignora"; nocase; distance:0; 
  content:"instrucciones"; nocase; distance:0; within:50; 
  classtype:attempted-recon; sid:2000010; rev:1;)

# Regla para detectar intentos de extracción de modelo
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET AI_MODEL_STEALING Model Stealing Attempt"; 
  flow:to_server,established; 
  content:"/api/v1/chat"; http_uri; 
  threshold:type threshold, track by_src, count 100, seconds 60; 
  classtype:attempted-recon; sid:2000011; rev:1;)

# Regla para detectar envenenamiento de datos en RAG
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET AI_DATA_POISONING Data Poisoning Attempt"; 
  flow:to_server,established; 
  content:"/rag/ingest"; http_uri; 
  content:"<script>"; nocase; 
  classtype:attempted-recon; sid:2000012; rev:1;)
"""

print("📋 REGLAS PERSONALIZADAS PARA ATAQUES A IA")
print(ai_rules)
