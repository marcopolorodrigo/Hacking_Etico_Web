# Simulación de una regla de Suricata para detectar inyección de prompts
# En producción, esta regla se añadiría al archivo de reglas de Suricata

rule_template = """
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET AI_PROMPT_INJECTION Attempt"; 
  flow:to_server,established; 
  content:"ignora"; nocase; 
  content:"todas"; distance:0; nocase; 
  content:"instrucciones"; distance:0; nocase; 
  classtype:attempted-recon; 
  sid:2000010; rev:1;)
"""

print("📋 REGLA DE SURICATA PARA INYECCIÓN DE PROMPTS")
print(rule_template)
