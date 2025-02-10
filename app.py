import os
import instaloader  
import uuid
import re
from flask import Flask, request, render_template, session, send_from_directory, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.debug = True  

def get_download_directory(session_id, profile_name, post_shortcode):
    return os.path.join('downloads', session_id, profile_name, post_shortcode)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_url', methods=['POST'])
def process_url():
    url = request.form.get('url')
    if not url:
        flash("Please enter a valid URL", "danger")
        return redirect(url_for('home'))
    
    if 'instagram.com' in url:
        return process_instagram(url)
    
    flash("Unsupported URL. Please enter a valid Instagram post URL.", "danger")
    return redirect(url_for('home'))

def process_instagram(url):
    L = instaloader.Instaloader()
    L.sanitize_paths = True

    session_id = session.get('session_id', str(uuid.uuid4()))
    session['session_id'] = session_id

    try:
        match = re.search(r'instagram\.com/(p|reel|tv|stories)/([^/?]+)', url)
        if not match:
            flash("Invalid Instagram URL", "danger")
            return redirect(url_for('home'))

        post_shortcode = match.group(2)
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)
        profile_name = post.owner_username
        
        download_dir = get_download_directory(session_id, profile_name, post_shortcode)
        os.makedirs(download_dir, exist_ok=True)
        
        L.dirname_pattern = download_dir
        L.filename_pattern = '{date_utc}_UTC_{shortcode}'
        L.download_post(post, target=post_shortcode)
        
        downloaded_files = os.listdir(download_dir)
        media_files = [f for f in downloaded_files if f.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.gif'))]
        
        return render_template(
            'instagram_preview.html',
            post=post,
            media_files=media_files,
            download_dir=download_dir,
            url=url,
            session_id=session_id,
            profile_name=profile_name,
            post_shortcode=post_shortcode
        )

    except instaloader.exceptions.InstaloaderException as e:
        flash(f"Error fetching Instagram post: {str(e)}", "danger")
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "danger")
    
    return redirect(url_for('home'))

@app.route('/download/<session_id>/<profile_name>/<post_shortcode>/<filename>')
def download_file(session_id, profile_name, post_shortcode, filename):
    try:
        post_folder = get_download_directory(session_id, profile_name, post_shortcode)
        return send_from_directory(post_folder, filename)
    except Exception as e:
        flash(f"Error serving file: {str(e)}", "danger")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)