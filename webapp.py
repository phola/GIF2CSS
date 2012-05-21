from gifexplode import GifExplode
from flask import Flask, render_template, request, abort, jsonify

from werkzeug.contrib.cache import SimpleCache

DEBUG=False

app = Flask(__name__)
cache = SimpleCache()


@app.route("/", methods=['GET', 'POST'])
@app.route("/<path:image_url>")
def index(image_url=None):
    
    if not image_url and request.form:
        image_url = request.form['image_url']
        
    if image_url:
        
        image_data = _explode_image_url(image_url)
                                
        return render_template('index.html', 
                               frames=image_data['frames'],
                               image_width=image_data['size'][0],
                               image_height=image_data['size'][1],
                               image_url=image_url)
                                          
    else:
        return render_template('index.html')

@app.route("/api")
def api():
    return render_template('api.html')
    
    
@app.route("/api/explode", methods=['GET'])
def api_explode():
    
    image_url = request.args['image_url']
    image_data = _explode_image_url(image_url)
    
    return jsonify(image_data=image_data)

@app.errorhandler(500)
def general_error(e):
    return render_template('500.html'), 500


def _explode_image_url(image_url):

    image_data = cache.get(image_url)
    
    if image_data is None:
        print "Nothing found in cache for %s" % image_url
        try:
            exploder = GifExplode(image_url)
            image_data = exploder.explode()

            print "Setting cache for %s" % image_url
            cache.set(image_url, image_data, timeout=5*60)
        except ValueError:
            abort(500)
    else:
        print "Using cache for %s" % image_url
    
    return image_data


if __name__ == "__main__":
    app.run(debug=DEBUG, host='0.0.0.0')
