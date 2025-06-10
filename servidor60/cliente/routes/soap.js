const express = require('express');
const soap = require('soap');
const fs = require('fs');
const path = require('path');
const router = express.Router();

const SOAP_URL = 'http://192.168.246.26:8010/?wsdl'; // URL do WSDL gerado pelo servidor Spyne

// ✅ Listar contatos (já existente)
router.get('/soap/contatos', async (req, res) => {
  try {
    const client = await soap.createClientAsync(SOAP_URL);
    const resultado = await client.listar_contatosAsync({});

    const linhas = resultado[0].listar_contatosResult?.string || [];

    const contatosFormatados = linhas.map(linha => {
      const partes = linha.split(' - ');
      return {
        id: partes[0],
        nome: partes[1],
        email: partes[2],
        telefone: partes[3],
      };
    });

    res.json(contatosFormatados);
  } catch (error) {
    console.error('❌ Erro ao obter contatos SOAP:', error.message);
    res.status(500).json({ erro: 'Erro ao obter contatos SOAP' });
  }
});

// ✅ Exportar JSON (download)
router.get('/soap/exportar/json', async (req, res) => {
  try {
    const client = await soap.createClientAsync(SOAP_URL);
    const resultado = await client.exportar_jsonAsync({});
    const dados = resultado[0].exportar_jsonResult;

    const caminho = path.join(__dirname, '..', '..', 'temp_export.json');
    fs.writeFileSync(caminho, dados, 'utf-8');

    res.download(caminho, 'contatos_exportados.json', () => {
      fs.unlinkSync(caminho);
    });
  } catch (error) {
    console.error('❌ Erro ao exportar JSON via SOAP:', error.message);
    res.status(500).json({ erro: 'Erro ao exportar JSON via SOAP' });
  }
});

// ✅ Exportar XML (download)
router.get('/soap/exportar/xml', async (req, res) => {
  try {
    const client = await soap.createClientAsync(SOAP_URL);
    const resultado = await client.exportar_xmlAsync({});
    const dados = resultado[0].exportar_xmlResult;

    const caminho = path.join(__dirname, '..', '..', 'temp_export.xml');
    fs.writeFileSync(caminho, dados, 'utf-8');

    res.download(caminho, 'contatos_exportados.xml', () => {
      fs.unlinkSync(caminho);
    });
  } catch (error) {
    console.error('❌ Erro ao exportar XML via SOAP:', error.message);
    res.status(500).json({ erro: 'Erro ao exportar XML via SOAP' });
  }
});

// ✅ Importar JSON via SOAP (base64)
// Importar JSON via SOAP
router.post('/soap/importar/json', express.text({ type: '*/*' }), async (req, res) => {
  try {
    const base64Str = req.body;
    const token = req.headers['authorization'];  // ✅ correto no Node.js

    const client = await soap.createClientAsync(SOAP_URL);
    client.addHttpHeader('Authorization', token);  // ✅ adiciona corretamente

    const resultado = await client.importar_json_base64Async({ base64_str: base64Str });
    const resposta = resultado[0].importar_json_base64Result;
    res.json({ mensagem: resposta });
  } catch (error) {
    console.error('❌ Erro ao importar JSON via SOAP:', error.message);
    res.status(500).json({ erro: 'Erro ao importar JSON via SOAP' });
  }
});

// Importar XML via SOAP
router.post('/soap/importar/xml', express.text({ type: '*/*' }), async (req, res) => {
  try {
    const base64Str = req.body;
    const token = req.headers['authorization'];  // ✅ correto no Node.js

    const client = await soap.createClientAsync(SOAP_URL);
    client.addHttpHeader('Authorization', token);  // ✅ adiciona corretamente

    const resultado = await client.importar_xml_base64Async({ base64_str: base64Str });
    const resposta = resultado[0].importar_xml_base64Result;
    res.json({ mensagem: resposta });
  } catch (error) {
    console.error('❌ Erro ao importar XML via SOAP:', error.message);
    res.status(500).json({ erro: 'Erro ao importar XML via SOAP' });
  }
});


module.exports = router;