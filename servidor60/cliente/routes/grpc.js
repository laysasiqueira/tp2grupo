const express = require('express');
const router = express.Router();
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Carregar proto
const PROTO_PATH = path.join(__dirname, '../agenda.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const agendaProto = grpc.loadPackageDefinition(packageDefinition).agenda;

// Criar cliente
const client = new agendaProto.AgendaService(
  '192.168.246.26:50051',
  grpc.credentials.createInsecure()
);

// Endpoint para listar contatos via streaming
router.get('/listar', (req, res) => {
  const contatos = [];

  const token = req.headers.authorization; 
  const metadata = new grpc.Metadata();
  metadata.add('authorization', token);

  const call = client.StreamContatos({}, metadata);

  let respostaEnviada = false;

  call.on('data', (contato) => {
    contatos.push(contato);
  });

  call.on('end', () => {
    if (!res.headersSent) {
      res.json(contatos);
      respostaEnviada = true;
    }
  });

  call.on('error', (err) => {
    console.error('Erro no stream:', err.message);
    if (!res.headersSent && !respostaEnviada) {
      res.status(401).json({ erro: err.message });
    }
  });
});


module.exports = router;
