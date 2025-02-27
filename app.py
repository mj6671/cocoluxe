from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

# Default shop location (Cocoluxe, for example)
shop_location_link = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3890.2759058628412!2d80.03831307507399!3d12.825439387476608!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a52f7cb7c90461d%3A0xb41d334731b4d361!2sCocoluxe!5e0!3m2!1sen!2sin!4v1740648544249!5m2!1sen!2sin"
shop_loc = "near MBA block"


def convert_to_embed_link(location_link: str) -> str:
    # Check for short links (e.g., goo.gl or maps.app.goo.gl)
    if "goo.gl/maps" in location_link or "maps.app.goo.gl" in location_link:
        return f"https://www.google.com/maps?q={location_link}&output=embed"
    
    # Extract Place ID from full Google Maps link if available
    place_id_match = re.search(r'!1s([a-zA-Z0-9_-]+)!2s', location_link)
    if place_id_match:
        place_id = place_id_match.group(1)
        return f"https://www.google.com/maps/embed?pb=!1m2!1s{place_id}!2s"

    # Extract coordinates from full Google Maps link if available
    coordinates_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', location_link)
    if coordinates_match:
        lat, lng = coordinates_match.groups()
        return f"https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q={lat},{lng}"

    # Default to the original link if no matches
    return location_link

@app.route('/')
def index():
    return render_template('index.html', shop_location_link=shop_location_link, shop_loc=shop_loc)

@app.route('/update-location', methods=['GET', 'POST'])
def update_location():
    global shop_location_link, shop_loc
    if request.method == 'POST':
        location_link = request.form.get('location_link')
        input_password = request.form.get('password')
        shop_loc = request.form.get('key')

        if location_link and input_password == "luxe:
            shop_location_link = convert_to_embed_link(location_link)
            flash('Shop location updated successfully!', 'success')
        else:
            flash('Invalid link or password.', 'error')

        return redirect(url_for('update_location'))
    
    return render_template('update_location.html', shop_location_link=shop_location_link)

if __name__ == '__main__':
    app.run(debug=True)
