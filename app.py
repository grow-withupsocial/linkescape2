from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Main converter page"""
    target_url = request.args.get('url')
    platform = request.args.get('platform', 'auto')
    redirect_type = request.args.get('redirect', 'direct')
    tracking = request.args.get('tracking', '0')
    
    if target_url:
        # If URL parameters exist, redirect
        return handle_redirect(target_url, platform, redirect_type)
    
    # Otherwise show converter UI
    return render_template('index.html')

@app.route('/redirect')
def redirect_endpoint():
    """Handle redirects with browser detection"""
    target_url = request.args.get('url')
    platform = request.args.get('platform', 'auto')
    redirect_type = request.args.get('redirect', 'direct')
    
    if not target_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    return handle_redirect(target_url, platform, redirect_type)

def handle_redirect(target_url, platform, redirect_type):
    """Main redirect logic"""
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Detect in-app browsers
    is_whatsapp = 'whatsapp' in user_agent
    is_instagram = 'instagram' in user_agent
    is_facebook = 'fban' in user_agent or 'fbav' in user_agent
    is_tiktok = 'tiktok' in user_agent
    is_telegram = 'telegram' in user_agent
    is_snapchat = 'snapchat' in user_agent
    is_twitter = 'twitter' in user_agent
    is_linkedin = 'linkedin' in user_agent
    
    # Detect device type
    is_ios = 'iphone' in user_agent or 'ipad' in user_agent
    is_android = 'android' in user_agent
    is_mobile = is_ios or is_android
    
    # Determine if we should apply escape tactics
    is_in_app_browser = (is_whatsapp or is_instagram or is_facebook or 
                         is_tiktok or is_telegram or is_snapchat or 
                         is_twitter or is_linkedin)
    
    # Build redirect response based on platform
    if platform == 'ios' or (platform == 'auto' and is_ios):
        # iOS redirect techniques
        if is_in_app_browser:
            # Use intent/URI schemes to open in Safari
            return redirect_ios(target_url, is_in_app_browser)
        else:
            return redirect_simple(target_url, redirect_type)
    
    elif platform == 'android' or (platform == 'auto' and is_android):
        # Android redirect techniques
        if is_in_app_browser:
            return redirect_android(target_url, is_in_app_browser)
        else:
            return redirect_simple(target_url, redirect_type)
    
    else:
        # Desktop or unknown
        return redirect_simple(target_url, redirect_type)

def redirect_simple(target_url, redirect_type):
    """Simple HTTP redirect"""
    if redirect_type == 'delay':
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Redirecting...</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #050505 0%, #0a0a0a 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    color: white;
                }}
                .container {{
                    text-align: center;
                }}
                .loader {{
                    border: 4px solid rgba(255, 107, 53, 0.2);
                    border-top: 4px solid #FF6B35;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
                p {{
                    color: #b0b0b0;
                    font-size: 1.1em;
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="loader"></div>
                <p>Opening in your browser...</p>
            </div>
            <script>
                setTimeout(() => {{
                    window.location.href = '{target_url}';
                }}, 1500);
            </script>
        </body>
        </html>
        """
        return html, 200, {'Content-Type': 'text/html'}
    else:
        return redirect(target_url)

def redirect_ios(target_url, is_in_app):
    """iOS-specific redirect tactics"""
    if is_in_app:
        # For iOS in-app browsers, try multiple techniques
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Opening...</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #050505 0%, #0a0a0a 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    color: white;
                    text-align: center;
                }}
                .container {{
                    max-width: 300px;
                }}
                .icon {{
                    font-size: 3em;
                    margin-bottom: 20px;
                }}
                h1 {{
                    font-size: 1.5em;
                    margin-bottom: 10px;
                    color: #FF6B35;
                }}
                p {{
                    color: #b0b0b0;
                    margin-bottom: 30px;
                    line-height: 1.6;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 30px;
                    background: linear-gradient(90deg, #FF6B35, #ff8a50);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    margin-bottom: 15px;
                    width: 100%;
                    box-sizing: border-box;
                }}
                .button:active {{
                    opacity: 0.9;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🌐</div>
                <h1>Open in Safari</h1>
                <p>This link works better in Safari. Tap the button below to open it.</p>
                <a href="{target_url}" class="button">Open in Safari</a>
                <p style="font-size: 0.85em; margin-top: 20px;">Or copy and paste this URL into Safari:</p>
                <p style="word-break: break-all; font-family: monospace; font-size: 0.8em; color: #1AC8ED;">{target_url}</p>
            </div>
            <script>
                // Try to open using Safari
                setTimeout(() => {{
                    window.location.href = "{target_url}";
                }}, 500);
            </script>
        </body>
        </html>
        """
        return html, 200, {'Content-Type': 'text/html'}
    else:
        return redirect(target_url)

def redirect_android(target_url, is_in_app):
    """Android-specific redirect tactics"""
    if is_in_app:
        # For Android in-app browsers
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Opening...</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #050505 0%, #0a0a0a 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    color: white;
                    text-align: center;
                }}
                .container {{
                    max-width: 300px;
                }}
                .icon {{
                    font-size: 3em;
                    margin-bottom: 20px;
                }}
                h1 {{
                    font-size: 1.5em;
                    margin-bottom: 10px;
                    color: #FF6B35;
                }}
                p {{
                    color: #b0b0b0;
                    margin-bottom: 30px;
                    line-height: 1.6;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 30px;
                    background: linear-gradient(90deg, #FF6B35, #ff8a50);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    margin-bottom: 15px;
                    width: 100%;
                    box-sizing: border-box;
                }}
                .button:active {{
                    opacity: 0.9;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🌐</div>
                <h1>Open in Chrome</h1>
                <p>This link works better in Chrome. Tap the button below to open it.</p>
                <a href="{target_url}" class="button">Open in Chrome</a>
                <p style="font-size: 0.85em; margin-top: 20px;">Or copy and paste this URL into Chrome:</p>
                <p style="word-break: break-all; font-family: monospace; font-size: 0.8em; color: #1AC8ED;">{target_url}</p>
            </div>
            <script>
                // Try to open using intent
                setTimeout(() => {{
                    // Android intent to open in Chrome
                    const chromeIntent = "intent://{target_url.replace('https://', '').replace('http://', '')}#Intent;scheme=https;package=com.android.chrome;end";
                    window.location.href = "{target_url}";
                }}, 500);
            </script>
        </body>
        </html>
        """
        return html, 200, {'Content-Type': 'text/html'}
    else:
        return redirect(target_url)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API endpoint for generating escape links"""
    data = request.json
    original_url = data.get('url')
    platform = data.get('platform', 'auto')
    redirect_type = data.get('redirect', 'direct')
    tracking = data.get('tracking', False)
    
    if not original_url:
        return jsonify({'error': 'URL required'}), 400
    
    # Generate the escape link
    escape_link = f"/redirect?url={requests.utils.quote(original_url)}&platform={platform}&redirect={redirect_type}"
    if tracking:
        escape_link += "&tracking=1"
    
    return jsonify({
        'escape_link': escape_link,
        'full_url': request.host_url.rstrip('/') + escape_link
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
