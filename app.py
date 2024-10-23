from flask import Flask, request,render_template,redirect,url_for,session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'producto' in session and len(session['producto']) > 0:
        return max(item['id'] for item in session['producto']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'producto' not in session:
        session['producto'] = []
        
    producto = session.get('producto',[])
    return render_template('index.html',producto=producto)

def generar_id():
    if 'producto' in session and len(session['producto']>0):
        return max(item['id'] for item in session['producto'])+ 1
    else:
        return 1

@app.route("/agregar",methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        nombre =  request.form['nombre']
        cantidad =  int(request.form['cantidad'])
        precio =  float(request.form['precio'])
        fecha_vencimiento =  request.form['fecha_vencimiento']
        categoria =  request.form['categoria']

        agregar_producto = {
            'id': generar_id(),
            'nombre':nombre,
            'cantidad':cantidad,
            'precio':precio,
            'fecha_vencimiento':fecha_vencimiento,
            'categoria':categoria
        }

        if 'producto' not in session:
            session['producto'] = []

        session['producto'].append(agregar_producto)
        session.modified = True
        return redirect(url_for('index'))    

    return render_template('agregar.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    gestion_producto = session.get('producto',[])
    producto = next( (c for c in gestion_producto if c['id'] == id), None)
    if not producto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html',producto=producto)

@app.route("/eliminar/<int:id>",methods=["POST"])
def eliminar(id):
    gestion_producto = session.get('producto',[])
    producto = next((c for c in gestion_producto if c['id'] == id),None)
    if producto:
        session['producto'].remove(producto)
        session.modified = True
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(debug=True)