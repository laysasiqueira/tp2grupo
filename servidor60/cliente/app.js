const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Importar rotas
const rotaRest = require('./routes/rest');
app.use(rotaRest);


const rotaSoap = require('./routes/soap');
app.use(rotaSoap);

const graphqlRouter = require('./routes/graphql');
app.use('/graphql', graphqlRouter);


const grpcRoutes = require('./routes/grpc');
app.use('/grpc', grpcRoutes);

const rotaAuth = require('./routes/auth');
app.use(rotaAuth);

// Página inicial
app.get('/', (req, res) => {
  res.send('🚀 Cliente Web - Agenda de Contatos');
});

// Iniciar servidor
app.listen(PORT, '192.168.246.60', () => {
  console.log(`✅ Cliente Web disponível em: http://localhost:${PORT}`);
});
