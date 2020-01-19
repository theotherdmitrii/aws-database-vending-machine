

def escape_json_string(json):
    return json.replace("\\n", "\\n") \
        .replace("\\'", "\\'") \
        .replace('\\"', '\\"') \
        .replace("\\&", "\\&") \
        .replace("\\r", "\\r") \
        .replace("\\t", "\\t") \
        .replace("\\b", "\\b") \
        .replace("\\f", "\\f")
