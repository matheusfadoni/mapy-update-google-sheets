<h1>Projeto: Automação de Processamento e Upload de Planilhas para Google Sheets</h1>

<p>Este projeto faz parte do sistema <strong>consulta_produtos_chatbot_server_gcloud</strong> e corresponde à segunda etapa do fluxo de integração. Ele automatiza o upload de dados para planilhas do Google Sheets com informações de produtos extraídas do sistema local da empresa. Dessa forma, a outra parte do projeto pode acessar as informações diretamente no Google Sheets e utilizá-las em integrações ou consultas via chatbot.</p>

<p><strong>Nota:</strong> Este projeto precisa ser adaptado para as particularidades de cada sistema local, incluindo a query SQL e o formato dos dados extraídos, com base nas necessidades específicas de cada empresa.</p>

<hr>

<h2>Funcionalidades:</h2>
<ol>
  <li><strong>Gerar planilhas por categoria</strong>:<br>
    - Extrai dados do banco Oracle e salva planilhas Excel para cada categoria configurada.
  </li>
  <li><strong>Juntar categorias (opcional)</strong>:<br>
    - Combina os dados de "Informática" com "Eletrônica" ou pode ser adaptado para consolidar todas as categorias em uma única planilha.
  </li>
  <li><strong>Upload para Google Sheets</strong>:<br>
    - Envia as planilhas geradas para os respectivos IDs configurados no Google Sheets.
  </li>
  <li><strong>Criar arquivo TXT (opcional)</strong>:<br>
    - Converte os dados das planilhas geradas em um arquivo <code>produtos.txt</code> com colunas separadas por <code>|</code>.
  </li>
  <li><strong>Execução automatizada</strong>:<br>
    - O script principal organiza a execução de todos os passos na ordem correta.
  </li>
</ol>

<hr>

<h2>Ordem de Execução:</h2>
<ol>
  <li><code>gerar-planilhas.py</code>:<br>
    - Conecta ao banco de dados e gera planilhas Excel com base nas categorias configuradas.<br>
    - <strong>Importante:</strong> Este script deve ser adaptado para o sistema de cada usuário, incluindo a configuração da query SQL e o formato dos dados exportados com base nas preferências e objetivos do projeto.
  </li>
  <li><code>insert-informatica-em-eletronica.py</code> (opcional):<br>
    - Insere os dados de "Informática" em "Eletrônica" e remove SKUs duplicados. Pule esta etapa se desejar manter categorias separadas.<br>
    - Este script também pode ser ajustado para consolidar todas as categorias em uma única planilha, caso seja necessário.
  </li>
  <li><code>criar-txt.py</code> (opcional):<br>
    - Combina todas as planilhas geradas em um arquivo <code>produtos.txt</code>, com colunas separadas por <code>|</code>. Use este passo se precisar de um arquivo consolidado no formato texto.
  </li>
  <li><code>subir-planilhas.py</code>:<br>
    - Faz upload das planilhas geradas para o Google Sheets. Se alguma planilha não for encontrada, ela será ignorada.
  </li>
  <li><code>main.py</code>:<br>
    - Executa os scripts na ordem correta automaticamente. Este é o ponto de entrada para executar todo o fluxo de automação.
  </li>
</ol>

<hr>

<h2>Exemplo de Configuração no Cron (Linux):</h2>
<p>Automatize a execução do projeto conforme a frequência desejada:</p>
<h4>Passos:</h4>
<ol>
  <li>Edite o cron com:
    <pre><code>crontab -e</code></pre>
  </li>
  <li>Adicione uma linha com a frequência desejada, substituindo o caminho pelo diretório do projeto:
    <ul>
      <li><strong>Executar a cada 1 hora:</strong>
        <pre><code>0 * * * * python3 /caminho/para/main.py >> /caminho/para/log.txt 2>&1</code></pre>
      </li>
      <li><strong>Executar uma vez por dia às 3h:</strong>
        <pre><code>0 3 * * * python3 /caminho/para/main.py >> /caminho/para/log.txt 2>&1</code></pre>
      </li>
    </ul>
  </li>
</ol>

<hr>

<h2>Observações:</h2>
<ul>
  <li>Certifique-se de configurar corretamente:
    <ul>
      <li>Conexão com o banco no arquivo <code>acesso_oracle.py</code>.</li>
      <li>Credenciais e IDs das planilhas no Google no arquivo <code>credentials-automacao-atendimento-zendesk.json</code>.</li>
    </ul>
  </li>
  <li>Os dados exportados pelo script <code>gerar-planilhas.py</code> devem ser alterados pelo usuário com base nas suas preferências e objetivos.</li>
  <li>Se desejar consolidar todas as categorias em uma única planilha, adapte o script <code>insert-informatica-em-eletronica.py</code>.</li>
</ul>

<p>Sinta-se à vontade para personalizar conforme suas necessidades!</p>
