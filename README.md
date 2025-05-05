<h1>Automação de Geração e Atualização de Planilhas no Google Sheets</h1>

<p>Este projeto automatiza a extração de dados do Oracle, geração de planilhas Excel e sincronização com o Google Sheets, usando um container Docker gerenciado via <code>docker-compose</code>.</p>

<hr>

<h2>Funcionalidades</h2>
<ul>
  <li><strong>Extração de dados Oracle</strong>: consulta categorias definidas em <code>MV_PRODUCTOS</code>.</li>
  <li><strong>Geração de planilha única</strong>: cria <code>Produtos.xlsx</code> consolidado.</li>
  <li><strong>Atualização no Google Sheets</strong>:
    <ul>
      <li>Atualiza apenas preços que mudaram.</li>
      <li>Adiciona novos produtos com colunas extras (<code>CORRIGIDO_IA</code>, <code>REVISADO</code>, <code>DESCRIPCION_ANTIGA</code>).</li>
      <li>Remove produtos que não estão mais no Excel.</li>
    </ul>
  </li>
  <li><strong>Execução automatizada com cron</strong> (duas vezes ao dia).</li>
  <li><strong>Empacotado via Docker + Docker Compose</strong>.</li>
</ul>

<hr>

<h2>Pré-requisitos</h2>
<ol>
  <li>Docker e Docker Compose instalados</li>
  <li>Baixar manualmente o arquivo:
    <br>
    <a href="https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html">
    instantclient-basiclite-linux.x64-21.18.0.0.0dbru.zip</a><br>
    <strong>Coloque na raiz do projeto</strong> antes de rodar o build.
  </li>
  <li>Credenciais do Google:
    <ul>
      <li>Baixe a conta de serviço e salve como <code>credentials-google.json</code></li>
    </ul>
  </li>
</ol>

<hr>

<h2>Uso com Docker Compose</h2>

<h3>1. Exemplo de <code>docker-compose.yml</code></h3>
<pre><code>version: '3.9'

services:
  exportar-planilha-google:
    build: .
    container_name: exportar-planilha-google
    volumes:
      - .:/app
    working_dir: /app
    command: cron -f
    restart: unless-stopped
    networks:
      - rede-exportar-planilha

networks:
  rede-exportar-planilha:
    driver: bridge
</code></pre>

<h3>2. Build da imagem</h3>
<pre><code>docker-compose build</code></pre>

<h3>3. Iniciar o container</h3>
<pre><code>docker-compose up -d</code></pre>

<p>O cron interno cuidará da execução automática.</p>

<hr>

<h2>Agendamento (cron interno)</h2>
<p>O container executa o script principal automaticamente nos horários:</p>
<pre><code>
0 8 * * * /usr/local/bin/python3 /app/main-gerar-alterar-planilha.py
0 14 * * * /usr/local/bin/python3 /app/main-gerar-alterar-planilha.py
</code></pre>

<hr>

<h2>Principais arquivos</h2>
<ul>
  <li><code>gerar-planilha.py</code>: extrai dados do Oracle e cria o Excel</li>
  <li><code>atualizar-planilha.py</code>: atualiza, adiciona e remove dados no Google Sheets</li>
  <li><code>main-gerar-alterar-planilha.py</code>: executa os dois scripts em sequência</li>
  <li><code>Dockerfile</code>: configura o ambiente com Oracle Client, cron e dependências Python</li>
  <li><code>crontab.txt</code>: define os horários do cron</li>
</ul>

<hr>

<h2>Configurações</h2>
<ul>
  <li><strong>Oracle</strong> (em <code>gerar-planilha.py</code>):
    <pre><code>
db_host = "ip-do-servidor"
db_port = 12345
db_user = "user"
db_pass = "password"
db_database = "db_name"
    </code></pre>
  </li>
  <li><strong>Google Sheets</strong> (em <code>atualizar-planilha.py</code>):
    <pre><code>
spreadsheet_id = 'id-da-planilha-encontrado-no-link'
    </code></pre>
  </li>
</ul>

<hr>

<h2>Segurança</h2>
<ul>
  <li><code>credentials-google.json</code> está no <code>.gitignore</code> (não deve ser versionado)</li>
  <li>Planilhas e credenciais não devem ser expostas publicamente</li>
  <li>Recomenda-se usar variáveis de ambiente ou arquivo <code>.env</code> para configurações sensíveis</li>
</ul>

<hr>

<h2>Observação final</h2>
<p>Este projeto é modular e pode ser adaptado para diferentes bancos e planilhas. Ideal para sincronização de dados internos com planilhas acessíveis por outros sistemas ou bots.</p>
