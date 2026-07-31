class AliasManager:
    """
    Simulación de gestión de alias en pfSense.
    """
    
    def __init__(self):
        self.aliases = {}
    
    def add_alias(self, name: str, value: str, alias_type: str = "host"):
        self.aliases[name] = {"value": value, "type": alias_type}
    
    def get_alias(self, name: str) -> str:
        if name in self.aliases:
            return self.aliases[name]["value"]
        return None
    
    def resolve(self, expression: str) -> str:
        """Resuelve un alias en su valor real"""
        if expression in self.aliases:
            return self.aliases[expression]["value"]
        return expression

class RuleWithAlias:
    """Regla de firewall que puede usar alias"""
    def __init__(self, action: str, protocol: str, source_alias: str, dest_alias: str, port_alias: str):
        self.action = action
        self.protocol = protocol
        self.source_alias = source_alias
        self.dest_alias = dest_alias
        self.port_alias = port_alias
    
    def resolve_rule(self, alias_manager: AliasManager):
        """Resuelve los alias en valores reales"""
        self.source = alias_manager.resolve(self.source_alias)
        self.destination = alias_manager.resolve(self.dest_alias)
        self.port = alias_manager.resolve(self.port_alias)

# Ejemplo de uso
manager = AliasManager()
manager.add_alias("LAN_NET", "192.168.1.0/24", "network")
manager.add_alias("WEB_SERVER", "10.0.0.1", "host")
manager.add_alias("HTTP_PORT", "80", "port")
manager.add_alias("HTTPS_PORT", "443", "port")

rule = RuleWithAlias(
    action="pass",
    protocol="tcp",
    source_alias="LAN_NET",
    dest_alias="WEB_SERVER",
    port_alias="HTTP_PORT"
)

rule.resolve_rule(manager)
print(f"Regla resuelta: {rule.action} {rule.protocol} {rule.source} -> {rule.destination}:{rule.port}")
