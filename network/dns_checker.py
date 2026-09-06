import dns.resolver

def check_dns(domain, record_types=None):
    if record_types is None:
        record_types = ["A", "AAAA", "MX", "NS", "TXT"]
        
        results = {}
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                results[record_type] = [str(answer) for answer in answers]
            except dns.resolver.NoAnswer:
                results[record_type] = []
            except dns.resolver.NXDOMAIN:
                return {"error": "domain does not exist"}
            except Exception as e:
                results[record_type] = [f"error: {e}"]
                
        return results