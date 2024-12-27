import zipfile
import os

def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    try:
        # Content for manifest.json
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version": "22.0.0"
        }
        """

        # Content for background.js
        background_js = f"""
        var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy_host}",
                    port: parseInt({proxy_port})
                }},
                bypassList: ["localhost"]
            }}
        }};
        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
        chrome.webRequest.onAuthRequired.addListener(
            function(details) {{
                return {{
                    authCredentials: {{
                        username: "{proxy_username}",
                        password: "{proxy_password}"
                    }}
                }};
            }},
            {{urls: ["<all_urls>"]}},
            ["blocking"]
        );
        """

        # Define the output file name
        plugin_file = 'proxy_auth_plugin.zip'

        # Create the zip file
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json.strip())
            zp.writestr("background.js", background_js.strip())

        print(f"Proxy authentication extension created: {plugin_file}")
        return plugin_file

    except Exception as e:
        print(f"Error creating proxy authentication extension: {e}")
        return None

plugin_file = create_proxy_auth_extension("in.proxymesh.com", 31280, "abidan", "abidan")
print(f"Plugin file: {plugin_file}")
