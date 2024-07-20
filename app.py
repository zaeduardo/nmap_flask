from flask import Flask, request, jsonify, render_template
import subprocess
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obter_ip')
def obter_ip():
    site = request.args.get('site')
    if not site:
        return jsonify({'erro': 'Nenhum site fornecido'}), 400

    try:
        ip = socket.gethostbyname(site)
        return jsonify({'ip': ip})
    except socket.gaierror:
        return jsonify({'erro': 'Site não encontrado'}), 404

@app.route('/executar_nmap', methods=['POST'])
def executar_nmap():
    ip = request.form.get('ip')
    parametros = request.form.get('parametros')
    if not ip or not parametros:
        return jsonify({'erro': 'IP ou parâmetros não fornecidos'}), 400

    try:
        # Execute o comando Nmap com os parâmetros fornecidos
        comando = f"nmap {parametros} {ip}"
        resultado = subprocess.check_output(comando, shell=True, text=True)
        return jsonify({'resultado': resultado})
    except subprocess.CalledProcessError as e:
        return jsonify({'erro': 'Erro ao executar o Nmap', 'mensagem': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
