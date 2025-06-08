const express = require('express');
const router = express.Router();
const axios = require('axios');

// POST para buscar contato por nome
router.post('/buscar', async (req, res) => {
  const nome = req.body.nome;

  const query = {
    query: `
      query {
        buscarContatoPorNome(nome: "${nome}") {
          nome
          email
          telefone
        }
      }
    `
  };

  try {
    const response = await axios.post('http://192.168.246.26:5000/graphql', query, {
      headers: { 'Content-Type': 'application/json' }
    });
    res.json(response.data.data.buscarContatoPorNome);
  } catch (err) {
    res.status(500).send('Erro ao buscar contato.');
  }
});

module.exports = router;
