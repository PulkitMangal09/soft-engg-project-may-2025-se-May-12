import yaml
import sys

def generate_api_documentation(yaml_content):
    try:
        api_spec = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return f"Error parsing YAML: {str(e)}"

    # Group endpoints by tags
    tags_dict = {}
    for path, methods in api_spec.get('paths', {}).items():
        for method, spec in methods.items():
            if method.lower() not in ['get', 'post', 'put', 'patch', 'delete']:
                continue
                
            for tag in spec.get('tags', ['uncategorized']):
                endpoint = {
                    'path': path,
                    'method': method.upper(),
                    'summary': spec.get('summary', ''),
                    'description': spec.get('description', ''),
                    'operationId': spec.get('operationId', ''),
                    'parameters': spec.get('parameters', []),
                    'requestBody': spec.get('requestBody'),
                    'responses': spec.get('responses', {})
                }
                tags_dict.setdefault(tag, []).append(endpoint)

    # Generate markdown
    md = "# API Documentation\n\n"
    
    # Table of Contents
    md += "## Table of Contents\n"
    for tag in sorted(tags_dict.keys()):
        md += f"- [{tag.capitalize()}](#{tag.lower().replace(' ', '-')})\n"
    md += "\n"
    
    # Detailed documentation by tag
    for tag, endpoints in tags_dict.items():
        md += f"## {tag.capitalize()}\n\n"
        
        for endpoint in endpoints:
            # Header
            md += f"### `{endpoint['method']} {endpoint['path']}`\n"
            md += f"**{endpoint['summary']}**\n\n"
            
            # Description
            if endpoint['description']:
                md += f"{endpoint['description']}\n\n"
                
            # Operation ID
            md += f"- **Operation ID:** `{endpoint['operationId']}`\n"
            
            # Parameters
            if endpoint['parameters']:
                md += "- **Parameters:**\n"
                for param in endpoint['parameters']:
                    required = "required" if param.get('required', False) else "optional"
                    param_type = param.get('schema', {}).get('type', 'unknown')
                    md += f"  - `{param['name']}` ({param['in']}, {required}, {param_type}): {param.get('description', '')}\n"
                md += "\n"
                
            # Request Body
            if endpoint['requestBody']:
                md += "- **Request Body:**\n"
                for content_type, media_type in endpoint['requestBody'].get('content', {}).items():
                    schema_ref = media_type.get('schema', {}).get('$ref', '').split('/')[-1]
                    md += f"  - `{content_type}`: {schema_ref}\n"
                md += "\n"
                
            # Responses
            if endpoint['responses']:
                md += "- **Responses:**\n"
                for code, response in endpoint['responses'].items():
                    md += f"  - `{code}`: {response.get('description', '')}\n"
                md += "\n"
                
            md += "---\n\n"
            
    return md

if __name__ == "__main__":
    yaml_content = open("yaml_file.yaml", "r").read()
    markdown_output = generate_api_documentation(yaml_content)
    with open("api_documentation.md", "w") as f:
        f.write(markdown_output)